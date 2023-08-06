use anyhow::{bail, Result};
use circuit_base::{
    deep_map_op_context, deep_map_preorder_unwrap, deep_map_unwrap, on_circuit_names, prelude::*,
    visit_circuit_unwrap, Add, Index,
};
use itertools::Itertools;
use macro_rules_attribute::apply;
use num_bigint::BigUint;
use pyo3::{exceptions::PyValueError, prelude::*};
use rr_util::{
    python_error_exception, timed, timed_value,
    util::{apply_fn_until_none, apply_fn_until_same, mapping_until_end, AsOp, HashBytes},
};
use rustc_hash::FxHashMap as HashMap;
use thiserror::Error;

use crate::{
    algebraic_rewrite::*,
    batching::batch_einsum,
    canonicalize::deep_canonicalize,
    circuit_optimizer::OptimizationContext,
    concat_rewrite::{
        add_pull_concat, concat_drop_size_zero, concat_fuse, einsum_pull_concat,
        generalfunction_pull_concat, index_concat_drop_unreached,
    },
    diag_rewrite::{add_pull_diags, einsum_push_down_trace},
    generalfunction_rewrite::{
        generalfunction_evaluate_simple, generalfunction_merge_inverses,
        generalfunction_special_case_simplification,
    },
    module_rewrite::elim_empty_module,
    nb_rewrites::{add_elim_removable_axes_weak, einsum_elim_removable_axes_weak},
    scatter_rewrite::{
        add_pull_scatter, concat_to_scatter, einsum_pull_scatter, index_einsum_to_scatter,
        scatter_elim_identity, scatter_fuse, scatter_pull_removable_axes,
    },
};

fn run_simp<T: CircuitNode + Into<Circuit> + Clone>(
    x: &'_ T,
    fns: &[(&'static str, &dyn Fn(&'_ T) -> Option<CircuitRc>)],
    mut on_name: impl FnMut(&'static str),
) -> Option<CircuitRc> {
    for (name, f) in fns {
        if let Some(result) = f(x) {
            if **result == x.clone().c() {
                println!("{}", name);
                x.printu();
                panic!()
            }
            on_name(name);
            return Some(result);
        }
    }

    None
}

macro_rules! f_wrap {
    ($f:expr) => {
        f_wrap!($f, stringify!($f))
    };
    ($f:expr, $str:expr) => {
        ($str, &|x| $f(x).map(|v| v.rc()))
    };
}

macro_rules! l_wrap {
    ($f:expr) => {
        l_wrap!($f, stringify!($f))
    };
    ($f:expr, $str:expr) => {
        ($str, &|x| $f(x))
    };
}

macro_rules! mk_simp_fns {
    ($($circ_ty:ident,)*) => (
        paste::paste! {
            #[derive(Default)]
            struct SimpFns {
                $(
                    [<$circ_ty:snake>] : Vec<(&'static str, &'static dyn Fn(&circuit_base::$circ_ty) -> Option<CircuitRc>)>,
                )*
            }

            macro_rules! match_circ_with_simp_fns {
                ($match_expr:expr; ($node_name:ident, $simp_fns_name:ident) => $e:expr) => (
                    match $match_expr {
                    $(
                        (Circuit::$circ_ty($node_name), SimpFns { [<$circ_ty:snake>] : $simp_fns_name, ..}) => $e,
                    )*
                    }
                )
            }

            macro_rules! map_simp_fns {
                ($match_expr:expr;  $simp_fns_name:ident => $e:expr) => (
                    SimpFns {
                    $(
                    [<$circ_ty:snake>] : {
                        let SimpFns { [<$circ_ty:snake>] : $simp_fns_name, .. } = $match_expr;
                        $e
                    },
                    )*
                    }
                )
            }

            macro_rules! simp_fns_for_all {
                ($match_expr:expr;  $simp_fns_name:ident => $e:expr) => (
                    $(
                    {
                        let SimpFns { [<$circ_ty:snake>] : $simp_fns_name, .. } = $match_expr;
                        $e
                    };
                    )*
                )
            }

            macro_rules! map_simp_fns_arr_name {
                ($match_expr:expr;  ($simp_fns_name:ident, $circ_ty_name:ident) => $e:expr) => (
                    [
                    $(
                    {
                        let SimpFns { [<$circ_ty:snake>] : $simp_fns_name, .. } = $match_expr;
                        let $circ_ty_name = stringify!($circ_ty);
                        $e
                    },
                    )*
                    ]

                )
            }
        }
    )
}

on_circuit_names!(mk_simp_fns);

fn all_simp_fns() -> SimpFns {
    SimpFns {
        add: vec![
            l_wrap!(remove_add_few_input),
            f_wrap!(add_flatten_once, "add_flatten"),
            f_wrap!(add_elim_zeros),
            f_wrap!(add_collapse_scalar_inputs),
            f_wrap!(add_deduplicate),
            l_wrap!(
                |x| add_pull_removable_axes(x, true),
                "add_pull_removable_axes"
            ),
            f_wrap!(add_pull_scatter),
            f_wrap!(add_pull_diags),
            f_wrap!(add_fuse_scalar_multiples),
            f_wrap!(add_elim_removable_axes_weak), // TODO: I don't understand this
        ],
        einsum: vec![
            f_wrap!(einsum_elim_zero),
            l_wrap!(einsum_elim_identity),
            f_wrap!(einsum_flatten_once, "einsum_flatten"),
            f_wrap!(einsum_of_permute_merge),
            f_wrap!(einsum_merge_scalars),
            l_wrap!(einsum_pull_removable_axes),
            f_wrap!(einsum_elim_removable_axes_weak), // TODO: maybe understand this
            f_wrap!(einsum_permute_to_rearrange),
            l_wrap!(einsum_pull_scatter),
            f_wrap!(einsum_push_down_trace),
            f_wrap!(einsum_concat_to_add),
        ],
        index: vec![
            l_wrap!(index_elim_identity),
            f_wrap!(index_fuse),
            l_wrap!(index_merge_scalar),
            l_wrap!(index_einsum_to_scatter),
            l_wrap!(index_concat_drop_unreached),
        ],
        rearrange: vec![
            l_wrap!(rearrange_elim_identity),
            f_wrap!(rearrange_fuse),
            l_wrap!(rearrange_merge_scalar),
            f_wrap!(permute_of_einsum_merge),
        ],
        concat: vec![
            l_wrap!(concat_elim_identity),
            l_wrap!(concat_pull_removable_axes),
            l_wrap!(concat_merge_uniform),
            f_wrap!(concat_drop_size_zero),
            f_wrap!(concat_fuse),
            f_wrap!(concat_repeat_to_rearrange),
            f_wrap!(concat_to_scatter),
        ],
        general_function: vec![
            l_wrap!(generalfunction_pull_removable_axes),
            l_wrap!(generalfunction_merge_inverses),
            l_wrap!(generalfunction_special_case_simplification),
            l_wrap!(generalfunction_evaluate_simple),
        ],
        scatter: vec![
            l_wrap!(scatter_elim_identity),
            f_wrap!(scatter_fuse),
            f_wrap!(scatter_pull_removable_axes),
        ],
        module: vec![l_wrap!(elim_empty_module)],
        ..Default::default()
    }
}

#[pyclass]
#[derive(Debug, Clone, Eq, PartialEq)]
pub struct SimpFnSubset(HashMap<String, bool>);

impl Default for SimpFnSubset {
    /// default to python simp, see compiler_default for compiler simplification
    fn default() -> Self {
        let sub_fns = [
            "remove_add_few_input",
            "add_elim_zeros",
            "add_deduplicate",
            "add_elim_removable_axes_weak",
            "einsum_elim_zero",
            "einsum_elim_identity",
            "einsum_of_permute_merge",
            "einsum_elim_removable_axes_weak",
            "einsum_permute_to_rearrange",
            "index_elim_identity",
            "index_merge_scalar",
            "rearrange_elim_identity",
            "rearrange_fuse",
            "rearrange_merge_scalar",
            "permute_of_einsum_merge",
            "concat_elim_identity",
            "concat_merge_uniform",
            "concat_drop_size_zero",
            "concat_fuse",
            "concat_repeat_to_rearrange",
        ]
        .into_iter()
        .map(|x| x.to_owned())
        .collect();

        Self::none().include(sub_fns).unwrap()
    }
}

#[pymethods]
impl SimpFnSubset {
    #[staticmethod]
    pub fn all_names() -> Vec<&'static str> {
        let fns = all_simp_fns();
        let mut out = Vec::new();
        simp_fns_for_all!(&fns; fns_sub => out.extend(fns_sub.iter().map(|(s, _)| s)));
        out
    }

    #[getter]
    pub fn values(&self) -> HashMap<String, bool> {
        self.0.clone()
    }

    #[staticmethod]
    pub fn init_all_with(include: bool) -> Self {
        let mapping = Self::all_names()
            .into_iter()
            .map(|x| (x.to_owned(), include))
            .collect();
        Self(mapping)
    }

    #[staticmethod]
    pub fn none() -> Self {
        Self::init_all_with(false)
    }

    #[staticmethod]
    pub fn all() -> Self {
        Self::init_all_with(true)
    }

    #[staticmethod]
    #[pyo3(name = "default")]
    pub fn default_py() -> Self {
        Self::default()
    }

    #[staticmethod]
    pub fn compiler_default() -> Self {
        Self::all()
            .exclude(
                [
                    "add_elim_removable_axes_weak",
                    "einsum_elim_removable_axes_weak",
                ]
                .into_iter()
                .map(|x| x.to_owned())
                .collect(),
            )
            .unwrap()
    }

    pub fn none_repr(&self) -> String {
        let all_args = Self::arg_fmt(
            |n| Some(format!(" = {}", if self.0[n] { "True" } else { "False" })),
            false,
        );
        format!("SimpFnSubset.none().set(\n{}\n)", all_args)
    }

    pub fn __repr__(&self) -> String {
        let default = Self::default();
        let all_args = Self::arg_fmt(
            |n| {
                (self.0[n] != default.0[n])
                    .then(|| format!(" = {}", if self.0[n] { "True" } else { "False" }))
            },
            true,
        );
        if all_args.is_empty() {
            "SimpFnSubset.default()".to_owned()
        } else {
            format!("SimpFnSubset.default().set(\n{}\n)", all_args)
        }
    }

    pub fn check_names(&self, names: Vec<String>) -> Result<()> {
        let not_contained: Vec<_> = names.iter().filter(|x| !self.0.contains_key(*x)).collect();
        if !not_contained.is_empty() {
            bail!(SimpConfigError::FnNamesNotValid {
                names: not_contained.into_iter().map(|x| x.to_owned()).collect()
            })
        }
        Ok(())
    }

    pub fn set_all_to(&self, names: Vec<String>, include: bool) -> Result<Self> {
        self.check_names(names.clone())?;

        let mut new = self.0.clone();
        for k in names {
            new.insert(k, include).expect("should have this key");
        }
        Ok(Self(new))
    }

    #[args(set_vals = "**")]
    #[pyo3(name = "set")]
    pub fn set_py(&self, set_vals: Option<HashMap<String, Option<bool>>>) -> Result<Self> {
        if set_vals.is_none() {
            return Ok(self.clone());
        }
        let set_vals = set_vals.unwrap();
        self.check_names(set_vals.keys().cloned().collect())?;
        let mut new = self.0.clone();
        new.extend(set_vals.into_iter().filter_map(|(k, v)| v.map(|v| (k, v))));
        Ok(Self(new))
    }

    pub fn exclude(&self, names: Vec<String>) -> Result<Self> {
        self.set_all_to(names, false)
    }

    pub fn include(&self, names: Vec<String>) -> Result<Self> {
        self.set_all_to(names, true)
    }

    #[pyo3(name = "simp_step")]
    pub fn simp_step_py(&self, circuit: CircuitRc) -> Option<CircuitRc> {
        self.simp_step(&*circuit)
    }

    pub fn simp(&self, circuit: CircuitRc) -> CircuitRc {
        self.simp_ctx(circuit, &mut Default::default())
    }
}

impl SimpFnSubset {
    fn simp_fns(&self) -> SimpFns {
        map_simp_fns!(all_simp_fns(); fns_sub => fns_sub.into_iter().filter(|(s, _)| self.0[*s]).collect())
    }

    pub fn simp_step(&self, circuit: &Circuit) -> Option<CircuitRc> {
        match_circ_with_simp_fns!(
            (circuit, self.simp_fns());
            (node, fns_sub) => run_simp(node, &fns_sub, |_| ())
        )
    }

    pub fn simp_step_log(
        &self,
        circuit: &Circuit,
        context: &mut OptimizationContext,
    ) -> Option<CircuitRc> {
        let on_name = |name| {
            if context.settings.log_simplifications {
                if context.settings.verbose >= 3 {
                    println!("{}", name);
                }
                context.cache.simplification_log.push(name);
            }
        };

        match_circ_with_simp_fns!(
            (circuit, self.simp_fns());
            (node, fns_sub) => run_simp(node, &fns_sub, on_name)
        )
    }

    /// mild footgun: if you use the same context with multiple different SimpFnSubset, then caching will be wrong
    pub fn simp_ctx(&self, circuit: CircuitRc, opt_context: &mut OptimizationContext) -> CircuitRc {
        deep_simp(circuit, opt_context, |c, context| {
            self.simp_step_log(c, context)
        })
    }

    pub fn arg_fmt(f: impl Fn(&'static str) -> Option<String>, exclude_if_none: bool) -> String {
        let fns = all_simp_fns();
        let tab = " ".repeat(4);
        map_simp_fns_arr_name!(&fns; (sub_fns, circ_ty) => {
            let sub_str = sub_fns
                .iter()
                .filter_map(|(n, _)| Some(format!("{}{}{},", tab, n, f(n)?)))
                .join("\n");

            if sub_str.is_empty() {
                if exclude_if_none {
                    None
                } else {
                    Some(format!("{}# {} (none)", tab, circ_ty))
                }
            } else {
                Some(format!("{}# {}\n{}", tab, circ_ty, sub_str))
            }
        })
        .into_iter()
        .filter_map(|x| x)
        .join("\n")
    }
}

#[apply(python_error_exception)]
#[base_error_name(SimpConfig)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum SimpConfigError {
    #[error("names={names:?} ({e_name})")]
    FnNamesNotValid { names: Vec<String> },
}

#[pyfunction]
#[pyo3(name = "compiler_simp_step")]
pub fn compiler_simp_step_py(circuit: CircuitRc) -> Option<CircuitRc> {
    SimpFnSubset::compiler_default().simp_step(&circuit)
}

#[pyfunction]
#[pyo3(name = "compiler_simp")]
pub fn compiler_simp_py(circuit: CircuitRc) -> CircuitRc {
    SimpFnSubset::compiler_default().simp(circuit)
}

pub fn compiler_simp(circ: CircuitRc, opt_context: &mut OptimizationContext) -> CircuitRc {
    SimpFnSubset::compiler_default().simp_ctx(circ, opt_context)
}

#[pyfunction]
pub fn simp(circuit: CircuitRc) -> CircuitRc {
    SimpFnSubset::default().simp(circuit)
}

/// Deep simplification strategy
///
/// The strategy to apply `f` to each node in the circuit from the bottom up (post-order).
/// Every time a node is simplified, we iterate over the children to make sure that any children we haven't
/// seen before get recursively fully simplified before continuing.
/// The final result is a fixed point where no further `f` simplifications are possible.
pub fn deep_simp<F>(circ: CircuitRc, opt_context: &mut OptimizationContext, f: F) -> CircuitRc
where
    F: Fn(&Circuit, &mut OptimizationContext) -> Option<CircuitRc>,
{
    /// check if any new children have not been simplified yet, and simplify them if so
    fn simplify_changed_descendants<F>(
        circ: CircuitRc,
        context: &mut OptimizationContext,
        f: &F,
    ) -> Option<CircuitRc>
    where
        F: Fn(&Circuit, &mut OptimizationContext) -> Option<CircuitRc>,
    {
        circ.map_children_op(&mut |x: CircuitRc| {
            if context.cache.simplified.contains_key(&x.info().hash) {
                None
            } else {
                Some(fully_simplify(x, context, f))
            }
        })
        .map(|c| c.rc())
    }
    /// fully simplify a circuit and all its descendants recursively until we hit a fixed point
    fn fully_simplify<F>(circ: CircuitRc, context: &mut OptimizationContext, f: &F) -> CircuitRc
    where
        F: Fn(&Circuit, &mut OptimizationContext) -> Option<CircuitRc>,
    {
        if let Some(result) = context.cache.simplified.get(&circ.info().hash) {
            return result.clone();
        }
        let mut result: CircuitRc = circ
            .map_children_unwrap(&mut |x: CircuitRc| fully_simplify(x, context, f))
            .rc();
        for iter_count in 0.. {
            match f(&result, context) {
                Some(r) => {
                    result = simplify_changed_descendants(r.clone(), context, f).unwrap_or(r)
                }
                None => break,
            }
            if iter_count > 50 {
                result.printu();
                f(&result, context).unwrap().printu();
                panic!();
            }
        }
        context
            .cache
            .simplified
            .insert(circ.info().hash, result.clone());
        result
    }
    fully_simplify(circ, opt_context, &f)
}

#[pyfunction] // maybe remove
pub fn deep_push_down_index_raw(circ: CircuitRc, min_size: Option<usize>) -> CircuitRc {
    deep_map_preorder_unwrap(circ, |circ| {
        if min_size.is_none()
            || circ
                .children()
                .chain(std::iter::once(circ.clone()))
                .any(|z| z.info().numel() >= BigUint::from(min_size.unwrap()))
        {
            (**circ).map_or_clone(&|index: &Index| {
                let fused = apply_fn_until_none(index, index_fuse);
                index_elim_identity(&fused)
                    .unwrap_or_else(|| push_down_index_op(&fused).unwrap_or_else(|| fused.crc()))
            })
        } else {
            circ
        }
    })
}

#[derive(Debug, Clone, Default)]
pub struct CircBloomFilter {
    pub bits: u128,
}
impl CircBloomFilter {
    #[inline]
    pub fn insert(&mut self, x: usize) {
        self.bits |= 1 << (x & 0b1111111)
    }
    #[inline]
    pub fn contains(&mut self, x: usize) -> bool {
        self.bits & 1 << (x & 0b1111111) != 0
    }
    #[inline]
    pub fn is_superset(&self, other: &CircBloomFilter) -> bool {
        other.bits & !self.bits == 0
    }
    #[inline]
    pub fn intersection_count(&self, other: &CircBloomFilter) -> u32 {
        (other.bits & self.bits).count_ones()
    }
}

/// we want adds to be nested rather than flat so arguments can be dropped if they're only needed
/// in future adds
/// this is suboptimal in many ways. one is broadcasts allow outer products which should be avoided but aren't
/// for each add, greedily nest into preexisting adds
fn child_bloom_filter(add: &Add) -> CircBloomFilter {
    let mut result: CircBloomFilter = Default::default();
    for node in &add.nodes {
        result.insert(node.info().hash_usize());
    }
    result
}
#[pyfunction]
pub fn deep_heuristic_nest_adds(circ: CircuitRc) -> CircuitRc {
    let circ = deep_canonicalize(circ, &mut Default::default());
    let mut seen_adds: Vec<(Add, CircBloomFilter)> = vec![];
    visit_circuit_unwrap(circ.clone(), |c: CircuitRc| {
        if let Some(add) = c.as_add() {
            seen_adds.push((add.clone(), child_bloom_filter(add)));
        }
    });
    // TODO: profile and optimize these

    let mut intersections: HashMap<Add, CircBloomFilter> = HashMap::default();
    for circ in &seen_adds {
        for circ2 in &seen_adds {
            if circ.1.intersection_count(&circ2.1) >= 2 && circ.0 != circ2.0 {
                let intersection = Add::new(
                    circ.0
                        .nodes
                        .iter()
                        .filter(|x| circ2.0.nodes.contains(x))
                        .cloned()
                        .collect(),
                    None,
                );
                if intersection.nodes.len() >= 2
                    && &intersection != &circ.0
                    && &intersection != &circ2.0
                {
                    intersections.insert(intersection.clone(), child_bloom_filter(&intersection));
                }
            }
        }
    }
    seen_adds.extend(intersections);
    let mut seen_adds_index: HashMap<HashBytes, usize> = seen_adds
        .iter()
        .enumerate()
        .map(|(i, (c, _b))| (c.info().hash, i))
        .collect();
    let mut mapping: HashMap<Add, Add> = HashMap::default();
    for _ in 0..3 {
        let mut to_do: Vec<((Add, CircBloomFilter), (Add, CircBloomFilter))> = vec![];
        for cand_sup in &seen_adds {
            if cand_sup.0.nodes.len() >= 3 {
                for cand_sub in &seen_adds {
                    if cand_sup.1.is_superset(&cand_sub.1)
                        && cand_sub.0.nodes.len() < cand_sup.0.nodes.len()
                        && cand_sub.0 != cand_sup.0
                    {
                        if let Some(new) = extract_add(&cand_sup.0, &cand_sub.0) {
                            let new_entry = (new.clone(), child_bloom_filter(&new));
                            to_do.push(((cand_sup.0.clone(), cand_sup.1.clone()), new_entry));
                        }
                    }
                }
            }
        }
        // println!("nest op counts bloom {} extract {} join {}",bloom_count,extract_count,join_count);
        if to_do.is_empty() {
            break;
        }
        for (sup, new_sup) in to_do {
            let mut seen_index = seen_adds_index.remove(&sup.0.info().hash);
            let to_insert = (new_sup.0.clone(), new_sup.1.clone());
            if let Some(si) = seen_index {
                seen_adds[si] = to_insert;
            } else {
                seen_index = Some(seen_adds.len());
                seen_adds.push(to_insert);
            }
            if !seen_adds_index.contains_key(&new_sup.0.info().hash) {
                seen_adds_index.insert(new_sup.0.info().hash, seen_index.unwrap());
            }
            mapping.insert(sup.0.clone(), new_sup.0.clone());
        }
        // break
    }

    deep_map_preorder_unwrap(circ, |c| {
        (**c).map_or_clone(|add: &Add| {
            let add = mapping_until_end(add, &mapping);

            if add.info().numel() > BigUint::from(100_000_000usize) {
                add_nest_ltr(&add)
            } else {
                add
            }
        })
    })
}

pub fn add_nest_ltr(add: &Add) -> Add {
    let (l, r) = add.nodes.split_at(2.min(add.nodes.len()));
    let base = Add::new(l.to_vec(), None);
    r.iter()
        .fold(base, |acc, x| Add::new(vec![acc.rc(), x.clone()], None))
}

#[pyfunction]
#[pyo3(name = "add_nest_ltr")]
pub fn add_nest_ltr_py(add: Add) -> Add {
    add_nest_ltr(&add)
}

#[pyfunction]
pub fn deep_pull_concat_messy(circuit: CircuitRc, min_size: Option<usize>) -> CircuitRc {
    deep_map_unwrap(circuit, &|x: CircuitRc| {
        if min_size.is_none()
            || x.children()
                .chain(std::iter::once(x.clone()))
                .any(|z| z.info().numel() >= BigUint::from(min_size.unwrap()))
        {
            match &**x {
                Circuit::Add(add) => add.and_then_or_clone(add_pull_concat),
                Circuit::GeneralFunction(func) => {
                    func.and_then_or_clone(generalfunction_pull_concat)
                }
                Circuit::Einsum(einsum) => einsum.and_then_or_clone(einsum_pull_concat),
                Circuit::Concat(concat) => concat.and_then_or_clone(concat_fuse),
                _ => x.clone(),
            }
        } else {
            x
        }
    })
}

#[pyfunction]
pub fn deep_pull_concat(circuit: CircuitRc, min_size: Option<usize>) -> CircuitRc {
    let mut cache = Default::default();
    let pulled = deep_pull_concat_messy(circuit, min_size);
    apply_fn_until_same(&pulled, |x: &CircuitRc| {
        deep_push_down_index_raw(compiler_simp(x.clone(), &mut cache), min_size)
    })
}

#[pyfunction]
#[pyo3(name = "deep_optimize_einsums")]
pub fn deep_optimize_einsums_py(circ: CircuitRc) -> CircuitRc {
    deep_optimize_einsums(circ, &mut Default::default())
}

pub fn deep_optimize_einsums(circ: CircuitRc, context: &mut OptimizationContext) -> CircuitRc {
    deep_map_op_context(
        circ.clone(),
        &|x: CircuitRc, context: &mut OptimizationContext| match &**x {
            Circuit::Einsum(ein) => {
                let (result, took) = timed_value!(einsum_nest_optimize(ein, context));
                if result.is_none() {
                    Some(timed!(batch_einsum(ein, context).unwrap()))
                } else {
                    let result = result?;
                    if context.settings.log_slow_einsums && took.as_millis() > 10 {
                        context.cache.slow_einsum_log.push(ein.get_spec());
                    }
                    Some(result.rc())
                }
            }
            _ => None,
        },
        context,
        &mut HashMap::default(),
    )
    .unwrap_or(circ)
}
