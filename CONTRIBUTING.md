# Contributing

Thanks for helping improve the Web Technologies MindMap. It is used as teaching material, so
**accuracy of definitions and durability of links matter more than volume of content.**

## The golden rule: `README.md` is generated

From Phase 2 of the [roadmap](docs/ROADMAP.md) onward, `README.md` is build output. A pull request
that edits it directly cannot be merged — the change would be erased by the next build.

To change what appears in the README, edit the concept that owns it:

```
concepts/<section>/<id>.yml     <- edit this
        |
        v  python scripts/build.py
README.md, docs/mindmap.html, dist/webtech.ttl
```

| Generated — do not edit | Hand-written — edit freely |
|---|---|
| `README.md` | `concepts/**/*.yml` |
| `docs/mindmap.html` | `content/*.md` |
| `docs/concepts/**` | `templates/*.j2` |
| `LEARNING-PATHS.md` | `scripts/**` |
| `dist/**`, `site/**` | `docs/ROADMAP.md`, `CONTRIBUTING.md`, `RESOURCES.md` |

If you use Claude Code in this repository, a `PreToolUse` hook enforces this automatically.

## Adding or changing a concept

One concept per file, at `concepts/<section>/<id>.yml`:

```yaml
id: typescript                     # kebab-case, unique, matches the filename
label: TypeScript
parent: frontend-languages         # an existing concept id, or null
section: 03-web-development
level: intermediate                # beginner | intermediate | advanced
status: current                    # current | emerging | legacy
aliases: [TS]                      # optional
see_also: [javascript]             # optional, concept ids
definition: >
  A typed superset of JavaScript that compiles to plain JavaScript, adding
  static type checking to catch errors before runtime.
links:
  - {type: official, label: Official Website, url: 'https://www.typescriptlang.org/'}
  - {type: wikipedia, label: Wikipedia, url: 'https://en.wikipedia.org/wiki/TypeScript'}
```

`type` ∈ `official | wikipedia | mdn | spec | video | course | reference`
(`reference` is the catch-all for an authoritative page that is none of the others).

### House style

- **Every concept needs at least one authoritative link.** Prefer primary sources — official
  documentation, specifications, MDN — over blog posts and aggregators.
- **Write 1–3 sentences.** Read the sibling files in the same section first and match their register.
  A definition that reads differently from its neighbours is a defect in teaching material.
- **The spelling is `Resource`.** The French `Ressource` was present throughout the original README
  and has been corrected; please don't reintroduce it.
- **Don't delete superseded technology** — mark it `status: legacy`. Students meet old tutorials and
  need to know what is dated. jQuery, AngularJS and Heroku are legacy.
- **`Angular` and `AngularJS` are different things.** Angular is the current framework; AngularJS is
  the separate one retired in 2010. Please don't conflate them.
- **Prefer free, durable resources** — MDN, web.dev, CS50, Full Stack Open, The Odin Project — over
  links that require a subscription, and over any link that redistributes paid course material.

## Restricted resources

Some course links are private, shared with specific people through Google Drive. A link marked
`access: restricted` **must never have its URL or Drive folder ID committed** — not to a concept
file, not to the README, not to a commit message.

```yaml
  - type: course
    label: TP recordings
    access: restricted          # note: no url key
    drive_folder_id: <id>
    audience: webtech-students
```

Public output renders these as `🔒 <label> — request access`. `scripts/validate.py` fails the build
if a restricted identifier reaches a public artifact. If that check trips, treat it as a security
finding and find out why — don't work around it.

## Before opening a pull request

```bash
python scripts/validate.py     # schema, graph integrity, restricted-leak check
python scripts/build.py        # regenerate, and commit the regenerated output
mkdocs build --strict          # only if you touched the site
```

Commit the regenerated files alongside your source change. CI runs `build.py --check` and fails if
committed output does not match a fresh build.

On Windows the default shell is PowerShell, where `&&` is a parse error — chain with `;`.

## Reporting content problems without a pull request

Open an issue. Broken links, out-of-date definitions and missing topics are all genuinely useful
reports; you do not need to supply the fix.

## Licence

Contributions are accepted under the repository's dual licence: **CC BY-SA 4.0** for content
(concepts, prose, the mind map) and **Apache 2.0** for code (`scripts/`, `templates/`, `.claude/`).
See [LICENSE-CONTENT](LICENSE-CONTENT) and [LICENSE](LICENSE).
