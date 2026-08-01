"""Render a self-contained interactive mind map with two views.

Deliberately dependency-free: no CDN, no npm, no vendored third-party JavaScript.
The layout, physics, interaction and styling are plain JS emitted inline, so
``docs/mindmap.html`` is a single file that works from a local disk with no
network at all.

That constraint is the point. The purpose of this phase is to stop the project's
central artifact from depending on a service the author does not control; loading
a rendering library from a CDN would trade one such dependency for another. It
also means the file keeps working in restricted-network classrooms and inside
strict Content-Security-Policy contexts.

Two views over the same data:

**Tree** -- a collapsible indented outline. Good for reading the taxonomy in
order, which is how the README presents it.

**Graph** -- a force-directed node-link view. Good for the thing an outline
structurally cannot show: ``see_also`` edges that reach *across* sections, such
as the AI-Era Web entries pointing back at Knowledge Graphs in Additional
Topics. Hierarchy edges are the skeleton; related edges are drawn dashed and in
a distinct colour on top of it.

Why hand-rolled physics rather than d3-force, Sigma or Cytoscape: at 217 nodes
and ~250 edges a naive O(n^2) many-body step is roughly 47k pair evaluations per
tick, well under a millisecond. Quadtrees, WebGL and Web Workers exist to make
10k+ node graphs viable and buy nothing at this scale -- while every one of them
would cost the offline guarantee above.

SVG rather than canvas for the same reason: at this size SVG holds frame rate
comfortably, and it keeps the CSS custom properties, the dark-mode palette, real
text nodes and DOM-addressable elements that the Playwright suite drives.

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
  --rel:#c9761d;
  --shadow:0 1px 3px rgba(0,0,0,.08),0 8px 24px rgba(0,0,0,.06);
  /* One hue per top-level section, used to colour graph nodes. */
  --s0:#3b6ea5; --s1:#2e8b74; --s2:#b4653a; --s3:#8a5cb8; --s4:#a03d5f; --s5:#6b7a2e;
}
@media (prefers-color-scheme:dark){
  :root{
    --bg:#1a1a19; --fg:#e8e8e4; --muted:#9a9a94; --line:#3d3d3a; --panel:#232322;
    --accent:#7aa8d4; --emerging:#b48ad8; --legacy:#5f5f5b; --hit:#e0a060;
    --rel:#e0a060;
    --shadow:0 1px 3px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.3);
    --s0:#7aa8d4; --s1:#5cc0a4; --s2:#e0a06a; --s3:#b48ad8; --s4:#d97a9a; --s5:#a8bb5e;
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
#tabs{display:flex;border:1px solid var(--line);border-radius:6px;overflow:hidden;flex:none}
#tabs button{border:0;border-radius:0;padding:.35rem .8rem}
#tabs button+button{border-left:1px solid var(--line)}
#tabs button[aria-pressed="true"]{background:var(--accent);color:#fff}
#xlinks[aria-pressed="true"]{border-color:var(--rel);color:var(--rel)}
#count{color:var(--muted);font-size:.8rem;white-space:nowrap}
.legend{display:flex;gap:.7rem;font-size:.78rem;color:var(--muted);flex-wrap:wrap;align-items:center}
.legend i{display:inline-block;width:.55rem;height:.55rem;border-radius:50%;margin-right:.25rem}
.legend s{display:inline-block;width:1.1rem;border-top:1px solid var(--line);
  margin-right:.25rem;vertical-align:middle}
.legend s.rel{border-top:1.5px dashed var(--rel)}
main{flex:1;display:flex;min-height:0}
/* touch-action must be on the wrapper as well as the svg. iOS Safari looks at
   the element the gesture *starts* on and its ancestors; with the wrapper left
   at `auto` it can claim a two-finger gesture for its own page zoom and cancel
   our pointers mid-pinch. -webkit-touch-callout stops the long-press menu
   appearing over a node during a drag. */
#canvas{flex:1;overflow:hidden;position:relative;cursor:grab;
  touch-action:none;-webkit-touch-callout:none;-webkit-user-select:none;user-select:none}
#canvas.drag{cursor:grabbing}
svg{width:100%;height:100%;display:block;touch-action:none}

/* -- tree view ------------------------------------------------------- */
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

/* -- graph view ------------------------------------------------------ */
.gedge{stroke:var(--line);stroke-width:1;stroke-opacity:.75}
/* Cross-links are deliberately quiet at rest -- there are more of them than
   there are sections, and at full strength they read as noise over the
   hierarchy. Focusing a node brings the relevant ones forward. */
.gedge.rel{stroke:var(--rel);stroke-width:1.1;stroke-dasharray:4 3;stroke-opacity:.42}
.gedge.rel.lit{stroke-width:1.7;stroke-opacity:1}
body.no-xlinks .gedge.rel{display:none}
.gnode{cursor:pointer}
.gnode circle{stroke:var(--panel);stroke-width:1.2}
.gnode.emerging circle{stroke:var(--emerging);stroke-width:2;stroke-dasharray:2.5 2}
.gnode.legacy{opacity:.6}
.gnode text{font-size:10.5px;fill:var(--fg);text-anchor:middle;user-select:none;
  pointer-events:none;paint-order:stroke;stroke:var(--bg);stroke-width:3px;
  stroke-linejoin:round}
.gnode.big text{font-size:12.5px;font-weight:650}
.gnode.legacy text{font-style:italic}
.gnode.sel circle,.gnode.hit circle{stroke:var(--hit);stroke-width:2.6}
.gnode.hushed{opacity:.12}
.gedge.hushed{stroke-opacity:.06}
/* Toggling the view hides the other layer's controls rather than removing
   them, so no state is lost when switching back and forth. */
body[data-mode="graph"] .tree-only,body[data-mode="tree"] .graph-only{display:none}
body[data-mode="graph"] #view,body[data-mode="tree"] #gview{display:none}

#panel{width:22rem;max-width:42vw;border-left:1px solid var(--line);background:var(--panel);
  padding:1rem;overflow-y:auto}
#panel.empty{color:var(--muted);font-size:.85rem}
#panel h2{font-size:1rem;margin:0 0 .15rem}
#panel .path{font-size:.75rem;color:var(--muted);margin-bottom:.7rem}
#panel .badge{display:inline-block;font-size:.7rem;padding:.05rem .4rem;border-radius:99px;
  border:1px solid var(--line);color:var(--muted);margin-left:.35rem;vertical-align:middle}
#panel p.def{margin:.4rem 0 .9rem}
/* Arabic sits directly under the English it translates. `dir` is an attribute
   on the element rather than a CSS rule because it is a property of the text,
   not of its presentation: it governs the bidirectional algorithm, so a Latin
   term like "HTTP" embedded mid-sentence orders correctly. Naskh faces need
   more leading than Latin at the same size to stay legible. */
#panel p.def-ar{margin:-.5rem 0 .9rem;padding:.5rem .7rem;
  border-right:2px solid var(--line);background:color-mix(in srgb,var(--fg) 3%,transparent);
  border-radius:4px;font-size:1.05em;line-height:1.95;
  font-family:"Segoe UI","Noto Naskh Arabic",Tahoma,"Traditional Arabic",serif}
body.no-ar #panel p.def-ar{display:none}
#ar[aria-pressed="true"]{border-color:var(--accent);color:var(--accent)}
#ar{font-family:"Segoe UI","Noto Naskh Arabic",Tahoma,serif}
#panel ul{margin:0;padding-left:1.1rem}
#panel li{margin:.2rem 0}
#panel a{color:var(--accent)}
#panel .locked{color:var(--muted)}
#panel code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:.9em;
  background:color-mix(in srgb,var(--fg) 8%,transparent);padding:.05rem .25rem;border-radius:3px}
#panel h3{font-size:.75rem;text-transform:uppercase;letter-spacing:.04em;
  color:var(--muted);margin:1rem 0 .3rem;font-weight:650}
#panel .jump{background:none;border:0;padding:0;color:var(--rel);cursor:pointer;
  font:inherit;text-align:left;text-decoration:underline;text-underline-offset:2px}
@media (max-width:720px){
  main{flex-direction:column}
  #panel{width:auto;max-width:none;border-left:0;border-top:1px solid var(--line);max-height:42%}
}
</style>
<div id="app">
  <header>
    <h1>__TITLE__</h1>
    <span id="tabs">
      <button id="tab-tree" aria-pressed="true">Tree</button>
      <button id="tab-graph" aria-pressed="false">Graph</button>
    </span>
    <input id="search" type="search" placeholder="Search concepts and definitions…" autocomplete="off">
    <button id="expand" class="tree-only">Expand all</button>
    <button id="collapse" class="tree-only">Collapse</button>
    <button id="xlinks" class="graph-only" aria-pressed="true">Cross-links</button>
    <button id="relayout" class="graph-only">Re-run layout</button>
    <button id="ar" aria-pressed="true" title="Show or hide the Arabic definitions">العربية</button>
    <button id="reset">Reset view</button>
    <span id="count"></span>
    <span class="legend">
      <span><i style="background:var(--accent)"></i>current</span>
      <span><i style="background:var(--emerging)"></i>emerging</span>
      <span><i style="background:var(--legacy)"></i>legacy</span>
    </span>
    <span class="legend graph-only">
      <span><s></s>hierarchy</span>
      <span><s class="rel"></s>related</span>
    </span>
  </header>
  <main>
    <div id="canvas"><svg><g id="view"></g><g id="gview"></g></svg></div>
    <aside id="panel" class="empty">Select a node to see its definition and resources.</aside>
  </main>
</div>
<script>
const DATA = __DATA__;
const REL = __REL__;
const ROW = 22, INDENT = 26, PAD = 28;
const SVG = "http://www.w3.org/2000/svg";
const svgEl = document.querySelector("svg");
const view = document.getElementById("view");
const gview = document.getElementById("gview");
const panel = document.getElementById("panel");
const countEl = document.getElementById("count");

// Wire parents once; everything else derives from DATA + collapsed set.
let total = 0;
const byId = new Map();
(function wire(n, parent, depth){
  n._p = parent; n._d = depth; total++;
  byId.set(n.id, n);
  (n.children || []).forEach(c => wire(c, n, depth + 1));
})(DATA, null, 0);

// Start with sections visible and their contents folded away: 193 concepts at
// once is noise, and the first thing a reader needs is the shape of the map.
const collapsed = new Set();
function foldToSections(){
  collapsed.clear();
  (DATA.children || []).forEach(s => (s.children || []).forEach(c => {
    if (c.children && c.children.length) collapsed.add(c.id);
  }));
}
foldToSections();

let mode = "tree";
let selected = null, hits = null;

// see_also is declared on one side only in the YAML -- SKOS treats skos:related
// as symmetric, and duplicating every edge in two files would be a maintenance
// trap. Build the reverse index once so a concept's Related list shows who
// points *at* it as well as who it points to.
const relatedTo = new Map();
function link(a, b){
  if (!byId.has(a) || !byId.has(b) || a === b) return;
  if (!relatedTo.has(a)) relatedTo.set(a, []);
  if (!relatedTo.get(a).includes(b)) relatedTo.get(a).push(b);
}
for (const n of byId.values()) for (const other of (n.rel || [])){ link(n.id, other); link(other, n.id); }

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

    // Invisible full-row hit target. Without it only the 4px circle and the text
    // glyphs themselves are clickable: the gap between them, the space above and
    // below the label, and everything past the end of a short label are all dead.
    // fill=none with pointer-events=all is the canonical way to make an
    // unpainted shape receive clicks.
    const hit = document.createElementNS(SVG, "rect");
    hit.setAttribute("x", -9);
    hit.setAttribute("y", -ROW / 2);
    hit.setAttribute("height", ROW);
    hit.setAttribute("fill", "none");
    hit.setAttribute("pointer-events", "all");
    g.appendChild(hit);

    const c = document.createElementNS(SVG, "circle");
    c.setAttribute("r", n.kind === "section" ? 5 : 4);
    g.appendChild(c);

    const t = document.createElementNS(SVG, "text");
    t.setAttribute("x", 11);
    t.textContent = n.label + (kids && collapsed.has(n.id) ? `  (${countAll(n)})` : "");
    g.appendChild(t);
    n._hit = hit; n._text = t;

    g.addEventListener("click", e => {
      if (justDragged) return;    // this click is the tail of a pan gesture
      e.stopPropagation();
      // Show details first, then fold/unfold: a parent node should reveal its
      // own definition, not only act as a folder.
      select(n);
      if (kids){ collapsed.has(n.id) ? collapsed.delete(n.id) : collapsed.add(n.id); }
      draw();
    });
    view.appendChild(g);
  }

  // Text can only be measured once it is in the document, so size the hit
  // targets in a second pass rather than guessing from label length.
  for (const n of list){
    if (!n._hit) continue;
    let w = 0;
    try { w = n._text.getComputedTextLength(); } catch (_){}
    n._hit.setAttribute("width", 36 + (w || n.label.length * 7));
  }

  if (mode === "tree"){
    setTreeViewBox(list.length);
    setCount(`${list.length} of ${total} shown`);
  }
  applyTransform();
}

//: Matches the layout breakpoint in the stylesheet.
const NARROW = 720;
let VBW = 900, VBH = 600;

function canvasSize(){
  const r = canvas.getBoundingClientRect();
  return {w: Math.max(1, r.width), h: Math.max(1, r.height)};
}

function setViewBox(w, h){
  VBW = w; VBH = h;
  svgEl.setAttribute("viewBox", `0 0 ${w} ${h}`);
}

/** The graph's viewBox is always the canvas, one unit per CSS pixel.
 *
 *  A fixed 1400x950 box would be letterboxed into whatever shape the canvas
 *  actually is, and `fitView` would then fit the graph inside *that* -- two
 *  nested fits, so on a portrait phone the map ended up in a band across the
 *  middle with most of the screen empty. With the box matching the canvas
 *  there is no letterboxing and fitView alone decides the framing.
 */
function setGraphViewBox(){
  const {w, h} = canvasSize();
  setViewBox(Math.round(w), Math.round(h));
}

function setTreeViewBox(rows){
  const {w, h} = canvasSize();
  if (w < NARROW){
    // Window model on a phone: one user unit is one CSS pixel, so a 12.5px
    // label really is 12.5px and the reader pans to what is below the fold.
    // Fitting all 217 rows into a 390px-wide screen instead -- what this did
    // before -- renders them at about 4px, legible only after zooming in.
    setViewBox(Math.round(w), Math.round(h));
  } else {
    // Wide screens keep the fit-to-content behaviour they have always had.
    setViewBox(900, Math.max(PAD * 2 + rows * ROW, 400));
  }
}

/** CSS pixels per world unit: the viewBox fit factor times the camera zoom.
 *  Needed wherever something must come out a fixed size *on screen* rather
 *  than in the coordinate space, which is the whole point of the graph's
 *  labels. */
function effScale(){
  const {w, h} = canvasSize();
  return Math.min(w / VBW, h / VBH) * cam[mode].s;
}

function setCount(fallback){
  countEl.textContent = hits
    ? `${hits.size} match${hits.size === 1 ? "" : "es"} of ${total}`
    : fallback;
}

function countAll(n){
  let k = 0;
  (function w(x){ (x.children || []).forEach(c => { k++; w(c); }); })(n);
  return k;
}

/** Write *text* into *el*, honouring `**bold**`, `*italic*` and `` `code` ``.
 *
 *  A handful of definitions use markdown emphasis -- the Web3 disambiguation
 *  leans on it to separate the two meanings -- and the README renders it while
 *  this panel used to show the asterisks raw.
 *
 *  Builds real nodes instead of assigning innerHTML. The text comes from the
 *  project's own YAML rather than from a user, but keeping the no-markup-from-
 *  data rule means a stray angle bracket in a definition can never become an
 *  element, and the rule needs no exception to reason about later.
 */
function setProse(el, text){
  el.textContent = "";
  const re = /\*\*([^*]+)\*\*|\*([^*]+)\*|`([^`]+)`/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null){
    if (m.index > last) el.appendChild(document.createTextNode(text.slice(last, m.index)));
    const tag = m[1] ? "strong" : m[2] ? "em" : "code";
    const node = document.createElement(tag);
    node.textContent = m[1] || m[2] || m[3];
    el.appendChild(node);
    last = re.lastIndex;
  }
  if (last < text.length) el.appendChild(document.createTextNode(text.slice(last)));
}

function select(n){
  selected = n.id;
  panel.className = "";
  if (n.kind === "section"){
    panel.innerHTML = `<h2></h2><div class="path">section · ${countAll(n)} concepts</div>
      <p class="def"></p>`;
    panel.querySelector("h2").textContent = n.label;
    setProse(panel.querySelector(".def"), n.def || "");
    return;
  }
  const parts = [`<h2></h2><div class="path"></div>`];
  if (n.def) parts.push(`<p class="def"></p>`);
  if (n.def_ar) parts.push(`<p class="def-ar" dir="rtl" lang="ar"></p>`);
  if ((n.links || []).length) parts.push(`<h3>Resources</h3><ul class="links"></ul>`);
  const related = relatedTo.get(n.id) || [];
  if (related.length) parts.push(`<h3>Related</h3><ul class="rel"></ul>`);
  panel.innerHTML = parts.join("");
  panel.querySelector("h2").textContent = n.label;

  const path = panel.querySelector(".path");
  path.textContent = ancestors(n).reverse().map(a => a.label).join(" › ");
  for (const [k, v] of [["status", n.status !== "current" ? n.status : null], ["level", n.level]]){
    if (!v) continue;
    const b = document.createElement("span");
    b.className = "badge"; b.textContent = `${k}: ${v}`;
    path.appendChild(b);
  }
  if (n.def) setProse(panel.querySelector(".def"), n.def);
  if (n.def_ar) setProse(panel.querySelector(".def-ar"), n.def_ar);

  const ul = panel.querySelector("ul.links");
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

  // Cross-links are the whole reason the graph view exists; surface them in the
  // panel too, so they are reachable from the tree without hunting.
  const rl = panel.querySelector("ul.rel");
  for (const id of related){
    const li = document.createElement("li");
    const b = document.createElement("button");
    b.className = "jump"; b.textContent = byId.get(id).label;
    b.addEventListener("click", () => goto(id));
    li.appendChild(b); rl.appendChild(li);
  }
}

/** Reveal a concept in whichever view is active, and select it. */
function goto(id){
  const n = byId.get(id);
  if (!n) return;
  if (mode === "tree"){
    ancestors(n).forEach(a => collapsed.delete(a.id));
    select(n); draw();
    n._hit && n._hit.scrollIntoView && n._hit.scrollIntoView({block:"center"});
  } else {
    focus = id; select(n); reheat(0.2); paintClasses();
  }
}

document.getElementById("search").addEventListener("input", e => {
  const q = e.target.value.trim().toLowerCase();
  if (!q){ hits = null; refresh(); return; }
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
  refresh();
});

function refresh(){ mode === "tree" ? draw() : (paintClasses(), setCount(graphCount())); }

document.getElementById("expand").onclick = () => { collapsed.clear(); draw(); };
document.getElementById("collapse").onclick = () => { foldToSections(); draw(); };
// Arabic is shown by default; the toggle is for a reader who wants only the
// English, or is projecting to a room that does not read Arabic. Hidden with
// CSS rather than by re-rendering, so the state survives selecting another
// concept without any bookkeeping.
document.getElementById("ar").onclick = (e) => {
  const on = e.currentTarget.getAttribute("aria-pressed") !== "true";
  e.currentTarget.setAttribute("aria-pressed", String(on));
  document.body.classList.toggle("no-ar", !on);
};

// Teaching control: show the taxonomy on its own, then reveal how it actually
// connects. Only the drawing is suppressed -- the edges stay in the simulation,
// so toggling does not rearrange the graph under the reader.
document.getElementById("xlinks").onclick = (e) => {
  const on = e.currentTarget.getAttribute("aria-pressed") !== "true";
  e.currentTarget.setAttribute("aria-pressed", String(on));
  document.body.classList.toggle("no-xlinks", !on);
};
document.getElementById("relayout").onclick = () => {
  for (const n of G.nodes) n.fx = n.fy = null;
  seedPositions(); userMoved = false; reheat(1);
};
document.getElementById("reset").onclick = () => {
  if (mode === "graph"){ userMoved = false; fitView(); paintClasses(); return; }
  const c = cam.tree; c.tx = c.ty = 0; c.s = 1; applyTransform();
};

// -- view switching ------------------------------------------------------
function setMode(next){
  if (mode === next) return;
  mode = next;
  document.body.dataset.mode = next;
  document.getElementById("tab-tree").setAttribute("aria-pressed", String(next === "tree"));
  document.getElementById("tab-graph").setAttribute("aria-pressed", String(next === "graph"));
  if (next === "graph"){
    // viewBox first: seedPositions reads it to shape the initial layout.
    setGraphViewBox();
    buildGraph();                       // idempotent; builds the DOM once
    setCount(graphCount());
    paintClasses();
    reheat(0.6);
  } else {
    draw();
  }
  applyTransform();
}
document.getElementById("tab-tree").onclick = () => setMode("tree");
document.getElementById("tab-graph").onclick = () => setMode("graph");
document.body.dataset.mode = "tree";

// -- graph view ----------------------------------------------------------
//
// A hand-written velocity-Verlet force simulation. At ~217 nodes the naive
// O(n^2) repulsion pass is cheap enough that a Barnes-Hut quadtree would be
// pure complexity, and the whole thing stays inside this file.
//
// Hierarchy edges (parent -> child) are short and stiff, so a section and its
// concepts hold together as a visible cluster. see_also edges are long and
// slack: they should pull two clusters slightly toward each other and be
// legible as a line, without dragging a concept out of its own section.

const W = 1400, H = 950, CX = W / 2, CY = H / 2;
const REPULSE = -2400;       // many-body strength
const HIER = {len: 58, k: 0.52};
const RELK = {len: 170, k: 0.040};
const GRAVITY = 0.018;       // weak: the camera auto-fits, so nothing needs
                             // squeezing toward the middle to stay in frame
const VEL_DECAY = 0.62;      // fraction of velocity carried into the next tick
const ALPHA_DECAY = 0.0165;  // ~280 ticks to settle
const ALPHA_MIN = 0.0015;

let G = null;                // {nodes, edges, adj}
let alpha = 0, raf = null, ticks = 0;
let focus = null, hover = null;
let dragNode = null, dragMoved = false;
let userMoved = false;       // has the reader taken over the camera?

/** Deterministic PRNG: the layout must be reproducible for tests and for the
 *  reader who reopens the file and expects the same picture. */
function mulberry32(a){
  return function(){
    a |= 0; a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

function radiusOf(n){
  if (n._d === 0) return 10;
  if (n._d === 1) return 7.5;
  if (n.kind === "section") return 6;
  return (n.children || []).length ? 5 : 3.8;
}

function buildGraph(){
  if (G) return;
  const nodes = [], edges = [];
  const secOf = new Map();   // node id -> index of its top-level section

  (function walk(n, sec){
    const idx = n._d === 1 ? (DATA.children || []).indexOf(n) : sec;
    secOf.set(n.id, idx);
    nodes.push(n);
    for (const c of (n.children || [])){
      edges.push({a: n, b: c, rel: false});
      walk(c, idx);
    }
  })(DATA, -1);

  for (const [a, b] of REL){
    const na = byId.get(a), nb = byId.get(b);
    if (na && nb) edges.push({a: na, b: nb, rel: true});
  }

  const adj = new Map(nodes.map(n => [n.id, new Set()]));
  for (const e of edges){ adj.get(e.a.id).add(e.b.id); adj.get(e.b.id).add(e.a.id); }

  for (const n of nodes){ n._r = radiusOf(n); n._sec = secOf.get(n.id); }
  G = {nodes, edges, adj};

  seedPositions();

  // Edges first so nodes paint over them.
  const eg = document.createElementNS(SVG, "g");
  for (const e of G.edges){
    const l = document.createElementNS(SVG, "line");
    l.setAttribute("class", e.rel ? "gedge rel" : "gedge");
    e.el = l; eg.appendChild(l);
  }
  gview.appendChild(eg);

  for (const n of G.nodes){
    const g = document.createElementNS(SVG, "g");
    const cls = ["gnode"];
    if (n._d <= 2 || n.kind === "section") cls.push("big");
    if (n.status && n.status !== "current") cls.push(n.status);
    g.setAttribute("class", cls.join(" "));
    g._cls = cls.join(" ");

    const c = document.createElementNS(SVG, "circle");
    c.setAttribute("r", n._r);
    // A CSS custom property, so the section palette follows the colour scheme.
    c.style.fill = n._sec >= 0 ? `var(--s${n._sec % 6})` : "var(--fg)";
    g.appendChild(c);

    const t = document.createElementNS(SVG, "text");
    t.setAttribute("y", -n._r - 4);
    t.textContent = n.label;
    g.appendChild(t);

    g.addEventListener("pointerdown", ev => {
      if (ev.pointerType === "mouse" && ev.button !== 0) return;
      if (pointers.size > 1) return;  // second finger down: this is a pinch
      ev.stopPropagation();           // a node drag is not a canvas pan
      dragNode = n; dragMoved = false;
    });
    g.addEventListener("pointerenter", () => { hover = n.id; paintClasses(); });
    g.addEventListener("pointerleave", () => { hover = null; paintClasses(); });

    n._g = g; n._label = t;
    gview.appendChild(g);
  }
}

function seedPositions(){
  const rnd = mulberry32(0x5EED);
  const nSec = (DATA.children || []).length || 1;
  for (const n of G.nodes){
    if (n._d === 0){ n.x = CX; n.y = CY; n.vx = n.vy = 0; continue; }
    // Give each section its own angular wedge. Starting from a layout that
    // already respects the taxonomy converges faster and settles into
    // something a reader can navigate, rather than a random tangle.
    const ang = 2 * Math.PI * (n._sec + 0.5) / nSec + (rnd() - 0.5) * 0.85;
    const r = 90 + n._d * 105 + rnd() * 70;
    // Seed into the shape of the viewport rather than a fixed landscape one,
    // so a portrait phone gets a tall layout instead of a wide one floating in
    // a band across the middle. Repulsion is radially symmetric and relaxes
    // this over the first few hundred ticks, but the starting shape still
    // decides how much of the screen the settled graph occupies.
    const squash = Math.min(2.2, Math.max(0.45, VBH / VBW));
    n.x = CX + Math.cos(ang) * r;
    n.y = CY + Math.sin(ang) * r * squash;
    n.vx = n.vy = 0;
  }
}

function step(){
  const ns = G.nodes, len = ns.length;

  // Many-body repulsion, every pair. Softened at very short range so two nodes
  // landing on top of each other cannot produce an infinite impulse.
  for (let i = 0; i < len; i++){
    const a = ns[i];
    for (let j = i + 1; j < len; j++){
      const b = ns[j];
      let dx = b.x - a.x, dy = b.y - a.y;
      let d2 = dx * dx + dy * dy;
      if (d2 < 1){ dx = (i % 7) - 3 || 1; dy = (j % 5) - 2 || 1; d2 = dx * dx + dy * dy; }
      const f = REPULSE * alpha / d2;
      const d = Math.sqrt(d2);
      const fx = dx / d * f, fy = dy / d * f;
      a.vx += fx; a.vy += fy;
      b.vx -= fx; b.vy -= fy;
    }
  }

  for (const e of G.edges){
    const s = e.rel ? RELK : HIER;
    const dx = e.b.x - e.a.x, dy = e.b.y - e.a.y;
    const d = Math.hypot(dx, dy) || 0.01;
    const f = (d - s.len) / d * alpha * s.k;
    const fx = dx * f, fy = dy * f;
    e.a.vx += fx; e.a.vy += fy;
    e.b.vx -= fx; e.b.vy -= fy;
  }

  for (const n of ns){
    n.vx += (CX - n.x) * GRAVITY * alpha;
    n.vy += (CY - n.y) * GRAVITY * alpha;
    if (n.fx != null){ n.x = n.fx; n.y = n.fy; n.vx = n.vy = 0; continue; }
    n.vx *= VEL_DECAY; n.vy *= VEL_DECAY;
    n.x += n.vx; n.y += n.vy;
  }
}

function paintPositions(){
  for (const e of G.edges){
    e.el.setAttribute("x1", e.a.x); e.el.setAttribute("y1", e.a.y);
    e.el.setAttribute("x2", e.b.x); e.el.setAttribute("y2", e.b.y);
  }
  for (const n of G.nodes) n._g.setAttribute("transform", `translate(${n.x},${n.y})`);
}

/** Fit the whole layout in frame, until the reader takes the camera over.
 *  Cheaper and far more robust than tuning the forces until the graph happens
 *  to fill a 1400x950 box: the bounding box is measured, not hoped for. */
function fitView(){
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  for (const n of G.nodes){
    if (n.x < x0) x0 = n.x;
    if (n.x > x1) x1 = n.x;
    if (n.y < y0) y0 = n.y;
    if (n.y > y1) y1 = n.y;
  }
  const pad = 70;
  const s = clampScale(
    Math.min(VBW / (x1 - x0 + pad * 2), VBH / (y1 - y0 + pad * 2)));
  const c = cam.graph;
  c.s = s;
  c.tx = VBW / 2 - s * (x0 + x1) / 2;
  c.ty = VBH / 2 - s * (y0 + y1) / 2;
  applyTransform();
}

/** Highlight and label visibility. Separated from the physics loop because it
 *  is comparatively expensive and does not need to run at frame rate. */
function paintClasses(){
  if (!G) return;
  // Screen scale, not camera scale: on a phone the viewBox is fitted into a
  // 390px canvas, so sizing labels by the camera alone leaves them a third of
  // the intended size before the reader has zoomed at all.
  const s = effScale();
  const anchor = hover || focus;
  const near = anchor ? new Set([anchor, ...G.adj.get(anchor)]) : null;

  // Two independent reasons to be lit -- being near the focus, and matching the
  // search. They must combine with OR: making one hush the other means typing a
  // query while a node is selected greys out the very match you searched for.
  const filtered = !!near || !!hits;

  const wanted = [];
  for (const n of G.nodes){
    const cls = [n._g._cls];
    const isHit = hits ? hits.has(n.id) : false;
    const isNear = near ? near.has(n.id) : false;
    if (isHit) cls.push("hit");
    if (n.id === focus) cls.push("sel");
    n._lit = !filtered || isNear || isHit;
    if (!n._lit) cls.push("hushed");
    n._g.setAttribute("class", cls.join(" "));

    // Labels are drawn at a constant *screen* size, so zooming in genuinely
    // buys room for more of them rather than magnifying the same collisions.
    const px = n._d <= 1 ? 13 : n._d === 2 ? 11.5 : 10.5;
    n._label.style.fontSize = (px / s) + "px";
    n._label.style.strokeWidth = (3 / s) + "px";
    n._label.setAttribute("y", -n._r - 4);

    // Priority decides who keeps a label when two want the same space:
    // whatever the reader is pointing at first, then the structural spine,
    // then everything else outward-in.
    const pri = (n.id === focus || n.id === anchor) ? -3
      : isHit ? -2 : isNear ? -1 : n._d;
    wanted.push({n, pri, w: n.label.length * px * 0.56 / s, h: (px + 3) / s});
  }

  // Greedy label placement: sort by priority, keep a label only if its box is
  // still clear. Without this the six section names alone overlap into a smear
  // at the centre of the graph.
  wanted.sort((a, b) => a.pri - b.pri);
  const placed = [];
  for (const it of wanted){
    const n = it.n;
    const box = [n.x - it.w / 2, n.y - n._r - 4 - it.h, n.x + it.w / 2, n.y - n._r - 4];
    // Negative priority means the reader asked for this node -- it is focused,
    // adjacent to the focus, or a search hit. Naming those is the whole point
    // of the interaction, so they are never suppressed; they claim their box
    // and everything else works around them.
    let clash = false;
    if (it.pri >= 0){
      for (const p of placed){
        if (box[0] < p[2] && box[2] > p[0] && box[1] < p[3] && box[3] > p[1]){ clash = true; break; }
      }
    }
    if (clash){ n._label.style.display = "none"; continue; }
    n._label.style.display = "";
    placed.push(box);
  }

  for (const e of G.edges){
    const on = e.a._lit && e.b._lit;
    let cls = e.rel ? "gedge rel" : "gedge";
    if (filtered) cls += on ? " lit" : " hushed";
    e.el.setAttribute("class", cls);
  }
}

function graphCount(){
  const rel = G ? G.edges.filter(e => e.rel).length : 0;
  return `${total} nodes · ${G ? G.edges.length - rel : 0} hierarchy · ${rel} related`;
}

function reheat(to){
  alpha = Math.max(alpha, to);
  if (!raf) raf = requestAnimationFrame(tick);
}

function tick(){
  raf = null;
  if (mode !== "graph"){ return; }
  step();
  paintPositions();
  if (!userMoved) fitView();
  // Label placement is O(n^2) in the worst case and only needs to keep up with
  // the eye, not the physics.
  if (++ticks % 8 === 0) paintClasses();
  alpha -= alpha * ALPHA_DECAY;
  if (alpha > ALPHA_MIN || dragNode) raf = requestAnimationFrame(tick);
  else paintClasses();       // one accurate pass once everything has stopped
}

// -- pan, zoom and node dragging -----------------------------------------
//
// Pointer capture must NOT be taken on pointerdown. Capturing retargets every
// subsequent pointer event -- and the resulting click -- to the capturing
// element, so a click on a node never reaches that node's own handler and the
// details panel never opens. Capture is therefore deferred until the pointer has
// actually moved past a small threshold, i.e. until this is genuinely a drag and
// not a click.
const DRAG_THRESHOLD = 4;   // px
const MIN_SCALE = 0.15, MAX_SCALE = 6;

const cam = {tree: {tx: 0, ty: 0, s: 1}, graph: {tx: 0, ty: 0, s: 1}};
let panning = false, moved = false, justDragged = false;
let activeId = null, startX = 0, startY = 0, originX = 0, originY = 0;

// Every pointer currently down, so a second finger is recognised as the start
// of a pinch rather than treated as more panning. Touch is the only input that
// can produce two at once, which is why zoom did not exist on a phone: the
// wheel handler has no equivalent there, and `touch-action:none` -- needed to
// stop the browser scrolling the page mid-drag -- also suppresses its native
// pinch. So the gesture has to be implemented here or it does not exist.
const pointers = new Map();
let pinch = null;           // {dist, mx, my} from the previous move

const canvas = document.getElementById("canvas");
function applyTransform(){
  const c = cam[mode], g = mode === "tree" ? view : gview;
  g.setAttribute("transform", `translate(${c.tx},${c.ty}) scale(${c.s})`);
}

function clampScale(v){ return Math.min(MAX_SCALE, Math.max(MIN_SCALE, v)); }

function pinchState(){
  if (pointers.size < 2) return null;
  const [a, b] = [...pointers.values()];
  return {
    dist: Math.max(1, Math.hypot(a.x - b.x, a.y - b.y)),
    mx: (a.x + b.x) / 2,
    my: (a.y + b.y) / 2,
  };
}

/** Zoom by *k* about a point in client coordinates, so whatever is under the
 *  fingers stays under them. Anchoring is what makes a pinch feel native --
 *  scaling about the origin slides the map out from under the gesture. */
function zoomAt(clientX, clientY, k){
  const c = cam[mode];
  const s2 = clampScale(c.s * k);
  const m = svgEl.getScreenCTM();
  if (m){
    // getScreenCTM maps viewBox units to screen, so its inverse gives the
    // point in the space the camera transform is expressed in.
    const p = new DOMPoint(clientX, clientY).matrixTransform(m.inverse());
    const r = s2 / c.s;
    c.tx = p.x - r * (p.x - c.tx);
    c.ty = p.y - r * (p.y - c.ty);
  }
  c.s = s2;
  applyTransform();
}

/** Shift the camera by a client-space delta, in viewBox units. */
function panBy(fromX, fromY, toX, toY){
  const m = svgEl.getScreenCTM();
  if (!m) return;
  const inv = m.inverse();
  const a = new DOMPoint(toX, toY).matrixTransform(inv);
  const b = new DOMPoint(fromX, fromY).matrixTransform(inv);
  const c = cam[mode];
  c.tx += a.x - b.x;
  c.ty += a.y - b.y;
  applyTransform();
}

/** Client pixels -> graph world units. Asking the <g> for its screen CTM folds
 *  the viewBox fit and the camera transform into one matrix, so this stays
 *  correct at any zoom, pan or window size. */
function toWorld(e){
  const m = gview.getScreenCTM();
  if (!m) return {x: 0, y: 0};
  return new DOMPoint(e.clientX, e.clientY).matrixTransform(m.inverse());
}

// Capture phase, so the tally is kept even for a press that lands on a graph
// node -- that handler stops propagation, and a pinch beginning with one
// finger already on a node must still be recognised.
canvas.addEventListener("pointerdown", e => {
  if (e.pointerType === "mouse" && e.button !== 0) return;
  pointers.set(e.pointerId, {x: e.clientX, y: e.clientY});
  startX = e.clientX; startY = e.clientY;

  if (pointers.size === 2){
    // A second finger converts whatever was happening into a pinch.
    panning = false;
    canvas.classList.remove("drag");
    if (dragNode){ dragNode.fx = dragNode.fy = null; dragNode = null; }
    pinch = pinchState();
  }
}, true);

canvas.addEventListener("pointerdown", e => {
  if (e.pointerType === "mouse" && e.button !== 0) return;
  if (pointers.size > 1) return;       // pinching, not panning
  panning = true; moved = false; justDragged = false;
  activeId = e.pointerId;
  originX = cam[mode].tx; originY = cam[mode].ty;
});

canvas.addEventListener("pointermove", e => {
  if (pointers.has(e.pointerId)) pointers.set(e.pointerId, {x: e.clientX, y: e.clientY});

  if (gestureActive) return;      // WebKit is driving this pinch, not us

  if (pointers.size >= 2){
    const now = pinchState();
    if (pinch && now){
      zoomAt(now.mx, now.my, now.dist / pinch.dist);
      // Follow the midpoint as well, so two fingers pan and zoom together --
      // the same gesture people already use on a map.
      panBy(pinch.mx, pinch.my, now.mx, now.my);
      justDragged = true;              // never resolve a pinch into a tap
      if (mode === "graph"){ userMoved = true; paintClasses(); }
    }
    pinch = now;
    return;
  }

  if (dragNode){
    const dx = e.clientX - startX, dy = e.clientY - startY;
    if (!dragMoved && Math.hypot(dx, dy) < DRAG_THRESHOLD) return;
    dragMoved = true;
    const p = toWorld(e);
    dragNode.fx = p.x; dragNode.fy = p.y;
    reheat(0.3);
    return;
  }
  if (!panning || e.pointerId !== activeId) return;
  const dx = e.clientX - startX, dy = e.clientY - startY;
  if (!moved && Math.hypot(dx, dy) < DRAG_THRESHOLD) return;   // still a click
  if (!moved){
    moved = true;
    userMoved = true;          // stop auto-fitting; the reader is driving now
    canvas.classList.add("drag");
    try { canvas.setPointerCapture(activeId); } catch (_){}
  }
  cam[mode].tx = originX + dx; cam[mode].ty = originY + dy;
  applyTransform();
});

function endPointer(){
  if (dragNode){
    // A press that never moved is a click: show the concept and focus it.
    if (!dragMoved){ focus = dragNode.id; select(dragNode); paintClasses(); }
    dragNode.fx = dragNode.fy = null;
    dragNode = null;
    panning = false;
    return;
  }
  if (!panning) return;
  panning = false;
  canvas.classList.remove("drag");
  if (moved){
    try { canvas.releasePointerCapture(activeId); } catch (_){}
    // A click fires after pointerup; suppress it so releasing a drag over a node
    // does not also toggle that node. Cleared on the next pointerdown.
    justDragged = true;
  }
  activeId = null;
}
function releasePointer(e){
  pointers.delete(e.pointerId);
  if (pointers.size >= 2){ pinch = pinchState(); return; }
  if (pinch){
    pinch = null;
    if (pointers.size === 1){
      // One finger still down after a pinch: hand back to panning from where
      // it currently is, so the map does not jump on the next move.
      const [[id, pt]] = [...pointers.entries()];
      activeId = id; startX = pt.x; startY = pt.y;
      originX = cam[mode].tx; originY = cam[mode].ty;
      panning = true; moved = true;    // a continuing gesture, never a tap
      return;
    }
  }
  endPointer();
}
canvas.addEventListener("pointerup", releasePointer);
canvas.addEventListener("pointercancel", releasePointer);
// Safety net: a finger lifted outside the canvas would otherwise stay in the
// tally forever and leave the map stuck in pinch mode.
addEventListener("pointerup", e => { if (!canvas.contains(e.target)) pointers.delete(e.pointerId); });
addEventListener("pointercancel", e => pointers.delete(e.pointerId));

// -- iOS Safari -----------------------------------------------------------
//
// WebKit delivers a two-finger pinch as its own non-standard GestureEvent
// sequence, and on iOS it does not reliably also deliver two concurrent
// pointers for the same gesture -- it may cancel the second one instead. So
// the pointer-based pinch above, which is correct everywhere else, can leave
// iOS Safari with no zoom at all. These handlers are that platform's path.
//
// `scale` is cumulative from the start of the gesture, so it is differenced
// against the previous event to get a per-frame factor.
let gestureActive = false, gestureScale = 1;

canvas.addEventListener("gesturestart", e => {
  e.preventDefault();
  gestureActive = true;
  gestureScale = e.scale || 1;
  // Any pointer bookkeeping belongs to the gesture now; drop it so the two
  // paths cannot both drive the camera and double the zoom.
  pointers.clear();
  pinch = null;
  panning = false;
  if (dragNode){ dragNode.fx = dragNode.fy = null; dragNode = null; }
});

canvas.addEventListener("gesturechange", e => {
  e.preventDefault();
  if (!gestureActive) return;
  const s = e.scale || 1;
  zoomAt(e.clientX, e.clientY, s / (gestureScale || 1));
  gestureScale = s;
  justDragged = true;
  if (mode === "graph"){ userMoved = true; paintClasses(); }
});

function endGesture(e){
  if (e && e.preventDefault) e.preventDefault();
  gestureActive = false;
  gestureScale = 1;
}
canvas.addEventListener("gestureend", endGesture);
canvas.addEventListener("gesturecancel", endGesture);

canvas.addEventListener("wheel", e => {
  e.preventDefault();
  // Ctrl+wheel is how a trackpad pinch arrives on the desktop; treat it as the
  // same gesture, just finer.
  const step = e.ctrlKey ? 1.04 : 1.1;
  zoomAt(e.clientX, e.clientY, e.deltaY < 0 ? step : 1 / step);
  if (mode === "graph"){
    userMoved = true;
    paintClasses();     // labels are screen-sized, so zoom reveals more of them
  }
}, {passive: false});

let resizeTimer = null;
addEventListener("resize", () => {
  clearTimeout(resizeTimer);
  // Rotating a phone crosses the NARROW breakpoint, which changes the tree's
  // whole viewBox model, so the view has to be rebuilt rather than stretched.
  resizeTimer = setTimeout(() => {
    if (mode === "tree"){ draw(); return; }
    setGraphViewBox();
    if (!userMoved) fitView();
    paintClasses();
  }, 120);
});

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
    if concept.definition_ar:
        d["def_ar"] = concept.definition_ar
    if concept.level:
        d["level"] = concept.level
    if concept.see_also:
        d["rel"] = list(concept.see_also)
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


def build_related(mm: MindMap) -> list[list[str]]:
    """Undirected, deduplicated ``see_also`` pairs.

    The tree carries the hierarchy, so the graph view derives parent edges by
    walking it and only needs the cross-links emitted separately. Sorted so the
    generated file is byte-stable across builds -- ``build.py --check`` compares
    committed output against a fresh render and would otherwise flap.
    """
    pairs: set[tuple[str, str]] = set()
    for c in mm.concepts.values():
        for other in c.see_also:
            if other == c.id or other not in mm.concepts:
                continue
            pairs.add(tuple(sorted((c.id, other))))  # type: ignore[arg-type]
    return [list(p) for p in sorted(pairs)]


def render(mm: MindMap) -> str:
    data = json.dumps(build_tree(mm), ensure_ascii=False, separators=(",", ":"))
    rel = json.dumps(build_related(mm), ensure_ascii=False, separators=(",", ":"))
    # `</script>` inside a JSON string would close the block early.
    data = data.replace("</", "<\\/")
    return (
        _TEMPLATE.replace("__DATA__", data)
        .replace("__REL__", rel)
        .replace("__TITLE__", TITLE)
    )
