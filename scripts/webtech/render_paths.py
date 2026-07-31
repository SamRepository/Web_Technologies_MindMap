"""Render the learning paths.

A path adds no content. It is an *ordering* over concept ids the map already
holds, which is what stops a curriculum from drifting away from the reference
it teaches — rewording a definition updates the path automatically, and a path
cannot cite a concept that does not exist because the build refuses to.

Two outputs, differing in exactly two respects:

``LEARNING-PATHS.md``
    For GitHub. Concept names are plain text. GitHub does not parse the
    ``{#id}`` attribute-list syntax that the reference pages use for their
    anchors, so a link into them would land on the page but not the concept —
    and this project does not ship links it cannot verify.

``docs/learning-paths.md``
    For the site, where every concept links to its anchor in the reference.
    ``mkdocs build --strict`` with anchor validation enabled checks all ~180 of
    them on every build, so a concept id that is renamed without updating the
    paths fails CI rather than rotting quietly.
"""

from __future__ import annotations

from .model import LearningPath, MindMap
from .slug import github_slug

SENTINEL = (
    "<!-- GENERATED FILE -- do not edit.\n"
    "     Source of truth: paths/*.yml and concepts/**/*.yml\n"
    "     Regenerate with: python scripts/build.py -->"
)

TITLE = "Learning Paths"

INTRO = (
    "The mind map is a reference: it is organised by *what things are*, not by "
    "the order you should meet them in. These paths are the missing second "
    "axis — a teaching sequence through the same concepts, with an estimate of "
    "what each stage costs in time."
)

NOTE = (
    "Every entry below is a concept from the map, not a restatement of it. "
    "Paths reference concepts by id, so a definition corrected in one place is "
    "corrected everywhere, and a path can never cite something the map does "
    "not contain."
)

SITE_REFERENCE = "https://samrepository.github.io/Web_Technologies_MindMap/reference/"


def _plural(n: float, word: str) -> str:
    shown = int(n) if float(n).is_integer() else n
    return f"{shown} {word}{'' if shown == 1 else 's'}"


def _summary_table(mm: MindMap, link: bool) -> list[str]:
    out = [
        "| Path | Level | Duration | Effort | Concepts |",
        "|---|---|---|---|---|",
    ]
    for lp in mm.paths:
        anchor = f"#{lp.id}" if link else f"#{github_slug(lp.title)}"
        out.append(
            f"| [{lp.title}]({anchor}) | `{lp.level}` | {_plural(lp.weeks, 'week')} "
            f"| {_plural(lp.hours, 'hour')} | {len(lp.concept_ids)} |"
        )
    return out + [""]


def _concept_list(mm: MindMap, ids: list[str], link: bool) -> str:
    bits = []
    for cid in ids:
        c = mm.concepts[cid]
        entry = (
            f"[{c.label}](reference/{c.section}.md#{cid})" if link else f"**{c.label}**"
        )
        # Outside the emphasis rather than inside it. `**jQuery *(legacy)***`
        # ends in three asterisks, which CommonMark and python-markdown happen
        # to agree on today but which is needless ambiguity in a file rendered
        # by two different engines.
        if c.status == "legacy":
            entry += " *(legacy)*"
        bits.append(entry)
    return " · ".join(bits)


def _path(mm: MindMap, lp: LearningPath, link: bool) -> list[str]:
    heading = f"## {lp.title}"
    if link:
        heading += f" {{#{lp.id}}}"
    out: list[str] = [heading, ""]

    meta = (
        f"`{lp.level}` · {_plural(lp.weeks, 'week')} · {_plural(lp.hours, 'hour')} "
        f"· about {lp.hours_per_week:g} h/week"
    )
    out += [meta, "", lp.summary, ""]

    if lp.audience:
        out += [f"**Who it is for.** {lp.audience}", ""]
    if lp.outcome:
        out += [f"**By the end.** {lp.outcome}", ""]

    if lp.prerequisites:
        names = []
        for pid in lp.prerequisites:
            other = next((p for p in mm.paths if p.id == pid), None)
            if other is None:
                continue
            anchor = f"#{pid}" if link else f"#{github_slug(other.title)}"
            names.append(f"[{other.title}]({anchor})")
        out += [f"**Prerequisites.** {', '.join(names)}", ""]
    else:
        out += ["**Prerequisites.** None — this is a starting point.", ""]

    for n, m in enumerate(lp.modules, start=1):
        sub = f"### {n}. {m.title}"
        if link:
            sub += f" {{#{lp.id}--{n}}}"
        out += [sub, ""]
        out += [f"*{_plural(m.weeks, 'week')} · {_plural(m.hours, 'hour')}*", ""]
        if m.goal:
            out += [m.goal, ""]
        if m.concepts:
            out += [_concept_list(mm, m.concepts, link), ""]
        if m.practice:
            out += [f"**Practice.** {m.practice}", ""]

    return out


def _coverage(mm: MindMap) -> str:
    covered = {cid for lp in mm.paths for cid in lp.concept_ids}
    total = len(mm.concepts)
    return (
        f"These paths sequence **{len(covered)} of {total} concepts**. The "
        f"remainder are in the map deliberately — reference material a student "
        f"should be able to look up without a course walking them through it."
    )


def _render(mm: MindMap, link: bool) -> str:
    out: list[str] = [SENTINEL, "", f"# {TITLE}", "", INTRO, ""]
    out += _summary_table(mm, link)
    out += [NOTE, "", _coverage(mm), ""]
    if not link:
        out += [
            f"Concept names below are plain text. On the "
            f"[published site]({SITE_REFERENCE}) each one links to its full "
            f"definition and sources.",
            "",
        ]
    out += ["---", ""]

    for lp in mm.paths:
        out += _path(mm, lp, link)
        out += ["---", ""]

    text = "\n".join(out)
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text.rstrip() + "\n"


def render(mm: MindMap) -> str:
    """``LEARNING-PATHS.md`` — the repository-root version."""
    return _render(mm, link=False)


def render_docs(mm: MindMap) -> str:
    """``docs/learning-paths.md`` — the site version, with concept links."""
    return _render(mm, link=True)
