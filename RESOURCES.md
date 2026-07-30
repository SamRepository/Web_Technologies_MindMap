# Restricted Resources — Operations Guide

How to publish private course material from this repository without exposing it.

The mechanism is built and tested; this document is the operational half. **No restricted content
is configured yet** — the schema, renderer and checks exist, and the tier is empty until you
populate it.

---

## The idea in one paragraph

Google Drive enforces access on the folder, not on the link. A folder set to *Restricted — specific
people* cannot be opened by anyone else **even with the exact URL** — they get a request-access
screen. So link secrecy is not the control; the sharing list is. That is what makes it safe to
publish a 🔒 badge in a public README: the badge is a signpost, and the ACL is the lock.

This repository nonetheless withholds the URLs entirely, because a URL that is never published
cannot be scraped, archived, or inherited by a future reader if a folder's sharing is ever loosened
by accident.

---

## Current state: four folders are publicly readable

The README links four Google Drive folders, from the **HTTP/HTTPS**, **XML**, **Flask** and
**Django** concepts. All four are currently shared with `type: anyone` — readable by anybody who
has the link.

To list them:

```bash
grep -n "drive.google.com" README.md
```

Two things to be clear about:

1. **Changing this is a Drive-side setting, not a repository change.** Nothing in this repo can
   restrict a folder; you have to change the sharing in Drive.
2. **The URLs are already in public git history** and will remain there even after the sharing is
   tightened and the links are removed. Tightening the ACL is what actually stops access; removing
   the link only stops advertising it.

---

## Setup, once

### 1. Set each folder to *Restricted*

In Drive: **Share → General access → Restricted**. Confirm afterwards by opening the link in a
signed-out browser window; you should see a request-access screen.

### 2. Create a Google Group, and share with the group

Create a group — e.g. `webtech-students@your-domain` — and grant **the group** Viewer on each
folder, rather than adding people individually.

This is the single highest-leverage step. Granting a new student access becomes *add one email to
one group*, instead of re-sharing every folder. Revoking is one removal. Without it, the
administration cost grows with folders × students and it stops being maintained.

Prefer **Viewer**, not Commenter or Editor, and turn off *viewers can download* if you want to
discourage redistribution.

### 3. Publish one request funnel

A Google Form asking for name, institution and the Google account address to grant. Then set it in
`concepts/_taxonomy.yml`:

```yaml
access_request_url: https://forms.gle/your-form-id
```

When that key is present, every 🔒 badge links to the form. When it is absent, the README instead
emits a short *Requesting Access to Restricted Resources* section and the badges link there — so the
badge always has a working target either way. Both paths are covered by tests.

### 4. Keep the private index outside the repository

`private/` is gitignored. Keep your own mapping of folder id → what it contains in
`private/RESOURCES-gated.md`. Nothing in `private/` is ever committed or published.

---

## Adding a restricted resource

In the owning concept's `links:` list:

```yaml
  - type: course
    label: TP recordings — Django
    access: restricted        # NO url key
    drive_folder_id: 1AbCdEf...
    audience: webtech-students
```

Then rebuild and validate:

```bash
python scripts/build.py
python scripts/validate.py
```

**Do not add a `url` to a restricted entry.** `validate.py` rejects it — the whole point is that the
URL never enters a file that gets published.

### What the automated checks guarantee

| Check | Guarantees |
|---|---|
| `check_schema` | a restricted entry has no `url` and does have a `drive_folder_id` |
| `check_restricted_leak` | no restricted id or URL appears in `README.md`, `docs/**` or `dist/**` — verified from the *output* side, so it does not trust the renderer |
| `build.py` | refuses to write anything at all if a leak is detected |
| `tests/test_restricted.py` | the above, plus a negative control proving the leak check can actually detect a planted secret |

### What they do not guarantee

- **Git history.** A URL committed once stays in history. The checks prevent new leaks; they cannot
  retract an old one.
- **Drive sharing.** Nothing here can read or change a folder's ACL. If a folder is set to *anyone
  with the link*, a 🔒 badge in the README is decorative.
- **Redistribution by people you granted.** Access control is not copy protection.

---

## What belongs in the restricted tier

The tier is designed for **material you authored and are free to distribute** — your recorded
lectures, TP and lab sessions, slides, exam preparation, project briefs. That content is also the
most valuable to your students, because it is the only place they can get it.

For third-party commercial courses, linking the **publisher's own course page** instead is worth
considering: students with institutional access get straight in, others learn what to look for, and
nothing is hosted. Several institutional programmes exist for this — Pluralsight Skills for
education, Coursera for Campus, the GitHub Student Developer Pack — alongside free material that is
durable enough to link permanently:

- [MDN Web Docs](https://developer.mozilla.org/) — reference
- [web.dev](https://web.dev/) — performance and platform guidance from the Chrome team
- [The Odin Project](https://www.theodinproject.com/) — full front-end and full-stack curriculum
- [Full Stack Open](https://fullstackopen.com/) — University of Helsinki, free certificate
- [CS50](https://cs50.harvard.edu/) — already linked throughout this mind map
- [freeCodeCamp](https://www.freecodecamp.org/)

---

## Related

- [CLAUDE.md](CLAUDE.md) — the restricted-links rule for agents working in this repository
- [CONTRIBUTING.md](CONTRIBUTING.md) — the same rule for human contributors
- [docs/ROADMAP.md](docs/ROADMAP.md) — where this sits in the project plan
