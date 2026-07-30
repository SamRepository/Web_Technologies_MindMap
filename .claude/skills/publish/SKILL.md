---
name: publish
description: Regenerate and verify all Web Technologies mind map outputs — README, interactive mind map, SKOS/RDF export, and the MkDocs site. Use when the user wants to rebuild, regenerate, publish, or verify the mind map after editing concepts, or asks to check that generated files are up to date.
---

# Publish the mind map

Runs the full generate-and-verify sequence in dependency order. Each step gates the next: a failure
means stop and fix, not continue and report partial success.

## Precondition

If `scripts/build.py` does not exist, the generator has not been built yet (Phase 2 in
[docs/ROADMAP.md](../../../docs/ROADMAP.md)). Say so and stop — do not improvise a build.

## Sequence

### 1. Validate the source data

```bash
python scripts/validate.py
```

Checks unique `id`s, that every `parent` and `see_also` resolves, absence of cycles, required
fields, and that `level`/`status`/`type` values are in their allowed sets. Fix any failure at the
YAML level before going further — everything downstream is derived from this data.

### 2. Build

```bash
python scripts/build.py
```

Regenerates `README.md`, `docs/mindmap.html`, `docs/concepts/**`, and `dist/webtech.ttl`.

### 3. Confirm the restricted-leak check passed

This is the one step to treat as a security gate rather than a lint. `validate.py` fails the build
if a `drive_folder_id` or URL belonging to an `access: restricted` link appears in `README.md`,
`docs/`, or `dist/`. If it trips, **do not** work around it — find why a restricted identifier
reached a public renderer.

### 4. Check the anchors resolve

Every in-page table-of-contents link in the generated README must match a real heading slug
(GitHub's rule: lowercase, strip punctuation, spaces → `-`). The original README shipped four dead
anchors because `Web 1.0` slugs to `web-10`, not `web-1.0`. This check exists so that cannot recur.

### 5. Build the site

```bash
mkdocs build --strict
```

`--strict` promotes warnings to errors, catching broken internal references.

### 6. Verify the mind map by eye

Open `docs/mindmap.html` in a browser. Confirm it renders **with no network access** (everything is
inlined by design), the root expands to all sections, and the node count matches the concept count.

### 7. Report honestly

Give the concept count, what changed in the generated files (`git diff --stat`), and each check's
result. If a step was skipped or failed, say which and why — do not describe an unverified build as
verified.

## Notes

- This is a Windows box; the default shell is PowerShell 5.1, where `&&` is a parse error. Chain
  with `;` or run the steps as separate calls.
- Do not `git commit` or `push` as part of this skill unless the user asks. If asked, branch first —
  `main` tracks the public GitHub repository.
