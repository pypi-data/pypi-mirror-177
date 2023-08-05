use std::iter::zip;

use anyhow::{bail, Context, Result};
use macro_rules_attribute::apply;
use once_cell::sync::Lazy;
use pyo3::{prelude::*, types::PyDict};
use regex::Regex;
use rr_util::{
    pycall,
    tensor_util::{Shape, TorchDeviceDtype},
};
use rustc_hash::FxHashMap as HashMap;
use uuid::{uuid, Uuid};

use crate::{
    all_children, circuit_node_auto_impl, circuit_node_extra_impl,
    circuit_utils::replace_nodes,
    deep_map_op_context, deep_map_op_context_preorder_stoppable, deep_map_unwrap,
    evaluate_fn_dtype_device,
    expand_node::{replace_expand_bottom_up, ExpandError},
    new_rc_unwrap,
    prelude::*,
    Array, CachedCircuitInfo, HashBytes, PyCircuitBase, Symbol,
};

#[pyclass]
#[derive(Debug, Clone, Hash, PartialEq, Eq)]
pub struct ModuleSpec {
    #[pyo3(get)]
    pub spec_circuit: CircuitRc,
    #[pyo3(get)]
    pub input_specs: Vec<ModuleArgSpec>,
    #[pyo3(get)]
    pub name: Option<String>,
}

impl ModuleSpec {
    pub const EXPAND_PLACEHOLDER_UUID: Uuid = uuid!("741ba404-eec3-4ac9-b6ce-062e903fb033");
    pub fn expand_raw(&self, nodes: &Vec<CircuitRc>) -> Result<CircuitRc> {
        if self.input_specs.len() != nodes.len() {
            bail!(ConstructError::ModuleWrongNumberChildren {
                expected: self.input_specs.len(),
                got: nodes.len(),
            });
        }
        for (spec, node) in zip(self.input_specs.iter(), nodes) {
            if node.info().rank() < spec.symbol.info().rank() {
                bail!(ExpandError::ModuleRankReduced {
                    node_rank: node.rank(),
                    symbol_rank: spec.symbol.rank(),
                    node_shape: node.shape().clone(),
                    symbol_shape: spec.symbol.shape().clone(),
                    spec_circuit: self.spec_circuit.clone()
                });
            }
            if !spec.batchable && node.info().rank() > spec.symbol.info().rank() {
                bail!(ExpandError::ModuleTriedToBatchUnbatchableInput {
                    node_rank: node.rank(),
                    symbol_rank: spec.symbol.rank(),
                    spec: spec.clone(),
                    spec_circuit: self.spec_circuit.clone()
                });
            }
            if !spec.expandable
                && node.info().shape[node.info().rank() - spec.symbol.info().rank()..]
                    != spec.symbol.info().shape[..]
            {
                bail!(ExpandError::ModuleTriedToExpandUnexpandableInput {
                    node_shape: node.shape().clone(),
                    symbol_shape: spec.symbol.shape().clone(),
                    spec: spec.clone(),
                    spec_circuit: self.spec_circuit.clone()
                });
            }
        }
        replace_expand_bottom_up(self.spec_circuit.clone(), |c| {
            self.input_specs
                .iter()
                .position(|x| x.symbol.info().hash == c.info().hash)
                .map(|i| nodes[i].clone())
        })
    }

    pub fn expand_shape(&self, shapes: &Vec<Shape>) -> Result<CircuitRc> {
        if let Some(result) = MODULE_EXPANSIONS_SHAPE
            .with(|cache| cache.borrow().get(&(self.clone(), shapes.clone())).cloned())
        {
            return Ok(result);
        }
        let symbols = shapes
            .iter()
            .enumerate()
            .map(|(i, s)| {
                Symbol::nrc(
                    s.clone(),
                    ModuleSpec::EXPAND_PLACEHOLDER_UUID,
                    Some(format!("{}_{:?}", i, s)),
                )
            })
            .collect();
        let result = self.expand_raw(&symbols)?;
        MODULE_EXPANSIONS_SHAPE.with(|cache| {
            cache
                .borrow_mut()
                .insert((self.clone(), shapes.clone()), result.clone())
        });
        Ok(result)
    }

    pub fn expand(&self, nodes: &Vec<CircuitRc>, name_prefix: Option<String>) -> Result<CircuitRc> {
        let key: (ModuleSpec, Vec<HashBytes>, Option<String>) = (
            self.clone(),
            nodes.iter().map(|x| x.info().hash).collect(),
            name_prefix.clone(),
        );

        if let Some(result) = MODULE_EXPANSIONS.with(|cache| cache.borrow().get(&key).cloned()) {
            return Ok(result);
        }
        let shapes = nodes.iter().map(|x| x.info().shape.clone()).collect();
        let mut expanded_shape = self.expand_shape(&shapes)?;
        let node_mapping: HashMap<HashBytes, CircuitRc> = nodes
            .iter()
            .enumerate()
            .map(|(i, n)| {
                (
                    Symbol::new(
                        n.info().shape.clone(),
                        ModuleSpec::EXPAND_PLACEHOLDER_UUID,
                        Some(format!("{}_{:?}", i, n.info().shape)),
                    )
                    .info()
                    .hash,
                    n.clone(),
                )
            })
            .collect();
        if let Some(prefix) = &name_prefix {
            expanded_shape = deep_map_unwrap(expanded_shape, |x| {
                if let Some(n) = x.name()  && !node_mapping.contains_key(&x.info().hash){
                    return x.clone().rename(Some(prefix.clone() + n));
                }
                x.clone()
            })
        }
        let result = replace_nodes(expanded_shape, &node_mapping);
        MODULE_EXPANSIONS.with(|cache| cache.borrow_mut().insert(key, result.clone()));
        Ok(result)
    }

    pub fn compute_hash(&self) -> HashBytes {
        let mut hasher = blake3::Hasher::new();
        hasher.update(&self.spec_circuit.info().hash);
        for input_spec in &self.input_specs {
            hasher.update(&[input_spec.batchable as u8, input_spec.expandable as u8]);
            hasher.update(&input_spec.symbol.info().hash);
        }
        hasher.finalize().into()
    }
    pub fn map_circuit<F>(&self, mut f: F, name: Option<Option<String>>) -> Result<Self>
    where
        F: FnMut(CircuitRc) -> Result<CircuitRc>,
    {
        ModuleSpec::new(
            f(self.spec_circuit.clone())?,
            self.input_specs.clone(),
            name.unwrap_or(self.name.clone()),
        )
    }
    pub fn map_circuit_unwrap<F>(&self, mut f: F, name: Option<Option<String>>) -> Self
    where
        F: FnMut(CircuitRc) -> CircuitRc,
    {
        ModuleSpec::new(
            f(self.spec_circuit.clone()),
            self.input_specs.clone(),
            name.unwrap_or(self.name.clone()),
        )
        .unwrap()
    }
    // TODO: add no_check_spec versions as needed!
}
#[pymethods]
impl ModuleSpec {
    #[new]
    fn new(
        spec_circuit: CircuitRc,
        input_specs: Vec<ModuleArgSpec>,
        name: Option<String>,
    ) -> Result<Self> {
        let all_symbols = input_specs.iter().map(|x| x.symbol.crc()).collect();
        let children = all_children(spec_circuit.clone());
        if !children.is_superset(&all_symbols) {
            bail!(ConstructError::ModuleSomeArgsNotPresent {
                spec_circuit,
                missing_symbols: all_symbols
                    .difference(&children)
                    .map(|x| x.as_symbol_unwrap().clone())
                    .collect(),
            })
        }

        Ok(Self {
            spec_circuit,
            input_specs,
            name,
        })
    }

    #[staticmethod]
    fn new_no_check_args(
        spec_circuit: CircuitRc,
        input_specs: Vec<ModuleArgSpec>,
        name: Option<String>,
    ) -> Self {
        Self {
            spec_circuit,
            input_specs,
            name,
        }
    }

    #[pyo3(name = "map_circuit")]
    pub fn map_circuit_py(&self, f: PyObject, name: Option<String>) -> Result<Self> {
        self.map_circuit(|x| pycall!(f, (x,), anyhow), Some(name))
    }

    #[staticmethod]
    pub fn new_auto(circuit: CircuitRc, name: Option<String>) -> Result<Self> {
        let mut input_specs_dict: HashMap<usize, ModuleArgSpec> = HashMap::default();
        let circuit = deep_map_op_context(
            circuit.clone(),
            &|sub: CircuitRc, input_specs_dict: &mut HashMap<usize, ModuleArgSpec>| {
                if let Some(sym) = sub.as_symbol() {
                    static RE_NUM_BEGIN: Lazy<Regex> =
                        Lazy::new(|| Regex::new(r"#(\d+) (.*)").unwrap());
                    let captures = RE_NUM_BEGIN.captures(sym.name().unwrap()).unwrap();
                    let num = captures.get(1).unwrap().as_str().parse::<usize>().unwrap();
                    let name = captures.get(2).unwrap().as_str().to_owned();
                    let newsym = Symbol::new(sym.info().shape.clone(), sym.uuid, Some(name));
                    input_specs_dict.insert(
                        num,
                        ModuleArgSpec {
                            symbol: newsym.clone(),
                            batchable: true,
                            expandable: true,
                        },
                    );
                    return Some(newsym.rc());
                }
                None
            },
            &mut input_specs_dict,
            &mut Default::default(),
        )
        .unwrap_or(circuit);
        let mut input_specs =
            vec![input_specs_dict.values().last().unwrap().clone(); input_specs_dict.len()];
        for (k, v) in input_specs_dict {
            input_specs[k] = v;
        }
        Ok(Self {
            spec_circuit: circuit,
            input_specs,
            name,
        })
    }

    #[staticmethod]
    #[args(require_all_inputs = "false")]
    pub fn new_extract(
        circuit: CircuitRc,
        input_specs: Vec<(CircuitRc, ModuleArgSpec)>,
        name: Option<String>,
        require_all_inputs: bool,
    ) -> Result<Self> {
        let mut new_input_specs: Vec<Option<ModuleArgSpec>> = vec![None; input_specs.len()];
        let spec_circuit = deep_map_op_context_preorder_stoppable(
            circuit.clone(),
            &|circuit,
              c: &mut (
                &mut Vec<Option<ModuleArgSpec>>,
                &Vec<(CircuitRc, ModuleArgSpec)>,
            )| {
                let (real_input_specs, proposed_input_specs) = c;
                if let Some(i) = proposed_input_specs
                    .iter()
                    .position(|x| x.0.info().hash == circuit.info().hash)
                {
                    let mut argspec = proposed_input_specs[i].1.clone();
                    argspec.symbol = Symbol::new(
                        circuit.info().shape.clone(),
                        argspec.symbol.uuid,
                        argspec.symbol.name_cloned().or(circuit.name_cloned()),
                    );
                    real_input_specs[i] = Some(argspec);
                    return (
                        Some(real_input_specs[i].as_ref().unwrap().symbol.crc()),
                        true,
                    );
                }
                (None, false)
            },
            &mut (&mut new_input_specs, &input_specs),
            &mut Default::default(),
        )
        .unwrap_or(circuit);
        let new_input_specs: Vec<ModuleArgSpec> = if require_all_inputs {
            let er = new_input_specs
                .iter()
                .cloned()
                .collect::<Option<Vec<_>>>()
                .ok_or_else(|| ConstructError::ModuleExtractNotPresent {
                    subcirc: input_specs[new_input_specs.iter().position(|x| x.is_none()).unwrap()]
                        .0
                        .clone(),
                });
            er?
        } else {
            new_input_specs
                .into_iter()
                .filter(|z| z.is_some())
                .collect::<Option<Vec<_>>>()
                .unwrap()
        };
        Ok(Self {
            spec_circuit,
            input_specs: new_input_specs,
            name,
        })
    }

    pub fn resize(&self, shapes: Vec<Shape>) -> Result<Self> {
        let input_specs: Vec<ModuleArgSpec> = zip(&self.input_specs, shapes)
            .map(|(spec, shape)| ModuleArgSpec {
                symbol: Symbol::new(shape, spec.symbol.uuid, spec.symbol.name_cloned()),
                batchable: spec.batchable,
                expandable: spec.expandable,
            })
            .collect();
        let spec_circuit = replace_expand_bottom_up(self.spec_circuit.clone(), |c| {
            self.input_specs
                .iter()
                .position(|x| x.symbol.info().hash == c.info().hash)
                .map(|p| input_specs[p].symbol.crc())
        })?;
        Ok(Self {
            spec_circuit,
            input_specs,
            name: self.name.clone(),
        })
    }
}

#[pyclass]
#[derive(Debug, Clone, Hash, PartialEq, Eq)]
pub struct ModuleArgSpec {
    #[pyo3(get)]
    pub symbol: Symbol,
    #[pyo3(get)]
    pub batchable: bool,
    #[pyo3(get)]
    pub expandable: bool,
}
#[pymethods]
impl ModuleArgSpec {
    #[new]
    #[args(batchable = "true", expandable = "true")]
    fn new(symbol: Symbol, batchable: bool, expandable: bool) -> Self {
        Self {
            symbol,
            batchable,
            expandable,
        }
    }
    #[staticmethod]
    #[args(batchable = "true", expandable = "true")]
    pub fn just_name(circuit: CircuitRc, batchable: bool, expandable: bool) -> Self {
        Self {
            symbol: Symbol::new_with_random_uuid(
                circuit.info().shape.clone(),
                circuit.name_cloned(),
            ),
            batchable,
            expandable,
        }
    }
}

#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Module {
    #[pyo3(get)]
    pub nodes: Vec<CircuitRc>,
    #[pyo3(get)]
    pub spec: ModuleSpec,
    info: CachedCircuitInfo,
    #[pyo3(get)]
    name: Option<String>,
}

impl Module {
    #[apply(new_rc_unwrap)]
    pub fn try_new(nodes: Vec<CircuitRc>, spec: ModuleSpec, name: Option<String>) -> Result<Self> {
        let shape = spec
            .expand_shape(&nodes.iter().map(|x| x.info().shape.clone()).collect())
            .context(format!(
                "module node expansion error{}",
                spec.name
                    .as_ref()
                    .map(|s| format!(" ({})", s))
                    .unwrap_or(String::new())
            ))?
            .info()
            .shape
            .clone();
        let mut out = Self {
            nodes,
            spec,
            name: name.clone(),
            info: Default::default(),
        };
        out.info.shape = shape;
        out.name = out.auto_name(name);

        out.init_info()
    }

    pub fn new_kwargs(
        kwargs: &HashMap<String, CircuitRc>,
        spec: ModuleSpec,
        name: Option<String>,
    ) -> Result<Self> {
        let mut nodes: Vec<CircuitRc> = vec![spec.spec_circuit.clone(); spec.input_specs.len()];
        for (k, v) in kwargs {
            match spec
                .input_specs
                .iter()
                .position(|x| x.symbol.name().map(|n| n == k).unwrap_or(false))
            {
                Some(i) => {
                    nodes[i] = v.clone();
                }
                None => {
                    bail!(ConstructError::ModuleUnknownArgument {
                        argument: k.clone(),
                    })
                }
            }
        }
        Self::try_new(nodes, spec, name)
    }
}

circuit_node_extra_impl!(Module);

impl CircuitNode for Module {
    circuit_node_auto_impl!("6825f723-f178-4dab-b568-cd85eb6d2bf3");

    fn compute_shape(&self) -> Shape {
        self.info().shape.clone()
    }

    fn compute_hash(&self) -> blake3::Hasher {
        let mut hasher = blake3::Hasher::new();
        for node in &self.nodes {
            hasher.update(&node.info().hash);
        }
        hasher.update(uuid!("8995f508-a7a5-4025-8d10-e46f55825cd1").as_bytes());
        hasher.update(&self.spec.compute_hash());
        hasher
    }

    fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new(self.nodes.iter().cloned())
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        Self::try_new(
            self.nodes
                .iter()
                .enumerate()
                .map(move |(i, circ)| f(i, circ.clone()))
                .collect::<Result<Vec<_>, _>>()?,
            self.spec.clone(),
            self.name.clone(),
        )
    }

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        vec![] // todo: return child axis map
    }

    fn eval_tensors(
        &self,
        tensors: &[rr_util::py_types::Tensor],
        device_dtype: &TorchDeviceDtype,
    ) -> Result<rr_util::py_types::Tensor> {
        evaluate_fn_dtype_device(
            Module::new(
                tensors
                    .iter()
                    .map(|z| Array::nrc(z.clone(), None))
                    .collect(),
                self.spec.clone(),
                self.name_cloned(),
            )
            .expand(),
            device_dtype.clone().into(),
        )
    }
}

impl CircuitNodeAutoName for Module {
    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            if self.children().any(|x| x.name().is_none()) || self.spec.name.is_none() {
                None
            } else {
                Some(
                    self.spec.name.clone().unwrap()
                        + " "
                        + &self
                            .children()
                            .filter_map(|x| {
                                x.name().map(|y| {
                                    if y.len() > 100 {
                                        "...".to_owned()
                                    } else {
                                        y.to_owned()
                                    }
                                })
                            })
                            .collect::<Vec<String>>()
                            .join(" , "),
                )
            }
        })
    }
}

#[pymethods]
impl Module {
    #[new]
    #[args(spec, name, py_kwargs = "**")]
    fn new_py(
        spec: ModuleSpec,
        name: Option<String>,
        py_kwargs: Option<&PyDict>,
    ) -> PyResult<PyClassInitializer<Module>> {
        let dict: HashMap<String, CircuitRc> = py_kwargs.unwrap().extract().unwrap();
        Ok(Module::new_kwargs(&dict, spec, name)?.into_init())
    }

    #[staticmethod]
    fn new_flat(nodes: Vec<CircuitRc>, spec: ModuleSpec, name: Option<String>) -> Result<Self> {
        Self::try_new(nodes, spec, name)
    }

    pub fn expand(&self) -> CircuitRc {
        self.spec
            .expand(&self.nodes, self.name_cloned().map(|x| x + "."))
            .expect("module expansion fail!") // maybe this is supposed to return error instead of panicking?
    }
}

#[pyfunction]
pub fn inline_all_modules(circuit: CircuitRc) -> CircuitRc {
    deep_map_unwrap(circuit, |c| match &**c {
        Circuit::Module(mn) => inline_all_modules(mn.expand()),
        _ => c.clone(),
    })
}
use std::cell::RefCell;
thread_local! {
    static MODULE_EXPANSIONS: RefCell<HashMap<(ModuleSpec, Vec<HashBytes>,Option<String>), CircuitRc>> =
        RefCell::new(HashMap::default());
    static MODULE_EXPANSIONS_SHAPE: RefCell<HashMap<(ModuleSpec, Vec<Shape>), CircuitRc>> =
        RefCell::new(HashMap::default());
}
