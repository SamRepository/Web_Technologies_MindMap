#!/usr/bin/env python3
"""ONE-TIME migration: parse the hand-written README into concept YAML.

Run once, in Phase 2, to convert the 620-line single-file wiki into
``concepts/**/*.yml`` plus prose partials in ``content/``. Kept in the repository
afterwards so the migration is auditable and repeatable, not as part of the
normal build -- ``scripts/build.py`` goes the other direction.

    python scripts/extract_readme.py --readme README.md --out .

Parsing notes, all driven by what the file actually contains rather than what a
tidy document would contain:

* Indentation is inconsistent (``UTF-8`` sits 4 spaces below its parent while
  most children sit 2). Parent/child is therefore resolved with a monotonic
  indent stack -- deeper indent means child of the nearest shallower node --
  which is robust to the varying widths.
* A concept's bold label may carry the colon inside (``**Data Encoding:**``) or
  outside (``**Data Exchange Formats**:``). Both are stripped.
* Some nodes are pure grouping nodes with no definition (``**Networking**``).
* One definition continues on an unindented line after its own children
  (``Cloud Computing``). Such orphan text is appended to the open concept.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml  # noqa: E402

from webtech.model import Concept, Link  # noqa: E402
from webtech.slug import concept_slug, unique_slug  # noqa: E402

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
BULLET_CONCEPT = re.compile(r"^(\s*)[-*]\s+\*\*(.+?)\*\*\s*:?\s*(.*)$")
BULLET_LINK = re.compile(r"^(\s*)[-*]\s+\[(.+?)\]\((\S+?)\)\s*$")
BULLET_PLAIN = re.compile(r"^(\s*)[-*]\s+(.*)$")
HRULE = re.compile(r"^\s*---+\s*$")

# Section layout of the source document. Order matters: it is the published order.
SECTION_PLAN = [
    ("00-pillars", "Top-Level Pillar Concepts", False),
    ("00-disciplines", "Main Computer Science Disciplines", False),
    ("01-introduction", "Introduction to Web Technologies", True),
    ("02-evolution", "Evolution of the Web", True),
    ("03-web-development", "Web Development", True),
    ("04-additional-topics", "Additional Topics", True),
]
SECTION_BY_HEADING = {h: (sid, toc) for sid, h, toc in SECTION_PLAN}

# Technology deliberately kept but marked as superseded.
LEGACY_LABELS = {"jQuery", "AngularJS", "Heroku"}


def link_type(label: str, url: str) -> str:
    low = label.lower()
    if "drive.google.com" in url:
        return "course"
    if "youtu" in url:
        return "video"
    if "wikipedia" in low or "wikipedia.org" in url:
        return "wikipedia"
    if "mdn" in low or "developer.mozilla.org" in url:
        return "mdn"
    if "w3.org/TR" in url or "specification" in low or "w3c documentation" in low:
        return "spec"
    if low.startswith("official"):
        return "official"
    return "reference"


LEGACY_MARKER = re.compile(r"^\s*\*\(legacy\)\*\s*:?\s*")


def clean_label(raw: str) -> str:
    """Strip a trailing colon from a bold label."""
    return raw.strip().rstrip(":").strip()


def split_legacy(definition: str) -> tuple[str, bool]:
    """Peel a leading ``*(legacy)*`` marker off a definition.

    Phase 1 wrote the marker inline, outside the bold label. Left in place it
    would be stored as part of the definition text and then re-emitted alongside
    the marker the renderer adds from ``status``, duplicating it.
    """
    if LEGACY_MARKER.match(definition):
        return LEGACY_MARKER.sub("", definition, count=1).strip(), True
    return definition, False


class Extractor:
    def __init__(self, lines: list[str]) -> None:
        self.lines = lines
        self.concepts: list[Concept] = []
        self.taken: set[str] = set()
        self.prose: dict[str, list[str]] = {}
        self.section_intros: dict[str, list[str]] = {}
        self.section_outros: dict[str, list[str]] = {}
        self.subsections: dict[str, list[tuple[str, str]]] = {}
        self.notes: list[str] = []
        self.by_id: dict[str, Concept] = {}

    # -- helpers ---------------------------------------------------------
    def _new_concept(self, label: str, definition: str, section: str,
                     subsection: str | None, parent: str | None, order: int) -> Concept:
        cid = unique_slug(label, self.taken, full_label=label)
        definition, marked_legacy = split_legacy(definition.strip())
        return Concept(
            id=cid,
            label=label,
            section=section,
            subsection=subsection,
            parent=parent,
            order=order,
            definition=definition,
            status="legacy" if (marked_legacy or label in LEGACY_LABELS) else "current",
        )

    def _owner(self, stack: list[tuple[int, str]], indent: int,
               *, inclusive: bool) -> Concept | None:
        """Nearest open concept that owns a child line at *indent*.

        Links use ``inclusive=False`` (a link indented 2 under a concept at 0
        belongs to that concept, not to a sibling also at 2). Definition
        continuations use ``inclusive=True``, since they sit at the same indent
        as the concept they continue.
        """
        for ind, cid in reversed(stack):
            if (ind <= indent) if inclusive else (ind < indent):
                return self.by_id.get(cid)
        return None

    def _next_meaningful(self, i: int) -> str:
        """Classify the next non-blank line after *i* -- used to disambiguate an
        unindented paragraph: a following link bullet means the paragraph
        continues a concept, a rule or heading means it closes the section."""
        for line in self.lines[i + 1:]:
            s = line.strip()
            if not s:
                continue
            if HRULE.match(line):
                return "rule"
            if HEADING.match(line):
                return "heading"
            if BULLET_LINK.match(line):
                return "link"
            if BULLET_CONCEPT.match(line):
                return "concept"
            return "text"
        return "eof"

    # -- main ------------------------------------------------------------
    def run(self) -> None:
        section: str | None = None
        subsection: str | None = None
        # stack of (indent, concept_id) for parent resolution
        stack: list[tuple[int, str]] = []
        order = 0
        current: Concept | None = None
        bucket: list[str] | None = self.prose.setdefault("header", [])
        seen_guide = False

        # Everything after the final horizontal rule is footer prose, never
        # concepts -- otherwise the licence bullets parse as concept nodes.
        footer_start = max(
            (i for i, ln in enumerate(self.lines) if HRULE.match(ln)), default=len(self.lines)
        )

        for i, raw in enumerate(self.lines):
            line = raw.rstrip("\n")

            if i >= footer_start:
                if HRULE.match(line):
                    continue
                self.prose.setdefault("footer", []).append(line)
                continue

            m = HEADING.match(line)
            if m:
                depth, text = len(m.group(1)), m.group(2)

                # The guide intro and the TOC sit between sections, inside none
                # of them. Clearing `section` is what keeps their prose and the
                # numbered TOC list out of the concept parser.
                if text.startswith("Comprehensive Guide"):
                    seen_guide = True
                    section, subsection = None, None
                    bucket = self.prose.setdefault("guide_intro", [])
                    # Keep the heading itself: it is part of the published
                    # document, not just a parser landmark.
                    bucket.append(f"{'#' * depth} {text}")
                    current, stack = None, []
                    continue
                if text == "Table of Contents":
                    section, subsection = None, None
                    bucket = None          # regenerated, never stored
                    current, stack = None, []
                    continue

                if depth == 3 and text in SECTION_BY_HEADING:
                    section, _ = SECTION_BY_HEADING[text]
                    subsection = None
                    bucket = self.section_intros.setdefault(section, [])
                    self.subsections.setdefault(section, [])
                    current, stack = None, []
                    continue

                if depth == 4 and section:
                    subsection = concept_slug(text)
                    self.subsections.setdefault(section, []).append((subsection, text))
                    bucket = None
                    current, stack = None, []
                    continue

                # Any other heading before the guide is header prose.
                if not seen_guide and bucket is not None:
                    bucket.append(line)
                continue

            if section is None:
                # Still in the front matter.
                if bucket is not None:
                    bucket.append(line)
                continue

            if HRULE.match(line):
                current, stack = None, []
                continue

            m = BULLET_LINK.match(line)
            if m and current is not None:
                indent = len(m.group(1))
                label, url = m.group(2).strip(), m.group(3).strip()
                owner = self._owner(stack, indent, inclusive=False) or current
                owner.links.append(
                    Link(type=link_type(label, url), label=label, url=url)
                )
                continue

            m = BULLET_CONCEPT.match(line)
            if m:
                indent = len(m.group(1))
                label = clean_label(m.group(2))
                definition = m.group(3).strip()

                while stack and stack[-1][0] >= indent:
                    stack.pop()
                parent = stack[-1][1] if stack else None

                order += 1
                current = self._new_concept(
                    label, definition, section, subsection, parent, order
                )
                self.concepts.append(current)
                self.by_id[current.id] = current
                stack.append((indent, current.id))
                continue

            # An unindented paragraph inside a section is ambiguous: it either
            # continues the definition of an open concept, or closes the section.
            # Disambiguate by what follows it.
            stripped = line.strip()
            if stripped and not BULLET_PLAIN.match(line):
                indent = len(line) - len(line.lstrip())
                nxt = self._next_meaningful(i)
                if current is None:
                    # No concept opened yet in this section: this is intro prose.
                    if bucket is not None:
                        bucket.append(line)
                    continue
                if nxt == "link":
                    owner = self._owner(stack, indent, inclusive=True) or current
                    owner.definition = (owner.definition + " " + stripped).strip()
                    self.notes.append(
                        f"continuation -> '{owner.id}': {stripped[:55]}..."
                    )
                else:
                    self.section_outros.setdefault(section, []).append(stripped)
                    self.notes.append(
                        f"section outro -> '{section}': {stripped[:55]}..."
                    )
                continue

            if stripped and bucket is not None:
                bucket.append(line)


def dump_yaml(data: dict) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--readme", default="README.md")
    ap.add_argument("--out", default=".")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = Path(args.out).resolve()
    lines = Path(args.readme).read_text(encoding="utf-8").splitlines()

    ex = Extractor(lines)
    ex.run()

    print(f"parsed {len(ex.concepts)} concepts")
    by_section: dict[str, int] = {}
    for c in ex.concepts:
        by_section[c.section] = by_section.get(c.section, 0) + 1
    for sid, _, _ in SECTION_PLAN:
        print(f"  {sid:22} {by_section.get(sid, 0):4}")
    total_links = sum(len(c.links) for c in ex.concepts)
    print(f"  {'links':22} {total_links:4}")
    print(f"  {'no definition':22} {sum(1 for c in ex.concepts if not c.definition):4}")
    for n in ex.notes:
        print("  note:", n)

    if args.dry_run:
        return 0

    # concepts/
    for c in ex.concepts:
        d = root / "concepts" / c.section
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{c.id}.yml").write_text(dump_yaml(c.to_yaml()), encoding="utf-8")

    # taxonomy
    taxonomy = {
        "prose": {k: f"content/{k}.md" for k in ("header", "guide_intro", "footer")},
        "sections": [
            {
                "id": sid,
                "heading": heading,
                "in_toc": in_toc,
                "intro": f"content/sections/{sid}.md",
                **(
                    {"outro": f"content/sections/{sid}-outro.md"}
                    if ex.section_outros.get(sid)
                    else {}
                ),
                "subsections": [
                    {"id": ssid, "heading": h}
                    for ssid, h in ex.subsections.get(sid, [])
                ],
            }
            for sid, heading, in_toc in SECTION_PLAN
        ],
    }
    (root / "concepts").mkdir(exist_ok=True)
    (root / "concepts" / "_taxonomy.yml").write_text(dump_yaml(taxonomy), encoding="utf-8")

    # content/
    cdir = root / "content"
    (cdir / "sections").mkdir(parents=True, exist_ok=True)
    for key in ("header", "guide_intro", "footer"):
        body = "\n".join(ex.prose.get(key, [])).strip() + "\n"
        (cdir / f"{key}.md").write_text(body, encoding="utf-8")
    for sid, _, _ in SECTION_PLAN:
        body = "\n".join(ex.section_intros.get(sid, [])).strip() + "\n"
        (cdir / "sections" / f"{sid}.md").write_text(body, encoding="utf-8")
        if ex.section_outros.get(sid):
            outro = "\n\n".join(ex.section_outros[sid]).strip() + "\n"
            (cdir / "sections" / f"{sid}-outro.md").write_text(outro, encoding="utf-8")

    print(f"\nwrote concepts/ and content/ under {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
