use std::{fmt::Debug, ops::Deref, sync::Arc};

use anyhow::Result;
use macro_rules_attribute::apply;
use pyo3::{exceptions::PyTypeError, prelude::*, pyclass::CompareOp, PyObject};
use rr_util::{py_types::use_rust_comp, python_error_exception};
use thiserror::Error;

use crate::CircuitRc;

#[derive(Debug, Clone)]
pub enum OpaqueIterativeMatcherVal {
    Py(PyObject),
    Dyn(Arc<dyn OpaqueIterativeMatcher + Send + Sync>),
}

impl<'source> FromPyObject<'source> for OpaqueIterativeMatcherVal {
    fn extract(inp: &'source PyAny) -> PyResult<Self> {
        let ty = inp.get_type();
        let name = ty.name()?;
        let expected_name = "IterativeMatcher";
        if name != expected_name {
            return Err(anyhow::Error::from(IncorrectOpaqueTypeError::NameMismatch {
                actual_name: name.to_owned(),
                expected_name: expected_name.to_owned(),
            })
            .into());
        }

        Ok(Self::Py(inp.into()))
    }
}

#[pyclass]
#[derive(Copy, Clone, Eq, PartialEq, Ord, PartialOrd)]
pub struct Finished;

#[pymethods]
impl Finished {
    fn __richcmp__(&self, object: &Self, comp_op: CompareOp) -> bool {
        use_rust_comp(&self, &object, comp_op)
    }
    fn __hash__(&self) -> u64 {
        15802471944074381489
    }
}

#[derive(FromPyObject, Clone)]
pub enum UpdateImpl<Matcher> {
    Finished(Finished),
    Update(Matcher),
}

#[derive(Debug, Clone)]
// none if finished
pub struct Update<Matcher>(pub Option<Matcher>);

impl<'source, Matcher: FromPyObject<'source>> FromPyObject<'source> for Update<Matcher> {
    fn extract(inp: &'source PyAny) -> PyResult<Self> {
        let x: UpdateImpl<_> = inp.extract()?;
        let out = match x {
            UpdateImpl::Update(x) => Some(x),
            UpdateImpl::Finished(Finished) => None,
        };
        Ok(Update(out))
    }
}

impl<Matcher: IntoPy<PyObject>> IntoPy<PyObject> for Update<Matcher> {
    fn into_py(self, py: Python<'_>) -> PyObject {
        match self.0 {
            Some(x) => x.into_py(py),
            None => Finished.into_py(py),
        }
    }
}

impl<Matcher> From<Option<Matcher>> for Update<Matcher> {
    fn from(value: Option<Matcher>) -> Self {
        Update(value)
    }
}

impl<Matcher> From<Update<Matcher>> for Option<Matcher> {
    fn from(value: Update<Matcher>) -> Self {
        value.0
    }
}

impl<Matcher> Deref for Update<Matcher> {
    type Target = Option<Matcher>;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Clone, Debug, FromPyObject)]
pub enum UpdatedIterativeMatcher<Matcher> {
    Many(Vec<Update<Matcher>>),
    Single(Update<Matcher>),
}

impl<Matcher: IntoPy<PyObject>> IntoPy<PyObject> for UpdatedIterativeMatcher<Matcher> {
    fn into_py(self, py: Python<'_>) -> PyObject {
        match self {
            Self::Many(x) => x.into_py(py),
            Self::Single(x) => x.into_py(py),
        }
    }
}

impl<Matcher> From<Update<Matcher>> for UpdatedIterativeMatcher<Matcher> {
    fn from(value: Update<Matcher>) -> Self {
        Self::Single(value)
    }
}
impl<Matcher> From<Option<Matcher>> for UpdatedIterativeMatcher<Matcher> {
    fn from(value: Option<Matcher>) -> Self {
        Self::Single(value.into())
    }
}
impl<Matcher> From<Vec<Update<Matcher>>> for UpdatedIterativeMatcher<Matcher> {
    fn from(value: Vec<Update<Matcher>>) -> Self {
        Self::Many(value)
    }
}
impl<Matcher> From<Vec<Option<Matcher>>> for UpdatedIterativeMatcher<Matcher> {
    fn from(value: Vec<Option<Matcher>>) -> Self {
        value
            .into_iter()
            .map(Update::from)
            .collect::<Vec<_>>()
            .into()
    }
}

pub trait HasTerm {
    fn term() -> Self;
}

impl<Matcher: Clone + HasTerm> UpdatedIterativeMatcher<Matcher> {
    // make this pyfunction as needed
    pub fn per_child(self, num_children: usize) -> Vec<Option<Matcher>> {
        let out = match self {
            Self::Single(Update(item)) => vec![item; num_children],
            Self::Many(items) => {
                // should already have been checked!
                assert_eq!(items.len(), num_children);
                items.into_iter().map(|x| x.0).collect::<Vec<_>>()
            }
        };
        out
    }

    pub fn per_child_with_term(self, num_children: usize) -> Vec<Matcher> {
        self.per_child(num_children)
            .into_iter()
            .map(|x| x.unwrap_or_else(|| Matcher::term().into()))
            .collect()
    }

    pub fn all_finished(&self) -> bool {
        match self {
            Self::Single(x) => x.is_none(),
            Self::Many(x) => x.iter().all(|x| x.is_none()),
        }
    }

    pub fn map_updated(self, mut f: impl FnMut(Matcher) -> Matcher) -> Self {
        match self {
            Self::Single(x) => Self::Single(x.0.map(f).into()),
            Self::Many(x) => Self::Many(x.into_iter().map(|x| x.0.map(&mut f).into()).collect()),
        }
    }
}

pub fn all_finished<Matcher: Clone + HasTerm>(
    x: &Option<UpdatedIterativeMatcher<Matcher>>,
) -> bool {
    x.as_ref().map(|x| x.all_finished()).unwrap_or(false)
}
type OpaqueUpdatedIterativeMatcher = UpdatedIterativeMatcher<OpaqueIterativeMatcherVal>;

impl HasTerm for OpaqueIterativeMatcherVal {
    fn term() -> Self {
        Self::for_end_depth(0)
    }
}

#[derive(Debug, FromPyObject)]
pub struct OpaqueIterateMatchResults {
    pub updated: Option<OpaqueUpdatedIterativeMatcher>,
    pub found: bool,
}

pub trait OpaqueIterativeMatcher: Debug {
    fn opaque_match_iterate(&self, circuit: CircuitRc) -> Result<OpaqueIterateMatchResults>;
}

impl OpaqueIterativeMatcher for OpaqueIterativeMatcherVal {
    fn opaque_match_iterate(&self, circuit: CircuitRc) -> Result<OpaqueIterateMatchResults> {
        match self {
            Self::Py(obj) => Python::with_gil(|py| Ok(obj.call1(py, (circuit,))?.extract(py)?)),
            Self::Dyn(d) => d.opaque_match_iterate(circuit),
        }
    }
}

#[derive(Clone, Debug)]
pub struct EndDepthOpaqueIterativeMatcher {
    pub end_depth: usize,
    pub depth: usize,
}

impl OpaqueIterativeMatcher for EndDepthOpaqueIterativeMatcher {
    fn opaque_match_iterate(&self, _: CircuitRc) -> Result<OpaqueIterateMatchResults> {
        let found = self.depth < self.end_depth;
        if self.depth < self.end_depth.saturating_sub(1) {
            Ok(OpaqueIterateMatchResults {
                updated: Some(
                    Some(OpaqueIterativeMatcherVal::Dyn(Arc::new(Self {
                        end_depth: self.end_depth,
                        depth: self.depth + 1,
                    })))
                    .into(),
                ),
                found,
            })
        } else {
            Ok(OpaqueIterateMatchResults {
                updated: Some(None.into()),
                found,
            })
        }
    }
}
#[derive(Clone, Debug)]
pub struct NeverOpaqueIterativeMatcher;

impl OpaqueIterativeMatcher for NeverOpaqueIterativeMatcher {
    fn opaque_match_iterate(&self, _: CircuitRc) -> Result<OpaqueIterateMatchResults> {
        Ok(OpaqueIterateMatchResults {
            updated: None,
            found: false,
        })
    }
}

impl OpaqueIterativeMatcherVal {
    pub fn for_end_depth(end_depth: usize) -> Self {
        Self::Dyn(Arc::new(EndDepthOpaqueIterativeMatcher {
            end_depth,
            depth: 0,
        }))
    }

    pub fn never() -> Self {
        Self::Dyn(Arc::new(NeverOpaqueIterativeMatcher))
    }
}

#[apply(python_error_exception)]
#[base_error_name(IncorrectOpaqueType)]
#[base_exception(PyTypeError)]
#[derive(Error, Debug, Clone)]
pub enum IncorrectOpaqueTypeError {
    #[error("expected={expected_name} actual={actual_name} ({e_name})")]
    NameMismatch {
        actual_name: String,
        expected_name: String,
    },
}
