use std::{
    cmp::{max, min},
    fmt::{self, Display},
    iter::zip,
    num::{ParseFloatError, ParseIntError},
    ops::Deref,
};

use anyhow::{bail, Context, Error, Result};
use macro_rules_attribute::apply;
use pyo3::{
    exceptions,
    exceptions::PyValueError,
    ffi, pyclass, pymethods,
    types::{IntoPyDict, PySlice, PyTuple},
    AsPyPointer, FromPyObject, IntoPy, PyAny, PyErr, PyObject, PyResult, Python, ToPyObject,
};
use rustc_hash::FxHashMap as HashMap;
use smallvec::SmallVec as Sv;
use thiserror::Error;
use uuid::uuid;

use super::py_types::ExtraPySelfOps;
use crate::{
    filter_by_variant,
    lru_cache::TensorCacheRrfs,
    py_types::{Tensor, PY_UTILS},
    pycall, python_error_exception, sv,
    tensor_db::{get_tensor_prefix, save_tensor},
    util::HashBytes,
};
pub type Shape = Sv<[usize; 6]>; // TODO: maybe this should be struct which preserves invariant that dim shapes >= 0?

pub fn broadcast_shapes(shapes: &Vec<Shape>) -> Result<Shape> {
    if shapes.is_empty() {
        return Ok(sv![]);
    }
    let ranks: Vec<usize> = shapes.iter().map(|x| x.len()).collect();
    let out_rank = *ranks.iter().max().unwrap();
    let mut result: Shape = sv![1; out_rank];
    for axis_from_end in 1..out_rank + 1 {
        for (i, shape) in shapes.iter().enumerate() {
            let axis_for_shape = ranks[i].checked_sub(axis_from_end);
            match axis_for_shape {
                None => {}
                Some(j) => {
                    let axis_len = shape[j];
                    if axis_len == 0
                        || axis_len != 1
                            && result[out_rank - axis_from_end] != 1
                            && result[out_rank - axis_from_end] != axis_len
                    {
                        bail!(MiscInputError::NotBroadcastable {
                            shapes: shapes.to_owned(),
                        });
                    }
                    result[out_rank - axis_from_end] =
                        max(axis_len, result[out_rank - axis_from_end]);
                }
            }
        }
    }
    Ok(result)
}

#[apply(python_error_exception)]
#[base_error_name(MiscInput)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum MiscInputError {
    #[error("Shapes aren't broadcastable, {shapes:?} ({e_name})")]
    NotBroadcastable { shapes: Vec<Shape> },

    #[error("item={item}, count={count} (needed -{count} <= {item} < {count}) ({e_name})")]
    ItemOutOfBounds { item: i64, count: usize },

    #[error("Children multiple dtypes {a:?} {b:?} ({e_name})")]
    ChildrenMultipleDtypes {
        a: Option<String>,
        b: Option<String>,
    },

    #[error("Children multiple dtypes {a:?} {b:?} ({e_name})")]
    ChildrenMultipleDevices {
        a: Option<String>,
        b: Option<String>,
    },
}

#[apply(python_error_exception)]
#[base_error_name(Index)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum IndexError {
    #[error("Only ndim of 1 is supported for index tensors and got {ndim} (tensor: {tensor:?}) ({e_name})")]
    TensorNDimNot1 { ndim: usize, tensor: Tensor },

    #[error("Index {axis:?} out of bounds, index: {index:?} shape: {shape:?}. NB: Rust circuit slices don't saturate like Python ones do. ({e_name})")]
    IndexOutOfBounds {
        index: TensorIndex,
        shape: Shape,
        at: usize,
        axis: TensorAxisIndex,
        l: usize,
    },

    #[error("index rank too high: {index_rank} vs {node_rank} ({e_name})")]
    IndexRankTooHigh { index_rank: usize, node_rank: usize },

    #[error("slice={slice:?} ({e_name})")]
    UnsupportedSlice { slice: Slice },
}

pub fn check_canon_idxs(count: usize, ints: &[i64]) -> Result<Vec<usize>> {
    let icount = count as i64;
    ints.iter()
        .map(|&item| {
            if item >= icount || item < -icount {
                bail!(MiscInputError::ItemOutOfBounds { item, count })
            } else {
                Ok(((item + icount) % icount) as usize)
            }
        })
        .collect()
}

// we could bit pack if we wanted...
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct Slice {
    pub start: Option<i64>,
    pub stop: Option<i64>,
}

impl Slice {
    pub const IDENT: Slice = Slice {
        start: None,
        stop: None,
    };

    pub fn to_unsigned_loc(x: i64, l: usize) -> usize {
        if x < 0 {
            l.saturating_sub((-x) as usize)
        } else {
            l.min(x as usize)
        }
    }

    pub fn start_u(self, l: usize) -> usize {
        self.start.map(|x| Self::to_unsigned_loc(x, l)).unwrap_or(0)
    }

    pub fn stop_u(self, l: usize) -> usize {
        self.stop.map(|x| Self::to_unsigned_loc(x, l)).unwrap_or(l)
    }

    pub fn to_uslice(self, l: usize) -> USlice {
        USlice {
            start: self.start_u(l),
            stop: self.stop_u(l),
        }
    }

    fn size(self, l: usize) -> usize {
        self.stop_u(l).saturating_sub(self.start_u(l))
    }

    fn canonicalize(self, l: usize) -> Self {
        Self {
            start: Some(self.start_u(l) as i64),
            stop: Some(self.stop_u(l) as i64),
        }
    }

    fn update_hash(self, hasher: &mut blake3::Hasher) {
        for op in [self.start, self.stop] {
            match op {
                Some(i) => {
                    hasher.update(&i.to_le_bytes());
                    hasher.update(&[0]);
                }
                None => {
                    hasher.update(&0_i64.to_le_bytes());
                    hasher.update(&[1]);
                }
            }
        }
    }

    fn is_identity(self, l: usize) -> bool {
        self.start_u(l) == 0 && self.stop_u(l) == l
    }
}

impl<'source> FromPyObject<'source> for Slice {
    fn extract(slice_in: &'source PyAny) -> PyResult<Self> {
        let py_slice: &PySlice = slice_in.extract()?;

        // could also use never type if that was supported : /
        let step: Option<isize> = py_slice.getattr("step").unwrap().extract()?;
        if step != None {
            return Err(PyErr::new::<exceptions::PyValueError, _>(
                "step must be None!",
            ));
        }

        Ok(Slice {
            start: py_slice.getattr("start").unwrap().extract()?,
            stop: py_slice.getattr("stop").unwrap().extract()?,
        })
    }
}

impl IntoPy<PyObject> for Slice {
    fn into_py(self, py: Python<'_>) -> PyObject {
        unsafe {
            // we use unsafe + ffi because pyo3 slice doesn't support None
            let ptr = ffi::PySlice_New(
                self.start.into_py(py).as_ptr(),
                self.stop.into_py(py).as_ptr(),
                None::<i64>.into_py(py).as_ptr(),
            );
            let slice: &PySlice = py.from_owned_ptr(ptr);
            slice.into()
        }
    }
}

#[derive(PartialEq, Eq, Hash, Clone, Debug, Copy)]
pub struct USlice {
    pub start: usize,
    pub stop: usize,
}
impl USlice {
    pub fn intersection(&self, other: &USlice) -> USlice {
        let start = max(self.start, other.start);
        USlice {
            start,
            stop: max(min(self.stop, other.stop), start),
        }
    }
    pub fn union(&self, other: &USlice) -> USlice {
        USlice {
            start: min(self.start, other.start),
            stop: max(self.stop, other.stop),
        }
    }

    pub fn shrink_base(&self, new_base: &USlice) -> USlice {
        assert!(new_base.stop >= self.stop);
        assert!(self.start >= new_base.start);
        USlice {
            start: self.start - new_base.start,
            stop: self.stop - new_base.start,
        }
    }

    pub fn containing_uslice(x: &TensorAxisIndex) -> Option<USlice> {
        match x {
            TensorAxisIndex::Single(single) => Some(USlice {
                start: *single as usize,
                stop: (*single + 1) as usize,
            }),
            TensorAxisIndex::Slice(slice) => (*slice).into(),
            TensorAxisIndex::Tensor(_) => None,
        }
    }
    pub fn length(&self) -> usize {
        self.stop - self.start
    }
}

pub fn uslices_shrink_base(x: &Vec<USlice>, new_base: &Vec<USlice>) -> Vec<USlice> {
    zip(x, new_base).map(|(x, b)| x.shrink_base(b)).collect()
}

pub fn uslices_to_index(x: &Vec<USlice>) -> TensorIndex {
    TensorIndex(
        x.iter()
            .map(|x| TensorAxisIndex::Slice((*x).into()))
            .collect(),
    )
}

impl From<USlice> for Slice {
    fn from(x: USlice) -> Self {
        Slice {
            start: Some(x.start as i64),
            stop: Some(x.stop as i64),
        }
    }
}

impl From<Slice> for Option<USlice> {
    fn from(slice: Slice) -> Self {
        if let Slice {
            start: Some(start),
            stop: Some(stop),
        } = slice
        {
            if start < 0 || stop < 0 {
                return None;
            }
            Some(USlice {
                start: start as usize,
                stop: stop as usize,
            })
        } else {
            None
        }
    }
}

impl From<USlice> for TensorAxisIndex {
    fn from(x: USlice) -> Self {
        TensorAxisIndex::Slice(Slice {
            start: Some(x.start as i64),
            stop: Some(x.stop as i64),
        })
    }
}

/// Wrapper which ensures ndim <= 1
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IndexTensor(Tensor);

impl Deref for IndexTensor {
    type Target = Tensor;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl TryFrom<Tensor> for IndexTensor {
    type Error = Error;
    fn try_from(tensor: Tensor) -> Result<Self> {
        if tensor.ndim() != 1 {
            bail!(IndexError::TensorNDimNot1 {
                ndim: tensor.ndim(),
                tensor,
            });
        }
        Ok(IndexTensor(tensor))
    }
}

impl<'source> FromPyObject<'source> for IndexTensor {
    fn extract(tensor: &'source PyAny) -> PyResult<Self> {
        let tensor: Tensor = tensor.extract()?;
        tensor.try_into().map_err(Into::into)
    }
}
impl IntoPy<PyObject> for IndexTensor {
    fn into_py(self, py: Python<'_>) -> PyObject {
        self.0.into_py(py)
    }
}
impl IntoPy<PyObject> for &IndexTensor {
    fn into_py(self, py: Python<'_>) -> PyObject {
        (&self.0).into_py(py)
    }
}

/// for now, doesn't support tensors with negatives
#[derive(Debug, Clone, FromPyObject, PartialEq, Eq)]
pub enum TensorAxisIndex {
    Tensor(IndexTensor), // tensor needs to come first so len 1 tensors go to tensor not single
    Single(i64),
    Slice(Slice),
}

impl TensorAxisIndex {
    pub const IDENT: TensorAxisIndex = TensorAxisIndex::Slice(Slice {
        start: None,
        stop: None,
    });
    /// untested
    pub fn shrink_base_uslice(&self, uslice: &USlice) -> Self {
        match self {
            TensorAxisIndex::Single(single) => {
                assert!(*single >= 0);
                assert!((single + uslice.start as i64) < uslice.stop as i64);
                TensorAxisIndex::Single(single - uslice.start as i64)
            }
            TensorAxisIndex::Slice(slice) => {
                assert!(
                    slice.stop.is_some()
                        && slice.stop.unwrap() >= 0
                        && slice.start.unwrap_or(0) >= 0
                );
                let start = Some(slice.start.unwrap_or(0) - uslice.start as i64);
                let stop = Some(slice.stop.unwrap() - uslice.start as i64);
                TensorAxisIndex::Slice(Slice { start, stop })
            }
            TensorAxisIndex::Tensor(_tensor) => {
                unimplemented!();
            }
        }
    }
    pub fn new_plain_slice(start: usize, stop: usize) -> Self {
        TensorAxisIndex::Slice(Slice {
            start: Some(start as i64),
            stop: Some(stop as i64),
        })
    }

    pub fn is_identity(&self, l: usize) -> bool {
        if let TensorAxisIndex::Slice(slice) = self {
            return slice.size(l) == l;
        }
        false
    }

    pub fn new_tensor_randint_seeded(
        length: usize,
        base_length: usize,
        device_dtype: TorchDeviceDtypeOp,
        seed: usize,
    ) -> Self {
        TensorAxisIndex::Tensor(pyo3::Python::with_gil(|py| {
            PY_UTILS
                .torch
                .getattr(py, "manual_seed")
                .unwrap()
                .call(py, (seed,), None)
                .unwrap();
            let mut kwargs = HashMap::default();
            if let Some(dtype) = device_dtype.dtype {
                let dtype: &str = &dtype;
                kwargs.insert("dtype", PY_UTILS.torch.getattr(py, dtype).unwrap());
            }
            if let Some(device) = device_dtype.device {
                kwargs.insert("device", device.into_py(py));
            }
            PY_UTILS
                .torch
                .getattr(py, "randint")
                .unwrap()
                .call(
                    py,
                    (0, base_length, pyo3::types::PyTuple::new(py, vec![length])),
                    Some(kwargs.into_py_dict(py)),
                )
                .unwrap()
                .extract(py)
                .unwrap()
        }))
    }
}

impl IntoPy<PyObject> for TensorAxisIndex {
    fn into_py(self, py: Python<'_>) -> PyObject {
        match self {
            Self::Single(x) => x.into_py(py),
            Self::Tensor(x) => x.into_py(py),
            Self::Slice(x) => x.into_py(py),
        }
    }
}

// https://github.com/PyO3/pyo3/issues/1595 for why needed
impl ToPyObject for TensorAxisIndex {
    fn to_object(&self, py: Python<'_>) -> PyObject {
        self.clone().into_py(py)
    }
}

#[derive(Debug, Clone, FromPyObject)]
pub struct TensorIndex(pub Vec<TensorAxisIndex>);

// TensorIndexSync is like TensorIndex but allows tensors to have any rank
// this is for extracting these numpy-style indices
// we don't have full support for this, only used in new_synchronized_to_start
pub struct TensorIndexSync(pub TensorIndex);
impl<'source> FromPyObject<'source> for TensorIndexSync {
    fn extract(ob: &'source PyAny) -> PyResult<Self> {
        Ok(TensorIndexSync(TensorIndex(
            ob.iter()?
                .map(|x| {
                    let x_unwrapped = x?;
                    let tensory: PyResult<Tensor> = x_unwrapped.extract();
                    tensory
                        .map(|z| TensorAxisIndex::Tensor(IndexTensor(z)))
                        .or_else(move |_| x_unwrapped.extract())
                })
                .collect::<PyResult<Vec<_>>>()?,
        )))
    }
}

impl Display for TensorIndex {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let mut result = "[".to_owned();
        for (i, idx) in self.0.iter().enumerate() {
            result.push_str(&match idx {
                TensorAxisIndex::Single(i) => i.to_string(),
                TensorAxisIndex::Slice(slice) => {
                    slice.start.map(|i| i.to_string()).unwrap_or("".to_owned())
                        + ":"
                        + &slice.stop.map(|i| i.to_string()).unwrap_or("".to_owned())
                }
                TensorAxisIndex::Tensor(tensor) => {
                    "[".to_owned() + &tensor.shape()[0].to_string() + "]"
                }
            });
            if i != self.0.len() - 1 {
                result.push(',');
            }
        }
        result.push(']');
        write!(f, "{}", result)
    }
}

#[test]
fn sat_as_expected() {
    assert_eq!(1, 4usize.saturating_sub((-(-3isize)) as usize));
    assert_eq!(0, 4usize.saturating_sub((-(-5isize)) as usize));
}

impl TensorIndex {
    pub fn apply_to_shape(&self, shape: &Shape) -> Shape {
        zip(&self.0, shape)
            .filter_map(|(idx, &l)| match idx {
                TensorAxisIndex::Single(_i) => None,
                TensorAxisIndex::Tensor(t) => {
                    if t.shape().is_empty() {
                        None
                    } else {
                        Some(t.shape()[0])
                    }
                }
                TensorAxisIndex::Slice(sl) => Some(sl.size(l)),
            })
            .collect()
    }

    pub fn is_identity(&self, shape: &Shape) -> bool {
        zip(&self.0, shape).all(|(idx, &l)| match idx {
            TensorAxisIndex::Single(_i) => false,
            TensorAxisIndex::Tensor(_t) => false, // dont bother to check tensor, if you want that canon first
            TensorAxisIndex::Slice(sl) => sl.is_identity(l),
        })
    }

    pub fn validate(&self, shape: &Shape) -> Result<()> {
        let get_err = |at| {
            Err(IndexError::IndexOutOfBounds {
                index: self.clone(),
                shape: shape.clone(),
                at,
                axis: self.0[at].clone(),
                l: shape[at],
            })
        };

        let check = |at: usize, i: Option<i64>, l: usize, is_slice: bool| {
            if let Some(i) = i {
                let end_b = if is_slice { l + 1 } else { l };
                if i >= end_b as i64 || i < -(l as i64) {
                    return get_err(at);
                }
            }
            Ok(())
        };

        for (at, (idx, &l)) in zip(&self.0, shape).enumerate() {
            match idx {
                &TensorAxisIndex::Single(i) => check(at, Some(i), l, false)?,
                &TensorAxisIndex::Slice(Slice { start, stop }) => {
                    check(at, start, l, true)?;
                    check(at, stop, l, true)?;

                    let mod_l_idx = |x| if x < 0 { l as i64 + x } else { x };
                    let start_u: i64 = start.map_or(0, mod_l_idx);
                    let stop_u: i64 = stop.map_or(l as i64, mod_l_idx);
                    if start_u > stop_u {
                        get_err(at)?;
                    }
                }
                _ => (),
            }
        }

        Ok(())
    }

    pub fn canonicalize(&self, shape: &Shape) -> TensorIndex {
        self.validate(shape).expect("invalid tensor index");
        TensorIndex(
            zip(&self.0, shape)
                .map(|(idx, &l)| match idx {
                    TensorAxisIndex::Single(i) => TensorAxisIndex::Single((*i + l as i64) % l as i64),
                    TensorAxisIndex::Tensor(t) => TensorAxisIndex::Tensor(t.clone()), // not bothering to canon tensor for now
                    TensorAxisIndex::Slice(sl) => TensorAxisIndex::Slice(sl.canonicalize(l)),
                })
                .collect(),
        )
    }

    pub fn all_slices(&self) -> Option<Vec<Slice>> {
        let filtered = filter_by_variant!(&self.0, TensorAxisIndex, Slice, Slice).0;
        if filtered.len() == self.0.len() {
            Some(filtered)
        } else {
            None
        }
    }

    pub fn all_uslices(&self) -> Option<Vec<USlice>> {
        self.all_slices().and_then(|x| {
            let result: Vec<USlice> = x.iter().filter_map(|x| (*x).into()).collect();
            if result.len() == x.len() {
                Some(result)
            } else {
                None
            }
        })
    }

    pub fn new_single(idx: TensorAxisIndex, pos: usize, rank: usize) -> Self {
        TensorIndex(
            (0..rank)
                .map(|i| {
                    if i == pos {
                        idx.clone()
                    } else {
                        TensorAxisIndex::IDENT
                    }
                })
                .collect(),
        )
    }

    pub fn ident(rank: usize) -> Self {
        Self(vec![TensorAxisIndex::IDENT; rank])
    }

    pub fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        for axis in self.0.iter() {
            hasher.update(&uuid!("3d14636b-a1ed-4235-91cd-5fc9e818c93d").into_bytes()); // delimit with uuid
            match axis {
                TensorAxisIndex::Single(i) => {
                    hasher.update(&i.to_le_bytes());
                }
                TensorAxisIndex::Tensor(t) => {
                    hasher.update(t.hashed().hash().unwrap());
                } // dont bother to check tensor, if you want that canon first
                TensorAxisIndex::Slice(sl) => sl.update_hash(&mut hasher),
            }
        }
        hasher.finalize().into()
    }

    pub fn repr_bijection(&self) -> Result<String> {
        let mut result = "[".to_owned();
        for (i, idx) in self.0.iter().enumerate() {
            result.push_str(&match idx {
                TensorAxisIndex::Single(i) => i.to_string(),
                TensorAxisIndex::Slice(slice) => {
                    slice.start.map(|i| i.to_string()).unwrap_or("".to_owned())
                        + ":"
                        + &slice.stop.map(|i| i.to_string()).unwrap_or("".to_owned())
                }
                TensorAxisIndex::Tensor(tensor) => {
                    save_tensor((**tensor).clone(), false)?;
                    "t".to_owned() + &base16::encode_lower(&tensor.hash().unwrap())[..10]
                }
            });
            if i != self.0.len() - 1 {
                result.push(',');
            }
        }
        result.push(']');
        Ok(result)
    }
    pub fn from_bijection_string(
        string: &str,
        tensor_cache: &mut Option<TensorCacheRrfs>,
    ) -> Result<Self> {
        let er = ParseError::Fail {
            string: string.to_owned(),
        };
        Ok(TensorIndex(
            string
                .strip_prefix('[')
                .ok_or(er.clone())?
                .strip_suffix(']')
                .ok_or(er.clone())?
                .split(',')
                .map(str::trim)
                .filter(|x| !x.is_empty())
                .map(|x| -> Result<_> {
                    // TODO: fix error handle + trim whitespace
                    if let Ok(int) = x.parse::<i64>() {
                        return Ok(TensorAxisIndex::Single(int));
                    }
                    if let Some(no_t) = x.strip_prefix('t') {
                        return tensor_cache
                            .as_mut()
                            .map(|tc| tc.get_tensor(no_t.to_owned()))
                            .unwrap_or_else(|| {
                                get_tensor_prefix(no_t).context("tensor hash from string")
                            })
                            .and_then(|x| {
                                Ok(TensorAxisIndex::Tensor(
                                    x.try_into()
                                        .context("index tensor loaded from disk is invalid")?,
                                ))
                            });
                    }

                    let get_slice_bound = |item: &str, name: &str| {
                        if item.is_empty() {
                            Ok(None)
                        } else {
                            item.parse::<i64>()
                                .map_err(ParseError::from)
                                .with_context(|| {
                                    format!(
                                        "failed to parse {} of slice, index string='{}'",
                                        name, string
                                    )
                                })
                                .map(Some)
                        }
                    };

                    if let [start, stop] = x.split(':').map(str::trim).collect::<Vec<_>>()[..] {
                        return Ok(TensorAxisIndex::Slice(Slice {
                            start: get_slice_bound(start, "start")?,
                            stop: get_slice_bound(stop, "stop")?,
                        }));
                    }
                    bail!(er.clone())
                })
                .collect::<Result<Vec<_>>>()?,
        ))
    }
}

impl IntoPy<PyObject> for TensorIndex {
    fn into_py(self, py: Python<'_>) -> PyObject {
        PyTuple::new(py, self.0).into_py(py)
    }
}

pub fn compose(top: &TensorIndex, bottom: &TensorIndex) -> Option<TensorIndex> {
    let mut result: Vec<TensorAxisIndex> = vec![];
    let mut top_idx: usize = 0;
    for bottom_idx in bottom.0.iter() {
        match bottom_idx {
            TensorAxisIndex::Single(_i) => result.push(bottom_idx.clone()),
            TensorAxisIndex::Tensor(t) => {
                let top_here = top.0[top_idx].clone();
                top_idx += 1;
                Python::with_gil(|py| {
                    let indexed_tensor = (**t).clone().py_getitem(py, top_here).unwrap();
                    if indexed_tensor.ndim() == 0 {
                        result.push(TensorAxisIndex::Single(pycall!(
                            PY_UTILS.cast_int,
                            (indexed_tensor,)
                        )));
                    } else {
                        result.push(TensorAxisIndex::Tensor(indexed_tensor.try_into().unwrap()));
                    }
                })
            }
            TensorAxisIndex::Slice(slice) => {
                let start = slice.start.unwrap_or(0);
                let stop = slice.stop;
                let top_here = top.0[top_idx].clone();
                match top_here {
                    TensorAxisIndex::Single(i) => {
                        if i < 0 {
                            result.push(TensorAxisIndex::Single(stop.unwrap_or(0) + i))
                        } else {
                            result.push(TensorAxisIndex::Single(start + i))
                        }
                    }
                    TensorAxisIndex::Tensor(t) => {
                        if start < 0 {
                            return None;
                        } else {
                            Python::with_gil(|py| {
                                result.push(TensorAxisIndex::Tensor(
                                    (*t).clone().py_add(py, start).unwrap().try_into().unwrap(),
                                ))
                            })
                        }
                    }
                    TensorAxisIndex::Slice(top_slice) => {
                        let top_start = top_slice.start.unwrap_or(0);
                        let top_stop = top_slice.stop;
                        let (mut new_start, mut new_stop) =
                            (Some(start + top_start), Some(start + top_stop.unwrap_or(0)));
                        if top_start < 0 {
                            new_start = Some(stop.unwrap_or(0) + top_start);
                        }
                        if top_stop.unwrap_or(-1) < 0 {
                            if top_stop.is_none() && stop.is_none() {
                                new_stop = None;
                            } else {
                                new_stop = Some(stop.unwrap_or(0) + top_stop.unwrap_or(0));
                            }
                        }
                        // if you add negative and positive indices and get 0, you really meant "end", or None
                        if (top_stop.is_some() && top_stop.unwrap() < 0 || start < 0)
                            && new_stop == Some(0)
                        {
                            new_stop = None
                        }
                        result.push(TensorAxisIndex::Slice(Slice {
                            start: new_start,
                            stop: new_stop,
                        }))
                    }
                }
                // dbg!(top, bottom);
                top_idx += 1;
            }
        }
    }
    Some(TensorIndex(result))
}

/// use string so you can compare fast when constructing and have full range (weird types like uint or bfloat16)
/// as opposed to PyObject torch.dtype or enum (could switch to enum)
#[pyclass]
#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct TorchDeviceDtypeOp {
    #[pyo3(get)]
    pub device: Option<String>,
    #[pyo3(get)]
    pub dtype: Option<String>,
}

#[pymethods]
impl TorchDeviceDtypeOp {
    #[staticmethod]
    #[pyo3(name = "default")]
    fn default_py() -> Self {
        Self::default()
    }

    #[new]
    #[args(device = "None", dtype = "None")]
    fn new(device: Option<String>, dtype: Option<String>) -> Self {
        Self { device, dtype }
    }
}

#[pyclass]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TorchDeviceDtype {
    #[pyo3(get)]
    pub device: String,
    #[pyo3(get)]
    pub dtype: String,
}

#[pymethods]
impl TorchDeviceDtype {
    #[new]
    fn new(device: String, dtype: String) -> Self {
        Self { device, dtype }
    }
    #[staticmethod]
    #[pyo3(name = "from_tensor")]
    pub fn from_tensor_py(tensor: Tensor) -> Self {
        Self::from_tensor(&tensor)
    }

    pub fn cast_tensor(&self, tensor: Tensor) -> Tensor {
        Python::with_gil(|py| {
            PY_UTILS
                .cast_tensor
                .call(py, (tensor, self.clone()), None)
                .unwrap()
                .extract(py)
                .unwrap()
        })
    }
}

impl TorchDeviceDtype {
    pub fn from_tensor(tensor: &Tensor) -> Self {
        Python::with_gil(|py| Self {
            device: tensor
                .tensor()
                .getattr(py, "device")
                .unwrap()
                .getattr(py, "__str__")
                .unwrap()
                .call0(py)
                .unwrap()
                .extract(py)
                .unwrap(),
            dtype: tensor
                .tensor()
                .getattr(py, "dtype")
                .unwrap()
                .getattr(py, "__str__")
                .unwrap()
                .call0(py)
                .unwrap()
                .extract::<String>(py)
                .unwrap()[6..]
                .to_owned(),
        })
    }
    pub fn size(&self) -> usize {
        let map = HashMap::from_iter([
            ("float32".to_owned(), 4),
            ("float64".to_owned(), 8),
            ("float16".to_owned(), 2),
            ("int64".to_owned(), 8),
            ("int32".to_owned(), 4),
            ("int16".to_owned(), 2),
            ("int8".to_owned(), 1),
        ]);
        map[&self.dtype]
    }
}

impl From<TorchDeviceDtype> for TorchDeviceDtypeOp {
    fn from(x: TorchDeviceDtype) -> Self {
        Self {
            device: Some(x.device),
            dtype: Some(x.dtype),
        }
    }
}

impl TorchDeviceDtypeOp {
    pub const NONE: Self = TorchDeviceDtypeOp {
        device: None,
        dtype: None,
    };

    pub fn combine(self, other: Self) -> Result<Self> {
        let out = Self {
            device: match (&self.device, &other.device) {
                (Some(l), Some(r)) if l != r => {
                    bail!(MiscInputError::ChildrenMultipleDevices {
                        a: self.device.clone(),
                        b: other.device.clone(),
                    });
                }
                (l, r) => l.as_ref().or(r.as_ref()).cloned(),
            },
            dtype: match (&self.dtype, &other.dtype) {
                (Some(l), Some(r)) if l != r => {
                    bail!(MiscInputError::ChildrenMultipleDtypes {
                        a: self.dtype.clone(),
                        b: other.dtype.clone(),
                    });
                }
                (l, r) => l.as_ref().or(r.as_ref()).cloned(),
            },
        };
        Ok(out)
    }

    pub fn unwrap_or_defaults(self) -> TorchDeviceDtype {
        TorchDeviceDtype {
            dtype: self.dtype.unwrap_or_else(|| "float32".to_owned()),
            device: self.device.unwrap_or_else(|| "cpu".to_owned()),
        }
    }

    pub fn size(&self) -> usize {
        self.clone().unwrap_or_defaults().size()
    }
}

impl Default for TorchDeviceDtype {
    fn default() -> Self {
        TorchDeviceDtypeOp::NONE.unwrap_or_defaults()
    }
}

const REGEX_101_MSG: &str = "\nTry using regex101.com : )\n(TODO: auto generate regex test page via https://github.com/firasdib/Regex101/wiki/API#python-3)";

// TODO: break up and move part to parsing.rs
#[apply(python_error_exception)]
#[base_error_name(Parse)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum ParseError {
    #[error(
        "regex didn't match '{line}'\nregex='{regex_string}'{}\n({e_name})",
        REGEX_101_MSG
    )]
    RegexDidntMatch { line: String, regex_string: String },

    #[error(
        "regex didn't match group={group} for '{line}'\n{}\nregex='{regex_string}'{}\n({e_name})",
        "Note: this error can also be caused by failing to lookup a reference circuit",
        REGEX_101_MSG
    )]
    RegexDidntMatchGroup {
        line: String,
        regex_string: String,
        group: usize,
    },

    #[error("Parsing number failed err={err_string} ({e_name})")]
    NumberFail { err_string: String },

    #[error("extra='{extra}' ({e_name})")]
    ExpectedNoExtraInfo { extra: String },

    #[error("Parsing failed {string} ({e_name})")]
    Fail { string: String },

    #[error("Expected UUID string, found  '{string}'\nerr_msg={err_msg} ({e_name})")]
    InvalidUuid { string: String, err_msg: String },

    #[error("Parsing wrong number of children, expected {expected} found {found}, ident={ident} ({e_name})")]
    WrongNumberChildren {
        expected: usize,
        found: usize,
        ident: String,
    },

    #[error("effectively negative indent!\n{}\n{}\n{}\n({e_name})",
        format!("this_num_spaces_base={} < first_num_spaces={}", this_num_spaces_base, first_num_spaces),
        format!("first_line='{}'", first_line),
        format!("this_line='{}'", this_line)
        )]
    LessIndentationThanFirstItem {
        this_num_spaces_base: usize,
        first_num_spaces: usize,
        first_line: String,
        this_line: String,
    },

    #[error("Parsing invalid indentation, tab width {tab_width} num spaces {spaces} stack indentation {stack_indentation} ({e_name})")]
    InvalidIndentation {
        spaces: usize,
        tab_width: usize,
        stack_indentation: usize,
    },

    #[error("Parsing invalid circuit variant {v} ({e_name})")]
    InvalidVariant { v: String },

    #[error("Parsing invalid serial number {serial_number} ({e_name})")]
    InvalidSerialNumber { serial_number: usize },

    #[error("Parsing Extra Unneeded String '{string}' ({e_name})")]
    ExtraUnneededString { string: String },

    #[error("Parsing shape needed but not provided on {variant} ({e_name})")]
    ShapeNeeded { variant: String },

    #[error("Circuit by name not found: {name} ({e_name})")]
    CircuitRefNotFound { name: String },

    #[error("Einsum string invalid {string} {substring} ({e_name})")]
    EinsumStringInvalid { string: String, substring: String },

    #[error("Einsum string doesn't have arrow {string} ({e_name})")]
    EinsumStringNoArrow { string: String },

    #[error("actual_num_circuits={actual_num_circuits} ({e_name})")]
    ExpectedOneCircuitGotMultiple { actual_num_circuits: usize },

    #[error("expected 't' or 'f' got='{got}' ({e_name})")]
    InvalidTerseBool { got: String },

    #[error("reference_name={reference_name} ({e_name})")]
    ReferenceCircuitHasChildrenInParseStr { reference_name: String },

    #[error("reference_name={reference_name} ({e_name})")]
    ReferenceCircuitNameFollowedByAdditionalInfo {
        reference_name: String,
        line: String,
    },

    #[error("repeat_ident={repeat_ident} \n{err_strs}line='{line}' ({e_name})")]
    OnCircuitRepeatInfoIsNotSame {
        repeat_ident: String,
        line: String,
        err_strs: String,
    },

    #[error("num_chars={num_chars} extra='{extra}' name={name:?}\nmodule extra should look like 'tt,tf,ft' and we check for 2 chars per comma delimited item.\n({e_name})")]
    Expected2CharsPerForModuleExtra {
        name: Option<String>,
        num_chars: usize,
        extra: String,
    },

    #[error("num_children={num_children} != 2 * num_args={num_args:?} + 1\nname={name:?} extra={extra}\n{}\n{}\n{}\n({e_name})",
    "modules have 1 child for the spec and then a symbol and a input circuit for each arg (2 * num_args + 1)",
    "this implies the number of children is always odd",
    "num_args is based on parsing the batchable and expandable info from 'extra' (see above) (in a form like 'tt,tf,ft' (Some(3)) or 'all_t' (None))")]
    ModuleInconsistentNumChildren {
        name: Option<String>,
        num_children: usize,
        extra: String,
        num_args: Option<usize>,
    },

    #[error("factors={factors:?} string='{string}' ({e_name})")]
    FactorProductTooLarge { factors: Vec<usize>, string: String },

    #[error("i={i} >= bound={bound} ({e_name})")]
    SymbolicSizeNumberOutOfBounds { i: usize, bound: usize },
}

impl From<ParseIntError> for ParseError {
    fn from(value: ParseIntError) -> Self {
        ParseError::NumberFail {
            err_string: value.to_string(),
        }
    }
}

impl From<ParseFloatError> for ParseError {
    fn from(value: ParseFloatError) -> Self {
        ParseError::NumberFail {
            err_string: value.to_string(),
        }
    }
}
