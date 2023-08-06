use std::iter::{self, zip};

use anyhow::{bail, Context, Result};
use macro_rules_attribute::apply;
use pyo3::{exceptions::PyValueError, prelude::*};
use rr_util::{
    pycall, python_error_exception,
    rearrange_spec::{OpShape, OpSize},
    sv,
    symbolic_size::SymbolicSizeProduct,
    tensor_util::{Shape, TensorAxisIndex, TensorIndex},
};
use rustc_hash::FxHashMap as HashMap;
use thiserror::Error;

use crate::{
    deep_map_fallible_pre_new_children, prelude::*, Add, Concat, Einsum, GeneralFunction, Index,
    Module, ModuleArgSpec, ModuleSpec, Rearrange, Scatter, SetSymbolicShape, Symbol, Tag,
};

#[pyfunction]
#[pyo3(name = "expand_node")]
pub fn expand_node_py(circuit: CircuitRc, inputs: Vec<CircuitRc>) -> Result<CircuitRc> {
    expand_node(circuit, &inputs)
}

pub fn expand_node(circuit: CircuitRc, inputs: &Vec<CircuitRc>) -> Result<CircuitRc> {
    if inputs.len() != circuit.children().count() {
        bail!(ExpandError::WrongNumChildren {
            expected: circuit.children().count(),
            got: inputs.len(),
        });
    }
    let batch_ranks: Vec<usize> = zip(circuit.children(), inputs)
        .filter_map(|(old, new)| new.info().rank().checked_sub(old.info().rank()))
        .collect();
    if batch_ranks.len() != inputs.len() {
        bail!(ExpandError::BatchingRankTooLow {
            default: circuit.children().map(|x| x.info().rank()).collect(),
            got: inputs.iter().map(|x| x.info().rank()).collect(),
        });
    }

    // TODO: maybe we should allow for inconsistent symbolic batch shapes?
    // (probably not...)
    let batch_shapes: Vec<&[usize]> = zip(&batch_ranks, inputs)
        .map(|(br, new)| &new.info().shape[0..*br])
        .collect();

    let find_non_symbolic = |sizes: &[usize]| {
        sizes
            .into_iter()
            .find_map(|&s| (!SymbolicSizeProduct::has_symbolic(s)).then_some(s))
            .unwrap_or(sizes[0])
    };

    match &**circuit {
        Circuit::SetSymbolicShape(_) => Ok(inputs[0].clone()), /* just return circuit, symbolic shapes will be added as needed! (TODO: maybe should keep?) */
        // TODO: symbolic shape case for below!!!
        Circuit::Symbol(_) | Circuit::Scalar(_) => Ok(circuit.clone()),
        Circuit::Rearrange(node) => {
            let input_shape_non_batch = inputs[0].info().shape[batch_ranks[0]..]
                .iter()
                .cloned()
                .collect();

            let new_input = SetSymbolicShape::some_set_and_symbolic_neq(
                inputs[0].clone(),
                iter::repeat(OpSize::NONE)
                    .take(batch_ranks[0])
                    .chain(node.spec.forced_input_shape(true))
                    .collect(),
                None,
            )
            .with_context(|| {
                format!(
                    "failed to set symbolic in expand rearrange, old rearrange={:?}",
                    node
                )
            })?;

            let new_spec = node
                .spec
                .conform_to_input_shape(&input_shape_non_batch, true)
                .context("failed to conform rearrange to input shape in expand")?
                .add_batch_dims(batch_ranks[0]);
            Ok(Rearrange::nrc(new_input, new_spec, circuit.name_cloned()))
        }
        // I think we just don't do any symbolic shape munging in Index/Scatter?
        Circuit::Index(node) => {
            // for now non-batch non-identity dims can't change
            for i in 0..node.node.info().rank() {
                if node.node.info().shape[i] != inputs[0].info().shape[i + batch_ranks[0]]
                    && node.index.0[i] != TensorAxisIndex::IDENT
                {
                    bail!(ExpandError::FixedIndex {
                        index: node.index.clone(),
                        old_shape: node.node.info().shape.clone(),
                        new_shape: inputs[0].info().shape.clone(),
                    });
                }
            }
            Ok(Index::nrc(
                inputs[0].clone(),
                TensorIndex(
                    vec![TensorAxisIndex::IDENT; batch_ranks[0]]
                        .into_iter()
                        .chain(node.index.0.iter().cloned())
                        .collect(),
                ),
                node.name_cloned(),
            ))
        }
        Circuit::Scatter(node) => {
            // for now non-batch non-identity dims can't change
            for i in 0..node.node.info().rank() {
                if node.node.info().shape[i] != inputs[0].info().shape[i + batch_ranks[0]]
                    && node.index.0[i] != TensorAxisIndex::IDENT
                {
                    bail!(ExpandError::FixedIndex {
                        index: node.index.clone(),
                        old_shape: node.node.info().shape.clone(),
                        new_shape: inputs[0].info().shape.clone(),
                    });
                }
            }
            Ok(Scatter::nrc(
                inputs[0].clone(),
                TensorIndex(
                    vec![TensorAxisIndex::IDENT; batch_ranks[0]]
                        .into_iter()
                        .chain(node.index.0.iter().cloned())
                        .collect(),
                ),
                inputs[0].info().shape[0..batch_ranks[0]]
                    .iter()
                    .cloned()
                    .chain(node.info().shape.iter().cloned())
                    .collect(),
                node.name_cloned(),
            ))
        }
        Circuit::Concat(node) => {
            // TODO: set symbolic size, error on concat axis having symbolic size? (or maybe concat axis is fine???
            if !batch_shapes.iter().all(|x| x == &batch_shapes[0]) {
                bail!(ExpandError::InconsistentBatches {
                    batch_shapes: batch_shapes
                        .iter()
                        .map(|x| x.iter().cloned().collect())
                        .collect(),
                    circuit: circuit.clone(),
                });
            }
            let br = batch_ranks[0];
            let new_axis = node.axis + br;
            if !zip(&node.nodes, inputs)
                .all(|(old, new)| old.info().shape[node.axis] == new.info().shape[new_axis])
            {
                bail!(ExpandError::ConcatAxis {
                    axis: node.axis,
                    old_shape: sv![],
                    new_shape: sv![],
                });
            }

            let inputs = if inputs.iter().all(|x| x.ndim() == inputs[0].ndim()) {
                // if statment just so that if we're going to fail anyway, we skip this case
                let new_shape: OpShape = (0..inputs[0].ndim())
                    .map(|i| {
                        if i == new_axis {
                            return None;
                        }

                        Some(find_non_symbolic(
                            &inputs.iter().map(|x| x.shape()[i]).collect::<Vec<_>>(),
                        ))
                    })
                    .map(|x| x.into())
                    .collect();

                inputs
                    .iter()
                    .map(|inp| {
                        SetSymbolicShape::some_set_and_symbolic_neq(
                            inp.clone(),
                            new_shape.clone(),
                            None,
                        )
                    })
                    .collect::<Result<_>>()
                    .with_context(|| {
                        format!(
                            "failed to set symbolic in expand concat, old concat={:?}",
                            node
                        )
                    })?
            } else {
                inputs.clone()
            };

            Concat::try_new(inputs, new_axis, node.name_cloned()).map(|x| x.rc())
        }
        Circuit::Add(node) => {
            let inputs = if let Some(max) = inputs.iter().map(|x| x.ndim()).max() {
                let full_shape: OpShape = (0..max)
                    .map(|i| {
                        let sizes: Vec<_> = inputs
                            .iter()
                            .filter_map(|x| {
                                i.checked_sub(max - x.ndim()).and_then(|i| {
                                    let size = x.shape()[i];
                                    (size != 1).then_some(size)
                                })
                            })
                            .collect();

                        if sizes.is_empty() {
                            None
                        } else {
                            Some(find_non_symbolic(&sizes))
                        }
                        .into()
                    })
                    .collect();
                inputs
                    .iter()
                    .map(|inp| {
                        SetSymbolicShape::some_set_and_symbolic_neq(
                            inp.clone(),
                            full_shape[max - inp.ndim()..].iter().cloned().collect(),
                            None,
                        )
                    })
                    .collect::<Result<_>>()
                    .with_context(|| {
                        format!("failed to set symbolic in expand add, old add={:?}", node)
                    })?
            } else {
                inputs.clone()
            };

            Add::try_new(inputs, node.name_cloned()).map(|x| x.rc())
        }
        Circuit::GeneralFunction(node) => {
            // TODO: symbolic!
            GeneralFunction::try_new(inputs.clone(), node.spec.clone(), node.name_cloned())
                .map(|x| x.rc())
        }
        Circuit::Einsum(node) => {
            let mut batch_shape: Option<&[usize]> = None;
            for bs in &batch_shapes {
                if !bs.is_empty() {
                    if let Some(existing) = batch_shape {
                        if *bs != existing {
                            bail!(ExpandError::InconsistentBatches {
                                batch_shapes: batch_shapes
                                    .iter()
                                    .map(|x| x.iter().cloned().collect())
                                    .collect(),
                                circuit: circuit.clone(),
                            });
                        }
                    } else {
                        batch_shape = Some(bs.clone());
                    }
                }
            }
            let next_axis = node.next_axis();
            let newies = || (next_axis as u8..next_axis + batch_shape.unwrap().len() as u8);
            let out_axes = if let Some(_bs) = batch_shape {
                newies().chain(node.out_axes.iter().cloned()).collect()
            } else {
                node.out_axes.clone()
            };
            let new_args: Vec<_> = node
                .args
                .iter()
                .enumerate()
                .map(|(i, (_child, ints))| {
                    (inputs[i].clone(), {
                        if !batch_shapes[i].is_empty() {
                            newies().chain(ints.iter().cloned()).collect()
                        } else {
                            ints.clone()
                        }
                    })
                })
                .collect();

            let mut shape_map_many = HashMap::default();
            for (circ, axes) in &new_args {
                for (&circuit_shape, axis) in circ.info().shape.iter().zip(axes) {
                    shape_map_many
                        .entry(*axis)
                        .or_insert(Vec::new())
                        .push(circuit_shape);
                }
            }

            let axis_to_set_shape: HashMap<_, _> = shape_map_many
                .into_iter()
                .map(|(axis, sizes)| (axis, find_non_symbolic(&sizes)))
                .collect();

            let new_args = new_args
                .into_iter()
                .map(|(x, axes)| {
                    assert_eq!(
                        x.ndim(),
                        axes.len(),
                        "should be true due to above batching code"
                    );
                    Ok((
                        SetSymbolicShape::some_set_and_symbolic_neq(
                            x,
                            axes.iter()
                                .map(|x| Some(axis_to_set_shape[x]).into())
                                .collect(),
                            None,
                        )?,
                        axes,
                    ))
                })
                .collect::<Result<_>>()
                .with_context(|| {
                    format!(
                        "failed to set symbolic in expand einsum, old einsum={:?}",
                        node
                    )
                })?;

            Einsum::try_new(new_args, out_axes, node.name_cloned()).map(|x| x.rc())
        }
        Circuit::Module(node) => {
            assert_eq!(inputs.len(), node.children().count());
            let mut children = inputs.clone();
            let rest = children.split_off(1);
            let spec_circuit = children.pop().unwrap();

            // TODO: maybe dedup with parse and other places!
            let (arg_specs, nodes) = rest
                .chunks(2)
                .zip(&node.spec.arg_specs)
                .map(|(sym_inp, arg_spec)| {
                    if let [sym, inp] = sym_inp {
                        let symbol = if let Some(symbol) = sym.as_symbol() {
                            symbol.clone()
                        } else {
                            bail!(ExpandError::ModuleSpecArgSymbolReplacedWithNonSymbol {
                                old_symbol: arg_spec.symbol.clone(),
                                new_circuit: sym.clone(),
                            });
                        };
                        Ok((
                            ModuleArgSpec {
                                symbol,
                                batchable: arg_spec.batchable,
                                expandable: arg_spec.expandable,
                            },
                            inp.clone(),
                        ))
                    } else {
                        unreachable!()
                    }
                })
                .collect::<Result<Vec<_>>>()?
                .into_iter()
                .unzip();

            let spec = ModuleSpec::new(spec_circuit, arg_specs, false)
                .context("constructing new ModuleSpec failed in expand")?;

            Module::try_new(nodes, spec, node.name_cloned()).map(|z| z.rc())
        }
        Circuit::Tag(node) => Ok(Tag::new(inputs[0].clone(), node.uuid, node.name_cloned()).rc()),
        _ => {
            if inputs[..] == circuit.children().collect::<Vec<_>>()[..] {
                Ok(circuit.clone())
            } else {
                bail!(ExpandError::NodeUnhandledVariant {
                    variant: circuit.variant_string(),
                })
            }
        }
    }
}

#[apply(python_error_exception)]
#[base_error_name(Expand)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum ExpandError {
    #[error("expand wrong number of children, expected {expected} got {got} ({e_name})")]
    WrongNumChildren { expected: usize, got: usize },

    #[error("Batching Rank Too Low ({e_name})")]
    BatchingRankTooLow {
        default: Vec<usize>,
        got: Vec<usize>,
    },

    #[error("Trying to expand fixed index, index {index:?} old shape{old_shape:?} new shape {new_shape:?} ({e_name})")]
    FixedIndex {
        index: TensorIndex,
        old_shape: Shape,
        new_shape: Shape,
    },

    #[error(
        "Trying to expand concat axis, index {axis} old shape{old_shape:?} new shape {new_shape:?} ({e_name})"
    )]
    ConcatAxis {
        axis: usize,
        old_shape: Shape,
        new_shape: Shape,
    },

    #[error("Inputs that should have same batching have different batchings, {batch_shapes:?} {circuit:?} ({e_name})")]
    InconsistentBatches {
        batch_shapes: Vec<Shape>,
        circuit: CircuitRc,
    },

    #[error("trying to expand node, unknown variant {variant} ({e_name})")]
    NodeUnhandledVariant { variant: String },

    #[error("Not currently supported! old_shape={old_shape:?} != new_shape={new_shape:?}\nold_spec_circuit={old_spec_circuit:?} new_spec_circuit={new_spec_circuit:?} ({e_name})")]
    ModuleSpecCircuitChangedShapeInExpand {
        old_shape: Shape,
        new_shape: Shape,
        old_spec_circuit: CircuitRc,
        new_spec_circuit: CircuitRc,
    },

    #[error("old_symbol={old_symbol:?} new_circuit={new_circuit:?} ({e_name})")]
    ModuleSpecArgSymbolReplacedWithNonSymbol {
        old_symbol: Symbol,
        new_circuit: CircuitRc,
    },

    #[error("Not currently supported! old_shape={old_shape:?} != new_shape={new_shape:?}\nold_symbol={old_symbol:?} new_symbol={new_symbol:?} ({e_name})")]
    ModuleSpecArgSymbolChangedShapeInExpand {
        old_shape: Shape,
        new_shape: Shape,
        old_symbol: Symbol,
        new_symbol: Symbol,
    },

    #[error("node_rank={node_rank} < symbol_rank={symbol_rank}, arg_spec={arg_spec:?} node_shape={node_shape:?} spec_circuit={spec_circuit:?} ({e_name})")]
    ModuleRankReduced {
        node_rank: usize,
        symbol_rank: usize,
        arg_spec: ModuleArgSpec,
        node_shape: Shape,
        spec_circuit: CircuitRc,
    },

    #[error("node_rank={node_rank} > symbol_rank={symbol_rank} (which indicates batching) and arg_spec={arg_spec:?} spec_circuit={spec_circuit:?} ({e_name})")]
    ModuleTriedToBatchUnbatchableInput {
        node_rank: usize,
        symbol_rank: usize,
        arg_spec: ModuleArgSpec,
        spec_circuit: CircuitRc,
    },

    #[error("node_shape={node_shape:?} symbol_shape={symbol_shape:?} arg_spec={arg_spec:?} spec_circuit={spec_circuit:?} ({e_name})")]
    ModuleTriedToExpandUnexpandableInput {
        node_shape: Shape,
        symbol_shape: Shape,
        arg_spec: ModuleArgSpec,
        spec_circuit: CircuitRc,
    },
}

#[pyfunction]
#[pyo3(name = "replace_expand_bottom_up_dict")]
pub fn replace_expand_bottom_up_dict_py(
    circuit: CircuitRc,
    dict: HashMap<CircuitRc, CircuitRc>,
) -> Result<CircuitRc> {
    replace_expand_bottom_up(circuit, |x| dict.get(&x).cloned())
}

#[pyfunction]
#[pyo3(name = "replace_expand_bottom_up")]
pub fn replace_expand_bottom_up_py(circuit: CircuitRc, f: PyObject) -> Result<CircuitRc> {
    replace_expand_bottom_up(circuit, |x| pycall!(f, (x.clone(),)))
}

pub fn replace_expand_bottom_up<F>(circuit: CircuitRc, replacer: F) -> Result<CircuitRc>
where
    F: Fn(CircuitRc) -> Option<CircuitRc>,
{
    let recursor = |circuit: CircuitRc, new_children: &Vec<CircuitRc>| -> Result<CircuitRc> {
        if let Some(replaced) = replacer(circuit.clone()) {
            return Ok(replaced);
        }
        expand_node(circuit, new_children)
    };
    deep_map_fallible_pre_new_children(circuit, recursor)
}
