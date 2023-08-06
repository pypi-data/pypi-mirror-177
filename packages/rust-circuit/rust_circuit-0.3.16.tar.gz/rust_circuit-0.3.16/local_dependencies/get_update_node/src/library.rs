use anyhow::Result;
use circuit_base::{CircuitNode, CircuitRc, Symbol};
use circuit_rewrites::circuit_manipulation::replace_nodes_py;
use macro_rules_attribute::apply;
use pyo3::prelude::*;
use rr_util::{cached_method, pycall, util::HashBytes};
use rustc_hash::FxHashMap as HashMap;

use crate::IterativeMatcherRc;

#[pyfunction]
#[pyo3(name = "apply_in_traversal")]
pub fn apply_in_traversal_py(
    circuit: CircuitRc,
    traversal: IterativeMatcherRc,
    f: PyObject,
) -> Result<CircuitRc> {
    apply_in_traversal(circuit, traversal, |z| pycall!(f, (z,), anyhow))
}

pub fn apply_in_traversal<F>(
    circuit: CircuitRc,
    traversal: IterativeMatcherRc,
    f: F,
) -> Result<CircuitRc>
where
    F: Fn(CircuitRc) -> Result<CircuitRc>,
{
    let (symbol_replaced, back_map) = replace_outside_traversal_symbols(circuit, traversal, |x| {
        Ok(x.name().map(|n| format!("{}_symbol_replacement", n)))
    })?;
    let applied = f(symbol_replaced)?;
    Ok(replace_nodes_py(applied, back_map))
}

#[pyfunction]
#[pyo3(name = "replace_outside_traversal_symbols")]
pub fn replace_outside_traversal_symbols_py(
    circuit: CircuitRc,
    traversal: IterativeMatcherRc,
    namer: Option<PyObject>,
) -> Result<(CircuitRc, HashMap<CircuitRc, CircuitRc>)> {
    replace_outside_traversal_symbols(circuit, traversal, move |z| {
        if let Some(n) = &namer {
            pycall!(n, (z,), anyhow)
        } else {
            Ok(z.name_cloned())
        }
    })
}
pub fn replace_outside_traversal_symbols<F>(
    circuit: CircuitRc,
    traversal: IterativeMatcherRc,
    namer: F,
) -> Result<(CircuitRc, HashMap<CircuitRc, CircuitRc>)>
where
    F: Fn(CircuitRc) -> Result<Option<String>>,
{
    // using caching struct so i can mutate back map while cached recursing
    struct Thing {
        back_map: HashMap<CircuitRc, CircuitRc>,
        estimated_cache: cached::UnboundCache<(HashBytes, IterativeMatcherRc), CircuitRc>,
    }
    impl Thing {
        #[apply(cached_method)]
        #[self_id(self_)]
        #[key((circuit.info().hash,matcher.clone()))]
        #[use_try]
        #[cache_expr(estimated_cache)]
        fn recurse(
            &mut self,
            circuit: CircuitRc,
            matcher: IterativeMatcherRc,
            namer: &dyn Fn(CircuitRc) -> Result<Option<String>>,
        ) -> Result<CircuitRc> {
            if let (Some(new_matcher), _) = matcher
                .match_iterate(circuit.clone())?
                .none_if_finished(matcher)
            {
                // let z =  circuit.map_children(|x| recurse(x, new_matcher, back_map));
                return circuit.map_children(|x| self_.recurse(x, new_matcher.clone(), namer));
            } else {
                let newey = Symbol::new_with_random_uuid(
                    circuit.info().shape.clone(),
                    namer(circuit.clone())?,
                )
                .rc();
                self_.back_map.insert(newey.clone(), circuit.clone());
                return Ok(newey);
            }
        }
    }
    let mut thing = Thing {
        back_map: Default::default(),
        estimated_cache: cached::UnboundCache::new(),
    };
    let circ_result = thing.recurse(circuit, traversal, &namer)?;
    Ok((circ_result, thing.back_map))
}
