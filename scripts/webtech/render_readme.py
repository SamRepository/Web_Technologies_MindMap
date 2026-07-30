"""Render README.md from the concept tree.

The table of contents is generated from the same section list that generates the
headings, and anchors are computed with :func:`webtech.slug.github_slug`. That is
the structural fix for the four dead anchors the hand-written README shipped: a
TOC entry cannot disagree with its heading, because neither is typed by hand.
"""

from __future__ import annotations

from .model import Concept, Link, MindMap, Section
from .slug import github_slug

SENTINEL = (
    "<!-- GENERATED FILE -- do not edit.\n"
    "     Source of truth: concepts/**/*.yml and content/*.md\n"
    "     Regenerate with: python scripts/build.py\n"
    "     Hand-edits are denied by .claude/hooks/guard_generated.py and will be\n"
    "     overwritten by the next build. -->"
)

ACCESS_HEADING = "Requesting Access to Restricted Resources"

#: Fallback target for the 🔒 badge: the in-page section rendered below. Overridden
#: by ``access_request_url`` in ``concepts/_taxonomy.yml`` once a request form
#: exists. The badge must always point somewhere real -- an anchor to a section
#: that is not emitted would fail the build's own anchor check.
REQUEST_ACCESS_ANCHOR = f"#{github_slug(ACCESS_HEADING)}"

ACCESS_SECTION = f"""## {ACCESS_HEADING}

Some resources above are marked 🔒. These are hosted on Google Drive and shared
only with named people, so no URL is published for them — access is granted on
the sharing list, not by holding a link.

If you are a student or colleague who needs access, contact the author with your
name, institution, and the Google account address to grant.

Maintainers: see [RESOURCES.md](RESOURCES.md) for how this tier is administered.
"""


def render_link(link: Link, request_url: str = REQUEST_ACCESS_ANCHOR) -> str:
    """Render one link bullet.

    A restricted link never renders its URL or Drive folder id -- only a badge
    pointing at the access-request flow. This function is the single choke point
    for that rule; ``webtech.checks`` verifies the outcome independently.
    """
    if link.is_restricted:
        return f"🔒 {link.label} — [request access]({request_url})"
    return f"[{link.label}]({link.url})"


def render_concept(c: Concept, depth: int = 0,
                   request_url: str = REQUEST_ACCESS_ANCHOR) -> list[str]:
    out: list[str] = []
    pad = "  " * depth
    legacy = " *(legacy)*" if c.status == "legacy" else ""

    if c.definition:
        out.append(f"{pad}- **{c.label}**{legacy}: {c.definition}  ")
    else:
        out.append(f"{pad}- **{c.label}**{legacy}")

    for link in c.links:
        out.append(f"{pad}  - {render_link(link, request_url)}")

    for child in c.children:
        out.append("")
        out.extend(render_concept(child, depth + 1, request_url))

    return out


def render_section(mm: MindMap, section: Section,
                   request_url: str = REQUEST_ACCESS_ANCHOR) -> list[str]:
    out: list[str] = [f"### {section.heading}", ""]
    if section.intro:
        out += [section.intro, ""]

    if section.subsections:
        for ss in section.subsections:
            out += [f"#### {ss.heading}", ""]
            for root in mm.roots(section.id, ss.id):
                out += render_concept(root, 0, request_url)
                out.append("")
    else:
        for root in mm.roots(section.id, None):
            out += render_concept(root, 0, request_url)
            out.append("")

    outro = getattr(section, "outro", "")
    if outro:
        out += [outro, ""]
    return out


def render_toc(mm: MindMap) -> list[str]:
    out = ["### Table of Contents"]
    n = 0
    for s in mm.sections:
        if not s.in_toc:
            continue
        n += 1
        out.append(f"{n}. [{s.heading}](#{github_slug(s.heading)})")
        for ss in s.subsections:
            out.append(f"    - [{ss.heading}](#{github_slug(ss.heading)})")
    out.append("")
    return out


def render(mm: MindMap) -> str:
    # An external request form takes precedence; otherwise the badge points at
    # the in-page section, which is emitted only when it is actually needed.
    external = (mm.prose.get("access_request_url") or "").strip()
    has_restricted = bool(mm.restricted_links)
    request_url = external or REQUEST_ACCESS_ANCHOR

    parts: list[str] = [SENTINEL, ""]

    if mm.prose.get("header"):
        parts += [mm.prose["header"], ""]

    # Sections that sit before the guide (the pillars and disciplines primers).
    pre_guide = [s for s in mm.sections if not s.in_toc]
    for s in pre_guide:
        parts += ["---", ""]
        parts += render_section(mm, s, request_url)

    parts += ["---", ""]
    if mm.prose.get("guide_intro"):
        parts += [mm.prose["guide_intro"], ""]
    parts += render_toc(mm)
    parts += ["---", ""]

    for s in [s for s in mm.sections if s.in_toc]:
        parts += render_section(mm, s, request_url)
        parts += ["---", ""]

    # Emitted only when a 🔒 badge exists and there is no external form to point
    # at, so the badge's anchor always has a target.
    if has_restricted and not external:
        parts += [ACCESS_SECTION, "", "---", ""]

    if mm.prose.get("footer"):
        parts += [mm.prose["footer"], ""]

    text = "\n".join(parts)
    # Collapse runs of blank lines left by the section/concept joins.
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text.rstrip() + "\n"
