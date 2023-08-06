use std::{
    collections::HashSet,
    fmt::Debug,
    hash::{Hash, Hasher},
};

use anyhow::Result;
use pyo3::prelude::*;
use rand::Rng;
use rr_util::{fn_struct, py_types::MaybeNotSet, simple_default, util::hash_to_string};
use rustc_hash::FxHashMap as HashMap;

use crate::{
    opaque_iterative_matcher::OpaqueIterativeMatcherVal,
    prelude::*,
    print::{
        circuit_to_computability_color_code, circuit_to_size_color_code, op_traversal_per,
        PrintOptions,
    },
    HashBytes,
};

#[derive(FromPyObject, Clone)]
pub enum PrintOptionsBase {
    PrintOptions(PrintOptions),
    PrintHtmlOptions(PrintHtmlOptions),
}

impl PrintOptionsBase {
    pub fn print(&self, circuits: Vec<CircuitRc>) -> Result<()> {
        match self {
            PrintOptionsBase::PrintOptions(p) => p.print_circuits(circuits),
            PrintOptionsBase::PrintHtmlOptions(p) => p.print(circuits),
        }
    }
}

simple_default!(PrintOptionsBase {
    PrintOptionsBase::PrintOptions(Default::default())
});

fn_struct!(pub CircuitToColor:Fn(circuit:CircuitRc)->String);

#[pyclass]
#[derive(Clone)]
pub struct PrintHtmlOptions {
    #[pyo3(get, set)]
    pub shape_only_when_necessary: bool,
    pub traversal: Option<OpaqueIterativeMatcherVal>,
    #[pyo3(get, set)]
    pub display_copy_button: bool,
    #[pyo3(get, set)]
    pub colorer: Option<CircuitToColor>,
    #[pyo3(get, set)]
    pub primary_color: String,
    #[pyo3(get, set)]
    pub display_serial_numbers: bool,
    #[pyo3(get, set)]
    pub keep_all_cells: bool,
    pub overall_traversal: Option<OpaqueIterativeMatcherVal>,
}

impl Default for PrintHtmlOptions {
    fn default() -> Self {
        Self {
            shape_only_when_necessary: true,
            traversal: Some(OpaqueIterativeMatcherVal::for_end_depth(3)),
            display_copy_button: true,
            colorer: Some(PrintHtmlOptions::variant_colorer()),
            primary_color: "lightgray".to_owned(),
            display_serial_numbers: false,
            keep_all_cells: true,
            overall_traversal: Some(OpaqueIterativeMatcherVal::never()),
        }
    }
}

impl PrintHtmlOptions {
    pub fn fill_overall_data(
        &self,
        circuits: Vec<CircuitRc>,
        data: &mut HashMap<HashBytes, NodeJsonData>,
    ) -> Result<()> {
        fn recurse(
            circ: CircuitRc,
            data: &mut HashMap<HashBytes, NodeJsonData>,
            selfy: &PrintHtmlOptions,
            traversal: Option<OpaqueIterativeMatcherVal>,
        ) -> Result<()> {
            if let Some(_) = data.get(&circ.info().hash) {
                return Ok(());
            }
            let desc = selfy.repr_line(circ.clone())?;
            data.insert(
                circ.info().hash,
                NodeJsonData {
                    name: circ.name_cloned().unwrap_or("".to_owned()),
                    desc,
                    color: match &selfy.colorer {
                        Some(col_fn) => col_fn.call(circ.clone())?,
                        None => selfy.primary_color.clone(),
                    },
                    children: circ
                        .clone()
                        .children()
                        .map(|c| hash_to_string(&c.info().hash))
                        .collect(),
                },
            );

            let new_traversal_per =
                if let Some(new_traversal_per) = op_traversal_per(traversal, circ.crc())? {
                    new_traversal_per
                } else {
                    // all finished case
                    return Ok(());
                };

            for (child, new_traversal) in circ.children().zip(new_traversal_per) {
                recurse(child, data, selfy, new_traversal)?;
            }
            Ok(())
        }
        for circuit in circuits.clone() {
            recurse(circuit, data, &self, self.overall_traversal.clone())?;
        }
        Ok(())
    }
    pub fn fill_to_expand_data(
        &self,
        circuits: Vec<CircuitRc>,
        nodes_to_expand: &mut Vec<HashBytes>, // Nodes you can see the children of
        data: &mut HashMap<HashBytes, NodeJsonData>, /* Data of all nodes which you might want to see */
    ) -> Result<()> {
        let mut expanded_nodes: HashSet<HashBytes> = Default::default(); // Nodes that are seen from the beginning
        fn recurse(
            circ: CircuitRc,
            nodes_to_expand: &mut Vec<HashBytes>,
            expanded_nodes: &mut HashSet<HashBytes>,
            data: &mut HashMap<HashBytes, NodeJsonData>,
            selfy: &PrintHtmlOptions,
            traversal: Option<OpaqueIterativeMatcherVal>,
        ) -> Result<()> {
            if let Some(_) = expanded_nodes.get(&circ.info().hash) {
                return Ok(());
            }
            expanded_nodes.insert(circ.info().hash);

            let mut desc = String::new();
            if selfy.display_serial_numbers {
                desc.push_str(&(expanded_nodes.len() - 1).to_string());
                desc.push(' ');
            }
            if let Some(old_data) = data.get_mut(&circ.info().hash) {
                desc.push_str(&old_data.desc);
                old_data.desc = desc; // Overwrite description to have the right nodes_to_expand count
            } else {
                desc.push_str(&selfy.repr_line(circ.clone())?);
                data.insert(
                    circ.info().hash,
                    NodeJsonData {
                        name: circ.name_cloned().unwrap_or("".to_owned()),
                        desc,
                        color: match &selfy.colorer {
                            Some(col_fn) => col_fn.call(circ.clone())?,
                            None => selfy.primary_color.clone(),
                        },
                        children: circ
                            .clone()
                            .children()
                            .map(|c| hash_to_string(&c.info().hash))
                            .collect(),
                    },
                );
            }

            let new_traversal_per =
                if let Some(new_traversal_per) = op_traversal_per(traversal, circ.crc())? {
                    new_traversal_per
                } else {
                    // all finished case
                    return Ok(());
                };
            if !nodes_to_expand.contains(&circ.info().hash) {
                nodes_to_expand.push(circ.info().hash);
            }
            for (child, new_traversal) in circ.children().zip(new_traversal_per) {
                recurse(
                    child,
                    nodes_to_expand,
                    expanded_nodes,
                    data,
                    selfy,
                    new_traversal.clone(),
                )?;
            }
            Ok(())
        }
        for circuit in circuits {
            recurse(
                circuit,
                nodes_to_expand,
                &mut expanded_nodes,
                data,
                &self,
                self.traversal.clone(),
            )?;
        }
        Ok(())
    }

    fn get_print_options(&self) -> PrintOptions {
        PrintOptions {
            bijection: false,
            shape_only_when_necessary: self.shape_only_when_necessary,
            ..Default::default() // Other params are not used in repr_line_info
        }
    }
}

#[pymethods]
impl PrintHtmlOptions {
    #[new]
    #[args(
        shape_only_when_necessary = "PrintHtmlOptions::default().shape_only_when_necessary",
        traversal = "None",
        display_copy_button = "PrintHtmlOptions::default().display_copy_button",
        colorer = "None",
        primary_color = "PrintHtmlOptions::default().primary_color",
        display_serial_numbers = "PrintHtmlOptions::default().display_serial_numbers",
        keep_all_cells = "PrintHtmlOptions::default().keep_all_cells",
        overall_traversal = "None"
    )] // None are mapped to the default
    pub fn py_new(
        shape_only_when_necessary: bool,
        traversal: Option<OpaqueIterativeMatcherVal>,
        display_copy_button: bool,
        colorer: Option<CircuitToColor>,
        primary_color: String,
        display_serial_numbers: bool,
        keep_all_cells: bool,
        overall_traversal: Option<OpaqueIterativeMatcherVal>,
    ) -> Result<Self> {
        let result = Self {
            shape_only_when_necessary,
            traversal: Some(traversal.unwrap_or(PrintHtmlOptions::default().traversal.unwrap())),
            display_copy_button,
            colorer: Some(colorer.unwrap_or(PrintHtmlOptions::default().colorer.unwrap())),
            primary_color,
            display_serial_numbers,
            keep_all_cells,
            overall_traversal: Some(
                overall_traversal.unwrap_or(PrintHtmlOptions::default().overall_traversal.unwrap()),
            ),
        };
        Ok(result)
    }

    #[args(
        shape_only_when_necessary = "Default::default()",
        traversal = "Default::default()",
        colorer = "Default::default()",
        primary_color = "Default::default()",
        display_copy_button = "Default::default()",
        display_serial_numbers = "Default::default()",
        keep_all_cells = "Default::default()",
        overall_traversal = "Default::default()"
    )]
    pub fn evolve(
        &self,
        shape_only_when_necessary: MaybeNotSet<bool>,
        traversal: MaybeNotSet<Option<OpaqueIterativeMatcherVal>>,
        display_copy_button: MaybeNotSet<bool>,
        colorer: MaybeNotSet<Option<CircuitToColor>>,
        primary_color: MaybeNotSet<String>,
        display_serial_numbers: MaybeNotSet<bool>,
        keep_all_cells: MaybeNotSet<bool>,
        overall_traversal: MaybeNotSet<Option<OpaqueIterativeMatcherVal>>,
    ) -> Self {
        let cloned = self.clone();
        Self {
            shape_only_when_necessary: shape_only_when_necessary
                .0
                .unwrap_or(cloned.shape_only_when_necessary),
            traversal: traversal.0.unwrap_or(cloned.traversal),
            display_copy_button: display_copy_button.0.unwrap_or(cloned.display_copy_button),
            colorer: colorer.0.unwrap_or(cloned.colorer),
            primary_color: primary_color.0.unwrap_or(cloned.primary_color),
            display_serial_numbers: display_serial_numbers
                .0
                .unwrap_or(cloned.display_serial_numbers),
            keep_all_cells: keep_all_cells.0.unwrap_or(cloned.keep_all_cells),
            overall_traversal: overall_traversal.0.unwrap_or(cloned.overall_traversal),
        }
    }

    #[args(circuits = "*")]
    pub fn print(&self, circuits: Vec<CircuitRc>) -> Result<()> {
        let html = self.repr(circuits)?;
        Python::with_gil(|py| -> Result<()> {
            let fun: Py<PyAny> = PyModule::from_code(
                py,
                &format!(
                    "def run():
                    from IPython.display import HTML, display
                    display(HTML(\"\"\"{html}\"\"\"))"
                ), // Dangerous, but " were escaped so it should be fine?
                "",
                "",
            )?
            .getattr("run")?
            .into();
            fun.call0(py)?;
            Ok(())
        })
    }

    #[args(circuits = "*")]
    pub fn repr(&self, circuits: Vec<CircuitRc>) -> Result<String> {
        let mut nodes_to_expand: Vec<HashBytes> = Default::default();
        let mut data: HashMap<HashBytes, NodeJsonData> = Default::default();
        self.fill_overall_data(circuits.clone(), &mut data)?;
        self.fill_to_expand_data(circuits.clone(), &mut nodes_to_expand, &mut data)?;

        let mut html = HTML_HEADER.to_owned();

        // var toExpandtoggle___js___ = ['1', ...];
        html.push_str("var toExpandtoggle___js___ = [");
        html.push_str(
            &nodes_to_expand
                .iter()
                .map(|h| format!("\"{}\"", hash_to_string(h)))
                .collect::<Vec<String>>()
                .join(","),
        );
        html.push_str("];");

        // var data = {1: {
        //     name: 'I k2 logits_diff, true I',
        //     desc: 'I k2 logits_diff, true I [t: Cumulant] [s: ()]',
        //     color: 'red',
        //     children: ['2', '3'],
        //   }
        html.push_str("var datatoggle___js___ = {");
        html.push_str(
            &data
                .iter()
                .map(|(h, json_data)| hash_to_string(h) + ":" + &json_data.to_string())
                .collect::<Vec<String>>()
                .join(","),
        );
        html.push_str("};");

        // var rootstoggle___js___ = ['1', ...];
        html.push_str("var rootstoggle___js___ = [");
        html.push_str(
            &circuits
                .iter()
                .map(|c| format!("\"{}\"", hash_to_string(&c.info().hash)))
                .collect::<Vec<String>>()
                .join(","),
        );
        html.push_str("];");

        html.push_str(if self.display_copy_button {
            "var displayCopyButtontoggle___js___ = true;"
        } else {
            "var displayCopyButtontoggle___js___ = false;"
        });

        // Jupyter just keeps adding new html elements, so we have to create divs
        // with unique ids. Seed is the suffix of every id created in one block.
        let mut rng = rand::thread_rng();
        let seed = rng.gen_range(0..100000000);
        html.push_str(&format!("var seedtoggle___js___ = \"{seed}\";"));

        html.push_str(CSS_HEADER);

        html.push_str(&format!(
            "--primary: {};",
            make_str_safe(&self.primary_color)
        ));
        html.push_str(CSS);

        html.push_str(&format!(
            "<div class=\"mainUL\" id=\"{seed}\"><ul></ul></div>",
        ));
        html.push_str(JS);

        // If keep_all_cells, variables in all cells need to have different names.
        // To do so, the seed is appended to variable names.
        // Note: conflict with circuit name could be problematic since we do a bulk replacement
        // which is why variable are named with ___js___
        if self.keep_all_cells {
            html = html
                .replace(
                    "expandClonestoggle___js___",
                    &format!("expandClonestoggle___js___{seed}"),
                )
                .replace(
                    "toExpandtoggle___js___",
                    &format!("toExpandtoggle___js___{seed}"),
                )
                .replace("datatoggle___js___", &format!("datatoggle___js___{seed}"))
                .replace("rootstoggle___js___", &format!("rootstoggle___js___{seed}"))
                .replace(
                    "displayCopyButtontoggle___js___",
                    &format!("displayCopyButtontoggle___js___{seed}"),
                )
                .replace("seedtoggle___js___", &format!("seedtoggle___js___{seed}"))
                .replace(
                    "addChildtoggle___js___",
                    &format!("addChildtoggle___js___{seed}"),
                )
                .replace(
                    "toggletoggle___js___",
                    &format!("toggletoggle___js___{seed}"),
                )
                .replace(
                    "toggleSiblingsBoldtoggle___js___",
                    &format!("toggleSiblingsBoldtoggle___js___{seed}"),
                );
        }

        Ok(html)
    }

    pub fn repr_line(&self, circ: CircuitRc) -> Result<String> {
        let line_info = self.get_print_options().repr_line_info(circ.clone());
        if let Some(name) = circ.name() {
            Ok(format!("'{name}'{}", &line_info?))
        } else {
            line_info
        }
    }

    pub fn light(&self) -> Self {
        self.evolve(
            MaybeNotSet(None),
            MaybeNotSet(None),
            MaybeNotSet(None),
            MaybeNotSet(None),
            MaybeNotSet(Some("#303030".to_owned())), // darkgray isn't actually dark .-.
            MaybeNotSet(None),
            MaybeNotSet(None),
            MaybeNotSet(None),
        )
    }

    #[staticmethod]
    #[args(circuits = "*", depth = "3")]
    pub fn print_depth(circuits: Vec<CircuitRc>, depth: usize) -> Result<()> {
        PrintHtmlOptions {
            traversal: Some(OpaqueIterativeMatcherVal::for_end_depth(depth)),
            overall_traversal: Some(OpaqueIterativeMatcherVal::never()),
            ..Default::default()
        }
        .print(circuits)
    }

    #[staticmethod]
    pub fn size_colorer() -> CircuitToColor {
        CircuitToColor::new_dyn(Box::new(|c| {
            Ok(color_from_colorcode(circuit_to_size_color_code(c)))
        }))
    }

    #[staticmethod]
    pub fn variant_colorer() -> CircuitToColor {
        CircuitToColor::new_dyn(Box::new(|circuit: CircuitRc| {
            let mut hasher = std::collections::hash_map::DefaultHasher::default();
            circuit.variant_string().hash(&mut hasher);
            Ok(color_from_hash(hasher.finish() as usize))
        }))
    }

    #[staticmethod]
    pub fn hash_colorer() -> CircuitToColor {
        CircuitToColor::new_dyn(Box::new(|circuit: CircuitRc| {
            Ok(color_from_hash(circuit.info().hash_usize()))
        }))
    }
    #[staticmethod]
    pub fn fixed_color(color: String) -> CircuitToColor {
        CircuitToColor::new_dyn(Box::new(move |_circuit: CircuitRc| Ok(color.clone())))
    }

    #[staticmethod]
    pub fn computability_colorer() -> CircuitToColor {
        CircuitToColor::new_dyn(Box::new(|c| {
            Ok(color_from_colorcode(circuit_to_computability_color_code(c)))
        }))
    }
}

fn color_from_hash(hash: usize) -> String {
    let hue = (hash % (255 / 10)) * 10;
    return format!("hsl({hue}, 90%, 60%)");
}

const COLORCODE_TO_RGB: [&str; 5] = [
    "rgb(1,1,1)",
    "rgb(222,56,43)",
    "rgb(57,181,74)",
    "rgb(255,199,6)",
    "rgb(0,111,184)",
];

fn color_from_colorcode(code: usize) -> String {
    assert!(code < COLORCODE_TO_RGB.len(), "invalid colorcode");
    return COLORCODE_TO_RGB[code].to_owned();
}

pub struct NodeJsonData {
    name: String,
    desc: String,
    color: String,
    children: Vec<String>,
}

fn make_str_safe(s: &String) -> String {
    s.replace(";", "")
        .replace("\"", "")
        .replace("<", "&lt")
        .replace(">", "&gt")
}

impl ToString for NodeJsonData {
    fn to_string(&self) -> String {
        let mut r = String::from("{name:\"");
        r.push_str(&make_str_safe(&self.name));
        r.push_str("\", desc:\"");
        r.push_str(&make_str_safe(&self.desc));
        r.push_str("\", color:\"");
        r.push_str(&make_str_safe(&self.color));
        r.push_str("\", children:[");
        r.push_str(
            &self
                .children
                .iter()
                .map(|c| format!("\"{c}\""))
                .collect::<Vec<String>>()
                .join(","),
        );
        r.push_str("]}");
        r
    }
}

const HTML_HEADER: &str = r#"
  <script>
    var expandClonestoggle___js___ = true;"#;
const CSS_HEADER: &str = r#"
  </script>
  <style>
    :root {"#;
const CSS: &str = r#"
    }
    ul,
    .mainUL {
      list-style-type: none;
    }
    .mainUL {
      margin: 0;
      padding: 0;
    }
    ul,
    li {
      margin: 0;
      padding: 0;
      color: var(--primary);
    }
    .caret,
    .caret-end {
      cursor: pointer;
      -webkit-user-select: none; /* Safari 3.1+ */
      -moz-user-select: none; /* Firefox 2+ */
      -ms-user-select: none; /* IE 10+ */
      user-select: none;
      margin-left: 0.2em;
      margin-right: 0.4em;
    }
    .caret::before,
    .caret-end::before {
      content: '>';
      color: var(--primary);
      display: inline-block;
    }
    .caret-end::before {
      color: var(--primary);
      opacity: 0.5;
    }
    .caret-down::before {
      -ms-transform: rotate(90deg);
      -webkit-transform: rotate(90deg);
      transform: rotate(90deg);
      color: var(--primary);
    }
    .nested {
      display: none;
    }
    .active {
      padding-left: 0.2em;
      margin-left: 0.42em;

      display: block;
    }
    .active.onlychild {
      margin-left: 0em;
      padding-left: 0em;
    }
    button {
      margin: 0px 0.2em 0px 0.2em;
      padding: 0px;
      background-color: transparent;
      border-radius: 3px;
      border-color: transparent;
      outline: none;
      opacity: 0.6;
    }
    button:hover {
      opacity: 1;
    }
    button:active {
      background-color: var(--primary);
    }
    button:focus {
      outline: none;
    }
    pre {
      margin: 0;
      padding: 0;
      display: inline;
    }
    .bold {
      text-shadow: 1px 1px 0px;
    }
  </style>"#;
const JS: &str = r#"
<script>
  function getElement(id) {
    return document.getElementById(id);
  }

  function getLastChild(div) {
    return div.children[div.children.length - 1];
  }

  // Parameters: id of the parent html element, id of the node to expand
  function addChildtoggle___js___(parent_id, id) {
    var child = document.createElement('li');

    // Example of the generated inner HTML:
    // <span class="caret" onclick="toggle('1')"></span>
    // <span style="color: hsl(70, 100%, 70%)">1 'I k2 logits_diff, true I' [t: Cumulant] [s: ()]</span>
    // <button onclick="toClipboard('I k2 logits_diff, true I')">📋</button>
    // <ul class="nested" style="border-left: 3px solid hsl(70, 100%, 70%)"></ul>;

    const childData = datatoggle___js___[id];
    if (!childData.displayedCount) {
      childData.displayedCount = 0;
    }
    var elementId = id + '@' + childData.displayedCount + '@' + seedtoggle___js___;
    child.id = elementId; // Assumes no "@" in ID

    var desc = childData.desc;
    if (childData.displayedCount > 0) {
      desc += ' (repeat)';
    }
    var copyButton = displayCopyButtontoggle___js___
      ? `<button onclick="toClipboard('` + childData.name + `')">📋</button>`
      : '';

    var onlyChild = datatoggle___js___[id].children.length == 0;
    var expandForbidden = !expandClonestoggle___js___ && childData.displayedCount > 0;
    var cantExpand = onlyChild || expandForbidden;
    var caretClass = cantExpand ? 'caret-end' : 'caret';

    var innerHTML =
      `<span class="` +
      caretClass +
      `" onclick="toggletoggle___js___('` +
      elementId +
      `')"></span><pre style="color: ` +
      childData.color +
      `">` +
      desc +
      `</pre>` +
      copyButton +
      `<ul class="nested" style="border-left: 3px solid ` +
      childData.color +
      `"></ul>`;
    child.innerHTML = innerHTML;
    child.children[1].addEventListener('mouseenter', function () {
      toggleSiblingsBoldtoggle___js___(elementId);
    });
    child.children[1].addEventListener('mouseleave', function () {
      toggleSiblingsBoldtoggle___js___(elementId);
    });
    childData.displayedCount += 1;
    getLastChild(getElement(parent_id)).appendChild(child);
  }
  rootstoggle___js___.forEach(function (root) {
    console.log(root);
    addChildtoggle___js___(seedtoggle___js___, root);
  });
  toExpandtoggle___js___.forEach(function (expandElt) {
    console.log(expandElt);
    toggletoggle___js___(expandElt + '@0@' + seedtoggle___js___);
  });

  function toClipboard(copyText) {
    navigator.clipboard.writeText(copyText);
  }
  function toggletoggle___js___(elementId) {
    var elt = getElement(elementId);
    console.log(elt, elementId);
    var nodeId = elementId.split('@')[0];

    var noChild = datatoggle___js___[nodeId].children.length == 0;
    var expandAllowed = expandClonestoggle___js___ || elementId.split('@')[1] == '0';
    if (!noChild && expandAllowed) {
      getLastChild(elt).classList.toggle('active');
      elt.children[0].classList.toggle('caret-down');

      let alreadExpanded = getLastChild(elt).children.length > 0;
      if (!alreadExpanded) {
        datatoggle___js___[nodeId].children.forEach(function (childId) {
          addChildtoggle___js___(elementId, childId);
        });
      }
    }
  }
  function toggleSiblingsBoldtoggle___js___(elementId) {
    var nodeId = elementId.split('@')[0];
    if (!datatoggle___js___[nodeId].displayedCount) return;
    var thisElementCount = elementId.split('@')[1];
    for (var i = 0; i < datatoggle___js___[nodeId].displayedCount; i++) {
      if (i != thisElementCount) {
        var otherElementId = nodeId + '@' + i + '@' + seedtoggle___js___;
        getElement(otherElementId).children[1].classList.toggle('bold');
      }
    }
  }
</script>
"#;
