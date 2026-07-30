# Web Technologies MindMap — Enhancement Roadmap

> **Status:** Phase 0 in progress.
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
| Architecture | YAML source of truth + generator (README + Markmap + SKOS) |
| Restricted tier | Build the mechanism only; author populates content later |
| Existing course links in `README.md` | Left untouched; author manages Drive sharing directly |

> **Author action item (outside this roadmap, see `RESOURCES.md` once Phase 5 lands):** the two
> Google Drive folders linked from the Flask and Django entries are currently shared with
> `type: anyone` (i.e. publicly readable). Changing that is a Drive-side setting, not a repository
> change. Note that the URLs remain in public git history regardless of later sharing changes.

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
- [ ] `CLAUDE.md` — durable project brief: the golden rule, the restricted-links rule, build
      commands, concept schema in brief, PowerShell notes, pointer to this roadmap
- [ ] `.claude/settings.json` — permission allowlist for the frequently-run build/validate loop
- [ ] `.claude/hooks/guard_generated.py` — `PreToolUse` hook denying hand-edits of generated files
- [ ] `.claude/skills/add-concept/SKILL.md` — guided flow for adding a concept
- [ ] `.claude/skills/publish/SKILL.md` — validate → build → leak-check → site

### 0c. Hygiene and licensing
- [ ] `.gitignore`
- [ ] `LICENSE-CONTENT` — CC BY-SA 4.0 for the mind map, YAML concepts and prose (Apache 2.0 is a
      code licence and a poor fit for a document; it stays in `LICENSE` for `scripts/`)
- [ ] `CONTRIBUTING.md` — the golden rule for human contributors, mirroring `CLAUDE.md`

**Checkpoint:** author review before Phase 1.

---

## Phase 1 — Fix the existing README in place (no generator yet)

Done by hand first, so Phase 2 has a *correct* document to mechanically ingest. Every item below
was verified against the file as committed.

- [ ] 4 dead TOC anchors — `#web-1.0-documents-web` and siblings. GitHub strips the dot, so the
      real anchor is `#web-10---documents-web`. Fix all four Web 1.0–4.0 links.
- [ ] `### Standardizing Entities` — demote to `####` (it is a child of section 1)
- [ ] `### Web 4.0 - Intelligent Web` — demote to `####` (siblings 1.0/2.0/3.0 are `####`)
- [ ] **"Web Security" appears twice** with overlapping content, creating ambiguous
      `#web-security` / `#web-security-1` anchors. Merge into one `#### Web Security` under Web
      Development, keeping the richer prose from the second occurrence.
- [ ] `Angular.js` → `Angular`; add AngularJS separately as `status: legacy`
- [ ] `OWL (Object Web Language)` is wrong — Odoo's is the **Odoo Web Library**
- [ ] `Ressource`/`Ressources` (French spelling), ~6 occurrences → `Resource`/`Resources`
- [ ] bare `mailto:` in the footer → proper markdown link

**Checkpoint:** author reviews the diff before any restructuring begins.

---

## Phase 2 — Extract to YAML + build the generator

### Target layout

```
concepts/
  _taxonomy.yml              # section order, titles, per-section intro prose
  00-pillars/*.yml
  01-introduction/*.yml
  02-evolution/*.yml
  03-web-development/*.yml
  04-additional-topics/*.yml
content/                     # long-form prose partials (Purpose, How to Use, preamble)
scripts/
  build.py                   # orchestrator; --check mode for CI
  validate.py
  builders/{readme,markmap,skos}.py
templates/{README.md.j2,mindmap.html.j2}
docs/                        # GitHub Pages output
dist/webtech.ttl             # generated, gitignored
```

Stack: Python 3 + `PyYAML` + `Jinja2` + `rdflib`. No Node dependency (see Phase 3).

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

- [ ] YAML extraction of all existing concepts
- [ ] `validate.py` — schema and graph integrity
- [ ] `build.py` + README builder, reaching a clean fidelity diff
- [ ] SKOS builder

**Checkpoint:** author reviews the fidelity diff.

---

## Phase 3 — Self-hosted interactive mind map

Generate `docs/mindmap.html` from `templates/mindmap.html.j2`: the concept tree is emitted as a
nested markdown list inside a `<div class="markmap">`, with
[markmap-autoloader](https://markmap.js.org/) rendering it client-side. Content is inlined, so
there is no `fetch`, no CORS issue, and **no Node/npm build step**.

- [ ] `mindmap.html` generation, nodes coloured by `status` (legacy dimmed, emerging accented)
- [ ] Collapse-by-`level` support
- [ ] Demote the MindMeister link to an alternate view rather than the primary one
- [ ] Regenerate the static PNG from this map so the image can no longer drift

**Checkpoint:** open in a browser; node count must equal concept count.

---

## Phase 4 — Content modernization

Add as YAML concepts, with `status` set appropriately:

- [ ] **Languages/tooling:** TypeScript, Vite, esbuild, Bun, Deno, ESM & import maps
- [ ] **CSS/UI:** Tailwind, CSS Grid, Container Queries, component-library patterns
- [ ] **Meta-frameworks:** Next.js, Nuxt, SvelteKit, Astro, htmx, Remix
- [ ] **Protocols/platform:** HTTP/2, HTTP/3 + QUIC, WebAuthn/passkeys, WebRTC, WebGPU,
      Service Workers, Web Components maturity
- [ ] **Performance:** Core Web Vitals (LCP/INP/CLS) — supersedes the thin "Performance
      Optimization" section
- [ ] **AI-era web** (new subsection): LLM APIs, streaming UIs, RAG, embeddings, MCP, agent
      patterns — links forward to the existing Vector Databases entry
- [ ] Mark jQuery, AngularJS and Heroku as `status: legacy`
- [ ] **Web3 disambiguation** — a short prose block distinguishing *Web 3.0 = Semantic Web* (the
      existing framing) from *Web3 = blockchain*. **Author writes or reviews this**: it is his
      research area and the pedagogical judgement is his.

**Checkpoint:** author reviews the new concept list before prose is written for each.

---

## Phase 5 — Restricted-resource mechanism (mechanism only, no content)

- [ ] Renderer support for `access: restricted` plus the 🔒 badge legend in the README
- [ ] `RESOURCES.md` documenting the operational flow:
      1. Set each course folder to **Restricted — specific people**. Drive enforces access: a
         public URL grants nothing on a restricted folder, so the ACL is the control, not link
         secrecy.
      2. Create a **Google Group** (e.g. `webtech-students@…`) and share folders with *the group*,
         not with individuals — granting access then means adding one email, not re-sharing N
         folders.
      3. A Google Form (name / institution / email) as the single request funnel, linked from the
         README.
      4. How to add a restricted entry to a concept's `links:`.
- [ ] One restricted entry in a test fixture only, to exercise the leak check. No real content.

**Checkpoint:** author reviews before populating anything.

---

## Phase 6 — Docs site and CI

- [ ] **MkDocs Material** → GitHub Pages, serving `docs/`: real search, mobile navigation, and a
      stable URL per concept that can be linked from lecture slides
- [ ] GitHub Action on push: `validate.py`, then `build.py --check` — **fails if the committed
      `README.md` differs from the generated one**, so hand-edits cannot silently diverge
- [ ] Weekly scheduled link check (`lychee`) over public URLs. The README has ~150 external links
      and some will have rotted in two years.

---

## Phase 7 — Learning paths

`paths/*.yml` referencing concept `id`s in teaching order with week/hour estimates, rendered to
`LEARNING-PATHS.md`. This turns a reference tree into a curriculum — the highest-value addition
for a *teaching* tool.

- [ ] Front-End Foundations
- [ ] Back-End with Python
- [ ] Full Stack
- [ ] Semantic Web & Knowledge Graphs

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
