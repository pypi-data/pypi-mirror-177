use anyhow::Result;
use circuit_base::{CircuitNode, CircuitRc, Module, ModuleArgSpec};
use circuit_rewrites::module_rewrite::extract_rewrite_raw;
use get_update_node::MatcherRc;
use pyo3::{prelude::*, PyObject};
use rr_util::pycall;

#[pyfunction]
pub fn extract_rewrite(
    circuit: CircuitRc,
    matcher: MatcherRc,
    prefix_to_strip: Option<String>,
    module_name: Option<String>,
    spec_name: Option<String>,
    circuit_to_spec: Option<PyObject>,
) -> Result<Module> {
    let edges: Vec<CircuitRc> = matcher.get(circuit.clone(), true)?.into_iter().collect();
    dbg!(&edges);
    let mut specs: Vec<(CircuitRc, ModuleArgSpec)> = edges
        .into_iter()
        .map(|n| {
            if let Some(cts) = &circuit_to_spec {
                pycall!(cts, (n.clone(),), anyhow)
            } else {
                Ok(ModuleArgSpec::just_name(n.clone(), true, true))
            }
            .map(|z| (n, z))
        })
        .collect::<Result<Vec<_>>>()?;
    dbg!(&specs);
    specs.sort_by_key(|x| x.1.symbol.name_cloned());
    dbg!(&specs);
    extract_rewrite_raw(
        circuit,
        specs,
        prefix_to_strip,
        module_name,
        spec_name,
        false,
    )
}
