use anyhow::{bail, Context, Result};
use circuit_base::{prelude::*, Einsum};
use circuit_rewrites::algebraic_rewrite::{distribute_once_raw, DistributeError};
use get_update_node::{
    iterative_matcher::require_single, IterativeMatcher, IterativeMatcherRc, MatcherData,
};
use macro_rules_attribute::apply;
use pyo3::prelude::*;
use rr_util::{cached_lambda, util::HashBytes};

#[pyfunction]
pub fn traverse_until_depth(depth: Option<u32>) -> IterativeMatcherRc {
    IterativeMatcher::noop_traversal()
        .filter(
            false,
            None,
            depth.map(|i| i + 1),
            MatcherData::Always(false).into(),
        )
        .rc()
}

#[pyfunction(
    traversal = "traverse_until_depth(Some(1))",
    suffix = "None",
    allow_partial_distribute = "true",
    do_broadcasts = "true"
)]
pub fn distribute(
    einsum: Einsum,
    operand_idx: usize,
    traversal: Option<IterativeMatcherRc>,
    suffix: Option<String>,
    allow_partial_distribute: bool, // noop if can't distribute
    do_broadcasts: bool,
) -> Result<CircuitRc> {
    #[apply(cached_lambda)]
    #[key((einsum.info().hash, matcher.clone()), (HashBytes, IterativeMatcherRc))]
    #[use_try]
    fn distribute_rec(einsum: Einsum, matcher: IterativeMatcherRc) -> Result<CircuitRc> {
        if operand_idx >= einsum.args.len() {
            if allow_partial_distribute {
                return Ok(einsum.rc());
            } else {
                bail!(DistributeError::OperandIdxTooLarge {
                    einsum: einsum.clone(),
                    operand_idx,
                })
            };
        }
        let updated = matcher
            .match_iterate(einsum.args[operand_idx].0.clone())?
            .unwrap_or_same(matcher)
            .0;
        let new_matcher = if let Some(new_matcher) = require_single(updated)
            .context("distribute doesn't support matcher per child")?
            .0
        {
            new_matcher
        } else {
            return Ok(einsum.rc());
        };

        let distributed = distribute_once_raw(
            &einsum,
            operand_idx,
            do_broadcasts,
            suffix.clone(),
            |new_einsum| distribute_rec(new_einsum, new_matcher.clone()),
        );
        if distributed.is_err() && allow_partial_distribute {
            return Ok(einsum.clone().rc());
        }
        Ok(distributed?.rc())
    }

    let result = distribute_rec(
        einsum.clone(),
        traversal.unwrap_or(traverse_until_depth(Some(1))),
    );
    if let Ok(result_some)=&result && result_some.info().hash==einsum.info().hash{
        bail!(DistributeError::Noop { einsum, operand_idx })
    }
    result
}
