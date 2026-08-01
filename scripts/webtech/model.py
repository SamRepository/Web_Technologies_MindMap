"""Data model for the mind map.

The concept tree is the single source of truth. Everything published -- README,
interactive mind map, SKOS export, site -- is a projection of it.
"""

from __future__ import annotations

from dataclasses import dataclass, field

#: Allowed values for a link's ``type``.
#:
#: ``reference`` is the catch-all for an authoritative page that is none of the
#: more specific kinds (a standards body's home page, a vendor guide). Prefer a
#: specific type when one applies.
LINK_TYPES = frozenset(
    {"official", "wikipedia", "mdn", "spec", "video", "course", "reference"}
)

#: Link types that count as authoritative for the "every concept should have at
#: least one primary source" check.
AUTHORITATIVE_LINK_TYPES = frozenset({"official", "wikipedia", "mdn", "spec"})

#: Pedagogical difficulty. Optional -- the migrated content has no level data,
#: and inventing one for ~180 concepts would be fabrication. Phase 4 populates.
LEVELS = frozenset({"beginner", "intermediate", "advanced"})

#: Lifecycle. ``legacy`` marks superseded technology that is deliberately kept
#: because students still meet it in older tutorials.
STATUSES = frozenset({"current", "emerging", "legacy"})

#: Access control for a link. A ``restricted`` link's URL and Drive folder id
#: must never reach a public artifact -- see :mod:`webtech.checks`.
ACCESS_LEVELS = frozenset({"public", "restricted"})


@dataclass
class Link:
    """An outbound resource attached to a concept."""

    type: str
    label: str
    url: str | None = None
    access: str = "public"
    drive_folder_id: str | None = None
    audience: str | None = None

    @property
    def is_restricted(self) -> bool:
        return self.access == "restricted"

    def to_yaml(self) -> dict:
        d: dict = {"type": self.type, "label": self.label}
        if self.url:
            d["url"] = self.url
        if self.access != "public":
            d["access"] = self.access
        if self.drive_folder_id:
            d["drive_folder_id"] = self.drive_folder_id
        if self.audience:
            d["audience"] = self.audience
        return d


@dataclass
class Concept:
    """A single node of the mind map."""

    id: str
    label: str
    section: str
    definition: str = ""
    #: Arabic rendering of :attr:`definition`. Optional and independent: a
    #: concept may be translated or not, and an untranslated one simply shows
    #: no Arabic block. Never machine-translated at build time -- it is
    #: authored content held to the same standard as the English.
    definition_ar: str = ""
    parent: str | None = None
    subsection: str | None = None
    order: int = 0
    level: str | None = None
    status: str = "current"
    aliases: list[str] = field(default_factory=list)
    see_also: list[str] = field(default_factory=list)
    links: list[Link] = field(default_factory=list)

    # Populated by the loader, not stored in YAML.
    children: list["Concept"] = field(default_factory=list, repr=False, compare=False)

    @property
    def public_links(self) -> list[Link]:
        return [ln for ln in self.links if not ln.is_restricted]

    @property
    def restricted_links(self) -> list[Link]:
        return [ln for ln in self.links if ln.is_restricted]

    def to_yaml(self) -> dict:
        """Serialise in a stable key order so diffs stay readable."""
        d: dict = {
            "id": self.id,
            "label": self.label,
            "section": self.section,
        }
        if self.subsection:
            d["subsection"] = self.subsection
        d["parent"] = self.parent
        d["order"] = self.order
        d["level"] = self.level
        d["status"] = self.status
        if self.aliases:
            d["aliases"] = list(self.aliases)
        if self.see_also:
            d["see_also"] = list(self.see_also)
        if self.definition:
            d["definition"] = self.definition
        if self.definition_ar:
            d["definition_ar"] = self.definition_ar
        if self.links:
            d["links"] = [ln.to_yaml() for ln in self.links]
        return d


@dataclass
class Subsection:
    """A ``####`` heading inside a section."""

    id: str
    heading: str


@dataclass
class Section:
    """A ``###`` heading -- one of the top-level branches of the map."""

    id: str
    heading: str
    intro: str = ""
    in_toc: bool = True
    subsections: list[Subsection] = field(default_factory=list)
    rule_after: bool = True

    @property
    def anchor(self) -> str:
        from .slug import github_slug

        return github_slug(self.heading)


@dataclass
class Module:
    """One teaching unit of a learning path.

    ``concepts`` is an ordered list of concept ids: a path does not restate any
    content, it sequences what the map already holds. That is what keeps a
    curriculum from drifting away from the reference it is built on.
    """

    title: str
    weeks: float
    hours: float
    goal: str = ""
    concepts: list[str] = field(default_factory=list)
    practice: str = ""


@dataclass
class LearningPath:
    """An ordered route through the map, for one kind of learner.

    Named ``LearningPath`` rather than ``Path`` so it cannot be confused with
    :class:`pathlib.Path`, which the loader and every renderer also use.
    """

    id: str
    title: str
    level: str
    summary: str
    audience: str = ""
    outcome: str = ""
    prerequisites: list[str] = field(default_factory=list)
    hours_per_week: float = 6.0
    order: int = 0
    modules: list[Module] = field(default_factory=list)

    @property
    def weeks(self) -> float:
        return sum(m.weeks for m in self.modules)

    @property
    def hours(self) -> float:
        return sum(m.hours for m in self.modules)

    @property
    def concept_ids(self) -> list[str]:
        return [cid for m in self.modules for cid in m.concepts]


@dataclass
class MindMap:
    """The whole tree, plus the prose that surrounds it."""

    sections: list[Section]
    concepts: dict[str, Concept]
    prose: dict[str, str]
    paths: list[LearningPath] = field(default_factory=list)

    def by_section(self, section_id: str) -> list[Concept]:
        return [c for c in self.concepts.values() if c.section == section_id]

    def roots(self, section_id: str, subsection_id: str | None = None) -> list[Concept]:
        out = [
            c
            for c in self.concepts.values()
            if c.section == section_id
            and c.subsection == subsection_id
            and c.parent is None
        ]
        return sorted(out, key=lambda c: c.order)

    @property
    def restricted_links(self) -> list[tuple[Concept, Link]]:
        return [
            (c, ln)
            for c in self.concepts.values()
            for ln in c.links
            if ln.is_restricted
        ]
