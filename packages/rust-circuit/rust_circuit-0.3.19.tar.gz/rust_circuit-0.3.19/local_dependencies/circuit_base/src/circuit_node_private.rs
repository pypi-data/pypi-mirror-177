// ! CircuitNodeInit and various helpers for nicely implementing it
use std::{collections::BTreeMap, iter::zip};

use num_bigint::BigUint;
use rr_util::{
    symbolic_size::{SymbolicSizeConstraint, SymbolicSizeConstraints},
    tensor_util::{Shape, TorchDeviceDtypeOp},
};
use uuid::uuid;

use crate::{CachedCircuitInfo, CircuitNode, ConstructError, NamedAxes, Result};

pub trait CircuitNodeInit {
    fn init_info_impl(self) -> Result<Self>
    where
        Self: Sized;

    fn rename_impl(self, new_name: Option<String>) -> Self
    where
        Self: Sized;

    fn update_info_impl<F>(self, f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnOnce(&mut CachedCircuitInfo);
}

pub trait CircuitNodePrivate {
    fn info_mut(&mut self) -> &mut CachedCircuitInfo;
    fn name_mut(&mut self) -> &mut Option<String>;
}

pub trait CircuitNodeComputeInfoImpl: CircuitNode {
    fn compute_shape(&self) -> Shape;
    fn compute_is_constant(&self) -> bool {
        self.children().all(|c| c.info().is_constant)
    }
    fn compute_is_explicitly_computable(&self) -> bool {
        self.children().all(|c| c.info().is_explicitly_computable)
    }
    fn compute_can_be_sampled(&self) -> bool {
        self.children().all(|c| c.info().can_be_sampled)
    }
    fn device_dtype_extra(&self) -> Box<dyn Iterator<Item = TorchDeviceDtypeOp> + '_> {
        Box::new(std::iter::empty())
    }
    fn symbolic_size_constraints_extra(&self) -> Result<Vec<SymbolicSizeConstraint>> {
        Ok(Vec::new())
    }

    fn compute_device_dtype(&self) -> Result<TorchDeviceDtypeOp> {
        self.children()
            .map(|c| c.info().device_dtype.clone())
            .chain(self.device_dtype_extra())
            .fold(Ok(TorchDeviceDtypeOp::NONE), |acc, new| {
                acc.map(|old| TorchDeviceDtypeOp::combine(old, new))?
            })
    }

    fn compute_symbolic_size_constraints(&self) -> Result<SymbolicSizeConstraints> {
        SymbolicSizeConstraints::new(
            self.children()
                .flat_map(|c| {
                    c.info()
                        .symbolic_size_constraints
                        .clone()
                        .into_constraints()
                })
                .chain(self.symbolic_size_constraints_extra()?)
                .collect(),
        )
    }

    fn compute_max_non_leaf_size(&self) -> BigUint {
        self.children()
            .map(|x| x.info().max_non_leaf_size.clone())
            .chain(std::iter::once(self.info().numel()))
            .max()
            .unwrap()
    }

    fn compute_named_axes(&self) -> NamedAxes {
        if let Some(out) = self.already_set_named_axes() {
            return out;
        }
        if !self.children().any(|x| !x.info().named_axes.is_empty()) {
            return BTreeMap::new();
        }
        let child_axis_map = self.child_axis_map();
        let mut result: NamedAxes = BTreeMap::new();
        for (mp, child) in zip(child_axis_map, self.children()) {
            for (ax, name) in &child.info().named_axes {
                if let Some(top_ax) = mp[(*ax) as usize] {
                    result.insert(top_ax as u8, name.clone());
                }
            }
        }
        result
    }
}

pub trait CircuitNodeSetNonHashInfo: CircuitNodePrivate {
    fn set_non_hash_info(&mut self) -> Result<()>;
}

impl<T: CircuitNodeComputeInfoImpl + CircuitNodePrivate> CircuitNodeSetNonHashInfo for T {
    fn set_non_hash_info(&mut self) -> Result<()> {
        self.info_mut().shape = self.compute_shape(); // set shape so methods to compute other self.info_mut() can use it
        self.info_mut().is_constant = self.compute_is_constant();
        self.info_mut().is_explicitly_computable = self.compute_is_explicitly_computable();
        self.info_mut().can_be_sampled = self.compute_can_be_sampled();
        self.info_mut().max_non_leaf_size = self.compute_max_non_leaf_size();
        self.info_mut().device_dtype = self.compute_device_dtype()?;
        self.info_mut().symbolic_size_constraints = self.compute_symbolic_size_constraints()?;
        self.info_mut().named_axes = self.compute_named_axes();
        Ok(())
    }
}

pub trait CircuitNodeHashItems {
    fn compute_hash_non_name_non_children(&self, _hasher: &mut blake3::Hasher) {}
}

pub trait CircuitNodeHashWithChildren {
    fn compute_hash_non_name(&self, hasher: &mut blake3::Hasher);
}

impl<T: CircuitNodeHashItems + CircuitNode> CircuitNodeHashWithChildren for T {
    fn compute_hash_non_name(&self, hasher: &mut blake3::Hasher) {
        self.compute_hash_non_name_non_children(hasher);
        for child in self.children() {
            hasher.update(&child.info().hash);
        }
    }
}

impl<T> CircuitNodeInit for T
where
    T: CircuitNodeHashWithChildren + CircuitNodePrivate + CircuitNodeSetNonHashInfo + CircuitNode,
{
    fn init_info_impl(mut self) -> Result<Self>
    where
        Self: Sized,
    {
        let mut hasher = blake3::Hasher::new();
        self.compute_hash_non_name(&mut hasher);
        hasher.update(&self.node_type_uuid());
        hasher.update(self.name().unwrap_or("").as_bytes());
        hasher.update(uuid!("025e9af4-1366-4211-aa5f-7c28fc6cdf9f").as_bytes()); // delimit name with uuid

        let already_set_named_axes = self.already_set_named_axes(); // have named axes already been set?
        self.set_non_hash_info()?;
        if let Some(already_set_named_axes) = already_set_named_axes {
            self.info_mut().named_axes = already_set_named_axes; // if already set, keep these named axes
        }

        for (axis, name) in &self.info().named_axes {
            if *axis as usize >= self.info().shape.len() {
                return Err(ConstructError::NamedAxisAboveRank {}.into());
            }
            hasher.update(&[*axis]);
            hasher.update(name.as_bytes());
            // delimit axis names with uuid
            hasher.update(uuid!("db6b1967-35f7-4571-a69c-82ba3340215d").as_bytes());
        }

        self.info_mut().hash = hasher.finalize().into();
        Ok(self)
    }

    fn rename_impl(mut self, new_name: Option<String>) -> Self
    where
        Self: Sized,
    {
        *self.name_mut() = new_name;
        self.init_info_impl().unwrap() // we could avoid recomputing some stuff if we wanted
    }

    fn update_info_impl<F>(mut self, f: F) -> Result<Self>
    where
        Self: Sized,
        F: FnOnce(&mut CachedCircuitInfo),
    {
        f(self.info_mut());
        self.init_info_impl()
    }
}
