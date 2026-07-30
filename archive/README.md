# Archive

Frozen snapshots kept for reference. Nothing here is built, generated, published, or link-checked.

## `README-original.md`

The hand-written `README.md` as it stood before this project's restructuring — a byte-for-byte copy
of the file at commit [`4cb32bf`](https://github.com/SamRepository/Web_Technologies_MindMap/commit/4cb32bf),
the last commit before Phase 0. 620 lines, 52,738 bytes.

It is kept because that file *was* the project for two years, and a snapshot is easier to consult
than a git command. It is deliberately unaltered, which means it still contains the defects that
Phase 1 fixed:

- four dead table-of-contents anchors (`#web-1.0-documents-web` and its three siblings — GitHub
  slugs the dot away, so the real anchor is `#web-10---documents-web`)
- "Web Security" as a duplicated section
- `Angular.js`, describing the framework retired in 2010 while linking to modern Angular's site
- `OWL (Object Web Language)`, which is not what Odoo's OWL stands for
- six occurrences of the French spelling `Ressource`

Those are features of the snapshot, not problems with it. Do not "fix" this file — the current
content lives in `concepts/**/*.yml` and the published `README.md` is generated from it.

## Why this is not redundant with git history

Git already has every version, and `git show 4cb32bf:README.md` reproduces this file exactly. The
copy exists for discoverability: someone comparing the old single-file wiki against the generated
one should not need to know a commit hash to do it.

To see what changed across the restructuring:

```bash
python scripts/fidelity.py --before 4cb32bf:README.md --after README.md
```

That compares content rather than formatting, and reports every heading, label, definition and URL
present in one but not the other.

## The complete delta from this snapshot to now

Run at the time of archiving. Every item removed is accounted for by a deliberate change — nothing
was dropped accidentally.

| | original | now |
|---|---|---|
| headings | 31 | 33 |
| labels | 158 | 202 |
| definitions | 141 | 183 |
| URLs | 197 | 266 |

**1 heading removed:** *View the Detailed MindMap Online* — replaced by *View the Interactive Mind
Map* plus *Backup view: MindMeister* when the self-hosted map became primary.

**4 labels removed:**

- `Angular.js` → split into `Angular` (current) and `AngularJS` (marked legacy); they are different
  frameworks
- `OWL (Object Web Language)` → `OWL (Odoo Web Library)`, a factual correction
- `To Download the MindMeister App` → became prose in the backup-view section
- `Watch the Youtube Video` → `Watch the YouTube Video`

**5 definitions removed:**

- three thin duplicates of XSS, SQL Injection and CSRF, from the *Web Security* section that appeared
  twice; the richer versions were kept
- the old `Angular.js` definition ("A structural framework for dynamic web apps")
- the old, incorrect OWL definition

**1 URL removed:** `https://angular.io/` — modern Angular's site is `angular.dev`.

Everything else grew: +48 labels and +47 definitions from the Phase 4 modernization, and +70 URLs.
