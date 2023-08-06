use std::{
    collections::HashSet,
    fmt,
    fmt::Debug,
    hash::{Hash, Hasher},
    sync::Mutex,
};

use anyhow::{anyhow, bail, Context, Error, Result};
use num_bigint::BigUint;
use pyo3::{once_cell::GILLazy, prelude::*};
use rr_util::{
    fn_struct, py_types::MaybeNotSet, python_println, symbolic_size::SymbolicSizeProduct,
    tensor_util::ParseError,
};
use rustc_hash::FxHashMap as HashMap;

use crate::{
    circuit_utils::{count_nodes, total_flops},
    generalfunction::SpecTrait,
    opaque_iterative_matcher::{OpaqueIterativeMatcher, OpaqueIterativeMatcherVal},
    prelude::*,
    HashBytes,
};

// TODO: fix color scheme
const COLOR_CODES: [usize; 15] = [30, 31, 32, 33, 34, 35, 36, 90, 91, 92, 93, 94, 95, 96, 97];

const BAR: &'static str = "│";
const TEE: &'static str = "├";
const ARROW: &'static str = "‣";
const UP_ELBOW: &'static str = "└";
const DOWN_ELBOW: &'static str = "┌";

fn_struct!(pub CircuitToColorCode:Fn(circuit:CircuitRc)->usize);

#[pyclass]
#[derive(Clone)]
pub struct PrintOptions {
    #[pyo3(get, set)]
    pub bijection: bool,
    #[pyo3(get, set)]
    pub shape_only_when_necessary: bool,
    pub traversal: Option<OpaqueIterativeMatcherVal>,
    #[pyo3(get, set)]
    pub leaves_on_top: bool,
    #[pyo3(get, set)]
    pub arrows: bool,
    #[pyo3(get, set)]
    pub print_size_threshold: Option<usize>,
    #[pyo3(get, set)]
    pub force_use_serial_numbers: bool,
    pub colorer: Option<CircuitToColorCode>,
}

impl Default for PrintOptions {
    fn default() -> Self {
        Self {
            bijection: true,
            shape_only_when_necessary: true,
            traversal: None,
            leaves_on_top: false,
            arrows: false,
            print_size_threshold: None,
            force_use_serial_numbers: false,
            colorer: None,
        }
        .validate_ret()
        .unwrap()
    }
}

impl PrintOptions {
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
    pub fn validate_ret(self) -> Result<Self> {
        self.validate()?;
        Ok(self)
    }
}

const DEFAULT_END_DEPTH: usize = 2;
const DEFAULT_PRINT_SIZE_THRESHOLD: usize = 400_000_000;

#[derive(Debug, Clone)]
pub struct TerseBool(pub bool);

impl fmt::Display for TerseBool {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(if self.0 { "t" } else { "f" })
    }
}
impl std::str::FromStr for TerseBool {
    type Err = Error;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let out = match s {
            "t" => true,
            "f" => false,
            _ => bail!(ParseError::InvalidTerseBool { got: s.to_owned() }),
        };
        Ok(TerseBool(out))
    }
}
impl TryFrom<char> for TerseBool {
    type Error = Error;
    fn try_from(value: char) -> Result<Self, Self::Error> {
        let out = match value {
            't' => true,
            'f' => false,
            _ => bail!(ParseError::InvalidTerseBool {
                got: value.to_string()
            }),
        };
        Ok(TerseBool(out))
    }
}

pub fn op_traversal_per(
    op_traversal: Option<OpaqueIterativeMatcherVal>,
    circ: CircuitRc,
) -> Result<Option<Vec<Option<OpaqueIterativeMatcherVal>>>> {
    let num_children = circ.num_children();
    let new_traversal_per = if let Some(traversal) = op_traversal {
        let updated = traversal
            .opaque_match_iterate(circ.crc())?
            .updated
            .unwrap_or_else(|| Some(traversal).into());
        if updated.all_finished() {
            return Ok(None);
        }
        updated
            .per_child_with_term(num_children)
            .into_iter()
            .map(Some)
            .collect()
    } else {
        vec![None; num_children]
    };
    Ok(Some(new_traversal_per))
}

#[pymethods]
impl PrintOptions {
    // new function for rust and python (in rust for validation)
    #[new]
    #[args(
        bijection = "PrintOptions::default().bijection",
        shape_only_when_necessary = "PrintOptions::default().shape_only_when_necessary",
        traversal = "None",
        leaves_on_top = "PrintOptions::default().leaves_on_top",
        arrows = "PrintOptions::default().arrows",
        print_size_threshold = "None",
        force_use_serial_numbers = "PrintOptions::default().force_use_serial_numbers",
        colorer = "None"
    )]
    pub fn new(
        bijection: bool,
        shape_only_when_necessary: bool,
        traversal: Option<OpaqueIterativeMatcherVal>,
        leaves_on_top: bool,
        arrows: bool,
        print_size_threshold: Option<usize>,
        force_use_serial_numbers: bool,
        colorer: Option<CircuitToColorCode>,
    ) -> Result<Self> {
        let result = Self {
            bijection,
            shape_only_when_necessary,
            traversal,
            leaves_on_top,
            arrows,
            print_size_threshold,
            force_use_serial_numbers,
            colorer,
        };
        result.validate()?;
        Ok(result)
    }

    #[args(
        bijection = "Default::default()",
        shape_only_when_necessary = "Default::default()",
        traversal = "Default::default()",
        leaves_on_top = "Default::default()",
        arrows = "Default::default()",
        print_size_threshold = "Default::default()",
        force_use_serial_numbers = "Default::default()",
        colorer = "Default::default()"
    )]
    pub fn evolve(
        &self,
        bijection: MaybeNotSet<bool>,
        shape_only_when_necessary: MaybeNotSet<bool>,
        traversal: MaybeNotSet<Option<OpaqueIterativeMatcherVal>>,
        leaves_on_top: MaybeNotSet<bool>,
        arrows: MaybeNotSet<bool>,
        print_size_threshold: MaybeNotSet<Option<usize>>,
        force_use_serial_numbers: MaybeNotSet<bool>,
        colorer: MaybeNotSet<Option<CircuitToColorCode>>,
    ) -> Result<Self> {
        let cloned = self.clone();
        Self::new(
            bijection.0.unwrap_or(cloned.bijection),
            shape_only_when_necessary
                .0
                .unwrap_or(cloned.shape_only_when_necessary),
            traversal.0.unwrap_or(cloned.traversal),
            leaves_on_top.0.unwrap_or(cloned.leaves_on_top),
            arrows.0.unwrap_or(cloned.arrows),
            print_size_threshold
                .0
                .unwrap_or(cloned.print_size_threshold),
            force_use_serial_numbers
                .0
                .unwrap_or(cloned.force_use_serial_numbers),
            colorer.0.unwrap_or(cloned.colorer),
        )
    }

    #[staticmethod]
    pub fn compiler_default() -> PrintOptions {
        Self {
            print_size_threshold: Some(DEFAULT_PRINT_SIZE_THRESHOLD),
            force_use_serial_numbers: true,
            ..Default::default()
        }
        .validate_ret()
        .unwrap()
    }

    #[staticmethod]
    #[args(end_depth = "DEFAULT_END_DEPTH")]
    pub fn debug_default(end_depth: Option<usize>) -> PrintOptions {
        Self {
            bijection: false,
            shape_only_when_necessary: false,
            traversal: end_depth.map(|x| OpaqueIterativeMatcherVal::for_end_depth(x)),
            ..Default::default()
        }
        .validate_ret()
        .unwrap()
    }

    pub fn validate(&self) -> Result<()> {
        if self.bijection && self.leaves_on_top {
            bail!(anyhow!("bijection print cant have leaves on top"))
        }
        if self.bijection && self.traversal.is_some() {
            bail!(anyhow!(
                "bijection print cant terminate early, so traversal must be None"
            ))
        }
        Ok(())
    }

    #[pyo3(name = "print")]
    #[args(circuits = "*")]
    pub fn print_circuits(&self, circuits: Vec<CircuitRc>) -> Result<()> {
        python_println!("{}", self.repr_circuits(circuits)?);
        Ok(())
    }

    pub fn string_escape(&self, name: &str) -> String {
        if self.bijection {
            format!("'{}'", name.replace('\\', r"\\").replace('\'', r"\'"))
        } else {
            name.to_owned()
        }
    }

    pub fn repr_line_info(&self, circ: CircuitRc) -> Result<String> {
        let mut result = "".to_owned();

        if !self.shape_only_when_necessary
            || matches!(
                &**circ,
                Circuit::Scalar(_)
                    | Circuit::Scatter(_)
                    | Circuit::Symbol(_)
                    | Circuit::Array(_)
                    | Circuit::SetSymbolicShape(_)
            )
            || !circ.info().named_axes.is_empty()
        {
            result.push_str(&format!(
                " [{}]",
                (0..circ.info().rank())
                    .map(|x| match circ.info().named_axes.get(&(x as u8)) {
                        None => SymbolicSizeProduct::from(circ.shape()[x]).to_string(),
                        Some(s) => format!("{}:{}", self.string_escape(s), circ.shape()[x]),
                    })
                    .collect::<Vec<_>>()
                    .join(",")
            ))
        }
        result.push(' ');
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
                            .context("failed to get general function spec serialize in print")?
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
                    if mn.spec.arg_specs.len() >= 3
                        && mn
                            .spec
                            .arg_specs
                            .iter()
                            .all(|x| x.batchable && x.expandable)
                    {
                        "all_t".to_owned()
                    } else {
                        // print out out arg info, everything else in children
                        // TODO: less terse?
                        mn.spec
                            .arg_specs
                            .iter()
                            .map(|arg_spec| {
                                format!(
                                    "{}{}",
                                    TerseBool(arg_spec.batchable),
                                    TerseBool(arg_spec.expandable)
                                )
                            })
                            .collect::<Vec<_>>()
                            .join(",")
                    }
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
        if let Some(threshold) = self.print_size_threshold {
            if circ.info().numel() > BigUint::from(threshold) && !circ.is_array() {
                result.push_str(&format!(" # {}", color(&oom_fmt(circ.info().numel()), 1)));
            }
        }

        for _ in 0..2 {
            result = result
                .strip_suffix(' ')
                .map(|x| x.to_owned())
                .unwrap_or(result); // remove trailing spaces
        }
        Ok(result)
    }

    #[pyo3(name = "repr")]
    #[args(circuits = "*")]
    pub fn repr_circuits(&self, circuits: Vec<CircuitRc>) -> Result<String> {
        let mut seen_hashes: HashMap<HashBytes, String> = HashMap::default();

        let disallow_name_ident = if !self.force_use_serial_numbers {
            let mut multiple_with_name: HashMap<String, bool> = HashMap::default();
            let mut seen = HashSet::default();

            fn recurse(
                circ: CircuitRc,
                seen: &mut HashSet<HashBytes>,
                multiple_with_name: &mut HashMap<String, bool>,
            ) {
                if !seen.insert(circ.info().hash) {
                    return;
                }
                if let Some(name) = circ.name_cloned() {
                    use std::collections::hash_map::Entry::*;
                    match multiple_with_name.entry(name) {
                        Occupied(mut entry) => {
                            entry.insert(true);
                        }
                        Vacant(entry) => {
                            entry.insert(false);
                        }
                    }
                }

                for child in circ.children() {
                    recurse(child, seen, multiple_with_name)
                }
            }
            for c in &circuits {
                recurse(c.clone(), &mut seen, &mut multiple_with_name)
            }
            Some(multiple_with_name)
        } else {
            None
        };

        // ideally this would separate method, but to avoid breaking blame we keep like this
        fn recurse(
            circ: &Circuit,
            depth: usize,
            result: &mut String,
            seen_hashes: &mut HashMap<HashBytes, String>,
            runnning_serial_number: &mut usize,
            selfy: &PrintOptions,
            is_last_child: &Vec<bool>,
            traversal: Option<OpaqueIterativeMatcherVal>,
            disallow_name_ident: Option<&HashMap<String, bool>>,
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

            if let Some(colorer) = &selfy.colorer {
                result.push_str(&format!(
                    "\u{001b}[{}m",
                    COLOR_CODES[colorer.call(circ.clone().rc())? % COLOR_CODES.len()]
                ));
            }

            // allow_name_ident is_some iff !self.force_use_serial_numbers
            let disallow_name = disallow_name_ident
                .zip(circ.name())
                .map(|(map, name)| map[name])
                .unwrap_or(true);

            let (repeat_string, line_prefix) = match (disallow_name, circ.name()) {
                (_, Some(name)) => {
                    let escaped = selfy.string_escape(name);
                    let out = if disallow_name {
                        let this_serial_number = runnning_serial_number.to_string();
                        *runnning_serial_number += 1;
                        this_serial_number + " " + &escaped
                    } else {
                        escaped
                    };
                    (out.clone(), out)
                }
                (true, None) => {
                    let this_serial_number = runnning_serial_number.to_string();
                    *runnning_serial_number += 1;
                    (
                        this_serial_number.clone() + " " + &circ.variant_string(),
                        this_serial_number,
                    )
                }

                (false, None) => unreachable!(),
            };

            seen_hashes.insert(circ.info().hash, repeat_string);

            result.push_str(&line_prefix);
            result.push_str(
                &selfy
                    .repr_line_info(circ.clone().rc())
                    .with_context(|| format!("repr line info failed for circuit={:?}", circ))?,
            );
            if selfy.colorer.is_some() {
                result.push_str("\u{001b}[0m");
            }

            let num_children = circ.num_children();

            let new_traversal_per =
                if let Some(new_traversal_per) = op_traversal_per(traversal, circ.crc())? {
                    new_traversal_per
                } else {
                    // all finished case
                    // traversal can't be used with bijection, so we can add ... without having to parse later
                    if circ.children().count() != 0 {
                        result.push_str(" ...");
                    }
                    result.push('\n');
                    return Ok(());
                };

            result.push('\n');
            for (i, (child, new_traversal)) in circ.children().zip(new_traversal_per).enumerate() {
                recurse(
                    &child,
                    depth + 1,
                    result,
                    seen_hashes,
                    runnning_serial_number,
                    selfy,
                    &is_last_child
                        .iter()
                        .copied()
                        .chain(std::iter::once(i == num_children - 1))
                        .collect(),
                    new_traversal,
                    disallow_name_ident,
                )?;
            }
            Ok(())
        }
        let mut result = String::new();
        let mut runnning_serial_number = 0;
        for circuit in circuits {
            recurse(
                &**circuit,
                0,
                &mut result,
                &mut seen_hashes,
                &mut runnning_serial_number,
                &self,
                &vec![],
                self.traversal.clone(),
                disallow_name_ident.as_ref(),
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
        if result.chars().last() == Some('\n') {
            result.pop();
        }
        Ok(result)
    }

    #[staticmethod]
    #[pyo3(name = "repr_depth")]
    #[args(circuits = "*", end_depth = "3")]
    pub fn repr_circuits_depth(circuits: Vec<CircuitRc>, end_depth: usize) -> String {
        PrintOptions {
            bijection: false,
            traversal: Some(OpaqueIterativeMatcherVal::for_end_depth(end_depth)),
            ..Default::default()
        }
        .validate_ret()
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
    pub fn size_colorer() -> CircuitToColorCode {
        CircuitToColorCode::new_dyn(Box::new(|c| Ok(circuit_to_size_color_code(c))))
    }

    #[staticmethod]
    pub fn variant_colorer() -> CircuitToColorCode {
        CircuitToColorCode::new_dyn(Box::new(|circuit: CircuitRc| {
            let mut hasher = std::collections::hash_map::DefaultHasher::default();
            circuit.variant_string().hash(&mut hasher);
            Ok(hasher.finish() as usize)
        }))
    }

    #[staticmethod]
    pub fn hash_colorer() -> CircuitToColorCode {
        CircuitToColorCode::new_dyn(Box::new(|circuit: CircuitRc| {
            Ok(circuit.info().hash_usize())
        }))
    }
    #[staticmethod]
    pub fn fixed_color(color: usize) -> CircuitToColorCode {
        CircuitToColorCode::new_dyn(Box::new(move |_circuit: CircuitRc| Ok(color)))
    }

    #[staticmethod]
    pub fn computability_colorer() -> CircuitToColorCode {
        CircuitToColorCode::new_dyn(Box::new(|c| Ok(circuit_to_computability_color_code(c))))
    }
}

fn init_print_options() -> PrintOptions {
    let end_depth_str =
        std::env::var("RR_DEBUG_END_DEPTH").unwrap_or_else(|_| DEFAULT_END_DEPTH.to_string());
    let end_depth = if end_depth_str.to_lowercase() == "none" {
        None
    } else {
        Some(end_depth_str.parse().unwrap_or_else(|_| {
            eprintln!(
                "failed to parse RR_DEBUG_END_DEPTH={}, {} (default: {})",
                end_depth_str, "expected 'None' or positive integer", DEFAULT_END_DEPTH,
            );
            DEFAULT_END_DEPTH
        }))
    };
    PrintOptions::debug_default(end_depth)
}

pub fn circuit_to_size_color_code(circuit: CircuitRc) -> usize {
    let size = circuit.info().numel_usize();
    if size == usize::MAX {
        3
    } else if size > 10_000_000_000 {
        4
    } else if size > 300_000_000 {
        1
    } else if size > 300_000 {
        2
    } else {
        0
    }
}

pub fn circuit_to_computability_color_code(circuit: CircuitRc) -> usize {
    if circuit.info().can_be_sampled {
        1
    } else if !circuit.info().is_explicitly_computable {
        2
    } else {
        0
    }
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
        oom_fmt(circuit.info().max_non_leaf_size.clone()),
        oom_fmt(total_flops(circuit.crc()))
    ));
    println!("{}", result);
}

pub fn color(string: &str, color_int: usize) -> String {
    format!(
        "\u{001b}[{}m{}\u{001b}[0m",
        COLOR_CODES[color_int % COLOR_CODES.len()],
        string
    )
}
