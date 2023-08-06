#![feature(let_chains)]
//! Basic TODO: add more rust helpers + builders as needed!

pub mod iterative_matcher;
pub mod library;
pub mod matcher;
pub mod operations;
pub mod sample_transform;
pub mod transform;

pub use iterative_matcher::{
    IterateMatchResults, IterativeMatcher, IterativeMatcherData, IterativeMatcherRc,
};
pub use matcher::{Matcher, MatcherData, MatcherFromPy, MatcherFromPyBase, MatcherRc};
pub use operations::{Batcher, BoundGetter, BoundUpdater, Getter, Updater};
pub use transform::{Transform, TransformData, TransformRc};
