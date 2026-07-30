"""Render a self-contained interactive mind map.

Deliberately dependency-free: no CDN, no npm, no vendored third-party JavaScript.
The layout, interaction and styling are ~200 lines of plain JS emitted inline, so
``docs/mindmap.html`` is a single file that works from a local disk with no
network at all.

That constraint is the point. The purpose of this phase is to stop the project's
central artifact from depending on a service the author does not control; loading
a rendering library from a CDN would trade one such dependency for another. It
also means the file keeps working in restricted-network classrooms and inside
strict Content-Security-Policy contexts.

Restricted links render as a badge with no URL, same rule as the README.
"""

from __future__ import annotations

import json

from .model import MindMap

TITLE = "Web Technologies Mind Map"

_TEMPLATE = r"""<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>
:root{
  --bg:#fbfbfa; --fg:#1a1a19; --muted:#6b6b68; --line:#c9c9c4; --panel:#fff;
  --accent:#3b6ea5; --emerging:#8a5cb8; --legacy:#9a9a95; --hit:#c9761d;
  --shadow:0 1px 3px rgba(0,0,0,.08),0 8px 24px rgba(0,0,0,.06);
}
@media (prefers-color-scheme:dark){
  :root{
    --bg:#1a1a19; --fg:#e8e8e4; --muted:#9a9a94; --line:#3d3d3a; --panel:#232322;
    --accent:#7aa8d4; --emerging:#b48ad8; --legacy:#5f5f5b; --hit:#e0a060;
    --shadow:0 1px 3px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.3);
  }
}
*{box-sizing:border-box}
html,body{margin:0;height:100%;background:var(--bg);color:var(--fg);
  font:14px/1.5 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
#app{display:flex;flex-direction:column;height:100%}
header{display:flex;gap:.75rem;align-items:center;flex-wrap:wrap;
  padding:.6rem .9rem;border-bottom:1px solid var(--line);background:var(--panel)}
h1{font-size:.95rem;font-weight:650;margin:0;white-space:nowrap}
#search{flex:1;min-width:11rem;max-width:22rem;padding:.35rem .6rem;
  border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);font:inherit}
button{padding:.35rem .6rem;border:1px solid var(--line);border-radius:6px;
  background:var(--bg);color:var(--fg);font:inherit;cursor:pointer}
button:hover{border-color:var(--accent)}
#count{color:var(--muted);font-size:.8rem;white-space:nowrap}
#legend{display:flex;gap:.7rem;font-size:.78rem;color:var(--muted);flex-wrap:wrap}
#legend i{display:inline-block;width:.55rem;height:.55rem;border-radius:50%;margin-right:.25rem}
main{flex:1;display:flex;min-height:0}
#canvas{flex:1;overflow:hidden;position:relative;cursor:grab}
#canvas.drag{cursor:grabbing}
svg{width:100%;height:100%;display:block;touch-action:none}
.edge{fill:none;stroke:var(--line);stroke-width:1.2}
.node{cursor:pointer}
.node text{font-size:12.5px;fill:var(--fg);dominant-baseline:middle;user-select:none}
.node circle{fill:var(--bg);stroke:var(--accent);stroke-width:1.6}
.node.section text{font-weight:650}
.node.section circle{fill:var(--accent)}
.node.has-kids circle{fill:var(--accent)}
.node.collapsed circle{fill:var(--bg);stroke-dasharray:2 1.5}
.node.emerging circle{stroke:var(--emerging)}
.node.legacy circle{stroke:var(--legacy)}
.node.legacy text{fill:var(--legacy);font-style:italic}
.node.dim{opacity:.22}
.node.hit circle{stroke:var(--hit);stroke-width:2.6}
.node.hit text{fill:var(--hit);font-weight:650}
.node.sel text{text-decoration:underline;text-underline-offset:3px}
#panel{width:22rem;max-width:42vw;border-left:1px solid var(--line);background:var(--panel);
  padding:1rem;overflow-y:auto}
#panel.empty{color:var(--muted);font-size:.85rem}
#panel h2{font-size:1rem;margin:0 0 .15rem}
#panel .path{font-size:.75rem;color:var(--muted);margin-bottom:.7rem}
#panel .badge{display:inline-block;font-size:.7rem;padding:.05rem .4rem;border-radius:99px;
  border:1px solid var(--line);color:var(--muted);margin-left:.35rem;vertical-align:middle}
#panel p.def{margin:.4rem 0 .9rem}
#panel ul{margin:0;padding-left:1.1rem}
#panel li{margin:.2rem 0}
#panel a{color:var(--accent)}
#panel .locked{color:var(--muted)}
@media (max-width:720px){
  main{flex-direction:column}
  #panel{width:auto;max-width:none;border-left:0;border-top:1px solid var(--line);max-height:42%}
}
</style>
<div id="app">
  <header>
    <h1>__TITLE__</h1>
    <input id="search" type="search" placeholder="Search concepts and definitions…" autocomplete="off">
    <button id="expand">Expand all</button>
    <button id="collapse">Collapse</button>
    <button id="reset">Reset view</button>
    <span id="count"></span>
    <span id="legend">
      <span><i style="background:var(--accent)"></i>current</span>
      <span><i style="background:var(--emerging)"></i>emerging</span>
      <span><i style="background:var(--legacy)"></i>legacy</span>
    </span>
  </header>
  <main>
    <div id="canvas"><svg><g id="view"></g></svg></div>
    <aside id="panel" class="empty">Select a node to see its definition and resources.</aside>
  </main>
</div>
<script>
const DATA = __DATA__;
const ROW = 22, INDENT = 26, PAD = 28;
const SVG = "http://www.w3.org/2000/svg";
const view = document.getElementById("view");
const panel = document.getElementById("panel");
const countEl = document.getElementById("count");

// Wire parents once; everything else derives from DATA + collapsed set.
let total = 0;
(function wire(n, parent, depth){
  n._p = parent; n._d = depth; total++;
  (n.children || []).forEach(c => wire(c, n, depth + 1));
})(DATA, null, 0);

// Start with sections visible and their contents folded away: 151 concepts at
// once is noise, and the first thing a reader needs is the shape of the map.
const collapsed = new Set();
(DATA.children || []).forEach(s => (s.children || []).forEach(c => {
  if (c.children && c.children.length) collapsed.add(c.id);
}));

let selected = null, hits = null;

function rows(){
  const out = [];
  (function walk(n){
    out.push(n);
    if (!collapsed.has(n.id)) (n.children || []).forEach(walk);
  })(DATA);
  return out;
}

function ancestors(n){ const a = []; for (let p = n._p; p; p = p._p) a.push(p); return a; }

function draw(){
  const list = rows();
  list.forEach((n, i) => { n._y = PAD + i * ROW; n._x = PAD + n._d * INDENT; });
  view.textContent = "";

  const edges = document.createElementNS(SVG, "g");
  view.appendChild(edges);
  const seen = new Set(list.map(n => n.id));
  for (const n of list){
    if (!n._p || !seen.has(n._p.id)) continue;
    const p = n._p, path = document.createElementNS(SVG, "path");
    // Elbow with a rounded corner: cheap to compute, reads clearly at depth.
    const r = Math.min(8, (n._y - p._y) / 2);
    path.setAttribute("d",
      `M${p._x},${p._y + 6} V${n._y - r} Q${p._x},${n._y} ${p._x + r},${n._y} H${n._x - 4}`);
    path.setAttribute("class", "edge");
    edges.appendChild(path);
  }

  for (const n of list){
    const g = document.createElementNS(SVG, "g");
    const kids = (n.children || []).length;
    const cls = ["node"];
    if (n.kind === "section") cls.push("section");
    if (kids) cls.push("has-kids");
    if (collapsed.has(n.id)) cls.push("collapsed");
    if (n.status && n.status !== "current") cls.push(n.status);
    if (hits){ cls.push(hits.has(n.id) ? "hit" : (hits.ctx.has(n.id) ? "" : "dim")); }
    if (selected === n.id) cls.push("sel");
    g.setAttribute("class", cls.join(" "));
    g.setAttribute("transform", `translate(${n._x},${n._y})`);

    const c = document.createElementNS(SVG, "circle");
    c.setAttribute("r", n.kind === "section" ? 5 : 4);
    g.appendChild(c);

    const t = document.createElementNS(SVG, "text");
    t.setAttribute("x", 11);
    t.textContent = n.label + (kids && collapsed.has(n.id) ? `  (${countAll(n)})` : "");
    g.appendChild(t);

    g.addEventListener("click", e => {
      e.stopPropagation();
      if (kids){ collapsed.has(n.id) ? collapsed.delete(n.id) : collapsed.add(n.id); }
      select(n);
      draw();
    });
    view.appendChild(g);
  }

  const h = PAD * 2 + list.length * ROW;
  document.querySelector("svg").setAttribute("viewBox", `0 0 900 ${Math.max(h, 400)}`);
  countEl.textContent = hits
    ? `${hits.size} match${hits.size === 1 ? "" : "es"} of ${total}`
    : `${list.length} of ${total} shown`;
  applyTransform();
}

function countAll(n){
  let k = 0;
  (function w(x){ (x.children || []).forEach(c => { k++; w(c); }); })(n);
  return k;
}

function select(n){
  selected = n.id;
  if (n.kind === "section"){
    panel.className = "";
    panel.innerHTML = `<h2></h2><div class="path">section · ${countAll(n)} concepts</div>
      <p class="def"></p>`;
    panel.querySelector("h2").textContent = n.label;
    panel.querySelector(".def").textContent = n.def || "";
    return;
  }
  panel.className = "";
  const trail = ancestors(n).reverse().map(a => a.label).join(" › ");
  const parts = [];
  parts.push(`<h2></h2><div class="path"></div>`);
  if (n.def) parts.push(`<p class="def"></p>`);
  if ((n.links || []).length) parts.push(`<ul></ul>`);
  panel.innerHTML = parts.join("");
  panel.querySelector("h2").textContent = n.label;

  const path = panel.querySelector(".path");
  path.textContent = trail;
  for (const [k, v] of [["status", n.status !== "current" ? n.status : null], ["level", n.level]]){
    if (!v) continue;
    const b = document.createElement("span");
    b.className = "badge"; b.textContent = `${k}: ${v}`;
    path.appendChild(b);
  }
  if (n.def) panel.querySelector(".def").textContent = n.def;

  const ul = panel.querySelector("ul");
  for (const ln of (n.links || [])){
    const li = document.createElement("li");
    if (ln.restricted){
      // No URL exists in the data for a restricted link -- see render_readme.
      li.className = "locked";
      li.textContent = `🔒 ${ln.label} — access on request`;
    } else {
      const a = document.createElement("a");
      a.href = ln.url; a.target = "_blank"; a.rel = "noopener noreferrer";
      a.textContent = ln.label;
      li.appendChild(a);
    }
    ul && ul.appendChild(li);
  }
}

document.getElementById("search").addEventListener("input", e => {
  const q = e.target.value.trim().toLowerCase();
  if (!q){ hits = null; draw(); return; }
  const found = new Set(), ctx = new Set();
  (function w(n){
    const hay = (n.label + " " + (n.def || "")).toLowerCase();
    if (hay.includes(q)){
      found.add(n.id);
      // Reveal matches: open every ancestor so a hit is never hidden.
      ancestors(n).forEach(a => { ctx.add(a.id); collapsed.delete(a.id); });
    }
    (n.children || []).forEach(w);
  })(DATA);
  hits = found; hits.ctx = ctx;
  draw();
});

document.getElementById("expand").onclick = () => { collapsed.clear(); draw(); };
document.getElementById("collapse").onclick = () => {
  collapsed.clear();
  (DATA.children || []).forEach(s => (s.children || []).forEach(c => {
    if (c.children && c.children.length) collapsed.add(c.id);
  }));
  draw();
};
document.getElementById("reset").onclick = () => { tx = ty = 0; scale = 1; applyTransform(); };

// -- pan and zoom -------------------------------------------------------
let tx = 0, ty = 0, scale = 1, dragging = false, sx = 0, sy = 0;
const canvas = document.getElementById("canvas");
function applyTransform(){ view.setAttribute("transform", `translate(${tx},${ty}) scale(${scale})`); }
canvas.addEventListener("pointerdown", e => {
  dragging = true; sx = e.clientX - tx; sy = e.clientY - ty;
  canvas.classList.add("drag"); canvas.setPointerCapture(e.pointerId);
});
canvas.addEventListener("pointermove", e => {
  if (!dragging) return;
  tx = e.clientX - sx; ty = e.clientY - sy; applyTransform();
});
canvas.addEventListener("pointerup", e => {
  dragging = false; canvas.classList.remove("drag");
  try { canvas.releasePointerCapture(e.pointerId); } catch (_){}
});
canvas.addEventListener("wheel", e => {
  e.preventDefault();
  const k = e.deltaY < 0 ? 1.1 : 1 / 1.1;
  scale = Math.min(3, Math.max(0.3, scale * k));
  applyTransform();
}, { passive: false });

draw();
</script>
"""


def _node(concept) -> dict:
    d: dict = {
        "id": concept.id,
        "label": concept.label,
        "status": concept.status,
    }
    if concept.definition:
        d["def"] = concept.definition
    if concept.level:
        d["level"] = concept.level
    links = []
    for ln in concept.links:
        if ln.is_restricted:
            # The URL is deliberately absent, not merely hidden by CSS.
            links.append({"label": ln.label, "restricted": True})
        else:
            links.append({"label": ln.label, "url": ln.url})
    if links:
        d["links"] = links
    if concept.children:
        d["children"] = [_node(c) for c in concept.children]
    return d


def build_tree(mm: MindMap) -> dict:
    sections = []
    for s in mm.sections:
        kids: list[dict] = []
        if s.subsections:
            for ss in s.subsections:
                roots = mm.roots(s.id, ss.id)
                kids.append(
                    {
                        "id": f"{s.id}--{ss.id}",
                        "label": ss.heading,
                        "kind": "section",
                        "status": "current",
                        "children": [_node(c) for c in roots],
                    }
                )
        else:
            kids = [_node(c) for c in mm.roots(s.id, None)]
        sections.append(
            {
                "id": f"section--{s.id}",
                "label": s.heading,
                "kind": "section",
                "status": "current",
                "def": s.intro,
                "children": kids,
            }
        )
    return {
        "id": "root",
        "label": TITLE,
        "kind": "section",
        "status": "current",
        "children": sections,
    }


def render(mm: MindMap) -> str:
    data = json.dumps(build_tree(mm), ensure_ascii=False, separators=(",", ":"))
    # `</script>` inside a JSON string would close the block early.
    data = data.replace("</", "<\\/")
    return _TEMPLATE.replace("__DATA__", data).replace("__TITLE__", TITLE)
