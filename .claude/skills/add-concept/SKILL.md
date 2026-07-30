---
name: add-concept
description: Add a new concept to the Web Technologies mind map. Use when the user wants to add, document, or define a technology, standard, framework, or concept in this repository — e.g. "add TypeScript to the mind map", "document Core Web Vitals", "add a concept for WebGPU". Writes the concept YAML under concepts/, then validates.
---

# Add a concept

Concepts are the source of truth for this repository. `README.md`, the interactive mind map and
the SKOS/RDF export are all generated from them — so adding a concept here is the *only* correct
way to make something appear in the map.

## Precondition

If `scripts/validate.py` does not exist yet, the generator has not been built (see Phase 2 in
[docs/ROADMAP.md](../../../docs/ROADMAP.md)). You can still write the YAML — it is the durable
artifact — but say plainly that validation and the build cannot run yet, rather than implying they
did.

## Steps

### 1. Gather what the schema needs

Collect these before writing. Ask the user only for what you cannot reasonably infer:

| Field | Notes |
|---|---|
| `id` | kebab-case, unique across the whole repo, must match the filename |
| `label` | Display name as students will read it (`TypeScript`, not `typescript`) |
| `section` | One of the `concepts/` section directories |
| `parent` | An existing concept `id`, or `null` for a section-level concept |
| `level` | `beginner` \| `intermediate` \| `advanced` |
| `status` | `current` \| `emerging` \| `legacy` |
| `definition` | 1–3 sentences, pedagogical register, matching existing entries |
| `links` | At least one authoritative link |

Read two or three sibling files in the target section first and match their voice. This is teaching
material — a definition that reads differently from its neighbours is a defect.

### 2. Check it doesn't already exist

Search `concepts/` for the id, the label, and plausible aliases. The original README had a
duplicated "Web Security" section; do not reintroduce that class of problem. If a near-match
exists, propose extending it instead of adding a sibling.

### 3. Write `concepts/<section>/<id>.yml`

```yaml
id: typescript
label: TypeScript
parent: frontend-languages
section: 03-web-development
level: intermediate
status: current
aliases: [TS]
see_also: [javascript]
definition: >
  A typed superset of JavaScript that compiles to plain JavaScript, adding static
  type checking to catch errors before runtime.
links:
  - {type: official, label: Official Website, url: 'https://www.typescriptlang.org/'}
  - {type: wikipedia, label: Wikipedia, url: 'https://en.wikipedia.org/wiki/TypeScript'}
```

Rules that matter:

- **Prefer primary sources.** `official`, `spec`, `mdn`, `wikipedia` over blog posts. Every concept
  needs at least one.
- **Spelling is `Resource`,** never the French `Ressource`.
- **Restricted links carry no URL.** For a private Drive resource, use `access: restricted` with
  `drive_folder_id` and `audience`, and *no* `url` key. Full URLs belong only in
  `private/RESOURCES-gated.md`, which is gitignored. See the rule in
  [CLAUDE.md](../../../CLAUDE.md) — treat a leak as a security problem, not a lint error.
- **Don't delete superseded technology.** Mark it `status: legacy` so students reading old
  tutorials can tell what is dated.

### 4. Update the parent's `see_also` if the relationship is genuinely bidirectional

Only when it aids navigation. Don't inflate the graph.

### 5. Validate, then build

```bash
python scripts/validate.py
python scripts/build.py
```

`validate.py` checks id uniqueness, that `parent` and `see_also` resolve, and that no restricted
identifier leaked into a public artifact. **Never hand-edit `README.md` to make the concept
appear** — a `PreToolUse` hook will deny it, and the next build would overwrite the change anyway.

### 6. Report

State the file created, its position in the tree (`section > parent > label`), and the validate
result. If validation failed, fix the cause rather than reporting success.
