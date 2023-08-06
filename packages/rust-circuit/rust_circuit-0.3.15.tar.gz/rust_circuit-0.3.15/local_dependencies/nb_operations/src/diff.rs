use std::iter::zip;

use anyhow::Result;
use circuit_base::{
    print::{color, PrintOptions},
    CircuitNode, CircuitNodeSelfOnlyHash, CircuitRc,
};
use pyo3::prelude::*;
use rr_util::util::{indent, HashBytes};
use uuid::uuid;

#[pyfunction(hash_child_count = "true", hash_child_shapes = "false")]
pub fn compute_self_hash(
    circuit: CircuitRc,
    hash_child_count: bool,
    hash_child_shapes: bool,
) -> HashBytes {
    let mut m = blake3::Hasher::new();
    for l in &circuit.info().shape {
        m.update(&l.to_le_bytes());
    }
    m.update(uuid!("6261daa8-0085-46f7-9f38-b085601fa628").as_bytes());
    if hash_child_count {
        m.update(&circuit.children().count().to_le_bytes());
    }
    m.update(uuid!("c7034aef-2179-4afa-9b90-c9abfcd1405d").as_bytes());
    if hash_child_shapes {
        for x in circuit.children() {
            for l in x.shape() {
                m.update(&l.to_le_bytes());
            }
            m.update(uuid!("17519b66-2332-450e-bdb2-bf893f8ed699").as_bytes());
        }
    }
    m.update(uuid!("e95b4d23-0077-4f57-a993-224454cb8570").as_bytes());
    circuit.compute_self_only_hash(&mut m);
    m.finalize().into()
}

#[pyfunction(
    options = "Default::default()",
    hash_child_count = "true",
    hash_child_shapes = "false"
)]
pub fn diff_circuits(
    new: CircuitRc,
    old: CircuitRc,
    options: PrintOptions,
    hash_child_count: bool,
    hash_child_shapes: bool,
) -> Result<String> {
    let mut options = options;
    options.bijection = false;
    let mut result = "".to_owned();
    fn recurse(
        new: CircuitRc,
        old: CircuitRc,
        result: &mut String,
        options: &PrintOptions,
        last_child_stack: Vec<bool>,
        hash_child_count: bool,
        hash_child_shapes: bool,
    ) -> Result<()> {
        const SAME_SELF_COLOR: usize = 4;
        const SAME_COLOR: usize = 0;
        const NEW_COLOR: usize = 2;
        const REMOVED_COLOR: usize = 1;
        if new == old {
            let mut new_options = options.clone();
            new_options.colorer = Some(PrintOptions::fixed_color(SAME_COLOR));
            result.push_str(&indent(
                new_options.repr(new.clone())?,
                last_child_stack.len() * 2,
            ));
            result.push_str("\n");
            return Ok(());
        }
        if compute_self_hash(new.clone(), hash_child_count, hash_child_shapes)
            == compute_self_hash(old.clone(), hash_child_count, hash_child_shapes)
        {
            let line_prefix = if let Some(name) = new.name() {
                name.to_owned() + " "
            } else {
                "".to_owned()
            };

            result.push_str(&indent(
                color(
                    &format!("{}{}", line_prefix, options.repr_line_info(new.clone())?),
                    SAME_SELF_COLOR,
                ),
                last_child_stack.len() * 2,
            ));
            result.push_str("\n");

            assert_eq!(new.children().count(), old.children().count());
            for (i, (new_child, old_child)) in zip(new.children(), old.children()).enumerate() {
                let new_child_stack: Vec<bool> = last_child_stack
                    .iter()
                    .cloned()
                    .chain(std::iter::once(i == new.children().count()))
                    .collect();
                recurse(
                    new_child,
                    old_child,
                    result,
                    options,
                    new_child_stack,
                    hash_child_count,
                    hash_child_shapes,
                )?;
            }
            return Ok(());
        }
        let mut new_options = options.clone();
        new_options.colorer = Some(PrintOptions::fixed_color(NEW_COLOR));
        result.push_str(&indent(
            new_options.repr(new.clone())?,
            last_child_stack.len() * 2,
        ));
        result.push_str("\n");

        let mut new_options = options.clone();
        new_options.colorer = Some(PrintOptions::fixed_color(REMOVED_COLOR));
        result.push_str(&indent(
            new_options.repr(old.clone())?,
            last_child_stack.len() * 2,
        ));
        result.push_str("\n");

        Ok(())
    }
    recurse(
        new,
        old,
        &mut result,
        &options,
        vec![],
        hash_child_count,
        hash_child_shapes,
    )?;
    Ok(result)
}
