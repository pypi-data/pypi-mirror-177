use std::{fmt::Debug, sync::Arc};

use anyhow::Result;
use macro_rules_attribute::apply;
use pyo3::{exceptions::PyTypeError, prelude::*, PyObject};
use rr_util::python_error_exception;
use thiserror::Error;

use crate::CircuitRc;

#[derive(Debug, Clone)]
pub enum OpaqueIterativeMatcherVal {
    Py(PyObject),
    Dyn(Arc<dyn OpaqueIterativeMatcher + Send + Sync>),
}

impl<'source> FromPyObject<'source> for OpaqueIterativeMatcherVal {
    fn extract(inp: &'source PyAny) -> PyResult<Self> {
        let ty = inp.get_type();
        let name = ty.name()?;
        let expected_name = "IterativeMatcher";
        if name != expected_name {
            return Err(anyhow::Error::from(IncorrectOpaqueTypeError::NameMismatch {
                actual_name: name.to_owned(),
                expected_name: expected_name.to_owned(),
            })
            .into());
        }

        Ok(Self::Py(inp.into()))
    }
}

#[derive(Debug, FromPyObject)]
pub struct OpaqueIterateMatchResults {
    pub updated: Option<OpaqueIterativeMatcherVal>,
    pub finished: bool,
    pub found: bool,
}

pub trait OpaqueIterativeMatcher: Debug {
    fn opaque_match_iterate(&self, circuit: CircuitRc) -> Result<OpaqueIterateMatchResults>;
}

impl OpaqueIterativeMatcher for OpaqueIterativeMatcherVal {
    fn opaque_match_iterate(&self, circuit: CircuitRc) -> Result<OpaqueIterateMatchResults> {
        match self {
            Self::Py(obj) => Python::with_gil(|py| Ok(obj.call1(py, (circuit,))?.extract(py)?)),
            Self::Dyn(d) => d.opaque_match_iterate(circuit),
        }
    }
}

#[derive(Clone, Debug)]
pub struct EndDepthOpaqueIterativeMatcher {
    pub end_depth: usize,
    pub depth: usize,
}

impl OpaqueIterativeMatcher for EndDepthOpaqueIterativeMatcher {
    fn opaque_match_iterate(&self, _: CircuitRc) -> Result<OpaqueIterateMatchResults> {
        let found = self.depth < self.end_depth;
        if self.depth < self.end_depth.saturating_sub(1) {
            Ok(OpaqueIterateMatchResults {
                updated: Some(OpaqueIterativeMatcherVal::Dyn(Arc::new(Self {
                    end_depth: self.end_depth,
                    depth: self.depth + 1,
                }))),
                finished: false,
                found,
            })
        } else {
            Ok(OpaqueIterateMatchResults {
                updated: None,
                finished: true,
                found,
            })
        }
    }
}

impl OpaqueIterativeMatcherVal {
    pub fn for_end_depth(end_depth: usize) -> Self {
        Self::Dyn(Arc::new(EndDepthOpaqueIterativeMatcher {
            end_depth,
            depth: 0,
        }))
    }
}

#[apply(python_error_exception)]
#[base_error_name(IncorrectOpaqueType)]
#[base_exception(PyTypeError)]
#[derive(Error, Debug, Clone)]
pub enum IncorrectOpaqueTypeError {
    #[error("expected={expected_name} actual={actual_name}")]
    NameMismatch {
        actual_name: String,
        expected_name: String,
    },
}
