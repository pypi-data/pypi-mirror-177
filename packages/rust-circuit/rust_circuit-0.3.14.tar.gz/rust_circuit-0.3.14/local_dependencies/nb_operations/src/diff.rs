use std::iter::zip;

use anyhow::Result;
use circuit_base::{
    generalfunction::SpecTrait,
    print::{color, PrintOptions},
    Circuit, CircuitNode, CircuitRc,
};
use pyo3::prelude::*;
use rr_util::util::{indent, HashBytes};
use uuid::uuid;

#[pyfunction]
pub fn compute_self_hash(circuit: CircuitRc) -> HashBytes {
    let mut m = blake3::Hasher::new();
    for l in &circuit.info().shape {
        m.update(&l.to_le_bytes());
    }
    m.update(uuid!("6261daa8-0085-46f7-9f38-b085601fa628").as_bytes());
    match &**circuit {
        Circuit::Einsum(ein) => {
            m.update(&ein.out_axes);
            for (c, axes) in &ein.args {
                m.update(uuid!("b47a5d74-95ed-469e-b317-6be616f869b2").as_bytes());
                m.update(axes);
            }
        }
        Circuit::Concat(concat) => {
            m.update(&concat.axis.to_le_bytes());
        }
        Circuit::Rearrange(rearrange) => {
            m.update(&rearrange.spec.compute_hash());
        }
        Circuit::Index(index) => {
            m.update(&index.index.compute_hash());
        }
        Circuit::GeneralFunction(gf) => {
            m.update(&gf.spec.compute_hash());
        }
        Circuit::Tag(tag) => {
            m.update(tag.uuid.as_bytes());
        }
        Circuit::Module(module) => {
            m.update(&module.spec.compute_hash());
        }
        Circuit::Array(_) | Circuit::Scalar(_) | Circuit::Symbol(_) => {
            m.update(&circuit.info().hash);
        }
        _ => {}
    }
    m.finalize().into()
}

#[pyfunction]
pub fn diff_circuits(new: CircuitRc, old: CircuitRc, options: PrintOptions) -> Result<String> {
    let mut options = options;
    options.bijection = false;
    options.inc_ids = false;
    let mut result = "".to_owned();
    fn recurse(
        new: CircuitRc,
        old: CircuitRc,
        result: &mut String,
        options: &PrintOptions,
        last_child_stack: Vec<bool>,
    ) -> Result<()> {
        let SAME_SELF_COLOR = 4;
        let SAME_COLOR = 0;
        let NEW_COLOR = 2;
        let REMOVED_COLOR = 1;
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
        if compute_self_hash(new.clone()) == compute_self_hash(old.clone()) {
            result.push_str(&indent(
                color(&options.repr_line(new.clone())?, SAME_SELF_COLOR),
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
                recurse(new_child, old_child, result, options, new_child_stack)?;
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
    recurse(new, old, &mut result, &options, vec![])?;
    Ok(result)
}
