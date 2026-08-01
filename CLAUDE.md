# CLAUDE.md — Web Technologies MindMap

Project brief for agents and contributors working in this repository.
Roadmap and current phase: **[docs/ROADMAP.md](docs/ROADMAP.md)**.

## What this project is

A teaching mind map of web technologies, published by Samir SELLAMI, used with students and
accompanied by a [YouTube walkthrough](https://youtu.be/LSzm-eh2KwA). It is a *pedagogical
reference*, not an application — correctness of definitions and stability of links matter more
than anything else here.

---

## Golden rule: `README.md` is GENERATED

From Phase 2 onward, `README.md` is build output. **Never hand-edit it.** To change what appears
in the README, edit the owning file under `concepts/` or `content/` and rebuild.

A `PreToolUse` hook (`.claude/hooks/guard_generated.py`) denies writes to generated files, so an
attempted edit will fail with a message naming the file to edit instead. This is intentional — do
not work around it by shelling out to `sed`, `Set-Content`, or a Python script. If a generated
file is wrong, the *generator or its source data* is wrong.

### Generated (never hand-edit)
- `README.md`
- `docs/mindmap.html`
- `docs/reference/**`
- `LEARNING-PATHS.md`, `docs/learning-paths.md`
- `dist/**`, `site/**`

### Hand-written (edit freely)
- `concepts/**/*.yml` — the concept data, **the actual source of truth**
- `paths/*.yml` — learning paths: an *ordering* over concept ids, no content of its own
- `content/*.md` — long-form prose partials
- `scripts/**` — the generator and its tests
- `tests/**` — the test suite
- `docs/ROADMAP.md`, `CONTRIBUTING.md`, `RESOURCES.md`, this file

`docs/` follows the MkDocs convention: it holds *source* markdown (some hand-written, some
generated into it), while `site/` is the built HTML and is gitignored.

---

## Restricted links: the non-negotiable rule

Some course resources are private, shared only with specific people via Google Drive. A link
marked `access: restricted` **must never have its URL or Drive folder ID appear in any public
artifact** — not in `README.md`, not in `docs/`, not in `dist/*.ttl`, not in a commit message.

Public artifacts render restricted entries as a badge only:

```
🔒 Course name — [request access](FORM_URL)
```

Full URLs belong only in `private/RESOURCES-gated.md`, which is gitignored. `scripts/validate.py`
fails the build if a restricted identifier leaks into a public output — treat a failure there as a
security finding, not a lint error. `tests/test_restricted.py` holds this property under test,
including a negative control proving the check can detect a planted secret.

Operational guide for this tier: [RESOURCES.md](RESOURCES.md).

Corollary: **do not add a URL to a `restricted` link entry in YAML.** Use `drive_folder_id` plus
`audience`. The renderer never emits either.

---

## Concept schema

One concept per file under `concepts/<section>/<id>.yml`:

```yaml
id: typescript                     # unique, kebab-case, matches filename
label: TypeScript
parent: frontend-languages         # another concept id, or null for a top concept
section: 03-web-development
level: intermediate                # beginner | intermediate | advanced
status: current                    # current | emerging | legacy
aliases: [TS]                      # optional
see_also: [javascript]             # optional, concept ids
definition: >
  Typed superset of JavaScript that compiles to plain JavaScript...
definition_ar: >-                  # optional Arabic translation of definition
  مجموعة عليا مُنمَّطة من جافاسكريبت (JavaScript) تُترجَم إلى جافاسكريبت عادية...
links:
  - {type: official, label: Official Website, url: 'https://www.typescriptlang.org/'}
  - type: course
    label: TP recordings
    access: restricted             # NO url key — see the rule above
    drive_folder_id: <id>
    audience: webtech-students
```

`type` ∈ `official | wikipedia | mdn | spec | video | course | reference`
(`reference` is the catch-all for an authoritative page that is none of the others).
`access` ∈ `public | restricted`, defaulting to `public`.

Use `/add-concept` rather than writing these by hand — it validates as it goes.

### Arabic (`definition_ar`)

Every concept with a definition is translated (176/176). The field stays optional, so a new
concept without Arabic simply shows no Arabic block and is reported as an advisory. Rules the build enforces — `definition_ar` cannot exist without `definition` (it translates
it), and it must actually contain Arabic script, which catches English pasted into the wrong field.
Coverage is reported by `validate.py` as an advisory and never fails a build.

Conventions, set with the author:

- **Modern Standard Arabic**, matching the register of the English.
- **Technical terms give the Arabic followed by the Latin token in parentheses** — e.g.
  `بروتوكول نقل النصّ الفائق (HTTP)`. Students need the Arabic concept *and* the token they will
  meet in every spec, error message and search result.
- Never machine-translated at build time. It is authored content, held to the same standard as the
  English, and there is no translation step in `build.py`.

Where it surfaces: the mind map detail pane (RTL, under the English, toggled by the `العربية`
button) and `dist/webtech.ttl` as a second `skos:definition` tagged `@ar`. Deliberately *not* in
the README or `docs/reference/**` — that would roughly double both.

`scripts/fetch_ar_wikipedia.py` resolves `Wikipedia (Ar)` links from each existing English
Wikipedia link via the langlinks API. Network at tooling time only, same as `check_links.py`; the
URLs are written into the YAML so nothing published depends on it. It skips articles under 2 KB by
default — Arabic Wikipedia's coverage of web technology is uneven, and sending a student to a
two-sentence stub is worse than sending them nowhere. Re-running is safe; it skips what is done.

---

## Learning path schema

One path per file under `paths/<id>.yml`. A path **sequences concept ids and adds no content of
its own** — that is what keeps a curriculum from drifting away from the reference it teaches.

```yaml
id: front-end-foundations          # unique, kebab-case, matches filename
title: Front-End Foundations
level: beginner                    # beginner | intermediate | advanced
order: 10                          # display order
hours_per_week: 6
summary: >                         # one paragraph, shown in the index table
audience: >                        # who it is for
outcome: >                         # what you can do at the end
prerequisites: [ ]                 # other path ids; cycles are rejected
modules:
- title: How the web actually works
  weeks: 1
  hours: 6
  goal: >                          # why this module exists
  concepts: [dns, http-https]      # concept ids, in teaching order
  practice: >                      # one concrete exercise
```

Rules the build enforces: every concept id must resolve; a concept may appear **once per path**
(twice is a copy-paste slip — a genuine second pass belongs in its own module with its own hours);
prerequisites must resolve and must not cycle; `weeks` and `hours` must be positive. Concepts
appearing in *different* paths is normal and expected.

Do not paste a concept's definition into a path — `tests/test_paths.py` fails if a definition's
text appears verbatim in `paths/`.

---

## Commands

```bash
python -m pytest tests/ -q          # 160 tests: leak/slugs/anchors/UI/touch/Arabic/paths/hook
python scripts/validate.py          # schema + graph integrity + restricted-leak check
python scripts/build.py             # regenerate README, mindmap, SKOS
python scripts/build.py --check     # non-zero exit if committed output is stale (CI gate)
mkdocs build --strict               # build the site; warnings are errors
mkdocs serve                        # local preview

# Prove a restructuring lost no content (compare against any git ref):
python scripts/fidelity.py --before HEAD:README.md --after README.md
```

`scripts/extract_readme.py` is the one-time Phase 2 migration that produced `concepts/` from the
hand-written README. It is kept for auditability; do not run it again — it would overwrite the
concept files from whatever `README.md` currently contains, i.e. backwards.

Or use `/publish`, which runs the full validate → build → leak-check → site sequence in order.

---

## Content conventions

- **Spelling is `Resource`, not `Ressource`.** The French spelling was present throughout the
  original README and has been corrected; do not reintroduce it.
- Every concept needs at least one authoritative link (`official`, `spec`, `mdn`, or `wikipedia`).
  Prefer primary sources over blog posts.
- Mark superseded technology `status: legacy` rather than deleting it — students encounter old
  tutorials and need to know what is dated. jQuery, AngularJS and Heroku are legacy.
- `Angular` is the modern framework; `AngularJS` is the separate, retired 2010 one. Do not conflate.
- Web 3.0 in this project means the **Semantic Web**. Where students may read "Web3" as blockchain,
  the disambiguation prose is deliberate — do not "simplify" it away.
- Prefer free, durable, primary resources (MDN, web.dev, CS50, Full Stack Open, The Odin Project)
  over links that require a subscription or that redistribute paid course material.

---

## Environment notes

- Development is on **Windows (win32)**. The default shell is **PowerShell 5.1**, where `&&` and
  `||` are parse errors — use `;` or `if ($?) { ... }`. A Bash tool is also available for POSIX
  scripts; each takes its own syntax.
- Python 3.12. Dependencies: `PyYAML`, `rdflib`, `pytest`, plus `mkdocs-material` for the
  site. No template engine — the renderers build line lists directly, keeping the
  significant whitespace of nested markdown explicit rather than hidden in template
  indentation. There is no `templates/` directory.
- **`docs/mindmap.html` has zero external JavaScript, and must stay that way.** It holds two views
  — a collapsible tree and a force-directed graph — and both the layout and the physics are plain
  inline JS. No CDN, no npm, no vendored library. This is what makes the file work from a local
  disk in a classroom with no network and under a strict CSP; `tests/test_mindmap_ui.py` asserts
  the page issues no non-`file:` requests. At 217 nodes a hand-written O(n²) force simulation is
  cheaper than any library would be to bundle, so reaching for d3-force or Sigma.js here trades
  the guarantee away for nothing.
- Paths in this repo contain spaces (`E:\My Developments\...`) — quote them.

## Git

- Default branch is `main`, tracking `github.com/SamRepository/Web_Technologies_MindMap`.
- Branch before committing; do not commit or push unless asked.
- Never commit `private/`, `site/`, or `.claude/settings.local.json`.
- **Do** commit generated artifacts: `README.md`, `dist/webtech.ttl`, and (from Phase 3)
  `docs/mindmap.html`. They are the published outputs, and CI's `build.py --check` compares them
  against a fresh build. Generated but committed is not a contradiction — it is what makes the
  staleness check possible.
