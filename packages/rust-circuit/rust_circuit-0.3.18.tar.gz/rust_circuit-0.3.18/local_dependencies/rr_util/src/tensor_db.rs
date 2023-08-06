use std::{cmp::min, fs, io::Write, iter::zip, os::unix::prelude::OsStrExt};

use anyhow::{anyhow, bail, Context, Result};
use base16::encode_lower;
use pyo3::prelude::*;
use rustc_hash::FxHashSet as HashSet;

use crate::{
    py_types::{Tensor, PY_UTILS},
    rrfs::get_rrfs_dir,
};

pub fn get_tensor_cache_dir() -> String {
    std::env::var("TENSORS_CACHE_DIR")
        .unwrap_or(std::env::var("HOME").unwrap() + &"/tensors_by_hash_cache")
}

pub fn get_rrfs_tensor_db_dir() -> String {
    get_rrfs_dir() + "/tensor_db"
}

const SECTIONS: [usize; 3] = [4, 4, 56];
const SECTION_STARTS: [usize; 3] = [0, 4, 8];

pub fn get_tensor_hash_parts(tensor: &Tensor) -> Vec<String> {
    let b16 = encode_lower(&tensor.hashed().hash().unwrap());
    zip(&SECTION_STARTS, &SECTIONS)
        .map(|(a, b)| b16[*a..*a + *b].to_owned())
        .collect()
}

pub fn split_prefix(prefix: &str) -> (Vec<String>, String) {
    let n_full_sections = min(
        SECTIONS.len() - 1,
        (0..SECTION_STARTS.len())
            .map(|i| SECTION_STARTS[i] + SECTIONS[i] <= prefix.len())
            .count(),
    );

    (
        (0..n_full_sections)
            .map(|i| prefix[SECTION_STARTS[i]..SECTION_STARTS[i + 1]].to_owned())
            .collect(),
        prefix[SECTION_STARTS[n_full_sections]..].to_owned(),
    )
}

pub fn write_tensor_to_dir_tree(dir: &str, tensor: Tensor, force: bool) -> Result<bool> {
    let hash_parts = get_tensor_hash_parts(&tensor);
    let dir = dir.to_owned()
        + "/"
        + &hash_parts[..SECTIONS.len() - 1]
            .iter()
            .cloned()
            .collect::<Vec<_>>()
            .join("/");
    fs::create_dir_all(&dir)?;
    let filename = dir + "/" + hash_parts.last().unwrap();
    if !force && fs::metadata(&filename).is_ok() {
        return Ok(false);
    }
    Python::with_gil(|py| {
        PY_UTILS
            .torch
            .getattr(py, "save")
            .context("save tensor get save attribute")?
            .call(py, (tensor.tensor(), filename), None)
            .context("save tensor")
    })?;
    Ok(true)
}

pub fn get_only_file_in_nested_dirs(dir: &str) -> Result<String> {
    let mut dir = dir.to_owned();
    loop {
        let staty = fs::metadata(&dir).context("cant find dir in tree")?;
        if staty.is_file() {
            return Ok(dir);
        }
        if staty.is_dir() {
            let files: Vec<_> = fs::read_dir(&dir)?.collect();
            if files.len() > 1 {
                bail!(anyhow!("prefix dir contains multiple things"));
            }
            if files.len() == 0 {
                bail!(anyhow!("dir has no files"));
            }
            dir = dir + "/" + &files[0].as_ref().unwrap().file_name().to_str().unwrap();
        }
    }
}

pub fn get_tensor_dir_tree(dir: &str, hash_prefix: &str) -> Result<Tensor> {
    get_filename_dir_tree(dir, hash_prefix).and_then(|s| load_tensor(s))
}

pub fn get_filename_dir_tree(dir: &str, hash_prefix: &str) -> Result<String> {
    let (wholes, part) = split_prefix(&hash_prefix);
    let look_dir = dir.to_owned() + "/" + &wholes.join("/");
    let files =
        fs::read_dir(&look_dir).context(format!("tensors dir doesnt exist {}", &look_dir))?;
    let matching_entries: Vec<_> = files
        .filter(|x| &x.as_ref().unwrap().file_name().as_bytes()[..part.len()] == part.as_bytes())
        .collect();
    match matching_entries.len() {
        0 => {
            bail!(anyhow!("Found no tensors matching hash prefix"))
        }
        1 => get_only_file_in_nested_dirs(
            &(look_dir
                + "/"
                + &matching_entries[0]
                    .as_ref()
                    .unwrap()
                    .file_name()
                    .to_str()
                    .unwrap()),
        ),
        _ => {
            bail!(anyhow!("Found multiple tensors matching hash prefix"))
        }
    }
}

pub fn load_tensor(dir: String) -> Result<Tensor> {
    Python::with_gil(|py| {
        PY_UTILS
            .torch
            .getattr(py, "load")
            .unwrap()
            .call(py, (&dir,), None)
            .context(format!("Failed to load tensor from hash {}", &dir))?
            .extract(py)
            .context("Failed to extract pyobject in tensor from hash")
    })
}

pub fn register_tensor_unsynced(hash: &str) -> Result<()> {
    writeln!(
        fs::OpenOptions::new()
            .write(true)
            .append(true)
            .create(true)
            .open(get_tensor_cache_dir() + "/.unsynced_list")
            .unwrap(),
        "{}",
        hash
    )
    .context("couldnt write to unsynced list")
}

#[pyfunction(force = "false")]
pub fn save_tensor(tensor: Tensor, force: bool) -> Result<bool> {
    let cache_dir = get_tensor_cache_dir();
    fs::create_dir_all(&cache_dir)?;

    let result = write_tensor_to_dir_tree(&cache_dir, tensor.clone(), force);
    if let Ok(did_write) = result && did_write{
        register_tensor_unsynced(&tensor.hashed().hash_base16().unwrap())?
    }
    result
}

#[pyfunction]
pub fn sync_all_unsynced_tensors() -> Result<()> {
    let list_dir = get_tensor_cache_dir() + "/.unsynced_list";
    println!("starting to read list");
    let all_unsynced = fs::read_to_string(&list_dir)?;
    println!("read list");
    let lines = all_unsynced[..all_unsynced.len() - 1].lines();
    for line in lines {
        let local_filename = get_filename_dir_tree(&get_tensor_cache_dir(), line)?;
        println!("have dir tree");
        let remote_filename =
            local_filename.replace(&get_tensor_cache_dir(), &get_rrfs_tensor_db_dir());
        let remote_filename_dir: Vec<_> = remote_filename.split("/").collect();
        let remote_filename_dir = remote_filename_dir[..remote_filename_dir.len() - 1].join("/");
        fs::create_dir_all(&remote_filename_dir).context("failed to create dir in tree")?;
        fs::copy(local_filename, remote_filename).context("failed to copy")?;
        print!("wrote");
    }
    fs::write(&list_dir, &fs::read(&list_dir)?[all_unsynced.len()..]).context("write failed")
}

#[pyfunction]
pub fn get_tensor_prefix(prefix: &str) -> Result<Tensor> {
    let cache_dir = get_tensor_cache_dir();
    get_tensor_dir_tree(&cache_dir, &prefix).or_else(|_e| {
        let result = get_tensor_dir_tree(&get_rrfs_tensor_db_dir(), &prefix);
        if let Ok(t) = &result {
            write_tensor_to_dir_tree(&cache_dir, t.clone(), false)?;
        }
        result
    })
}

#[pyfunction]
pub fn migrate_tensors_from_old_dir(dir: &str) -> Result<()> {
    let files: Vec<String> = fs::read_dir(&dir)
        .unwrap()
        .map(|x| x.unwrap().file_name().to_str().unwrap().to_owned())
        .collect();
    print!("have list");
    let list_dir = get_tensor_cache_dir() + "/.unsynced_list";
    let all_unsynced = fs::read_to_string(&list_dir)?;
    let lines: HashSet<_> = all_unsynced[..all_unsynced.len() - 1].lines().collect();

    for file in files {
        if !lines.contains(&&file[..64]) {
            print!("O");
            let tensor = load_tensor(dir.to_owned() + "/" + &file)?;
            save_tensor(tensor, false)?;
        } else {
            print!("_");
        }
    }
    Ok(())
}
