use std::iter::zip;

use anyhow::{anyhow, bail, Result};
use circuit_base::{
    circuit_utils::count_nodes, CircuitNode, CircuitRc, Concat, Module, ModuleArgSpec, ModuleSpec,
};
use pyo3::prelude::*;
use rr_util::py_types::PyOpAtAxes;

use crate::{circuit_manipulation::replace_nodes_py, concat_rewrite::split_to_concat};

#[pyfunction]
pub fn elim_empty_module(circuit: &Module) -> Option<CircuitRc> {
    (count_nodes(circuit.spec.circuit.clone()) == 1).then(|| circuit.substitute(None, None))
}

#[pyfunction(
    prefix_to_strip = "None",
    module_name = "None",
    check_all_args_present = "true",
    check_unique_arg_names = "true"
)]
pub fn extract_rewrite_raw(
    circuit: CircuitRc,
    input_specs: Vec<(CircuitRc, ModuleArgSpec)>,
    prefix_to_strip: Option<String>,
    module_name: Option<String>,
    check_all_args_present: bool,
    check_unique_arg_names: bool,
) -> Result<Module> {
    let mut spec = ModuleSpec::new_extract(
        circuit,
        input_specs.clone(),
        check_all_args_present,
        check_unique_arg_names,
    )?;
    if let Some(pref) = &prefix_to_strip {
        spec = spec.map_circuit_unwrap(|x| {
            if let Some(name) = x.name() {
                x.clone()
                    .rename(Some(name.strip_prefix(pref).unwrap_or(name).to_owned()))
            } else {
                x
            }
        })
    }
    Module::try_new(
        spec.arg_specs
            .iter()
            .map(|x| input_specs.iter().find(|z| &z.1 == x).unwrap().0.clone())
            .collect(),
        spec,
        module_name,
    )
}

// right now this only handles batch rank 0 or 1, todo handle arbitrary batch rank
#[pyfunction]
pub fn fuse_concat_modules(
    circuit: CircuitRc,
    modules: Vec<Module>,
    name: Option<String>,
) -> Result<CircuitRc> {
    if modules.is_empty() {
        bail!(anyhow!("no modules specified"))
    }
    let spec = modules[0].spec.clone();
    if !modules.iter().all(|x| x.spec == spec) {
        bail!(anyhow!("modules_one_batch not all same"))
    }
    let pure_rank = spec.circuit.info().rank();
    let modules_one_batch = modules
        .iter()
        .map(|x| {
            let dif = x.info().rank() - spec.circuit.info().rank();
            match dif {
                0 => Ok(Module::new(
                    zip(&x.nodes, &x.spec.arg_specs)
                        .map(|(n, s)| {
                            if s.batchable {
                                n.unsqueeze(vec![0], None).unwrap().rc()
                            } else {
                                n.clone()
                            }
                        })
                        .collect(),
                    spec.clone(),
                    x.name_cloned(),
                )),
                1 => Ok(x.clone()),
                _ => Err(anyhow!("module has batch rank > 1")),
            }
        })
        .collect::<Result<Vec<_>>>()?;
    if !modules_one_batch[0]
        .spec
        .arg_specs
        .iter()
        .enumerate()
        .all(|(i, x)| {
            x.batchable
                || modules_one_batch
                    .iter()
                    .all(|node| node.nodes[i] == modules_one_batch[0].nodes[i])
        })
    {
        bail!(anyhow!(
            "all inputs must be batchable or have the same child on all inputs"
        ));
    }
    let concatted_input = Module::nrc(
        (0..spec.arg_specs.len())
            .map(|i| {
                if spec.arg_specs[i].batchable {
                    Concat::nrc(
                        modules_one_batch
                            .iter()
                            .map(|m| m.nodes[i].clone())
                            .collect(),
                        0,
                        None,
                    )
                } else {
                    modules_one_batch[0].nodes[i].clone()
                }
            })
            .collect(),
        spec.clone(),
        name,
    );
    let splitted_modules: Vec<CircuitRc> = split_to_concat(
        concatted_input,
        0,
        modules_one_batch
            .iter()
            .map(|x| x.info().shape[0])
            .collect(),
    )
    .nodes;
    let splitted_unsqueezed: Vec<CircuitRc> = (0..modules.len())
        .map(|i| {
            if modules[i].info().rank() == pure_rank {
                splitted_modules[i]
                    .squeeze(PyOpAtAxes::Single(0), None)
                    .unwrap()
                    .rc()
            } else {
                splitted_modules[i].clone()
            }
        })
        .collect();
    Ok(replace_nodes_py(
        circuit,
        zip(
            modules.into_iter().map(|x| x.rc()),
            splitted_unsqueezed.into_iter().map(|x| x.rc()),
        )
        .collect(),
    ))
}
