"""Render the MkDocs reference pages: one page per section.

Anchors are the point of this renderer. Every concept gets an id-based anchor, so
a lecture slide can link `.../03-web-development/#typescript` and keep working
even if the concept's label is later reworded. Label-derived anchors would break
on any wording change; concept ids are stable by design.

Structure per page: subsections become `##` headings, root concepts `###`
headings with an explicit `{#id}`, and deeper concepts nested list items carrying
a `<span id="...">` anchor. Heading levels stop at three because the tree is up
to seven deep and HTML has no `h8` -- the sidebar stays readable while every
node still has a target.

Restricted links render as a badge, same rule as everywhere else.
"""

from __future__ import annotations

from .model import Concept, Link, MindMap, Section
from .render_readme import REQUEST_ACCESS_ANCHOR, render_link

SENTINEL = (
    "<!-- GENERATED FILE -- do not edit.\n"
    "     Source of truth: concepts/**/*.yml\n"
    "     Regenerate with: python scripts/build.py -->"
)

STATUS_BADGE = {
    "legacy": "`legacy`",
    "emerging": "`emerging`",
}


def _badges(c: Concept) -> str:
    bits = []
    if c.status in STATUS_BADGE:
        bits.append(STATUS_BADGE[c.status])
    if c.level:
        bits.append(f"`{c.level}`")
    return (" " + " ".join(bits)) if bits else ""


def _links_block(c: Concept, indent: str, request_url: str) -> list[str]:
    return [f"{indent}- {render_link(ln, request_url)}" for ln in c.links]


def _nested(c: Concept, depth: int, request_url: str) -> list[str]:
    """Render a non-root concept as a list item with a stable anchor."""
    pad = "  " * depth
    anchor = f'<span id="{c.id}"></span>'
    head = f"{pad}- {anchor}**{c.label}**{_badges(c)}"
    out = [f"{head}: {c.definition}" if c.definition else head]
    out += _links_block(c, pad + "  ", request_url)
    for k in c.children:
        out.append("")
        out += _nested(k, depth + 1, request_url)
    return out


def _root(c: Concept, request_url: str) -> list[str]:
    """Render a root concept as a heading, so it appears in the page sidebar."""
    out = [f"### {c.label}{_badges(c)} {{#{c.id}}}", ""]
    if c.definition:
        out += [c.definition, ""]
    links = _links_block(c, "", request_url)
    if links:
        out += links + [""]
    for k in c.children:
        out += _nested(k, 0, request_url)
        out.append("")
    return out


def render_section(mm: MindMap, section: Section, request_url: str) -> str:
    out: list[str] = [SENTINEL, "", f"# {section.heading}", ""]
    if section.intro:
        out += [section.intro, ""]

    if section.subsections:
        for ss in section.subsections:
            out += [f"## {ss.heading}", ""]
            for r in mm.roots(section.id, ss.id):
                out += _root(r, request_url)
    else:
        for r in mm.roots(section.id, None):
            out += _root(r, request_url)

    outro = getattr(section, "outro", "")
    if outro:
        out += [outro, ""]

    text = "\n".join(out)
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text.rstrip() + "\n"


def render_all(mm: MindMap) -> dict[str, str]:
    """Return {repo-relative path: content} for every reference page."""
    external = (mm.prose.get("access_request_url") or "").strip()
    request_url = external or f"../{REQUEST_ACCESS_ANCHOR}"

    pages = {
        f"docs/reference/{s.id}.md": render_section(mm, s, request_url)
        for s in mm.sections
    }
    pages["docs/reference/index.md"] = _index(mm)
    return pages


def _index(mm: MindMap) -> str:
    out = [SENTINEL, "", "# Reference", "",
           "Every concept in the mind map, grouped by section. "
           "Each entry has a stable anchor based on its concept id, so links from "
           "slides or notes keep working even if wording changes.", ""]
    total = len(mm.concepts)
    out += [f"**{total} concepts** across {len(mm.sections)} sections.", ""]
    for s in mm.sections:
        n = len(mm.by_section(s.id))
        out += [f"## [{s.heading}]({s.id}.md)", "", f"{n} concepts.", ""]
        if s.subsections:
            out += ["  \n".join(f"- {ss.heading}" for ss in s.subsections), ""]
    text = "\n".join(out)
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text.rstrip() + "\n"
