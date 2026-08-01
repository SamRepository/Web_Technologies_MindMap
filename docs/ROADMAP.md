# Web Technologies MindMap — Enhancement Roadmap

> **Status:** Phases 0-9 complete, including the Phase 3b graph view.
> All planned phases have landed; what remains is content upkeep.
> **No action outstanding.** GitHub Pages is enabled and deploying from `main` (see Phase 6).
> This file is the in-repo source of truth for what has been done and what comes next.
> Tick the boxes as phases land.

## Context

This repository began as a teaching artifact published in 2024, with an accompanying
[YouTube walkthrough](https://youtu.be/LSzm-eh2KwA). Before this roadmap it consisted of four
files: a 620-line / 53 KB `README.md` acting as a single-file wiki, a 1.4 MB static PNG of the
mind map, a PDF, and `LICENSE`. The *interactive* mind map was not in the repository at all — it
lived on MindMeister, an external service the author does not control.

Three problems motivate this work:

1. **The core artifact isn't owned.** The interactive map depends on a third-party link that can
   rot or go paywalled; the repository only holds a static image that must be manually regenerated.
2. **The single README has hit its ceiling.** Verified defects: 4 broken table-of-contents anchors,
   2 mis-levelled headings, 1 fully duplicated section, plus factual errors — symptoms of a
   hand-maintained file that has outgrown the format.
3. **The content is ~2 years stale in the fastest-moving part of the stack.** TypeScript, Tailwind,
   Vite, Next.js/Nuxt/SvelteKit, HTTP/3, passkeys, Core Web Vitals and the entire AI-era web layer
   are absent; `Angular.js` refers to the framework retired in 2010.

**Intended outcome:** concepts become structured data (YAML) as the single source of truth, from
which the README, a self-hosted interactive mind map, and an RDF/SKOS export are all *generated*.
This removes the MindMeister dependency, makes the map incapable of drifting from the text, makes
future content updates one-place edits, and — since this project's author researches knowledge
graphs and the semantic web — turns the mind map into an actual machine-readable knowledge graph.

A **restricted-resource mechanism** is built alongside it (schema + renderer + operational docs, no
content yet) so private course links can later be published safely: entries marked
`access: restricted` render as a 🔒 request-access badge and their URLs are *structurally* never
emitted into any public artifact.

### Decisions taken

| Decision | Choice |
|---|---|
| Architecture | YAML source of truth + generator (README + interactive map + SKOS) |
| Restricted tier | Build the mechanism only; author populates content later |
| Existing course links in `README.md` | Left untouched; author manages Drive sharing directly |

> **Author action item (outside this roadmap, see `RESOURCES.md` once Phase 5 lands):** the README
> links **four** Google Drive folders, not two — from the HTTP/HTTPS, XML, Flask and Django entries.
> All four are currently shared with `type: anyone`, i.e. readable by anyone who has the link.
> Changing that is a Drive-side setting, not a repository change. Note that the URLs remain in
> public git history regardless of any later sharing change.

---

## Phase 0 — Project harness, plan persistence, and hygiene

**Rationale for going first:** the guard hook and `CLAUDE.md` must exist *before* `README.md`
becomes a generated file. The CI check in Phase 6 catches divergence after the fact; the hook
prevents it at the source — including when a future session or a collaborator's agent doesn't know
the rule. Building the generator first would leave a window where one stray hand-edit silently
reintroduces the exact drift this roadmap exists to eliminate.

### 0a. Persist the plan in-repo
- [x] `docs/ROADMAP.md` — this file, committed so it survives outside any single tooling session

### 0b. `.claude/` harness
- [x] `CLAUDE.md` — durable project brief: the golden rule, the restricted-links rule, build
      commands, concept schema in brief, PowerShell notes, pointer to this roadmap
- [x] `.claude/settings.json` — permission allowlist for the frequently-run build/validate loop
- [x] `.claude/hooks/guard_generated.py` — `PreToolUse` hook denying hand-edits of generated files
- [x] `.claude/skills/add-concept/SKILL.md` — guided flow for adding a concept
- [x] `.claude/skills/publish/SKILL.md` — validate → build → leak-check → site

#### Hook defect found in Phase 7, and fixed

The hook had two independent checks: a glob match, and a **sentinel scan** for the literal banner
`GENERATED FILE` in a file's first 2 KB. The second one misfired on the generators themselves — a
renderer contains that banner as *data*, because it is what it writes into its own output. So
`render_readme.py`, `render_docs.py`, `render_paths.py` and `guard_generated.py` were all
un-editable, and the denial message told the reader to "edit the source under `scripts/webtech/`"
while blocking exactly that. Latent since Phase 0; only surfaced when Phase 7 added a fourth
renderer.

Fix: the sentinel scan is skipped inside the hand-written source trees (`scripts/`, `tests/`,
`concepts/`, `content/`, `paths/`, `.claude/`). `GENERATED_GLOBS` still applies everywhere, so
nothing declared as build output is exempted. `docs/learning-paths.md` was added to the glob list
rather than left to the scan.

Repairing the hook required one deliberate write that bypassed it, since it was blocking its own
repair. `tests/test_guard_hook.py` now pins both halves — 8 build products denied, the four
generators and every source tree allowed, and a negative control proving the sentinel scan still
fires for an unlisted file outside those trees. That test is what makes the bypass a one-off rather
than a precedent.

### 0c. Hygiene and licensing
- [x] `.gitignore`
- [x] `LICENSE-CONTENT` — CC BY-SA 4.0 for the mind map, YAML concepts and prose (Apache 2.0 is a
      code licence and a poor fit for a document; it stays in `LICENSE` for `scripts/`)
- [x] `CONTRIBUTING.md` — the golden rule for human contributors, mirroring `CLAUDE.md`

**Checkpoint:** author review before Phase 1.

---

## Phase 1 — Fix the existing README in place (no generator yet)

Done by hand first, so Phase 2 has a *correct* document to mechanically ingest. Every item below
was verified against the file as committed.

- [x] 4 dead TOC anchors — `#web-1.0-documents-web` and siblings. GitHub strips the dot, so the
      real anchor is `#web-10---documents-web`. Fixed all four Web 1.0–4.0 links.
- [x] `### Standardizing Entities` — demoted to `####` (it is a child of section 1)
- [x] `### Web 4.0 - Intelligent Web` — demoted to `####` (siblings 1.0/2.0/3.0 are `####`)
- [x] **"Web Security" appeared twice** with overlapping content, creating ambiguous
      `#web-security` / `#web-security-1` anchors. Merged into one `#### Web Security` under Web
      Development, keeping the richer "Threats" prose (5 items incl. DDoS and Phishing).
- [x] `Angular.js` → `Angular` (TypeScript-based, angular.dev); AngularJS added separately as an
      explicitly-marked legacy entry
- [x] `OWL (Object Web Language)` was wrong — corrected to **Odoo Web Library**
- [x] `Ressource` (French spelling), 6 occurrences → `Resource`; also `Youtube` → `YouTube`
- [x] bare `mailto:` in the footer → proper markdown link
- [x] Footer licence block updated for the Phase 0 dual licence (was Apache-only)

**Known issue deferred to Phase 4 link triage:** the OWL entry's "Odoo Documentation" link points
at the *ORM* reference page, not OWL. A link checker only catches 404s, not a link aimed at the
wrong target, so this needs a human decision on the replacement URL.

**Checkpoint:** author reviews the diff before any restructuring begins.

---

## Phase 2 — Extract to YAML + build the generator

### Actual layout (as built)

```
concepts/
  _taxonomy.yml              # section/subsection order and headings, prose refs
  00-pillars/*.yml           13    00-disciplines/*.yml       10
  01-introduction/*.yml      26    02-evolution/*.yml         25
  03-web-development/*.yml   51    04-additional-topics/*.yml 26
content/
  header.md, guide_intro.md, footer.md
  sections/<section-id>.md         # per-section intro
  sections/<section-id>-outro.md   # closing paragraph, where one exists
scripts/
  build.py                   # orchestrator; --check is the CI gate
  validate.py                # schema, graph, cycles, anchors, leak check
  fidelity.py                # semantic before/after comparison
  extract_readme.py          # ONE-TIME migration; do not re-run
  webtech/                   # slug, model, loader, checks,
                             # render_readme, render_mindmap, render_skos
docs/                        # MkDocs source; mindmap.html generated into it
dist/webtech.ttl             # generated AND committed (published artifact)
site/                        # mkdocs output, gitignored
```

Stack: Python 3.12 + `PyYAML` + `rdflib`. No Node dependency, and no template
engine — Jinja2 was in the plan but proved unnecessary: the renderers assemble
line lists directly, which keeps whitespace (significant in nested markdown)
explicit rather than hidden in template indentation. `templates/` was therefore
never created.

### Concept schema

```yaml
id: typescript                     # unique, kebab-case
label: TypeScript
parent: frontend-languages         # must resolve to another id, or null for a top concept
section: 03-web-development
level: intermediate                # beginner | intermediate | advanced
status: current                    # current | emerging | legacy
aliases: [TS]
see_also: [javascript, esnext]
definition: >
  Typed superset of JavaScript that compiles to plain JS...
links:
  - {type: official, label: Official Website, url: 'https://www.typescriptlang.org/'}
  - {type: course, label: Full Stack Open Part 9, url: '...', access: public}
  - type: course                   # restricted example — NO url key at all
    label: TP recordings
    access: restricted
    drive_folder_id: <id>
    audience: webtech-students
```

`type` ∈ `official | wikipedia | mdn | spec | video | course`. `access` defaults to `public`.

### The non-negotiable rule

`access: restricted` → public artifacts render `🔒 <label> — [request access](FORM_URL)` and
**never** emit the URL or folder ID. Full URLs live only in `private/RESOURCES-gated.md`, which is
gitignored. `validate.py` fails the build if any restricted identifier appears in `README.md`,
`docs/`, or `dist/`.

### SKOS mapping

Each concept → `skos:Concept` with `skos:prefLabel`, `skos:definition`, `skos:altLabel` (aliases),
`skos:broader` (parent), `skos:related` (see_also). Each section → `skos:ConceptScheme` +
`skos:hasTopConcept`. Links → `rdfs:seeAlso`. Restricted links are omitted from RDF entirely.

### Fidelity gate

Regenerate `README.md` from the YAML and diff against the Phase 1 hand-corrected file. The
generator must reproduce it near-identically — this is what proves the extraction lost nothing.

- [x] YAML extraction of all existing concepts — **151 concepts, 200 links**
- [x] `validate.py` — schema, graph, cycles, anchors, restricted-leak
- [x] `build.py` (+ `--check` CI gate) and the README builder
- [x] SKOS builder
- [x] `fidelity.py` — the acceptance gate; **result: 0 headings, 0 labels, 0 definitions and
      0 URLs lost** (31 / 161 / 141 / 198 preserved)

**Deviation from plan, deliberate:** byte-identical reproduction was abandoned as a goal, because
the source mixes 2-, 4-, 5- and 6-space indentation for the same nesting depth, has trailing
whitespace on some link bullets but not others, and varies blank-line usage between sections. The
generator normalises all of that. `fidelity.py` therefore compares *content sets* — every label,
definition and URL — which is a stronger guarantee than a byte diff: it cannot be satisfied by
accident, and it tolerates only formatting change.

**URI design:** concepts are `wtc:<id>`, schemes `wts:<id>`, project predicates `wt:<term>`. Three
namespaces rather than one, so every term is a legal SPARQL prefixed name — a single namespace with
`concept/<id>` local parts puts a slash inside the local name and makes `wtc:django` unparseable.

**Checkpoint:** author reviews the fidelity diff.

---

## Phase 3 — Self-hosted interactive mind map

- [x] `docs/mindmap.html` generated by `scripts/webtech/render_mindmap.py`
- [x] Nodes coloured by `status` (legacy dimmed and italic, emerging accented)
- [x] Collapse/expand per node, expand-all, collapse-all, pan, zoom
- [x] Search across labels *and* definitions, auto-revealing matches by opening ancestors
- [x] Side panel per concept: breadcrumb trail, definition, status/level badges, resource links
- [x] Restricted links render as a 🔒 badge with no URL present in the data at all
- [x] MindMeister kept as a documented **backup** view (author's decision), with a note that the
      hosted copy is hand-maintained and may lag the repository
- [ ] Regenerate the static PNG from this map — **not done**, see below

**Deviation from plan, and why.** The plan specified markmap via `markmap-autoloader`, and in the
same breath required the map to "render offline (no network)". Those contradict: the autoloader
fetches the rendering library from a CDN. More importantly, the *point* of this phase is to stop the
project's central artifact depending on a service the author does not control — swapping MindMeister
for a CDN would trade one such dependency for another.

`render_mindmap.py` therefore emits a self-contained file with **no external JavaScript at all**:
layout, interaction and styling are plain inline JS and CSS. Consequences:

- works from a local disk with no network, which matters for classrooms with poor connectivity;
- survives strict Content-Security-Policy contexts that block third-party script origins;
- nothing third-party is vendored into the repository, so no bundled licences and nothing to go
  stale;
- the trade-off is that the layout is a clean collapsible indented tree rather than markmap's
  curved radial style. If the radial look is wanted, markmap can be added later as a second view.

**Static PNG not regenerated.** Doing so needs a headless browser to rasterise the HTML, which is
not available in this environment. The existing PNG (a MindMeister export) is retained as-is and is
still accurate as an overview. Options for later: export from MindMeister after syncing it, or add
a Playwright screenshot step.

**Verified:** 151 concepts in the map == 151 in the YAML (174 nodes including 6 sections, 16
subsections and the root); script parses under `node --check`; 0 external `script`/`link` tags;
46 rows on first load expanding to 174; search returns expected hits; guard hook denies hand-edits
of `docs/mindmap.html`.

### Phase 3b — graph view (added after Phase 6)

- [x] A second view in the same file, switched by a **Tree / Graph** toggle in the header
- [x] Force-directed layout over **hierarchy edges + `see_also` cross-links**, the latter dashed and
      in a contrasting colour
- [x] Nodes coloured by top-level section; `emerging` ringed, `legacy` faded and italic
- [x] Click to focus: the node and its neighbours stay lit, the rest of the graph dims
- [x] Node dragging, auto-fitting camera, constant-screen-size labels with collision suppression
- [x] A **Related** list added to the details panel in *both* views, with click-to-jump
- [x] 27 browser tests (desktop + touch) + 10 offline data tests

**Why not d3-force, Sigma.js, Cytoscape.js or cosmos.gl.** All four are engineered for graphs of
10k–1M nodes; this one has 217 nodes and 252 edges, where a naive O(n²) many-body pass is ~47k
pair evaluations per tick and finishes well inside a frame. Quadtrees, WebGL and Web Workers would
buy nothing measurable, while every one of them would cost the offline/CSP guarantee that Phase 3
was built to establish. The simulation is therefore ~90 lines of inline JS. SVG rather than canvas
for the same reason: at this size it holds frame rate, and it keeps the CSS custom properties, the
dark-mode palette, real text nodes, and the DOM handles the Playwright suite drives.

### Touch zoom, and the framing that hid the need for it

Reported from a phone after Phase 7 shipped: neither view could be zoomed. Two causes, both real.

- **No pinch handler existed.** `touch-action:none` is required so a one-finger drag pans the map
  instead of scrolling the page — but it also suppresses the browser's own pinch. Zoom was
  therefore wheel-only, and a phone has no wheel. Two-pointer pinch is now implemented directly,
  anchored to the midpoint between the fingers, and it pans and zooms in the same gesture. Wheel
  zoom is anchored at the cursor for the same reason, and `Ctrl`+wheel (how a trackpad pinch
  arrives) is treated as a finer version of the same thing.
- **The tree fitted all 217 rows into the viewport**, which on a 390px screen renders labels at
  about **4 CSS px** — so the missing zoom was unworkable rather than merely inconvenient. Narrow
  screens now use a window model: one user unit is one CSS pixel, labels are 12.5px, and the reader
  pans to what is below the fold. Wide screens keep the fit-to-content behaviour they had, pinned
  by a test.

**iOS Safari needed a second path.** Reported from an iPhone after the above was written. WebKit
delivers a two-finger pinch as its own non-standard `gesturestart`/`gesturechange`/`gestureend`
sequence, and on iOS it does not reliably also deliver two concurrent pointers — it may cancel the
second one. The pointer implementation, which is correct everywhere else, therefore left that one
platform with no zoom at all. There is now a `GestureEvent` handler alongside it, with a flag so
the two can never both drive the camera and double the zoom. `touch-action:none` also had to move
onto the `#canvas` wrapper: iOS consults the element a gesture starts on *and its ancestors*, and
claims the pinch for its own page zoom if an ancestor says `auto`.

Desktop WebKit runs the pointer path happily, so this difference is invisible to a Chromium-only
suite. `tests/test_mindmap_ui.py` now has a WebKit class covering both paths and their
interleaving; it skips when that engine is not installed, as it is not in CI.

Two more things fell out of measuring this. The graph's fixed 1400×950 viewBox was being letterboxed
into the canvas and then `fitView` fitted the graph inside *that* — two nested fits, leaving a
portrait phone with the map in a band across the middle. The viewBox now tracks the canvas, so
framing is `fitView`'s job alone. And graph labels were sized by camera zoom only, ignoring the
viewBox fit factor; correcting that lifted the desktop label count from about 60 to 107 as well.

**What the data actually looks like, and why it shaped the design.** Measured before building:
193 concepts, 109 `parent` edges, but only **36 unique `see_also` edges**, with **141 concepts
(73%) having none at all**. An Obsidian-style view driven by cross-links alone would therefore have
rendered mostly isolated dots. Hierarchy is the skeleton and cross-links are a second, visually
distinct layer on top — which is both honest about the data and the thing that makes the few
cross-links legible. See Phase 8.

---

## Phase 4 — Content modernization

**42 concepts added; total 151 → 193.** All 42 carry at least one authoritative link, so the
advisory count for concepts lacking a primary source is unchanged at 6 (all pre-existing).

- [x] **Languages/tooling:** TypeScript, ES Modules, Import Maps, Vite, esbuild, Deno, Bun
      (a new `Build Tooling` group holds Vite and esbuild)
- [x] **CSS/UI:** Tailwind CSS, CSS Grid Layout, Container Queries
- [x] **Frameworks:** Svelte, htmx, and a `Meta-Frameworks` group — Next.js, Nuxt, SvelteKit,
      Remix, Astro
- [x] **Protocols:** HTTP/2, HTTP/3, QUIC (nested under the existing HTTP/HTTPS entry)
- [x] **Security — a new `Defenses` group.** The section previously listed only threats, with no
      countermeasures at all: TLS/HTTPS, WebAuthn and Passkeys, CSP, CORS. Each cross-references
      the threat it addresses (CSP↔XSS, passkeys↔phishing).
- [x] **Performance:** Core Web Vitals with LCP, INP and CLS as children
- [x] **Platform:** WebGPU, WebRTC, Service Workers (under PWAs)
- [x] **AI-Era Web** — new subsection: LLMs, Prompt Engineering, Embeddings, RAG, MCP,
      Streaming Responses, AI Agents. Cross-linked to the existing Vector Databases, Knowledge
      Graphs, NLP and Agents entries rather than duplicating them.
- [x] jQuery, AngularJS and Heroku marked `status: legacy` (done in Phases 1–2)
- [x] **Web3 disambiguation** — added as the *first* entry in the Web 3.0 subsection (`order: 0`),
      before the material whose ambiguity it resolves. **Author review requested** (see below).

Status spread after this phase: 185 `current`, 5 `emerging` (Container Queries, Import Maps,
WebGPU, MCP, AI Agents), 3 `legacy`.

### Author review requested: the Web3 note

The concept `web3-disambiguation` states that in this project **Web 3.0 = the Semantic Web**, and
that **Web3** is a separate, later coinage from the cryptocurrency industry. It was drafted rather
than left blank so the gap is not shipped, but the pedagogical framing is the author's call — this
is his research area. Note the tension it resolves: the subsection already contained
`blockchain-and-decentralization` under *Web 3.0 — Semantic Web*, which is precisely the conflation
the note now addresses. Consider whether that entry should move, be reframed, or stay as-is.

### Link verification: NOT done in this environment

The 68 new URLs could **not** be verified here — the sandbox has no outbound network, so every
`curl` returned `000`. Six of the least-certain were checked through a different path and all
resolve; three MDN links were found to have moved and were corrected to their canonical form:

| Was | Now |
|---|---|
| `Web/HTTP/CSP` | `Web/HTTP/Guides/CSP` |
| `Web/HTTP/CORS` | `Web/HTTP/Guides/CORS` |
| `Web/HTML/Element/script/type/importmap` | `Web/HTML/Reference/Elements/script/type/importmap` |

The remaining 62 are unverified. **Phase 6's link checker must therefore report redirects, not only
404s** — the old MDN paths above returned 200 via redirect, so a 404-only check would have passed
them while the canonical URL silently drifted. One pre-existing link is a known suspect:
`Learn/Common_questions/What_are_browser_developer_tools`, from before this roadmap.

## Phase 5 — Restricted-resource mechanism (mechanism only, no content)

- [x] Renderer support for `access: restricted`, plus the conditional access section so a 🔒 badge
      always has a working anchor target
- [x] `access_request_url` in `concepts/_taxonomy.yml` — when set, badges link to an external form
      instead of the in-page section
- [x] [RESOURCES.md](https://github.com/SamRepository/Web_Technologies_MindMap/blob/main/RESOURCES.md) — the operations guide: Restricted sharing, a Google Group as
      the grant mechanism, one request funnel, the gitignored private index, and how to add an entry
- [x] `tests/test_restricted.py` — the guarantee under automated test, replacing Phase 2's one-off
      manual check
- [x] **No restricted content configured.** The tier is empty by design; the author populates it.

### The security property, stated precisely

Drive enforces access on the folder, not on the link: a *Restricted* folder cannot be opened with
the exact URL by someone not on the sharing list. Link secrecy is therefore not the control — but
this project withholds URLs anyway, because a URL never published cannot be scraped, archived, or
inherited by a reader if a folder's sharing is later loosened by accident.

**What the checks guarantee:** a restricted entry has no `url` and does have a `drive_folder_id`
(`check_schema`); no restricted identifier appears in `README.md`, `docs/**` or `dist/**`, verified
from the *output* side so it does not trust the renderer (`check_restricted_leak`); `build.py`
refuses to write anything if a leak is found.

**What they do not guarantee, stated in RESOURCES.md so it is not assumed:** git history (a URL
committed once stays committed), Drive sharing (nothing here can read or change an ACL — a 🔒 badge
on an `anyone`-shared folder is decorative), and redistribution by people already granted access.

### Tests: 26 tests, 23 subtests

`tests/test_restricted.py` and `tests/test_anchors.py` cover the leak guarantee, badge rendering,
the anchor-target regression, schema rejection of unsafe input, both slug algorithms, GitHub's
duplicate-heading disambiguation, and that the committed README matches a fresh render.

One of these is a **negative control**: it plants a secret in a fake artifact and requires the leak
check to find it. Without that, the check passing on clean input would prove nothing — it would be
indistinguishable from a check that never fires at all.

## Phase 6 — Docs site and CI

- [x] **MkDocs Material site** — `mkdocs.yml`, a hand-written `docs/index.md`, and generated
      reference pages under `docs/reference/` (one page per section, plus an index)
- [x] **A stable anchor for every concept.** All 193 use `{#concept-id}` on headings or an inline
      `<span id="...">`, verified unique and id-based. Label-derived anchors would break on any
      rewording; ids do not — so a link in a lecture slide keeps working.
- [x] `.github/workflows/ci.yml` — tests, `validate.py`, `build.py --check`, `mkdocs build --strict`
- [x] `.github/workflows/pages.yml` — deploy to Pages, gated on output not being stale
- [x] `.github/workflows/links.yml` — weekly link check
- [x] `requirements.txt`, with mkdocs pinned `<2.0`
- [x] **Enable GitHub Pages** — done by the author on 30 July 2026

### Pages: enabled and deploying

**Settings → Pages → Build and deployment → Source: GitHub Actions.** Nothing in the repository
could do this; it was an author action and it has been taken. The site publishes to
[samrepository.github.io/Web_Technologies_MindMap](https://samrepository.github.io/Web_Technologies_MindMap/),
so the interactive mind map is a clickable link rather than a file to download.

`pages.yml` triggers on pushes to `main` only. Work on a branch is therefore *not* on the public
site until it is merged — which is correct, but worth knowing when a newly added page appears to
404.

### Link checker: a custom script, not lychee

The plan named lychee. It was not used, because the requirement is to surface links that *moved*,
not only links that broke — and lychee cannot express that. It follows redirects and reports OK;
making it fail on 3xx (`--max-redirects 0`) would flag every harmless `http`→`https` and
trailing-slash normalisation instead.

`scripts/check_links.py` walks each redirect chain and classifies the outcome:

| Verdict | Meaning |
|---|---|
| `OK` | 2xx, final URL == requested URL |
| `MOVED` | 2xx, but the canonical URL differs meaningfully — **update the link** |
| `NORMALISED` | 2xx, differs only by scheme upgrade or trailing slash — ignore |
| `DEAD` | 4xx / 5xx / connection failure |

This matters concretely: the three MDN links corrected in Phase 4 all returned **HTTP 200 via
redirect** while their canonical URL had changed underneath. A 404-only checker passes those in
silence while the taught address drifts away from the content. Standard library only, so CI installs
nothing for it.

### Link verification still has not run

Confirmed again in Phase 6: this environment sits behind a proxy that permits PyPI but returns
**403 for general web traffic**, so every URL would be reported `DEAD` — a verdict obtained here
would be worse than none. The ~270 links are therefore **unverified**; the weekly workflow is what
will actually check them, on the first Monday after Pages is enabled (or via *Run workflow*).

The checker's classification logic *is* tested offline, in `tests/test_check_links.py` — that is
where the MOVED/NORMALISED distinction is pinned, since it needs no network to verify.

### `--strict` earned its place immediately

The first `mkdocs build --strict` failed on a real defect introduced in Phase 5: `docs/ROADMAP.md`
linked to `../RESOURCES.md`, which is outside the docs tree, so MkDocs could not resolve it. Fixed
with an absolute repository URL, which resolves from both GitHub and the published site.

## Phase 7 — Learning paths

`paths/*.yml` referencing concept `id`s in teaching order with week/hour estimates, rendered to
`LEARNING-PATHS.md`. This turns a reference tree into a curriculum — the highest-value addition
for a *teaching* tool.

**Done.** `paths/*.yml` → `LEARNING-PATHS.md` and `docs/learning-paths.md`.

- [x] Front-End Foundations — beginner, 9 modules, 12 weeks, 77 h, 55 concepts
- [x] Back-End with Python — intermediate, 10 modules, 14 weeks, 86 h, 48 concepts
- [x] Full Stack — advanced, 8 modules, 13 weeks, 85 h, 44 concepts
- [x] Semantic Web & Knowledge Graphs — advanced, 8 modules, 11 weeks, 66 h, 37 concepts

Together they sequence **145 of 193 concepts**. The other 48 are reference-only by design — the
map is something to look things up in as well as a course — so coverage is reported by
`validate.py` as an advisory and never fails a build.

### A path adds no content

A module lists concept **ids**, in teaching order, with a goal and one practice exercise. It never
restates a definition. That is the property that stops a curriculum becoming a second source of
truth: correct a definition once and every path is corrected; cite a concept that does not exist
and the build refuses. `tests/test_paths.py` fails if a definition's text appears verbatim under
`paths/`.

Enforced by `checks.check_paths`: ids resolve, no concept appears twice **within** one path
(always a copy-paste slip in practice), prerequisites resolve and do not cycle, weeks and hours are
positive. The same concept in two different paths is normal — `javascript` is taught in three.

### Two renderings, differing in one respect

`LEARNING-PATHS.md` prints concept names as plain text. `docs/learning-paths.md` links each one to
its anchor in the reference. The split is not cosmetic: GitHub does not parse the `{#id}`
attribute-list syntax those anchors are built from, so a link from the root file would land on the
right page at the wrong place — and this project does not ship links it cannot verify.

The site's ~180 concept links *are* verified. `mkdocs.yml` now sets `validation.anchors: warn`,
which under `--strict` turns a fragment that does not exist into a build failure. Confirmed with a
negative control: a planted `#no-such-concept-id` aborts the build, so the check is known to fire
rather than merely known to pass.

### Author review requested

The week and hour estimates, and the choice of what each module contains, are pedagogical
judgements drafted from the concept data — they are a starting point for the person who teaches
this course, not a measurement. The Odoo block in Full Stack is weighted at 3 weeks / 21 hours on
the assumption it is the centre of that module; adjust freely.

## Phase 9 — Arabic

A second definition per concept, shown in the detail pane under the English. Requested because the
students this map is taught to read Arabic, and a reference that exists only in English asks them
to learn the vocabulary twice.

**Schema.** `definition_ar`, optional and independent. Two rules the build enforces: it cannot
exist without `definition` (it is a translation, so a bare Arabic paragraph means the English was
deleted by mistake), and it must contain Arabic script — which catches English pasted into the
wrong field, a mistake that renders as a left-to-right paragraph inside a right-to-left block and
so looks broken rather than wrong. Coverage is an advisory and never fails a build.

**Register, decided with the author.** Modern Standard Arabic, with technical terms giving the
Arabic followed by the Latin token in parentheses: `بروتوكول نقل النصّ الفائق (HTTP)`. Students need
the Arabic concept *and* the token they will meet in every spec and error message. **17 concepts
are translated so far**, spread across all six sections so the register can be judged on a sample
before the remaining 159 are written. Nothing is machine-translated — there is no translation step
in `build.py`, and there will not be one.

**Direction.** `dir="rtl"` is an attribute on the paragraph rather than a CSS rule, because it is a
property of the text and not of its presentation: it drives the bidirectional algorithm, so an
embedded Latin term orders correctly mid-sentence. Naskh faces also need more leading than Latin at
the same size, hence the separate `line-height`.

**Where it surfaces.** The detail pane, and `dist/webtech.ttl` as a second `skos:definition` tagged
`@ar`. Multilingual labels are what SKOS is *for*, so `langMatches(?d, "ar")` now works against the
export. Deliberately not the README or `docs/reference/**` — that would roughly double both.

**Arabic Wikipedia.** `scripts/fetch_ar_wikipedia.py` resolves them from the existing English links
via the langlinks API: of 147 candidates, **133 have an Arabic article and 131 were written**. The
five under 2 KB were held back — Arabic Wikipedia's coverage here is uneven, and sending a student
to a two-sentence stub is worse than sending them nowhere; they are listed for the author to opt
into deliberately. Fourteen have no Arabic article at all. Network at tooling time only, exactly
like `check_links.py`; the URLs land in the YAML, so nothing published depends on the script.

One bug worth recording: the resolver first keyed its work by *English article title*, which
silently dropped one concept from each of the four pairs citing the same article — Algorithm is
cited by both `algorithms` and `algorithmic`. It surfaced only because a second run reported 22
concepts outstanding where 19 were expected. Re-running is now idempotent.

- [x] `definition_ar` through the schema, loader, validator and both renderers
- [x] RTL detail pane with an `العربية` toggle, shown by default
- [x] `skos:definition` with `@ar` in the RDF export
- [x] 17 sample translations across all six sections
- [x] 131 `Wikipedia (Ar)` links resolved, 5 stubs held back
- [x] 33 new tests (24 offline + 9 browser)
- [ ] **Author review of the register**, then the remaining 159 translations

## Phase 8 — Enrich `see_also`

**Done: 36 → 109 cross-links; concepts with no cross-link at all 141 → 65.** 50 concept files
touched, selected for teaching value rather than completeness.

The selection rule: a `see_also` must state something the hierarchy does not already show, and must
be a relation a student needs. Parent–child pairs were therefore excluded by construction
(`tests/test_graph_data.py` now enforces this), and so were most sibling pairs — the tree already
puts siblings next to each other.

- **The two primers stopped being islands.** `00-pillars` and `00-disciplines` had **zero**
  cross-links between them and the other 170 concepts, despite existing to make the rest
  comprehensible. Each discipline now reaches its concrete material: Networking→TCP/IP,
  Databases→SQL, Cyber Security→Threats/Defenses, Information Systems→ERP.
- **The historical arc.** Web 1.0 Static Pages→JAMstack/Astro, Search Engines→SEO, Web 2.0 Dynamic
  Web→JavaScript/SPAs. The field cycling back on itself is invisible in a tree.
- **Semantic web ↔ ordinary development**, this project's research area: SPARQL→SQL, Knowledge
  Graphs→Graph Databases, Linked Data→URI/URL, RDF→XML.
- **Cause and effect split across the tree:** SQL→SQL Injection, XSS→DOM Manipulation,
  CORS→RESTful APIs, ORM→OOP/SQL, jQuery→DOM Manipulation.
- **`Angular`↔`AngularJS`**, the one sibling pair deliberately included: conflating them is the
  named hazard in `CLAUDE.md`.

Removed: `service-workers → progressive-web-apps`, which restated its own parent.

Two supporting changes made this batch cheap to maintain:

- **The panel's Related list is symmetric.** `skos:related` is symmetric, so an edge is declared in
  **one** YAML file and the renderer builds a reverse index. Clicking `SQL` lists SPARQL, ORM and
  SQL Injection even though `sql.yml` declares none of them.
- **A `Cross-links` toggle** in the graph header, since 109 dashed edges are the lesson in one
  moment and clutter in another. Hidden, not removed — the edges stay in the simulation, so
  toggling never rearranges the graph mid-explanation.

**Explicitly rejected:** inferring edges from shared vocabulary in definitions. In a teaching
reference, an inferred relation that renders identically to an authored one is a claim the author
never made.

**Left for the author.** `owl` (Web Ontology Language) and `owl-odoo-web-library` share a name and
nothing else. A `see_also` would assert `skos:related`, which would be false — the correct fix is a
sentence of prose in one or both definitions, and the wording is a pedagogical call.

---

## Verification

Run after each phase; all of it becomes the CI gate in Phase 6.

1. **Schema/graph integrity** — `python scripts/validate.py`: unique `id`s, every `parent` and
   `see_also` resolves, no cycles, required fields present, `level`/`status`/`type` within allowed
   sets.
2. **Anchor resolution** — extract every in-page TOC link from the generated README and assert each
   matches a generated heading slug (GitHub's algorithm: lowercase, strip punctuation, spaces→`-`).
   *This is the check that would have caught the current 4 dead anchors; it must not regress.*
3. **Restricted-leak check** — grep generated `README.md`, `docs/`, `dist/webtech.ttl` for any
   Drive URL or folder ID belonging to an `access: restricted` link. Must be zero; fails the build.
4. **Generator fidelity** — `python scripts/build.py --check` exits non-zero if committed output
   differs from freshly generated. After Phase 2, `git diff --stat README.md` should be ~empty.
5. **RDF validity** — parse `dist/webtech.ttl` with `rdflib`; SPARQL sanity queries: total
   `skos:Concept` count matches the YAML file count, no concept lacks `skos:prefLabel`, no orphan
   `skos:broader` target.
6. **Mind map** — open `docs/mindmap.html` in a browser; confirm it renders with no network access,
   the root expands to all sections, and node count equals concept count.
7. **Site build** — `mkdocs build --strict` (warnings become errors, catching broken internal refs).
8. **Link rot** — `lychee` over public URLs; triage 404s.
9. **Harness** — attempt an `Edit` on `README.md` and confirm the guard hook denies it with the
   redirect message; confirm the same edit to a `concepts/*.yml` file is allowed; confirm
   `.claude/settings.local.json` is git-ignored while `.claude/settings.json` is tracked.

## Risks

- **Phase 2 is the risky step.** Mechanically converting 620 lines of prose into YAML can silently
  drop content. Mitigated by the fidelity gate (verification #4): the generator must reproduce the
  Phase 1 README before any restructuring is accepted.
- **Scope.** Phases 4 and 7 are open-ended content work. They are deliberately last, so the
  machinery is proven and useful even if content lands incrementally.
