use std::{iter::zip, str::FromStr};

use anyhow::{bail, Context, Result};
use macro_rules_attribute::apply;
use once_cell::sync::Lazy;
use pyo3::{exceptions::PyValueError, prelude::*};
use regex::Regex;
use rr_util::{
    lru_cache::TensorCacheRrfs,
    python_error_exception,
    symbolic_size::SymbolicSizeProduct,
    tensor_util::{ParseError, Shape, TensorIndex, TorchDeviceDtypeOp},
    util::{counts_g_1, flip_op_result, is_unique},
};
use rustc_hash::FxHashMap as HashMap;
use smallvec::SmallVec as Sv;
use thiserror::Error;
use uuid::Uuid;

use crate::{
    print::TerseBool, Add, Array, CircuitNode, CircuitRc, CircuitType, Concat, ConstructError,
    Cumulant, DiscreteVar, Einsum, GeneralFunction, Index, Module, ModuleArgSpec, ModuleSpec,
    Rearrange, Scalar, Scatter, SetSymbolicShape, StoredCumulantVar, Symbol, Tag,
};

#[pyclass]
#[derive(Clone, Debug)]
pub struct Parser {
    #[pyo3(get, set)]
    pub reference_circuits: HashMap<String, CircuitRc>,
    #[pyo3(get, set)]
    pub tensors_as_random: bool,
    #[pyo3(get, set)]
    pub tensors_as_random_device_dtype: TorchDeviceDtypeOp,
    #[pyo3(get, set)]
    pub on_repeat_check_info_same: bool,
    #[pyo3(get, set)]
    pub module_check_all_args_present: bool,
    #[pyo3(get, set)]
    pub module_check_unique_arg_names: bool,
}

impl Default for Parser {
    fn default() -> Self {
        Self {
            reference_circuits: Default::default(),
            tensors_as_random: false,
            tensors_as_random_device_dtype: TorchDeviceDtypeOp::NONE,
            on_repeat_check_info_same: true,
            module_check_all_args_present: true,
            module_check_unique_arg_names: false,
        }
    }
}

#[pymethods]
impl Parser {
    #[args(
        reference_circuits = "HashMap::default()",
        reference_circuits_by_name = "vec![]",
        tensors_as_random = "Parser::default().tensors_as_random",
        tensors_as_random_device_dtype = "Parser::default().tensors_as_random_device_dtype",
        on_repeat_check_info_same = "Parser::default().on_repeat_check_info_same",
        module_check_all_args_present = "Parser::default().module_check_all_args_present",
        module_check_unique_arg_names = "Parser::default().module_check_unique_arg_names"
    )]
    #[new]
    pub fn new(
        reference_circuits: HashMap<String, CircuitRc>,
        reference_circuits_by_name: Vec<CircuitRc>,
        tensors_as_random: bool,
        tensors_as_random_device_dtype: TorchDeviceDtypeOp,
        on_repeat_check_info_same: bool,
        module_check_all_args_present: bool,
        module_check_unique_arg_names: bool,
    ) -> Result<Self> {
        let ref_circ_names = reference_circuits_by_name
            .into_iter()
            .map(|circ| {
                Ok((
                    circ.name_cloned().ok_or_else(|| {
                        ParseArgError::ReferenceCircuitByNameHasNoneName {
                            circuit: circ.clone(),
                        }
                    })?,
                    circ,
                ))
            })
            .collect::<Result<Vec<_>>>()?;

        let all_idents: Vec<_> = ref_circ_names
            .iter()
            .map(|(name, _)| name)
            .chain(reference_circuits.keys().map(|x| x))
            .collect();
        if !is_unique(&all_idents) {
            bail!(ParseArgError::ReferenceCircuitDuplicateIdentifier {
                dup_idents: counts_g_1(all_idents.into_iter().cloned())
            })
        }

        let reference_circuits: HashMap<_, _> = ref_circ_names
            .into_iter()
            .chain(reference_circuits)
            .collect();

        Ok(Self {
            reference_circuits,
            tensors_as_random,
            tensors_as_random_device_dtype,
            on_repeat_check_info_same,
            module_check_all_args_present,
            module_check_unique_arg_names,
        })
    }

    #[pyo3(name = "parse_circuit")]
    pub fn parse_circuit_py(
        &self,
        string: &str,
        mut tensor_cache: Option<TensorCacheRrfs>,
    ) -> Result<CircuitRc> {
        self.parse_circuit(string, &mut tensor_cache)
    }

    pub fn __call__(
        &self,
        string: &str,
        tensor_cache: Option<TensorCacheRrfs>,
    ) -> Result<CircuitRc> {
        self.parse_circuit_py(string, tensor_cache)
    }

    #[pyo3(name = "parse_circuits")]
    pub fn parse_circuits_py(
        &self,
        string: &str,
        mut tensor_cache: Option<TensorCacheRrfs>,
    ) -> Result<Vec<CircuitRc>> {
        self.parse_circuits(string, &mut tensor_cache)
    }
}

#[derive(Debug, Clone, Eq, Hash, PartialEq, PartialOrd, Ord)]
enum CircuitIdent {
    Num(usize),
    Str(String),
}

use CircuitIdent::*;

impl CircuitIdent {
    fn as_str(&self) -> Option<&str> {
        match self {
            Num(_) => None,
            Str(s) => Some(s),
        }
    }
}

// make separate struct that can deeply mutate, can't use immutable Circuit bc see children later
#[derive(Debug, Clone)]
struct PartialCirc {
    pub variant: CircuitType,
    pub extra: String,
    pub shape: Option<Shape>,
    pub name: Option<String>,
    pub children: Vec<CircuitIdent>,
}

impl Parser {
    pub fn parse_circuit(
        &self,
        string: &str,
        tensor_cache: &mut Option<TensorCacheRrfs>,
    ) -> Result<CircuitRc> {
        let circuits = self.parse_circuits(string, tensor_cache)?;
        if circuits.len() != 1 {
            bail!(ParseError::ExpectedOneCircuitGotMultiple {
                actual_num_circuits: circuits.len()
            })
        }
        Ok(circuits.into_iter().next().unwrap())
    }

    pub fn parse_circuits(
        &self,
        string: &str,
        tensor_cache: &mut Option<TensorCacheRrfs>,
    ) -> Result<Vec<CircuitRc>> {
        let lines: Vec<_> = string.lines().collect();

        let tab_width: usize = 2;
        let mut partial_circuits: HashMap<CircuitIdent, PartialCirc> = HashMap::default();
        let mut stack: Vec<CircuitIdent> = vec![];
        let mut top_level = vec![];
        const WHITESPACE: &str = r"[\s│└├‣]*";
        const NAME_INSIDE_MATCH: &str = r"(?:(?:\\')?[^']*)*";

        let (
            prefix_whitespace_cap,
            num_ident_cap,
            name_ident_cap,
            name_cap,
            shape_cap,
            variant_cap,
            extra_cap,
        ) = (1, 2, 3, 4, 5, 6, 7);
        static RE_STR: Lazy<(Regex, String)> = Lazy::new(|| {
            let name_match_capture: String = format!("'({})'", NAME_INSIDE_MATCH);
            let name_match: String = format!("'{}'", NAME_INSIDE_MATCH);
            // first match named axis name, then size. Name is optional. We handle whitespace.
            let maybe_symbolic_num = r"s?\d+";
            let size_prod_match: String = format!(r"(?:{d}\s*\*\s*)*{d}", d = maybe_symbolic_num);
            let shape_axis_match: String =
                format!(r"(?:{}\s*:\s*)?{}\s*", name_match, size_prod_match);
            let trailing_comment_match = r"(?:#.*?)?"; // TODO: test this never matches stuff it's not supposed to...
            let full_regex = format!(
                r"^({ws})(?:(\d+)|{nm})(?: {nm})?(?: \[((?:{sh},\s*)*(?:{sh})?)\])?(?: ([a-zA-Z]+))?(?: (.*?))?(?:{ws}){com}$",
                ws = WHITESPACE,
                nm = name_match_capture,
                sh = shape_axis_match,
                com = trailing_comment_match,
            );

            (Regex::new(&full_regex).unwrap(), full_regex)
        });
        let re = &RE_STR.0;
        let regex_string = &RE_STR.1;
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

            let re_captures = re
                .captures(line)
                .ok_or_else(|| ParseError::RegexDidntMatch {
                    line: line.to_owned(),
                    regex_string: regex_string.clone(),
                })?;
            let num_spaces_base = re_captures
                .get(prefix_whitespace_cap)
                .expect("if regex matches, group should be present")
                .as_str()
                .chars()
                .count();
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
                });
            }
            let indentation_level = num_spaces / tab_width;
            if indentation_level > stack.len() {
                bail!(ParseError::InvalidIndentation {
                    tab_width,
                    spaces: num_spaces,
                    stack_indentation: stack.len(),
                });
            }
            stack.truncate(indentation_level);

            let unescape_name =
                |x: regex::Match| x.as_str().replace(r"\'", "'").replace(r"\\", r"\");

            let circuit_ident = match (
                re_captures.get(num_ident_cap),
                re_captures.get(name_ident_cap),
            ) {
                (None, None) => unreachable!(),
                (Some(c), None) => Num(c.as_str().parse().unwrap()),
                (None, Some(c)) => Str(unescape_name(c)),
                (Some(_), Some(_)) => unreachable!(),
            };

            let is_new_node = !partial_circuits.contains_key(&circuit_ident);

            let is_ref = circuit_ident
                .as_str()
                .map(|s| self.reference_circuits.contains_key(s))
                .unwrap_or(false);
            if is_ref {
                if re_captures.get(name_cap).is_some()
                    || re_captures.get(shape_cap).is_some()
                    || re_captures.get(variant_cap).is_some()
                    || re_captures.get(extra_cap).is_some()
                {
                    bail!(ParseError::ReferenceCircuitNameFollowedByAdditionalInfo {
                        reference_name: circuit_ident.as_str().unwrap().to_owned(),
                        line: line.to_owned()
                    });
                }
            } else {
                let name = re_captures.get(name_cap).map(unescape_name).or_else(|| {
                    if is_new_node {
                        circuit_ident.as_str().map(str::to_owned)
                    } else {
                        // if not new node, than this is just for checking and we want to avoid checking in this case
                        None
                    }
                });
                // TODO: named axes!
                let shape = flip_op_result(re_captures.get(shape_cap).map(|shape_cap| {
                    let mut axis_strs: Vec<_> =
                        shape_cap.as_str().split(',').map(|z| z.trim()).collect();
                    if axis_strs.last() == Some(&"") {
                        // allow last axis to be empty due to trailing comma
                        // (Regex guarantees that only last axis has this I think, but better to be clear)
                        axis_strs.pop();
                    }

                    let parse_axis_size = |x| {
                        SymbolicSizeProduct::from_str(x)
                            .context(concat!(
                                "failed to parse number (including symbolic product) for shape",
                                "\nthis is supposed to parse named axes but it currently doesn't!"
                            ))?
                            .try_into()
                            .context("failed to convert size product to usize in parse of shape")
                    };

                    axis_strs
                        .into_iter()
                        .map(parse_axis_size)
                        .collect::<Result<Sv<_>, _>>()
                }))?;
                let variant = flip_op_result(re_captures.get(variant_cap).map(|s| {
                    s.as_str()
                        .parse()
                        .context("failed to parse variant in parse_circuit")
                }))?;

                let extra = re_captures
                    .get(extra_cap)
                    .and_then(|z| (!z.as_str().is_empty()).then(|| z.as_str().to_owned()));

                if is_new_node {
                    partial_circuits.insert(
                        circuit_ident.clone(),
                        PartialCirc {
                            name,
                            shape,
                            variant: variant.ok_or_else(|| ParseError::RegexDidntMatchGroup {
                                line: line.to_owned(),
                                regex_string: regex_string.clone(),
                                group: variant_cap,
                            })?,
                            extra: extra.unwrap_or_else(|| "".to_owned()),
                            children: vec![],
                        },
                    );
                } else if self.on_repeat_check_info_same {
                    let old_node = &partial_circuits[&circuit_ident];

                    let mut any_fail = false;
                    let mut err_strs = String::new();

                    macro_rules! fail_check {
                        ($n:ident, $w:expr) => {{
                            let failed = $n.clone().map(|x| $w(x) != old_node.$n).unwrap_or(false);
                            if failed {
                                any_fail = true;
                                err_strs += &format!(
                                    "{} mismatch. new={:?} != old={:?}\n",
                                    stringify!($n),
                                    $n.unwrap(),
                                    old_node.$n
                                );
                            }
                        }};
                        ($n:ident) => {
                            fail_check!($n, |x| x)
                        };
                    }

                    fail_check!(name, Some);
                    fail_check!(shape, Some);
                    fail_check!(variant);
                    fail_check!(extra);
                    if any_fail {
                        bail!(ParseError::OnCircuitRepeatInfoIsNotSame {
                            repeat_ident: format!("{:?}", circuit_ident),
                            err_strs,
                            line: line.to_owned()
                        });
                    }
                }
            }

            // now manipulate stack
            if stack.is_empty() {
                top_level.push(circuit_ident.clone())
            }
            if let Some(l) = stack.last() {
                if let Str(s) = l {
                    if self.reference_circuits.contains_key(s) {
                        bail!(ParseError::ReferenceCircuitHasChildrenInParseStr {
                            reference_name: s.to_owned()
                        });
                    }
                }

                partial_circuits
                    .get_mut(l)
                    .unwrap()
                    .children
                    .push(circuit_ident.clone());
            }
            if is_new_node {
                stack.push(circuit_ident);
            }
        }

        let mut context = HashMap::default();
        top_level
            .iter()
            .map(|ident| {
                self.deep_convert_partial_circ(ident, &partial_circuits, &mut context, tensor_cache)
            })
            .collect()
    }

    fn deep_convert_partial_circ(
        &self,
        ident: &CircuitIdent,
        partial_circuits: &HashMap<CircuitIdent, PartialCirc>,
        context: &mut HashMap<CircuitIdent, CircuitRc>,
        tensor_cache: &mut Option<TensorCacheRrfs>,
    ) -> Result<CircuitRc> {
        if let Some(ref_circ) = ident
            .as_str()
            .map(|x| self.reference_circuits.get(x))
            .flatten()
        {
            return Ok(ref_circ.clone());
        }
        if let Some(already) = context.get(ident) {
            return Ok(already.clone());
        }
        let ps = &partial_circuits[ident];
        let children: Vec<CircuitRc> = ps
            .children
            .iter()
            .map(|x| self.deep_convert_partial_circ(x, partial_circuits, context, tensor_cache))
            .collect::<Result<Vec<_>, _>>()?;

        let result = self
            .deep_convert_partial_circ_children(ident, ps, children, tensor_cache)
            .with_context(|| {
                format!(
                    "in parse, failed to convert partial circuit with ident={:?}",
                    ident
                )
            })?;

        context.insert(ident.clone(), result.clone());
        Ok(result)
    }

    fn deep_convert_partial_circ_children(
        &self,
        ident: &CircuitIdent,
        ps: &PartialCirc,
        mut children: Vec<CircuitRc>,
        tensor_cache: &mut Option<TensorCacheRrfs>,
    ) -> Result<CircuitRc> {
        let expected_k_children = |k| {
            if children.len() != k {
                bail!(ParseError::WrongNumberChildren {
                    expected: k,
                    found: children.len(),
                    ident: format!("{:?}", ident)
                })
            }
            Ok(())
        };

        let extra_should_be_empty = || {
            if !ps.extra.is_empty() {
                bail!(ParseError::ExpectedNoExtraInfo {
                    extra: ps.extra.clone()
                })
            }
            Ok(())
        };

        type T = CircuitType;
        let result = match ps.variant {
            T::Array => {
                expected_k_children(0)?;
                if self.tensors_as_random {
                    Array::randn_named(
                        ps.shape.clone().ok_or(ParseError::ShapeNeeded {
                            variant: ps.variant.to_string(),
                        })?,
                        ps.name.clone(),
                        self.tensors_as_random_device_dtype.clone(),
                    )
                    .rc()
                } else {
                    Array::from_hash_prefix(ps.name.clone(), &ps.extra, tensor_cache)
                        .context("parse array constant from hash prefix")?
                        .rc()
                }
            }
            T::Scalar => {
                expected_k_children(0)?;
                Scalar::nrc(
                    ps.extra
                        .parse::<f64>()
                        .map_err(ParseError::from)
                        .context("failed to parse out scalar number")?,
                    ps.shape
                        .as_ref()
                        .ok_or(ParseError::ShapeNeeded {
                            variant: ps.variant.to_string(),
                        })?
                        .clone(),
                    ps.name.clone(),
                )
            }
            T::Add => {
                if !ps.extra.is_empty() {
                    bail!(ParseError::ExtraUnneededString {
                        string: ps.extra.to_owned(),
                    })
                } else {
                    Add::try_new(children, ps.name.clone())?.rc()
                }
            }
            T::Concat => Concat::try_new(
                children,
                ps.extra
                    .parse::<usize>()
                    .map_err(ParseError::from)
                    .context("failed to parse out concat axis")?,
                ps.name.clone(),
            )?
            .rc(),
            T::Einsum => Einsum::from_einsum_string(&ps.extra, children, ps.name.clone())?.rc(),
            T::Rearrange => {
                expected_k_children(1)?;
                Rearrange::from_einops_string(children[0].clone(), &ps.extra, ps.name.clone())?.rc()
            }
            T::Symbol => {
                expected_k_children(0)?;
                let shape = ps
                    .shape
                    .as_ref()
                    .ok_or(ParseError::ShapeNeeded {
                        variant: ps.variant.to_string(),
                    })?
                    .clone();
                if ps.extra.is_empty() {
                    Symbol::new_with_none_uuid(shape, ps.name.clone()).rc()
                } else {
                    Symbol::nrc(
                        shape,
                        Uuid::from_str(&ps.extra).map_err(|_e| ParseError::Fail {
                            string: ps.extra.to_owned(),
                        })?,
                        ps.name.clone(),
                    )
                }
            }
            T::GeneralFunction => {
                GeneralFunction::new_from_parse(children, ps.extra.clone(), ps.name.clone())?.rc()
            }
            T::Index => {
                expected_k_children(1)?;
                Index::try_new(
                    children[0].clone(),
                    TensorIndex::from_bijection_string(&ps.extra, tensor_cache)?,
                    ps.name.clone(),
                )?
                .rc()
            }
            T::Scatter => {
                expected_k_children(1)?;
                Scatter::try_new(
                    children[0].clone(),
                    TensorIndex::from_bijection_string(&ps.extra, tensor_cache)?,
                    ps.shape
                        .as_ref()
                        .ok_or(ParseError::ShapeNeeded {
                            variant: ps.variant.to_string(),
                        })?
                        .clone(),
                    ps.name.clone(),
                )?
                .rc()
            }
            T::Module => {
                let arg_info = if ps.extra == "all_t" {
                    if children.len() % 2 != 1 {
                        bail!(ParseError::ModuleInconsistentNumChildren {
                            name: ps.name.clone(),
                            extra: ps.extra.clone(),
                            num_children: children.len(),
                            num_args: None
                        })
                    }
                    (0..((children.len() - 1) / 2))
                        .map(|_| [true, true])
                        .collect()
                } else {
                    ps.extra
                        .split(",")
                        .map(|x| {
                            let num_chars = x.chars().count();
                            if num_chars != 2 {
                                bail!(ParseError::Expected2CharsPerForModuleExtra {
                                    name: ps.name.clone(),
                                    num_chars,
                                    extra: ps.extra.clone(),
                                });
                            }
                            let out = x
                                .chars()
                                .map(|x| TerseBool::try_from(x).map(|b| b.0))
                                .collect::<Result<Vec<_>>>()?
                                .try_into()
                                .unwrap();
                            Ok(out)
                        })
                        .collect::<Result<Vec<[bool; 2]>>>()?
                };

                if children.len() != 2 * arg_info.len() + 1 {
                    bail!(ParseError::ModuleInconsistentNumChildren {
                        name: ps.name.clone(),
                        extra: ps.extra.clone(),
                        num_children: children.len(),
                        num_args: Some(arg_info.len())
                    })
                }

                let rest = children.split_off(1);
                let spec_circuit = children.pop().unwrap();

                let (arg_specs, nodes) = rest
                    .chunks(2)
                    .zip(arg_info)
                    .map(|(sym_inp, [batchable, expandable])| {
                        let (sym, inp) = if let [sym, inp] = sym_inp {
                            (sym, inp)
                        } else {
                            unreachable!()
                        };
                        let symbol = sym
                            .as_symbol()
                            .ok_or_else(|| ConstructError::ModuleExpectedSymbol {
                                actual_circuit: sym.clone(),
                            })
                            .context("module expected symbol in parse")?
                            .clone();

                        Ok((
                            ModuleArgSpec {
                                symbol,
                                batchable,
                                expandable,
                            },
                            inp.clone(),
                        ))
                    })
                    .collect::<Result<Vec<_>>>()?
                    .into_iter()
                    .unzip();

                Module::try_new(
                    nodes,
                    ModuleSpec::new(
                        spec_circuit,
                        arg_specs,
                        self.module_check_all_args_present,
                        self.module_check_unique_arg_names,
                    )
                    .context("spec construction failed in parse")?,
                    ps.name.clone(),
                )
                .context("module construction failed in parse")?
                .rc()
            }
            T::Tag => {
                expected_k_children(1)?;
                Uuid::from_str(&ps.extra)
                    .map_err(|e| ParseError::InvalidUuid {
                        string: ps.extra.clone(),
                        err_msg: e.to_string(),
                    })
                    .map(|uuid| Tag::nrc(children[0].clone(), uuid, ps.name.clone()))?
            }
            T::Cumulant => {
                extra_should_be_empty()?;
                Cumulant::nrc(children, ps.name.clone())
            }
            T::DiscreteVar => {
                expected_k_children(2)?;
                DiscreteVar::try_new(children[0].clone(), children[1].clone(), ps.name.clone())?
                    .rc()
            }
            T::StoredCumulantVar => {
                if let [cum_nums, uuid] = ps.extra.split("|").collect::<Vec<_>>()[..] {
                    let keys = cum_nums
                        .split(",")
                        .map(|s| s.trim().parse::<usize>().map_err(ParseError::from))
                        .collect::<Result<Vec<_>, _>>()
                        .context("failed to parse keys for stored cumulant var")?;

                    let uuid = Uuid::from_str(uuid).map_err(|e| ParseError::InvalidUuid {
                        string: ps.extra.clone(),
                        err_msg: e.to_string(),
                    })?;
                    if keys.len() != children.len() {
                        bail!(ParseError::WrongNumberChildren {
                            expected: keys.len(),
                            found: children.len(),
                            ident: format!("{:?}", ident)
                        })
                    } else {
                        StoredCumulantVar::try_new(
                            zip(keys, children).collect(),
                            uuid,
                            ps.name.clone(),
                        )?
                        .rc()
                    }
                } else {
                    bail!(ParseError::Fail {
                        string: ps.extra.clone(),
                    })
                }
            }
            T::SetSymbolicShape => {
                expected_k_children(1)?;
                extra_should_be_empty()?;
                SetSymbolicShape::try_new(
                    children[0].clone(),
                    ps.shape
                        .as_ref()
                        .ok_or(ParseError::ShapeNeeded {
                            variant: ps.variant.to_string(),
                        })?
                        .clone(),
                    ps.name.clone(),
                )?
                .rc()
            }
            T::Conv => {
                unimplemented!()
            }
        };
        Ok(result)
    }
}

#[apply(python_error_exception)]
#[base_error_name(ParseArg)]
#[base_exception(PyValueError)]
#[derive(Error, Debug, Clone)]
pub enum ParseArgError {
    #[error("circuit={circuit:?} ({e_name})")]
    ReferenceCircuitByNameHasNoneName { circuit: CircuitRc },

    #[error("dup_idents={dup_idents:?} ({e_name})")]
    ReferenceCircuitDuplicateIdentifier { dup_idents: HashMap<String, usize> },
}
