use std::{
    fmt::Debug,
    hash::{Hash, Hasher},
    sync::Mutex,
};

use anyhow::{anyhow, bail, Context, Result};
use num_bigint::BigUint;
use pyo3::{once_cell::GILLazy, prelude::*};
use rr_util::{fn_struct, py_types::MaybeNotSet, python_println};
use rustc_hash::FxHashMap as HashMap;

use crate::{
    circuit_utils::{count_nodes, total_flops},
    generalfunction::SpecTrait,
    opaque_iterative_matcher::{OpaqueIterativeMatcher, OpaqueIterativeMatcherVal},
    prelude::*,
    HashBytes,
};
const COLOR_CODES: [usize; 15] = [30, 31, 32, 33, 34, 35, 36, 90, 91, 92, 93, 94, 95, 96, 97];

const BAR: &'static str = "│";
const TEE: &'static str = "├";
const ARROW: &'static str = "‣";
const UP_ELBOW: &'static str = "└";
const DOWN_ELBOW: &'static str = "┌";

fn_struct!(pub CircuitToColor:Fn(circuit:CircuitRc)->usize);
// fn_struct!(pub CircuitToName:Fn(circuit:CircuitRc)->String);

#[pyclass]
#[derive(Clone)]
pub struct PrintOptions {
    #[pyo3(get, set)]
    pub bijection: bool,
    #[pyo3(get, set)]
    pub shape_only_when_necessary: bool,
    pub term_at: Option<OpaqueIterativeMatcherVal>,
    #[pyo3(get, set)]
    pub leaves_on_top: bool,
    #[pyo3(get, set)]
    pub arrows: bool,
    #[pyo3(get, set)]
    pub colorer: Option<CircuitToColor>,
    #[pyo3(get, set)]
    pub inc_ids: bool,
}

impl Default for PrintOptions {
    fn default() -> Self {
        Self {
            bijection: true,
            shape_only_when_necessary: true,
            term_at: None,
            leaves_on_top: false,
            arrows: false,
            colorer: None,
            inc_ids: true,
        }
    }
}

impl PrintOptions {
    pub fn new(
        bijection: bool,
        shape_only_when_necessary: bool,
        term_at: Option<OpaqueIterativeMatcherVal>,
        leaves_on_top: bool,
        arrows: bool,
        colorer: Option<CircuitToColor>,
        inc_ids: bool,
    ) -> Result<Self> {
        let result = Self {
            bijection,
            shape_only_when_necessary,
            term_at,
            leaves_on_top,
            arrows,
            colorer,
            inc_ids,
        };
        result.validate()?;
        Ok(result)
    }

    pub fn repr(&self, circuit: CircuitRc) -> Result<String> {
        self.repr_circuits(vec![circuit])
    }
    pub fn print(&self, circuit: CircuitRc) -> Result<()> {
        self.print_circuits(vec![circuit])
    }
    pub fn repr_depth(circuit: CircuitRc, end_depth: usize) -> String {
        Self::repr_circuits_depth(vec![circuit], end_depth)
    }
    pub fn print_depth(circuit: CircuitRc, end_depth: usize) -> () {
        Self::print_circuits_depth(vec![circuit], end_depth)
    }
}
const DEFAULT_END_DEPTH: usize = 2;

#[pymethods]
impl PrintOptions {
    // new function for rust and python (in rust for validation)
    #[new]
    #[args(
        bijection = "PrintOptions::default().bijection",
        shape_only_when_necessary = "PrintOptions::default().shape_only_when_necessary",
        term_at = "None",
        leaves_on_top = "PrintOptions::default().leaves_on_top",
        arrows = "PrintOptions::default().arrows",
        inc_ids = "PrintOptions::default().inc_ids"
    )]
    pub fn py_new(
        bijection: bool,
        shape_only_when_necessary: bool,
        term_at: Option<OpaqueIterativeMatcherVal>,
        leaves_on_top: bool,
        arrows: bool,
        colorer: Option<CircuitToColor>,
        inc_ids: bool,
    ) -> Result<Self> {
        let result = Self {
            bijection,
            shape_only_when_necessary,
            term_at,
            leaves_on_top,
            arrows,
            colorer,
            inc_ids,
        };
        result.validate()?;
        Ok(result)
    }

    #[args(
        bijection = "Default::default()",
        shape_only_when_necessary = "Default::default()",
        term_at = "Default::default()",
        leaves_on_top = "Default::default()",
        arrows = "Default::default()",
        colorer = "Default::default()",
        inc_ids = "Default::default()"
    )]
    pub fn evolve(
        &self,
        bijection: MaybeNotSet<bool>,
        shape_only_when_necessary: MaybeNotSet<bool>,
        term_at: MaybeNotSet<Option<OpaqueIterativeMatcherVal>>,
        leaves_on_top: MaybeNotSet<bool>,
        arrows: MaybeNotSet<bool>,
        colorer: MaybeNotSet<Option<CircuitToColor>>,
        inc_ids: MaybeNotSet<bool>,
    ) -> Result<Self> {
        let cloned = self.clone();
        Self::new(
            bijection.0.unwrap_or(cloned.bijection),
            shape_only_when_necessary
                .0
                .unwrap_or(cloned.shape_only_when_necessary),
            term_at.0.unwrap_or(cloned.term_at),
            leaves_on_top.0.unwrap_or(cloned.leaves_on_top),
            arrows.0.unwrap_or(cloned.arrows),
            colorer.0.unwrap_or(cloned.colorer),
            inc_ids.0.unwrap_or(cloned.inc_ids),
        )
    }

    #[staticmethod]
    pub fn debug_default() -> Result<PrintOptions> {
        Self::new(
            false,
            false,
            Some(OpaqueIterativeMatcherVal::for_end_depth(DEFAULT_END_DEPTH)),
            false,
            false,
            None,
            true,
        )
    }

    pub fn validate(&self) -> Result<()> {
        if self.bijection && self.leaves_on_top {
            bail!(anyhow!("bijection print cant have leaves on top"))
        }
        if self.bijection && self.term_at.is_some() {
            bail!(anyhow!("bijection print cant terminate early"))
        }
        if self.bijection && !self.inc_ids {
            bail!(anyhow!("bijection print requires inc_ids = True"))
        }
        Ok(())
    }

    #[pyo3(name = "print")]
    #[args(circuits = "*")]
    pub fn print_circuits(&self, circuits: Vec<CircuitRc>) -> Result<()> {
        python_println!("{}", self.repr_circuits(circuits)?);
        Ok(())
    }

    pub fn repr_line(&self, circ: CircuitRc) -> Result<String> {
        let mut result = "".to_owned();
        if let Some(n) = circ.name() {
            result.push(' ');
            if self.bijection {
                result.push('\'');
                result.push_str(&n.replace('\\', r"\\").replace('\'', r"\'"));
                result.push('\'');
            } else {
                result.push_str(n);
            }
        }
        if !self.shape_only_when_necessary
            || matches!(
                &**circ,
                Circuit::Scalar(_) | Circuit::Scatter(_) | Circuit::Symbol(_) | Circuit::Array(_)
            )
        {
            result.push_str(&format!(" {:?}", circ.info().shape));
        }
        result.push(' ');
        if !self.bijection
            && circ.info().numel() > BigUint::from(400_000_000usize)
            && !matches!(&**circ, Circuit::Array(_))
        {
            result.push_str(&color(&oom_fmt(circ.info().numel()), 1));
        }
        let variant_string = circ.variant_string();
        let vs: &str = &variant_string;
        result.push_str(vs);
        result.push(' ');
        result.push_str(&{
            match &**circ {
                Circuit::Scalar(scalar) => {
                    format!("{:.}", scalar.value)
                }
                Circuit::Rearrange(rearrange) => rearrange.spec.to_einops_string(true),
                Circuit::Einsum(einsum) => einsum.get_spec().to_einsum_string(),
                Circuit::Index(index) => {
                    if self.bijection {
                        index.index.repr_bijection()?
                    } else {
                        format!("{}", index.index)
                    }
                }
                Circuit::Scatter(scatter) => {
                    if self.bijection {
                        scatter.index.repr_bijection()?
                    } else {
                        format!("{}", scatter.index)
                    }
                }
                Circuit::Concat(concat) => concat.axis.to_string(),
                Circuit::GeneralFunction(gf) => {
                    if self.bijection {
                        gf.spec
                            .serialize()
                            .context("failed to get spec serialize in print")?
                            .unwrap_or_else(|| format!("{} [NOT_SERIALIZABLE]", gf.spec.name()))
                    } else {
                        gf.spec.name()
                    }
                }
                Circuit::Symbol(sy) => {
                    if sy.uuid.is_nil() {
                        "".to_owned()
                    } else {
                        format!("{}", &sy.uuid)
                    }
                }
                Circuit::Module(mn) => {
                    (&mn.spec.name.as_ref().unwrap_or(&"".to_owned())).to_string()
                }
                Circuit::Array(ac) => {
                    if self.bijection {
                        ac.save_rrfs()?;
                        ac.tensor_hash_base16()[..24].to_owned()
                    } else {
                        "".to_owned()
                    }
                }
                Circuit::Tag(at) => at.uuid.to_string(),
                Circuit::StoredCumulantVar(scv) => {
                    format!(
                        "{}|{}",
                        scv.cumulants
                            .keys()
                            .map(|k| k.to_string())
                            .collect::<Vec<_>>()
                            .join(", "),
                        scv.uuid.to_string(),
                    )
                }
                _ => "".to_owned(),
            }
        });
        if !circ.info().named_axes.is_empty() {
            result.push_str(&format!(
                " NA[{}]",
                (0..circ.info().rank())
                    .map(|x| match circ.info().named_axes.get(&(x as u8)) {
                        None => "".to_owned(),
                        Some(s) => s.clone(),
                    })
                    .collect::<Vec<_>>()
                    .join(",")
            ))
        }

        for _ in 0..2 {
            result = result
                .strip_suffix(' ')
                .map(|x| x.to_owned())
                .unwrap_or(result); // remove trailing spaces
        }
        if result.starts_with(" ") {
            result = result[1..].to_owned();
        }
        Ok(result)
    }

    #[pyo3(name = "repr")]
    #[args(circuits = "*")]
    pub fn repr_circuits(&self, circuits: Vec<CircuitRc>) -> Result<String> {
        let mut seen_hashes: HashMap<HashBytes, String> = HashMap::default();
        fn recurse(
            circ: &Circuit,
            depth: usize,
            result: &mut String,
            seen_hashes: &mut HashMap<HashBytes, String>,
            selfy: &PrintOptions,
            is_last_child: &Vec<bool>,
            term_at: Option<OpaqueIterativeMatcherVal>,
        ) -> Result<()> {
            if selfy.arrows {
                if depth > 1 {
                    for i in 0..(depth - 1) {
                        result.push_str(if is_last_child[i] { " " } else { BAR });
                        result.push(' ');
                    }
                }
                if depth > 0 {
                    result.push_str(if *is_last_child.last().unwrap() {
                        UP_ELBOW
                    } else {
                        TEE
                    });
                    result.push_str(ARROW);
                }
            } else {
                result.push_str(&" ".repeat(depth * 2));
            }
            if let Some(prev) = seen_hashes.get(&circ.info().hash) {
                result.push_str(prev);
                result.push('\n');
                return Ok(());
            }
            seen_hashes.insert(
                circ.info().hash,
                seen_hashes.len().to_string() + " " + circ.name().unwrap_or(&circ.variant_string()),
            );

            if let Some(colorer) = &selfy.colorer {
                result.push_str(&format!(
                    "\u{001b}[{}m",
                    COLOR_CODES[colorer.call(circ.clone().rc())? % COLOR_CODES.len()]
                ));
            }
            if selfy.inc_ids {
                result.push_str(&(seen_hashes.len() - 1).to_string());
                result.push(' ');
            }
            result.push_str(&selfy.repr_line(circ.clone().rc())?);
            if selfy.colorer.is_some() {
                result.push_str("\u{001b}[0m");
            }

            let n_children = circ.children().count();
            // let mut new_term_at = term_at.clone();
            let new_term_at = if let Some(ta) = term_at {
                let match_result = ta.opaque_match_iterate(circ.crc())?;
                if match_result.finished {
                    //term_at can't be used with bijection, so we can add ... without having to parse later
                    result.push_str(" ...");
                    result.push('\n');
                    return Ok(());
                }
                Some(match_result.updated.unwrap_or(ta))
            } else {
                None
            };
            result.push('\n');
            for (i, child) in circ.children().enumerate() {
                recurse(
                    &child,
                    depth + 1,
                    result,
                    seen_hashes,
                    selfy,
                    &is_last_child
                        .iter()
                        .copied()
                        .chain(std::iter::once(i == n_children - 1))
                        .collect(),
                    new_term_at.clone(),
                )?;
            }
            Ok(())
        }
        let mut result = String::new();
        for circuit in circuits {
            recurse(
                &**circuit,
                0,
                &mut result,
                &mut seen_hashes,
                &self,
                &vec![],
                self.term_at.clone(),
            )?;
        }

        if self.leaves_on_top {
            result = result
                .trim()
                .lines()
                .rev()
                .map(|x| x.replace(UP_ELBOW, DOWN_ELBOW))
                .collect::<Vec<_>>()
                .join("\n");
        }
        if result.chars().last().unwrap() == '\n' {
            result.pop();
        }
        Ok(result)
    }

    #[staticmethod]
    #[pyo3(name = "repr_depth")]
    #[args(circuits = "*", end_depth = "3")]
    pub fn repr_circuits_depth(circuits: Vec<CircuitRc>, end_depth: usize) -> String {
        PrintOptions::new(
            false,
            true,
            Some(OpaqueIterativeMatcherVal::for_end_depth(end_depth)),
            false,
            false,
            None,
            true,
        )
        .expect("these options are valid")
        .repr_circuits(circuits)
        .expect("depth matcher can't fail + bijection is off")
    }
    #[staticmethod]
    #[pyo3(name = "print_depth")]
    #[args(end_depth = "3")]
    pub fn print_circuits_depth(circuits: Vec<CircuitRc>, end_depth: usize) {
        python_println!("{}", PrintOptions::repr_circuits_depth(circuits, end_depth))
    }

    #[staticmethod]
    pub fn size_colorer() -> CircuitToColor {
        CircuitToColor::new_dyn(Box::new(|circuit: CircuitRc| {
            let size = circuit.info().numel_usize();
            Ok(if size == usize::MAX {
                3
            } else if size > 10_000_000_000 {
                4
            } else if size > 300_000_000 {
                1
            } else if size > 300_000 {
                2
            } else {
                0
            })
        }))
    }

    #[staticmethod]
    pub fn variant_colorer() -> CircuitToColor {
        CircuitToColor::new_dyn(Box::new(|circuit: CircuitRc| {
            let mut hasher = std::collections::hash_map::DefaultHasher::default();
            circuit.variant_string().hash(&mut hasher);
            Ok(hasher.finish() as usize)
        }))
    }

    #[staticmethod]
    pub fn hash_colorer() -> CircuitToColor {
        CircuitToColor::new_dyn(Box::new(|circuit: CircuitRc| {
            Ok(circuit.info().hash_usize())
        }))
    }
    #[staticmethod]
    pub fn fixed_color(color: usize) -> CircuitToColor {
        CircuitToColor::new_dyn(Box::new(move |_circuit: CircuitRc| Ok(color)))
    }

    #[staticmethod]
    pub fn computability_colorer() -> CircuitToColor {
        CircuitToColor::new_dyn(Box::new(|circuit: CircuitRc| {
            Ok(if circuit.info().can_be_sampled {
                1
            } else if !circuit.info().is_explicitly_computable {
                2
            } else {
                0
            })
        }))
    }
}

fn init_print_options() -> PrintOptions {
    let end_depth_str =
        std::env::var("RR_DEBUG_END_DEPTH").unwrap_or_else(|_| DEFAULT_END_DEPTH.to_string());
    if end_depth_str.to_lowercase() == "none" {
        return Default::default();
    }

    let end_depth = end_depth_str.parse().unwrap_or_else(|_| {
        eprintln!(
            "failed to parse RR_DEBUG_END_DEPTH={}, {} (default: {})",
            end_depth_str, "expected 'None' or positive integer", DEFAULT_END_DEPTH,
        );
        DEFAULT_END_DEPTH
    });
    let out = PrintOptions {
        term_at: Some(OpaqueIterativeMatcherVal::for_end_depth(end_depth)),
        bijection: false,
        shape_only_when_necessary: false,
        ..PrintOptions::default()
    };
    out.validate().unwrap();
    out
}

static DEBUG_PRINT_OPTIONS: GILLazy<Mutex<PrintOptions>> =
    GILLazy::new(|| Mutex::new(init_print_options()));

#[pyfunction]
pub fn set_debug_print_options(options: PrintOptions) {
    *DEBUG_PRINT_OPTIONS.lock().unwrap() = options;
}

pub fn debug_repr(circ: CircuitRc) -> Result<String> {
    Ok(format!(
        "({})", // we wrap in parens to make it clear what's a single circuit.
        DEBUG_PRINT_OPTIONS.lock().unwrap().repr(circ)?
    ))
}

pub fn oom_fmt<T: Into<BigUint>>(num: T) -> String {
    let mut num: BigUint = num.into();
    let k = BigUint::from(1000usize);
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"].iter() {
        if &num < &k {
            return format!("{}{}", num, unit);
        }
        num /= &k;
    }
    format!("{}Y", num)
}

pub fn print_circuit_stats(circuit: &Circuit) {
    let mut result = String::new();
    result.push_str(
        &circuit
            .name_cloned()
            .map(|x| x + " ")
            .unwrap_or(" ".to_owned()),
    );
    result.push_str(&circuit.variant_string());
    result.push_str(&format!(
        " nodes {} max_size {} flops {}",
        count_nodes(circuit.crc()),
        oom_fmt(circuit.max_non_input_size()),
        oom_fmt(total_flops(circuit.crc()))
    ));
    println!("{}", result);
}

pub fn color(string: &str, color_int: usize) -> String {
    format!(
        "\u{001b}[{}m{}\u{001b}[0m ",
        COLOR_CODES[color_int % COLOR_CODES.len()],
        string
    )
}
