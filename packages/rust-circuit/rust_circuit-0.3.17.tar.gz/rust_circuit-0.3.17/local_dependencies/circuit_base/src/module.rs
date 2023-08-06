use std::iter::zip;

use anyhow::{bail, Context, Result};
use macro_rules_attribute::apply;
use pyo3::prelude::*;
use rr_util::{
    pycall,
    tensor_util::{Shape, TorchDeviceDtype},
    util::{counts_g_1, is_unique},
};
use rustc_hash::FxHashMap as HashMap;
use uuid::{uuid, Uuid};

use crate::{
    all_children, circuit_node_auto_impl, circuit_node_extra_impl,
    circuit_node_private::{CircuitNodeHashItems, CircuitNodePrivate, CircuitNodeSetNonHashInfo},
    circuit_utils::OperatorPriority,
    deep_map, deep_map_op_context_preorder_stoppable, deep_map_unwrap,
    expand_node::{replace_expand_bottom_up, ExpandError},
    new_rc_unwrap,
    prelude::*,
    visit_circuit_unwrap, CachedCircuitInfo, HashBytes, PyCircuitBase, Symbol, TensorEvalError,
};

/// can also be thought of as lambda from lambda calculus (expression with free variables + list of these variables)
#[pyclass]
#[derive(Debug, Clone, Hash, PartialEq, Eq)]
pub struct ModuleSpec {
    #[pyo3(get)]
    pub circuit: CircuitRc,
    #[pyo3(get)]
    pub arg_specs: Vec<ModuleArgSpec>,
}

impl ModuleSpec {
    pub const EXPAND_PLACEHOLDER_UUID: Uuid = uuid!("741ba404-eec3-4ac9-b6ce-062e903fb033");
    pub fn expand_raw(&self, nodes: &Vec<CircuitRc>) -> Result<CircuitRc> {
        if self.arg_specs.len() != nodes.len() {
            bail!(ConstructError::ModuleWrongNumberChildren {
                expected: self.arg_specs.len(),
                got: nodes.len(),
                arg_specs: self.arg_specs.clone(),
                nodes: nodes.clone(),
            });
        }
        for (arg_spec, node) in zip(self.arg_specs.iter(), nodes) {
            if node.info().rank() < arg_spec.symbol.info().rank() {
                bail!(ExpandError::ModuleRankReduced {
                    node_rank: node.rank(),
                    symbol_rank: arg_spec.symbol.rank(),
                    arg_spec: arg_spec.clone(),
                    node_shape: node.shape().clone(),
                    spec_circuit: self.circuit.clone()
                });
            }
            if !arg_spec.batchable && node.info().rank() > arg_spec.symbol.info().rank() {
                bail!(ExpandError::ModuleTriedToBatchUnbatchableInput {
                    node_rank: node.rank(),
                    symbol_rank: arg_spec.symbol.rank(),
                    arg_spec: arg_spec.clone(),
                    spec_circuit: self.circuit.clone()
                });
            }
            if !arg_spec.expandable
                && node.info().shape[node.info().rank() - arg_spec.symbol.info().rank()..]
                    != arg_spec.symbol.info().shape[..]
            {
                bail!(ExpandError::ModuleTriedToExpandUnexpandableInput {
                    node_shape: node.shape().clone(),
                    symbol_shape: arg_spec.symbol.shape().clone(),
                    arg_spec: arg_spec.clone(),
                    spec_circuit: self.circuit.clone()
                });
            }
        }
        replace_expand_bottom_up(self.circuit.clone(), |c| {
            self.arg_specs
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

    pub fn substitute(
        &self,
        nodes: &Vec<CircuitRc>,
        name_prefix: Option<String>,
        name_suffix: Option<String>,
    ) -> Result<CircuitRc> {
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
        if name_prefix.is_some() || name_suffix.is_some() {
            expanded_shape = deep_map_unwrap(expanded_shape, |x| {
                if let Some(n) = x.name() {
                    if !node_mapping.contains_key(&x.info().hash) {
                        return x.clone().rename(Some(
                            name_prefix.clone().unwrap_or_else(|| "".to_owned())
                                + n
                                + name_suffix.as_ref().map(|x| -> &str { x }).unwrap_or(""),
                        ));
                    }
                }
                x.clone()
            })
        }
        // we're replacing leaves so no need to do anything with stoppable preorder
        let result = deep_map(expanded_shape, |circ| {
            Ok(node_mapping.get(&circ.info().hash).cloned().unwrap_or(circ))
        })
        .with_context(|| {
            format!(
                concat!(
                    "replacing symbols with nodes (which are not necessarily symbols)",
                    " failed in ModuleSpec substitute\n",
                    "(perhaps you replaced the input symbols to a nested module?)\n",
                    "module_spec={:?}\nnodes={:?}"
                ),
                self, nodes
            )
        })?;
        MODULE_EXPANSIONS.with(|cache| cache.borrow_mut().insert(key, result.clone()));
        Ok(result)
    }

    pub fn compute_non_children_hash(&self, hasher: &mut blake3::Hasher) {
        for arg_spec in &self.arg_specs {
            // this is fine because each item is fixed size and we delimit with node hashs (which are uu)
            hasher.update(&[arg_spec.batchable as u8, arg_spec.expandable as u8]);
        }
    }

    pub fn map_circuit<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(CircuitRc) -> Result<CircuitRc>,
    {
        ModuleSpec::new(f(self.circuit.clone())?, self.arg_specs.clone(), false)
    }
    pub fn map_circuit_unwrap<F>(&self, mut f: F) -> Self
    where
        F: FnMut(CircuitRc) -> CircuitRc,
    {
        ModuleSpec::new(f(self.circuit.clone()), self.arg_specs.clone(), false).unwrap()
    }
    // TODO: add no_check_spec versions as needed!
}

#[pyfunction]
pub fn all_free(circuit: CircuitRc) -> Vec<Symbol> {
    let mut all_syms = Vec::new();
    visit_circuit_unwrap(inline_all_modules(circuit), |x| {
        if let Some(sym) = x.as_symbol() {
            all_syms.push(sym.clone())
        }
    });
    all_syms.sort();
    all_syms
}

#[pymethods]
impl ModuleSpec {
    #[new]
    #[args(check_unique_arg_names = "true")]
    pub fn new(
        circuit: CircuitRc,
        arg_specs: Vec<ModuleArgSpec>,
        check_unique_arg_names: bool,
    ) -> Result<Self> {
        let all_symbols = arg_specs.iter().map(|x| x.symbol.crc()).collect();
        let children = all_children(circuit.clone());
        if !children.is_superset(&all_symbols) {
            bail!(ConstructError::ModuleSomeArgsNotPresent {
                spec_circuit: circuit,
                missing_symbols: all_symbols
                    .difference(&children)
                    .map(|x| x.as_symbol_unwrap().clone())
                    .collect(),
            })
        }

        let out = Self { circuit, arg_specs };
        if check_unique_arg_names {
            out.check_unique_arg_names()?;
        }
        Ok(out)
    }

    #[staticmethod]
    fn new_no_check_args(circuit: CircuitRc, arg_specs: Vec<ModuleArgSpec>) -> Self {
        Self { circuit, arg_specs }
    }

    fn check_unique_arg_names(&self) -> Result<()> {
        // TODO: maybe cache me (as needed)!
        if self.arg_specs.iter().any(|x| x.symbol.name().is_none()) {
            bail!(ConstructError::ModuleSomeArgsNamedNone {
                symbols_named_none: self
                    .arg_specs
                    .iter()
                    .filter_map(|x| x.symbol.name().is_none().then(|| x.symbol.clone()))
                    .collect()
            })
        }
        let names: Vec<_> = self
            .arg_specs
            .iter()
            .map(|x| x.symbol.name().unwrap())
            .collect();
        if !is_unique(&names) {
            bail!(ConstructError::ModuleArgsDupNames {
                dup_names: counts_g_1(names.into_iter().map(|x| x.to_owned()))
            })
        }

        Ok(())
    }

    #[pyo3(name = "map_circuit")]
    pub fn map_circuit_py(&self, f: PyObject) -> Result<Self> {
        self.map_circuit(|x| pycall!(f, (x,), anyhow))
    }

    #[staticmethod]
    #[args(check_unique_arg_names = "true")]
    pub fn new_all_free(circuit: CircuitRc, check_unique_arg_names: bool) -> Result<Self> {
        let arg_specs = all_free(circuit.clone())
            .into_iter()
            .map(|x| ModuleArgSpec::new(x, true, true))
            .collect();
        let out = Self::new(circuit, arg_specs, false).expect("method should guarantee valid");
        if check_unique_arg_names {
            // check after instead of in new so we can .expect on other errors in new
            out.check_unique_arg_names()?;
        }
        // maybe we should use no_check_args for speed
        Ok(out)
    }

    #[staticmethod]
    #[args(require_all_args = "true", check_unique_arg_names = "true")]
    pub fn new_extract(
        circuit: CircuitRc,
        arg_specs: Vec<(CircuitRc, ModuleArgSpec)>,
        require_all_args: bool,
        check_unique_arg_names: bool,
    ) -> Result<Self> {
        let mut new_arg_specs: Vec<Option<ModuleArgSpec>> = vec![None; arg_specs.len()];
        let spec_circuit = deep_map_op_context_preorder_stoppable(
            circuit.clone(),
            &|circuit,
              c: &mut (
                &mut Vec<Option<ModuleArgSpec>>,
                &Vec<(CircuitRc, ModuleArgSpec)>,
            )| {
                let (real_arg_specs, proposed_arg_specs) = c;
                if let Some(i) = proposed_arg_specs
                    .iter()
                    .position(|x| x.0.info().hash == circuit.info().hash)
                {
                    let mut arg_spec = proposed_arg_specs[i].1.clone();
                    arg_spec.symbol = Symbol::new(
                        circuit.info().shape.clone(),
                        arg_spec.symbol.uuid,
                        arg_spec.symbol.name_cloned().or(circuit.name_cloned()),
                    );
                    real_arg_specs[i] = Some(arg_spec);
                    return (Some(real_arg_specs[i].as_ref().unwrap().symbol.crc()), true);
                }
                (None, false)
            },
            &mut (&mut new_arg_specs, &arg_specs),
            &mut Default::default(),
        )
        .unwrap_or(circuit);
        let new_arg_specs: Vec<ModuleArgSpec> = if require_all_args {
            let er = new_arg_specs
                .iter()
                .cloned()
                .collect::<Option<Vec<_>>>()
                .ok_or_else(|| ConstructError::ModuleExtractNotPresent {
                    subcirc: arg_specs[new_arg_specs.iter().position(|x| x.is_none()).unwrap()]
                        .0
                        .clone(),
                });
            er?
        } else {
            new_arg_specs
                .into_iter()
                .filter(|z| z.is_some())
                .collect::<Option<Vec<_>>>()
                .unwrap()
        };
        // maybe we should use no_check_args for speed
        let out =
            Self::new(spec_circuit, new_arg_specs, false).expect("method should guarantee valid");
        if check_unique_arg_names {
            // check after instead of in new so we can .expect on other errors in new
            out.check_unique_arg_names()?;
        }
        Ok(out)
    }

    // TODO: add some naming options maybe
    pub fn resize(&self, shapes: Vec<Shape>) -> Result<Self> {
        let arg_specs: Vec<ModuleArgSpec> = zip(&self.arg_specs, shapes)
            .map(|(arg_spec, shape)| ModuleArgSpec {
                symbol: Symbol::new(shape, arg_spec.symbol.uuid, arg_spec.symbol.name_cloned()),
                batchable: arg_spec.batchable,
                expandable: arg_spec.expandable,
            })
            .collect();

        let circuit = self
            .substitute(
                &arg_specs.iter().map(|x| x.symbol.crc()).collect(),
                None,
                None,
            )
            .context("substitute failed from resize")?;
        Ok(Self::new(circuit, arg_specs, false).expect("method should guarantee valid"))
    }

    pub fn __repr__(&self) -> String {
        format!("{:?}", self)
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

impl Default for ModuleArgSpec {
    fn default() -> Self {
        Self {
            symbol: Symbol::new_with_none_uuid([].into_iter().collect(), None),
            batchable: true,
            expandable: true,
        }
    }
}

#[pymethods]
impl ModuleArgSpec {
    #[new]
    #[args(
        batchable = "Self::default().batchable",
        expandable = "Self::default().expandable"
    )]
    fn new(symbol: Symbol, batchable: bool, expandable: bool) -> Self {
        Self {
            symbol,
            batchable,
            expandable,
        }
    }
    #[staticmethod]
    #[args(
        batchable = "Self::default().batchable",
        expandable = "Self::default().expandable"
    )]
    pub fn just_name_shape(circuit: CircuitRc, batchable: bool, expandable: bool) -> Self {
        Self {
            symbol: Symbol::new_with_random_uuid(
                circuit.info().shape.clone(),
                circuit.name_cloned(),
            ),
            batchable,
            expandable,
        }
    }

    pub fn __repr__(&self) -> String {
        format!("{:?}", self)
    }
}

/// can also be thought of as a lambda + it's arguments in lambda calculus (but not yet beta reduced)
/// aka call site
#[pyclass(extends=PyCircuitBase)]
#[derive(Clone)]
pub struct Module {
    #[pyo3(get)]
    pub nodes: Vec<CircuitRc>,
    #[pyo3(get)]
    pub spec: ModuleSpec,
    cached_substituted: CircuitRc,
    info: CachedCircuitInfo,
    #[pyo3(get)]
    name: Option<String>,
}

impl Module {
    #[apply(new_rc_unwrap)]
    pub fn try_new(nodes: Vec<CircuitRc>, spec: ModuleSpec, name: Option<String>) -> Result<Self> {
        let cached_substituted = spec
            .substitute(&nodes, None, None)
            .with_context(|| format!("module construction failed on expand name={:?}", name))?;

        let mut out = Self {
            nodes,
            spec,
            cached_substituted,
            name: name.clone(),
            info: Default::default(),
        };
        out.name = out.auto_name(name);
        out.init_info()
    }

    pub fn new_kwargs(
        kwargs: &HashMap<String, CircuitRc>,
        spec: ModuleSpec,
        name: Option<String>,
    ) -> Result<Self> {
        let mut nodes: Vec<_> = vec![None; spec.arg_specs.len()];
        spec.check_unique_arg_names()?;
        for (k, v) in kwargs {
            match spec
                .arg_specs
                .iter()
                .position(|x| x.symbol.name().expect("check_unique_arg_names above") == k)
            {
                Some(i) => {
                    nodes[i] = Some(v.clone());
                }
                None => {
                    bail!(ConstructError::ModuleUnknownArgument {
                        argument: k.clone(),
                        all_module_inputs: spec
                            .arg_specs
                            .iter()
                            .map(|x| x.symbol.name_cloned().unwrap())
                            .collect()
                    })
                }
            }
        }
        if nodes.iter().any(|x| x.is_none()) {
            bail!(ConstructError::ModuleMissingNames {
                missing_arguments: nodes
                    .iter()
                    .zip(spec.arg_specs)
                    .filter_map(|(n, arg_spec)| n.is_none().then(|| arg_spec
                        .symbol
                        .name_cloned()
                        .expect("check_unique_arg_names above")))
                    .collect()
            });
        }

        Self::try_new(nodes.into_iter().map(Option::unwrap).collect(), spec, name)
    }
}

circuit_node_extra_impl!(Module, self_hash_default);

impl CircuitNodeHashItems for Module {
    fn compute_hash_non_name_non_children(&self, hasher: &mut blake3::Hasher) {
        self.spec.compute_non_children_hash(hasher)
    }
}

impl CircuitNodeSetNonHashInfo for Module {
    fn set_non_hash_info(&mut self) -> Result<()> {
        *self.info_mut() = self.cached_substituted.info().clone();
        Ok(())
    }
}

impl CircuitNode for Module {
    circuit_node_auto_impl!("6825f723-f178-4dab-b568-cd85eb6d2bf3");

    fn child_axis_map(&self) -> Vec<Vec<Option<usize>>> {
        // TODO: this can be done by first stripping named axes and then
        // propagating named axes up from symbols in spec circuit
        unimplemented!();
    }

    fn children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new(
            std::iter::once(self.spec.circuit.clone()).chain(
                self.spec
                    .arg_specs
                    .iter()
                    // zip so we get the right ordering (same as map_children_enumerate)
                    .zip(self.nodes.iter().cloned())
                    .flat_map(|(arg_spec, n)| [arg_spec.symbol.crc(), n]),
            ),
        )
    }

    fn non_free_children(&self) -> Box<dyn Iterator<Item = CircuitRc> + '_> {
        Box::new(self.nodes.iter().cloned())
    }

    fn map_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        let new_spec_circ = f(0, self.spec.circuit.clone())?;

        assert_eq!(
            self.spec.arg_specs.len(),
            self.nodes.len(),
            "guaranteed by constructor via expand"
        );

        // map both symbols and nodes
        let out = self
            .spec
            .arg_specs
            .clone()
            .into_iter()
            .zip(&self.nodes)
            .enumerate()
            .map(|(i, (arg_spec, node))| {
                let maybe_new_sym = f(2 * i + 1, arg_spec.symbol.rc())?;
                let symbol = maybe_new_sym.as_symbol().cloned().ok_or_else(|| {
                    ConstructError::ModuleExpectedSymbolOnMap {
                        orig_module: self.clone(),
                        got_instead_of_symbol: maybe_new_sym,
                    }
                })?;
                let new_arg = ModuleArgSpec { symbol, ..arg_spec };
                let new_node = f(2 * i + 2, node.clone())?;
                Ok((new_arg, new_node))
            })
            .collect::<Result<Vec<_>>>()?;

        let (arg_specs, nodes) = out.into_iter().unzip();

        Self::try_new(
            nodes,
            ModuleSpec::new(new_spec_circ, arg_specs, false)?,
            self.name.clone(),
        )
    }

    fn map_non_free_children_enumerate<F>(&self, mut f: F) -> Result<Self>
    where
        F: FnMut(usize, CircuitRc) -> Result<CircuitRc>,
    {
        let nodes = self
            .nodes
            .iter()
            .cloned()
            .enumerate()
            .map(|(i, x)| f(i, x))
            .collect::<Result<_>>()?;
        Self::try_new(nodes, self.spec.clone(), self.name_cloned())
    }

    fn eval_tensors(
        &self,
        _tensors: &[rr_util::py_types::Tensor],
        _device_dtype: &TorchDeviceDtype,
    ) -> Result<rr_util::py_types::Tensor> {
        bail!(TensorEvalError::ModulesCantBeDirectlyEvalutedInternal {
            module: self.clone(),
        })
    }
}

impl CircuitNodeAutoName for Module {
    const PRIORITY: OperatorPriority = OperatorPriority::Function {};

    fn auto_name(&self, name: Option<String>) -> Option<String> {
        name.or_else(|| {
            if self.children().any(|x| x.name().is_none()) {
                None
            } else {
                Some(
                    self.spec.circuit.name_cloned().unwrap()
                        + "("
                        + &self
                            .nodes
                            .iter()
                            .map(|node| node.name_cloned().unwrap())
                            .collect::<Vec<String>>()
                            .join(", ")
                        + ")",
                )
            }
        })
    }
}

#[pymethods]
impl Module {
    #[new]
    #[args(name = "None", kwargs = "**")]
    fn new_py(
        spec: ModuleSpec,
        name: Option<String>,
        kwargs: Option<HashMap<String, CircuitRc>>,
    ) -> PyResult<PyClassInitializer<Module>> {
        Ok(Module::new_kwargs(&kwargs.unwrap_or_else(HashMap::default), spec, name)?.into_init())
    }

    #[staticmethod]
    fn new_flat(nodes: Vec<CircuitRc>, spec: ModuleSpec, name: Option<String>) -> Result<Self> {
        Self::try_new(nodes, spec, name)
    }

    /// TODO: fancier renaming technology?
    #[pyo3(name = "substitute")]
    #[args(
        name_prefix = "None",
        name_suffix = "None",
        use_self_name_as_prefix = "false"
    )]
    pub fn substitute_py(
        &self,
        name_prefix: Option<String>,
        name_suffix: Option<String>,
        use_self_name_as_prefix: bool,
    ) -> Result<CircuitRc> {
        let name_prefix = if use_self_name_as_prefix {
            if let Some(name_prefix) = name_prefix {
                bail!(
                    ConstructError::ModulePassedNamePrefixAndUseSelfNameAsPrefix {
                        name_prefix,
                        module: self.clone()
                    }
                )
            }

            self.name_cloned().map(|x| x + ".")
        } else {
            name_prefix
        };
        Ok(self.substitute(name_prefix, name_suffix))
    }

    // TODO: add some naming options maybe
    pub fn conform_to_input_shapes(&self) -> Self {
        Self::new(
            self.nodes.clone(),
            self.spec
                .resize(self.nodes.iter().map(|x| x.shape().clone()).collect())
                .expect("constructor should ensure this works"),
            self.name_cloned(),
        )
    }
}

impl Module {
    pub fn substitute_self_name_prefix(&self) -> CircuitRc {
        self.substitute(self.name_cloned().map(|x| x + "."), None)
    }

    pub fn substitute(
        &self,
        name_prefix: Option<String>,
        name_suffix: Option<String>,
    ) -> CircuitRc {
        self.spec
            .substitute(&self.nodes, name_prefix, name_suffix)
            .map(|x| x.rename(self.name_cloned()))
            .expect("constructor should ensure this works")
    }
}

#[pyfunction]
pub fn inline_all_modules(circuit: CircuitRc) -> CircuitRc {
    deep_map_unwrap(circuit, |c| match &**c {
        Circuit::Module(mn) => mn.substitute(None, None),
        _ => c.clone(),
    })
}

#[pyfunction]
pub fn conform_all_modules(circuit: CircuitRc) -> CircuitRc {
    deep_map_unwrap(circuit, |c| match &**c {
        Circuit::Module(mn) => mn.conform_to_input_shapes().rc(),
        _ => c.clone(),
    })
}

use std::cell::RefCell;
// TODO: maybe cache check_unique_arg_names here?
thread_local! {
    static MODULE_EXPANSIONS: RefCell<HashMap<(ModuleSpec, Vec<HashBytes>, Option<String>), CircuitRc>> =
        RefCell::new(HashMap::default());
    static MODULE_EXPANSIONS_SHAPE: RefCell<HashMap<(ModuleSpec, Vec<Shape>), CircuitRc>> =
        RefCell::new(HashMap::default());
}
