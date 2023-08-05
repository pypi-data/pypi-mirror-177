use std::{iter::zip, str::FromStr};

use anyhow::{bail, Context, Result};
use once_cell::sync::Lazy;
use pyo3::prelude::*;
use regex::Regex;
use rr_util::{
    lru_cache::TensorCacheRrfs,
    tensor_util::{ParseError, Shape, TensorIndex, TorchDeviceDtypeOp},
};
use rustc_hash::FxHashMap as HashMap;
use smallvec::SmallVec as Sv;
use uuid::Uuid;

use crate::{
    Add, Array, CircuitNode, CircuitRc, Concat, Cumulant, DiscreteVar, Einsum, GeneralFunction,
    Index, Module, ModuleSpec, Rearrange, Scalar, Scatter, StoredCumulantVar, Symbol, Tag,
};

#[pyfunction(
    string,
    module_spec_map = "HashMap::default()",
    reference_circuits = "HashMap::default()",
    tensors_as_random = "false",
    tensors_as_random_device_dtype = "TorchDeviceDtypeOp::NONE",
    tensor_getter = "None"
)]
#[pyo3(name = "parse_circuit")]
pub fn parse_circuit_py(
    string: &str,
    module_spec_map: HashMap<String, ModuleSpec>,
    reference_circuits: HashMap<String, CircuitRc>,
    tensors_as_random: bool,
    tensors_as_random_device_dtype: TorchDeviceDtypeOp,
    mut tensor_cache: Option<TensorCacheRrfs>,
) -> Result<CircuitRc> {
    parse_circuit(
        string,
        module_spec_map,
        reference_circuits,
        tensors_as_random,
        tensors_as_random_device_dtype,
        &mut tensor_cache,
    )
}

#[pyfunction(
    string,
    module_spec_map = "HashMap::default()",
    reference_circuits = "HashMap::default()",
    tensors_as_random = "false",
    tensors_as_random_device_dtype = "TorchDeviceDtypeOp::NONE",
    tensor_getter = "None"
)]
#[pyo3(name = "parse_circuits")]
pub fn parse_circuits_py(
    string: &str,
    module_spec_map: HashMap<String, ModuleSpec>,
    reference_circuits: HashMap<String, CircuitRc>,
    tensors_as_random: bool,
    tensors_as_random_device_dtype: TorchDeviceDtypeOp,
    mut tensor_cache: Option<TensorCacheRrfs>,
) -> Result<Vec<CircuitRc>> {
    parse_circuits(
        string,
        module_spec_map,
        reference_circuits,
        tensors_as_random,
        tensors_as_random_device_dtype,
        &mut tensor_cache,
    )
}

pub fn parse_circuit(
    string: &str,
    module_spec_map: HashMap<String, ModuleSpec>,
    reference_circuits: HashMap<String, CircuitRc>,
    tensors_as_random: bool,
    tensors_as_random_device_dtype: TorchDeviceDtypeOp,
    tensor_cache: &mut Option<TensorCacheRrfs>,
) -> Result<CircuitRc> {
    let circuits = parse_circuits(
        string,
        module_spec_map,
        reference_circuits,
        tensors_as_random,
        tensors_as_random_device_dtype,
        tensor_cache,
    )?;
    if circuits.len() != 1 {
        bail!(ParseError::ExpectedOneCircuitGotMultiple {
            actual_num_circuits: circuits.len()
        })
    }
    Ok(circuits.into_iter().next().unwrap())
}

pub fn parse_circuits<'a>(
    string: &'a str,
    module_spec_map: HashMap<String, ModuleSpec>,
    reference_circuits: HashMap<String, CircuitRc>,
    tensors_as_random: bool,
    tensors_as_random_device_dtype: TorchDeviceDtypeOp,
    tensor_cache: &mut Option<TensorCacheRrfs>,
) -> Result<Vec<CircuitRc>> {
    let lines: Vec<_> = string.lines().collect();
    let mut replaced_string_owner: Vec<Box<String>> = vec![];
    // make separate struct that can deeply mutate, can't use immutable Circuit bc see children later
    #[derive(Debug, Clone)]
    struct PartialCirc<'a> {
        pub variant: &'a str, // copying bc refs annoying / don't care
        pub extra: &'a str,
        pub shape: Option<Shape>,
        pub name: Option<&'a str>,
        pub children: Vec<usize>,
    }
    let tab_width: usize = 2;
    let mut partial_circuits: Vec<Option<PartialCirc>> = vec![None; lines.len()];
    let mut stack: Vec<usize> = vec![];
    let mut top_level = vec![];
    const WHITESPACE: &str = r"[ │└├‣]*";
    static RE: Lazy<Regex> = Lazy::new(|| {
        Regex::new(&format!(r"^({ws})(\d+)(?: '((?:(?:\\')?[^']*)*)')?(?: \[([\d, ]*)\])?(?: ([a-zA-Z]+))?(?: (.*))?({ws})$", ws = WHITESPACE)).unwrap()
    });
    static RE_SKIP_LINE: Lazy<Regex> = Lazy::new(|| {
        // supports newlines and comment lines starting with #
        Regex::new(&format!(r"^{ws}(#.*)?$", ws = WHITESPACE)).unwrap()
    });
    let mut first_num_spaces = None;
    let mut first_line = None;
    for line in lines {
        if RE_SKIP_LINE.is_match(line) {
            continue;
        }

        let rf = || ParseError::NoRegexMatch {
            line: line.to_owned(),
        };
        let re_captures = RE.captures(line).ok_or_else(rf)?;
        let num_spaces_base = re_captures.get(1).ok_or_else(rf)?.as_str().chars().count();
        if first_num_spaces.is_none() {
            first_num_spaces = Some(num_spaces_base);
            first_line = Some(line.to_owned());
        }
        let first_num_spaces = first_num_spaces.unwrap();
        if num_spaces_base < first_num_spaces {
            bail!(ParseError::LessIndentationThanFirstItem {
                first_num_spaces,
                this_num_spaces_base: num_spaces_base,
                first_line: first_line.unwrap(),
                this_line: line.to_owned(),
            });
        }
        let num_spaces = num_spaces_base - first_num_spaces;
        if num_spaces % tab_width != 0 {
            bail!(ParseError::InvalidIndentation {
                tab_width,
                spaces: num_spaces,
                stack_indentation: stack.len(),
                stack_top: stack.last().map(|z| partial_circuits[*z]
                    .clone()
                    .unwrap()
                    .variant
                    .to_owned()),
            });
        }
        let indentation_level = num_spaces / tab_width;
        if indentation_level > stack.len() {
            bail!(ParseError::InvalidIndentation {
                tab_width,
                spaces: num_spaces,
                stack_indentation: stack.len(),
                stack_top: stack.last().map(|z| partial_circuits[*z]
                    .clone()
                    .unwrap()
                    .variant
                    .to_owned()),
            });
        }
        stack.truncate(indentation_level);
        let serial_number = re_captures
            .get(2)
            .ok_or_else(rf)?
            .as_str()
            .parse::<usize>()
            .unwrap();

        if serial_number > partial_circuits.len() - 1 {
            partial_circuits.resize(serial_number + 1, None)
        }
        let is_new_node = partial_circuits[serial_number].is_none();
        if is_new_node {
            partial_circuits[serial_number] = Some(PartialCirc {
                name: re_captures.get(3).map(|x| {
                    let name_replaced = x.as_str().replace(r"\'", "'").replace(r"\\", r"\");
                    replaced_string_owner.push(Box::new(name_replaced));
                    let last_thing: &str = replaced_string_owner.last().unwrap();
                    // we need this string to have same lifetime as input string, should find better way to do this
                    unsafe { std::mem::transmute::<&str, &'a str>(last_thing) }
                }),
                shape: if re_captures.get(4).is_some() {
                    Some(
                        re_captures
                            .get(4)
                            .ok_or_else(rf)?
                            .as_str()
                            .split(',')
                            .map(|z| z.trim())
                            .filter(|z| !z.is_empty())
                            .map(|x| x.parse::<usize>())
                            .collect::<Result<Sv<_>, _>>()
                            .map_err(|e| ParseError::NumberFail {
                                string: format!("{}", e),
                            })?,
                    )
                } else {
                    None
                },
                variant: re_captures.get(5).ok_or_else(rf)?.as_str(),
                extra: re_captures.get(6).map(|z| z.as_str()).unwrap_or("").trim(),
                children: vec![],
            });
        }
        if let Some(l) = stack.last() {
            partial_circuits[*l]
                .as_mut()
                .unwrap()
                .children
                .push(serial_number);
        }
        if is_new_node {
            if stack.is_empty() {
                top_level.push(serial_number)
            }
            stack.push(serial_number);
        }
    }

    fn deep_convert_partial_circ<'a>(
        serial_number: usize,
        partial_circuits: &Vec<Option<PartialCirc>>,
        context: &mut HashMap<usize, CircuitRc>,
        module_spec_map: &HashMap<String, ModuleSpec>,
        reference_circuits: &HashMap<String, CircuitRc>,
        tensors_as_random: bool,
        tensors_as_random_device_dtype: TorchDeviceDtypeOp,
        tensor_cache: &mut Option<TensorCacheRrfs>,
    ) -> Result<CircuitRc> {
        if let Some(already) = context.get(&serial_number) {
            return Ok(already.clone());
        }
        if serial_number > partial_circuits.len() - 1 {
            bail!(ParseError::InvalidSerialNumber { serial_number });
        }
        let ps = partial_circuits[serial_number]
            .as_ref()
            .ok_or(ParseError::InvalidSerialNumber { serial_number })?;
        let children: Vec<CircuitRc> = ps
            .children
            .iter()
            .map(|x| {
                deep_convert_partial_circ(
                    *x,
                    partial_circuits,
                    context,
                    module_spec_map,
                    reference_circuits,
                    tensors_as_random,
                    tensors_as_random_device_dtype.clone(),
                    tensor_cache,
                )
            })
            .collect::<Result<Vec<_>, _>>()?;
        let variant: &str = &ps.variant;
        let result = match variant {
            "Array" => {
                if tensors_as_random {
                    Array::randn_named(
                        ps.shape.clone().ok_or(ParseError::ShapeNeeded {
                            variant: variant.to_owned(),
                        })?,
                        ps.name.map(|s1| s1.to_owned()),
                        tensors_as_random_device_dtype,
                    )
                    .rc()
                } else {
                    Array::from_hash_prefix(
                        ps.name.map(|s1| s1.to_owned()),
                        &ps.extra,
                        tensor_cache,
                    )
                    .context("parse array constant from hash prefix")?
                    .rc()
                }
            }
            "Scalar" => Scalar::nrc(
                ps.extra
                    .parse::<f64>()
                    .map_err(|e| ParseError::NumberFail {
                        string: format!("{}", e),
                    })?,
                ps.shape
                    .as_ref()
                    .ok_or(ParseError::ShapeNeeded {
                        variant: variant.to_owned(),
                    })?
                    .clone(),
                ps.name.map(|s1| s1.to_owned()),
            ),
            "Add" => {
                if !ps.extra.is_empty() {
                    bail!(ParseError::ExtraUnneededString {
                        string: ps.extra.to_owned(),
                    })
                } else {
                    Add::try_new(children, ps.name.map(|s1| s1.to_owned()))?.rc()
                }
            }
            "Concat" => Concat::try_new(
                children,
                ps.extra
                    .parse::<usize>()
                    .map_err(|e| ParseError::NumberFail {
                        string: format!("{}", e),
                    })?,
                ps.name.map(|s1| s1.to_owned()),
            )?
            .rc(),
            "Einsum" => {
                Einsum::from_einsum_string(&ps.extra, children, ps.name.map(|s1| s1.to_owned()))?
                    .rc()
            }
            "Rearrange" => Rearrange::from_einops_string(
                children[0].clone(),
                &ps.extra,
                ps.name.map(|s1| s1.to_owned()),
            )?
            .rc(),
            "Symbol" => {
                let shape = ps
                    .shape
                    .as_ref()
                    .ok_or(ParseError::ShapeNeeded {
                        variant: variant.to_owned(),
                    })?
                    .clone();
                if ps.extra.is_empty() {
                    Symbol::new_with_none_uuid(shape, ps.name.map(|s1| s1.to_owned())).rc()
                } else {
                    Symbol::nrc(
                        shape,
                        Uuid::from_str(&ps.extra).map_err(|_e| ParseError::Fail {
                            string: ps.extra.to_owned(),
                        })?,
                        ps.name.map(|s1| s1.to_owned()),
                    )
                }
            }
            "GeneralFunction" => GeneralFunction::new_from_parse(
                children,
                ps.extra.to_owned(),
                ps.name.map(|s1| s1.to_owned()),
            )?
            .rc(),
            "Index" => Index::try_new(
                children[0].clone(),
                TensorIndex::from_bijection_string(&ps.extra, tensor_cache)?,
                ps.name.map(|s1| s1.to_owned()),
            )?
            .rc(),
            "Scatter" => Scatter::try_new(
                children[0].clone(),
                TensorIndex::from_bijection_string(&ps.extra, tensor_cache)?,
                ps.shape
                    .as_ref()
                    .ok_or(ParseError::ShapeNeeded {
                        variant: variant.to_owned(),
                    })?
                    .clone(),
                ps.name.map(|s1| s1.to_owned()),
            )?
            .rc(),
            "Module" => Module::try_new(
                children,
                module_spec_map
                    .get(&ps.extra.to_owned())
                    .cloned()
                    .ok_or_else(|| ParseError::ModuleNotFound {
                        name: ps.extra.to_owned(),
                    })?,
                ps.name.map(|s1| s1.to_owned()),
            )?
            .rc(),
            "Ref" => reference_circuits
                .get(&ps.extra.to_owned())
                .cloned()
                .ok_or_else(|| ParseError::CircuitRefNotFound {
                    name: ps.extra.to_owned(),
                })?,
            "Tag" => Uuid::from_str(&ps.extra)
                .map_err(|_| ParseError::InvalidUuid {
                    string: ps.extra.to_owned(),
                })
                .map(|uuid| Tag::nrc(children[0].clone(), uuid, ps.name.map(|s1| s1.to_owned())))?,
            "Cumulant" => Cumulant::nrc(children, ps.name.map(|s1| s1.to_owned())),
            "DiscreteVar" => DiscreteVar::try_new(
                children[0].clone(),
                children[1].clone(),
                ps.name.map(|s1| s1.to_owned()),
            )?
            .rc(),
            "StoredCumulantVar" => {
                if let [cum_nums, uuid] = ps.extra.split("|").collect::<Vec<_>>()[..] {
                    let keys = cum_nums
                        .split(",")
                        .map(|s| s.trim().parse::<usize>())
                        .collect::<Result<Vec<_>, _>>()
                        .map_err(|e| ParseError::NumberFail {
                            string: format!("{}", e),
                        })?;

                    let uuid = Uuid::from_str(uuid).map_err(|_| ParseError::InvalidUuid {
                        string: ps.extra.to_owned(),
                    })?;
                    if keys.len() != children.len() {
                        bail!(ParseError::WrongNumberChildren {
                            expected: keys.len(),
                            found: children.len(),
                        })
                    } else {
                        StoredCumulantVar::try_new(
                            zip(keys, children).collect(),
                            uuid,
                            ps.name.map(|s1| s1.to_owned()),
                        )?
                        .rc()
                    }
                } else {
                    bail!(ParseError::Fail {
                        string: ps.extra.to_owned(),
                    })
                }
            }
            _ => bail!(ParseError::InvalidVariant {
                v: variant.to_owned(),
            }),
        };
        context.insert(serial_number, result.to_owned());
        Ok(result)
    }
    let mut context: HashMap<usize, CircuitRc> = HashMap::default();
    let result = top_level
        .into_iter()
        .map(|num| {
            deep_convert_partial_circ(
                num,
                &partial_circuits,
                &mut context,
                &module_spec_map,
                &reference_circuits,
                tensors_as_random,
                tensors_as_random_device_dtype.clone(),
                tensor_cache,
            )
        })
        .collect();
    std::hint::black_box(&replaced_string_owner); // this needs to be alive for whole function
                                                  // and is used as if it's just the same as input &str
    result
}
