use anyhow::Result;
use circuit_base::{prelude::*, CircuitType, Index};
use circuit_rewrites::algebraic_rewrite::{index_elim_identity, push_down_index_raw};
use get_update_node::{IterativeMatcher, IterativeMatcherRc, Matcher};
use macro_rules_attribute::apply;
use pyo3::prelude::*;
use rr_util::{cached_lambda, util::HashBytes};

#[pyfunction]
pub fn default_index_traversal() -> IterativeMatcherRc {
    IterativeMatcher::noop_traversal()
        .filter(
            false,
            None,
            None,
            Matcher::types(vec![CircuitType::Index, CircuitType::Array]).rc(),
        )
        .rc()
}

#[pyfunction(
    traversal = "default_index_traversal()",
    suffix = "None",
    allow_partial_pushdown = "false",
    elim_identity = "true"
)]
pub fn push_down_index(
    index: Index,
    traversal: IterativeMatcherRc,
    suffix: Option<String>,
    allow_partial_pushdown: bool,
    elim_identity: bool,
) -> Result<CircuitRc> {
    #[apply(cached_lambda)]
    #[key((index.info().hash, matcher.clone()), (HashBytes, IterativeMatcherRc))]
    #[use_try]
    fn push_down_rec(index: Index, matcher: IterativeMatcherRc) -> Result<CircuitRc> {
        if elim_identity {
            if let Some(removed_node) = index_elim_identity(&index) {
                return Ok(removed_node);
            }
        }
        let new_matcher = if let (Some(new_matcher), _) = matcher
            .match_iterate(index.node.clone())?
            .none_if_finished(matcher)
        {
            new_matcher
        } else {
            return Ok(index.rc());
        };

        push_down_index_raw(
            &index,
            allow_partial_pushdown,
            |new_index| push_down_rec(new_index, new_matcher.clone()),
            suffix.clone(),
        )
    }

    push_down_rec(index, traversal)
}
