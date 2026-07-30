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
