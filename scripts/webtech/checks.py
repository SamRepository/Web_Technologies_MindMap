"""Integrity checks.

Two of these are the reason the generator exists at all:

* :func:`check_anchors` would have caught the four dead table-of-contents anchors
  the hand-written README shipped for two years.
* :func:`check_restricted_leak` is a security gate, not a lint. It verifies from
  the *output side* that no restricted URL or Drive folder id reached a public
  artifact, independently of the renderer that was supposed to withhold it.
"""

from __future__ import annotations

import collections
import re
from pathlib import Path

from .model import (
    ACCESS_LEVELS,
    AUTHORITATIVE_LINK_TYPES,
    LEVELS,
    LINK_TYPES,
    STATUSES,
    MindMap,
)
from .slug import github_slug

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.MULTILINE)
INPAGE_LINK_RE = re.compile(r"\]\(#([^)]+)\)")

#: Arabic block, plus the Supplement and Extended-A ranges. Used only to catch
#: English text pasted into ``definition_ar``, which otherwise renders as a
#: left-to-right paragraph inside a right-to-left block and looks broken.
ARABIC_RE = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿ]")


class Problem(collections.namedtuple("Problem", "kind detail")):
    def __str__(self) -> str:
        return f"[{self.kind}] {self.detail}"


# -- data-level checks ---------------------------------------------------


def check_schema(mm: MindMap) -> list[Problem]:
    out: list[Problem] = []
    section_ids = {s.id for s in mm.sections}
    sub_ids = {(s.id, ss.id) for s in mm.sections for ss in s.subsections}

    for c in sorted(mm.concepts.values(), key=lambda c: c.id):
        if not c.label:
            out.append(Problem("schema", f"{c.id}: empty label"))
        if c.section not in section_ids:
            out.append(Problem("schema", f"{c.id}: unknown section {c.section!r}"))
        elif c.subsection and (c.section, c.subsection) not in sub_ids:
            out.append(
                Problem("schema", f"{c.id}: unknown subsection {c.subsection!r}")
            )
        if c.level is not None and c.level not in LEVELS:
            out.append(Problem("schema", f"{c.id}: bad level {c.level!r}"))
        if c.status not in STATUSES:
            out.append(Problem("schema", f"{c.id}: bad status {c.status!r}"))

        if c.definition_ar:
            # The Arabic is a translation *of* the English, so it cannot exist
            # without it -- that combination means the English was deleted by
            # mistake, and the detail pane would show a bare Arabic paragraph.
            if not c.definition:
                out.append(
                    Problem("schema", f"{c.id}: definition_ar with no definition")
                )
            if not ARABIC_RE.search(c.definition_ar):
                out.append(
                    Problem(
                        "schema",
                        f"{c.id}: definition_ar contains no Arabic script "
                        f"-- English text in the wrong field?",
                    )
                )

        for ln in c.links:
            if ln.type not in LINK_TYPES:
                out.append(Problem("schema", f"{c.id}: bad link type {ln.type!r}"))
            if ln.access not in ACCESS_LEVELS:
                out.append(Problem("schema", f"{c.id}: bad access {ln.access!r}"))
            if ln.is_restricted:
                if ln.url:
                    out.append(
                        Problem(
                            "restricted",
                            f"{c.id}: restricted link {ln.label!r} must not carry a url",
                        )
                    )
                if not ln.drive_folder_id:
                    out.append(
                        Problem(
                            "schema",
                            f"{c.id}: restricted link {ln.label!r} needs drive_folder_id",
                        )
                    )
            elif not ln.url:
                out.append(Problem("schema", f"{c.id}: link {ln.label!r} has no url"))
    return out


def check_graph(mm: MindMap) -> list[Problem]:
    out: list[Problem] = []
    for c in sorted(mm.concepts.values(), key=lambda c: c.id):
        if c.parent and c.parent not in mm.concepts:
            out.append(Problem("graph", f"{c.id}: dangling parent {c.parent!r}"))
        for ref in c.see_also:
            if ref not in mm.concepts:
                out.append(Problem("graph", f"{c.id}: dangling see_also {ref!r}"))
            elif ref == c.id:
                out.append(Problem("graph", f"{c.id}: see_also points at itself"))

    # Cycle detection over the parent relation.
    colour: dict[str, int] = {}

    def visit(cid: str, trail: list[str]) -> None:
        state = colour.get(cid, 0)
        if state == 1:
            cyc = " -> ".join(trail[trail.index(cid):] + [cid])
            out.append(Problem("graph", f"cycle: {cyc}"))
            return
        if state == 2:
            return
        colour[cid] = 1
        parent = mm.concepts[cid].parent
        if parent and parent in mm.concepts:
            visit(parent, trail + [cid])
        colour[cid] = 2

    for cid in mm.concepts:
        visit(cid, [])
    return out


def check_paths(mm: MindMap) -> list[Problem]:
    """Learning paths must sequence concepts that exist, exactly once each.

    A path is an ordering over the map, so a dangling id is not a broken link
    but a lesson pointing at nothing. Repetition inside one path is treated as
    an error rather than deliberate revision: in practice it has always been a
    copy-paste slip, and a genuine second pass belongs in its own module with
    its own hours.
    """
    out: list[Problem] = []
    path_ids = {lp.id for lp in mm.paths}

    for lp in mm.paths:
        if lp.level not in LEVELS:
            out.append(Problem("paths", f"{lp.id}: bad level {lp.level!r}"))
        if not lp.modules:
            out.append(Problem("paths", f"{lp.id}: no modules"))

        seen: dict[str, str] = {}
        for m in lp.modules:
            if m.weeks <= 0 or m.hours <= 0:
                out.append(
                    Problem("paths", f"{lp.id}/{m.title!r}: weeks and hours must be > 0")
                )
            if not m.concepts:
                out.append(Problem("paths", f"{lp.id}/{m.title!r}: no concepts"))
            for cid in m.concepts:
                if cid not in mm.concepts:
                    out.append(
                        Problem("paths", f"{lp.id}/{m.title!r}: unknown concept {cid!r}")
                    )
                elif cid in seen:
                    out.append(
                        Problem(
                            "paths",
                            f"{lp.id}: {cid!r} appears in both "
                            f"{seen[cid]!r} and {m.title!r}",
                        )
                    )
                else:
                    seen[cid] = m.title

        for pre in lp.prerequisites:
            if pre not in path_ids:
                out.append(Problem("paths", f"{lp.id}: unknown prerequisite {pre!r}"))
            elif pre == lp.id:
                out.append(Problem("paths", f"{lp.id}: is its own prerequisite"))

    # Cycle detection over prerequisites, same shape as the parent-relation
    # check above: a path that transitively requires itself can never be started.
    colour: dict[str, int] = {}
    by_id = {lp.id: lp for lp in mm.paths}

    def visit(pid: str, trail: list[str]) -> None:
        state = colour.get(pid, 0)
        if state == 1:
            cyc = " -> ".join(trail[trail.index(pid):] + [pid])
            out.append(Problem("paths", f"prerequisite cycle: {cyc}"))
            return
        if state == 2:
            return
        colour[pid] = 1
        for pre in by_id[pid].prerequisites:
            if pre in by_id:
                visit(pre, trail + [pid])
        colour[pid] = 2

    for pid in by_id:
        visit(pid, [])
    return out


def check_path_coverage(mm: MindMap) -> list[Problem]:
    """Advisory: concepts no path teaches.

    Not an error. The map is a reference as well as a curriculum, and some of
    it is meant to be looked up rather than taught.
    """
    if not mm.paths:
        return []
    covered = {cid for lp in mm.paths for cid in lp.concept_ids}
    return [
        Problem("coverage", f"{cid}: in no learning path")
        for cid in sorted(set(mm.concepts) - covered)
    ]


def check_translation_coverage(mm: MindMap) -> list[Problem]:
    """Advisory: definitions with no Arabic yet.

    Not an error. Translation is authored content that lands incrementally, and
    an untranslated concept simply shows no Arabic block.
    """
    return [
        Problem("arabic", f"{c.id}: no definition_ar")
        for c in sorted(mm.concepts.values(), key=lambda c: c.id)
        if c.definition and not c.definition_ar
    ]


def check_sources(mm: MindMap) -> list[Problem]:
    """Advisory: a concept with a definition should cite a primary source."""
    out: list[Problem] = []
    for c in sorted(mm.concepts.values(), key=lambda c: c.id):
        if not c.definition:
            continue  # pure grouping node
        if not any(ln.type in AUTHORITATIVE_LINK_TYPES for ln in c.links):
            out.append(Problem("sources", f"{c.id}: no authoritative link"))
    return out


# -- output-level checks -------------------------------------------------


def check_anchors(markdown: str) -> list[Problem]:
    """Every in-page link must resolve to a heading in the same document.

    Replicates GitHub's duplicate-heading disambiguation (``-1``, ``-2``, ...) so
    the check matches what a reader's browser will actually do.
    """
    seen: collections.Counter[str] = collections.Counter()
    slugs: set[str] = set()
    for _, text in HEADING_RE.findall(markdown):
        base = github_slug(text)
        n = seen[base]
        seen[base] += 1
        slugs.add(base if n == 0 else f"{base}-{n}")

    return [
        Problem("anchor", f"dead in-page link #{a}")
        for a in INPAGE_LINK_RE.findall(markdown)
        if a not in slugs
    ]


def check_duplicate_headings(markdown: str) -> list[Problem]:
    counts = collections.Counter(t for _, t in HEADING_RE.findall(markdown))
    return [
        Problem("heading", f"duplicate heading {t!r} appears {n}x")
        for t, n in sorted(counts.items())
        if n > 1
    ]


def check_restricted_leak(mm: MindMap, artifacts: dict[str, str]) -> list[Problem]:
    """Fail if any restricted identifier appears in a public artifact.

    *artifacts* maps a display name to file content. Checked from the output side
    on purpose: it must not trust the renderer to have done the right thing.
    """
    secrets: list[tuple[str, str]] = []
    for concept, ln in mm.restricted_links:
        if ln.drive_folder_id:
            secrets.append((ln.drive_folder_id, f"{concept.id}/{ln.label}"))
        if ln.url:
            secrets.append((ln.url, f"{concept.id}/{ln.label}"))

    out: list[Problem] = []
    for name, content in artifacts.items():
        for secret, origin in secrets:
            if secret and secret in content:
                out.append(
                    Problem(
                        "LEAK",
                        f"{name} contains restricted identifier from {origin}",
                    )
                )
    return out


def collect_artifacts(root: Path) -> dict[str, str]:
    """Read every public artifact that the leak check should scan."""
    out: dict[str, str] = {}
    readme = root / "README.md"
    if readme.exists():
        out["README.md"] = readme.read_text(encoding="utf-8")
    for sub in ("docs", "dist"):
        base = root / sub
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix in {".md", ".html", ".ttl", ".json", ".xml"}:
                out[str(p.relative_to(root)).replace("\\", "/")] = p.read_text(
                    encoding="utf-8", errors="replace"
                )
    return out
