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
- `docs/concepts/**`
- `LEARNING-PATHS.md`
- `dist/**`, `site/**`

### Hand-written (edit freely)
- `concepts/**/*.yml` — the concept data, **the actual source of truth**
- `content/*.md` — long-form prose partials
- `templates/*.j2` — output templates
- `scripts/**` — the generator
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
security finding, not a lint error.

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
links:
  - {type: official, label: Official Website, url: 'https://www.typescriptlang.org/'}
  - type: course
    label: TP recordings
    access: restricted             # NO url key — see the rule above
    drive_folder_id: <id>
    audience: webtech-students
```

`type` ∈ `official | wikipedia | mdn | spec | video | course`.
`access` ∈ `public | restricted`, defaulting to `public`.

Use `/add-concept` rather than writing these by hand — it validates as it goes.

---

## Commands

```bash
python scripts/validate.py          # schema + graph integrity + restricted-leak check
python scripts/build.py             # regenerate README, mindmap, SKOS
python scripts/build.py --check     # non-zero exit if committed output is stale (CI gate)
mkdocs build --strict               # build the site; warnings are errors
mkdocs serve                        # local preview
```

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
- Python 3.12. Dependencies: `PyYAML`, `Jinja2`, `rdflib`, plus `mkdocs-material` for the site.
- Paths in this repo contain spaces (`E:\My Developments\...`) — quote them.

## Git

- Default branch is `main`, tracking `github.com/SamRepository/Web_Technologies_MindMap`.
- Branch before committing; do not commit or push unless asked.
- Never commit `private/`, `dist/`, `site/`, or `.claude/settings.local.json`.
