use anyhow::Result;
use circuit_base::{CircuitNode, CircuitRc, Module, ModuleArgSpec};
use circuit_rewrites::module_rewrite::extract_rewrite_raw;
use get_update_node::IterativeMatcherRc;
use pyo3::{prelude::*, PyObject};
use rr_util::pycall;

#[pyfunction(
    prefix_to_strip = "None",
    module_name = "None",
    require_all_args = "true",
    check_unique_arg_names = "true",
    circuit_to_spec = "None"
)]
pub fn extract_rewrite(
    circuit: CircuitRc,
    matcher: IterativeMatcherRc,
    prefix_to_strip: Option<String>,
    module_name: Option<String>,
    require_all_args: bool,
    check_unique_arg_names: bool,
    circuit_to_spec: Option<PyObject>,
) -> Result<Module> {
    let edges: Vec<CircuitRc> = matcher.get(circuit.clone(), true)?.into_iter().collect();
    let mut specs: Vec<(CircuitRc, ModuleArgSpec)> = edges
        .into_iter()
        .map(|n| {
            if let Some(cts) = &circuit_to_spec {
                pycall!(cts, (n.clone(),), anyhow)
            } else {
                Ok(ModuleArgSpec::just_name_shape(n.clone(), true, true))
            }
            .map(|z| (n, z))
        })
        .collect::<Result<Vec<_>>>()?;
    specs.sort_by_key(|x| x.1.symbol.name_cloned());
    extract_rewrite_raw(
        circuit,
        specs,
        prefix_to_strip,
        module_name,
        require_all_args,
        check_unique_arg_names,
    )
}
