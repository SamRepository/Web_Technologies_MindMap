"""Load the concept tree from disk."""

from __future__ import annotations

from pathlib import Path

import yaml

from .model import Concept, LearningPath, Link, MindMap, Module, Section, Subsection

TAXONOMY = "concepts/_taxonomy.yml"
PATHS_DIR = "paths"


class LoadError(RuntimeError):
    pass


def _read_text(root: Path, rel: str | None) -> str:
    if not rel:
        return ""
    p = root / rel
    return p.read_text(encoding="utf-8").strip() if p.exists() else ""


def load(root: Path) -> MindMap:
    """Read ``concepts/`` and ``content/`` under *root* into a :class:`MindMap`."""
    tax_path = root / TAXONOMY
    if not tax_path.exists():
        raise LoadError(f"missing {TAXONOMY} -- run scripts/extract_readme.py first")
    tax = yaml.safe_load(tax_path.read_text(encoding="utf-8"))

    sections: list[Section] = []
    for s in tax.get("sections", []):
        sections.append(
            Section(
                id=s["id"],
                heading=s["heading"],
                intro=_read_text(root, s.get("intro")),
                in_toc=bool(s.get("in_toc", True)),
                subsections=[
                    Subsection(id=ss["id"], heading=ss["heading"])
                    for ss in s.get("subsections", [])
                ],
            )
        )
        # Outro prose is stashed on the Section via an attribute the dataclass
        # does not declare, to keep the model minimal; renderers look it up.
        setattr(sections[-1], "outro", _read_text(root, s.get("outro")))

    concepts: dict[str, Concept] = {}
    for path in sorted((root / "concepts").rglob("*.yml")):
        if path.name.startswith("_"):
            continue
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not raw:
            raise LoadError(f"{path} is empty")
        cid = raw.get("id")
        if not cid:
            raise LoadError(f"{path} has no id")
        if cid in concepts:
            raise LoadError(f"duplicate concept id {cid!r} ({path})")
        if path.stem != cid:
            raise LoadError(f"{path}: filename must match id {cid!r}")

        links = [
            Link(
                type=ln.get("type", "reference"),
                label=ln.get("label", ""),
                url=ln.get("url"),
                access=ln.get("access", "public"),
                drive_folder_id=ln.get("drive_folder_id"),
                audience=ln.get("audience"),
            )
            for ln in (raw.get("links") or [])
        ]
        concepts[cid] = Concept(
            id=cid,
            label=raw["label"],
            section=raw["section"],
            subsection=raw.get("subsection"),
            definition=(raw.get("definition") or "").strip(),
            parent=raw.get("parent"),
            order=int(raw.get("order") or 0),
            level=raw.get("level"),
            status=raw.get("status") or "current",
            aliases=list(raw.get("aliases") or []),
            see_also=list(raw.get("see_also") or []),
            links=links,
        )

    # Wire children, ordered as published.
    for c in sorted(concepts.values(), key=lambda c: c.order):
        if c.parent:
            parent = concepts.get(c.parent)
            if parent is None:
                raise LoadError(f"{c.id}: parent {c.parent!r} does not exist")
            parent.children.append(c)

    prose = {
        key: _read_text(root, rel)
        for key, rel in (tax.get("prose") or {}).items()
    }
    # Not a file reference: an optional external access-request URL that the
    # 🔒 badge points at once one exists (Phase 5).
    if tax.get("access_request_url"):
        prose["access_request_url"] = str(tax["access_request_url"]).strip()
    return MindMap(
        sections=sections,
        concepts=concepts,
        prose=prose,
        paths=load_paths(root),
    )


def load_paths(root: Path) -> list[LearningPath]:
    """Read ``paths/*.yml``. Absent directory means no paths, not an error."""
    base = root / PATHS_DIR
    if not base.exists():
        return []

    out: list[LearningPath] = []
    seen: set[str] = set()
    for p in sorted(base.glob("*.yml")):
        if p.name.startswith("_"):
            continue
        raw = yaml.safe_load(p.read_text(encoding="utf-8"))
        if not raw:
            raise LoadError(f"{p} is empty")
        pid = raw.get("id")
        if not pid:
            raise LoadError(f"{p} has no id")
        if pid in seen:
            raise LoadError(f"duplicate path id {pid!r} ({p})")
        if p.stem != pid:
            raise LoadError(f"{p}: filename must match id {pid!r}")
        seen.add(pid)

        out.append(
            LearningPath(
                id=pid,
                title=raw["title"],
                level=raw.get("level") or "beginner",
                summary=(raw.get("summary") or "").strip(),
                audience=(raw.get("audience") or "").strip(),
                outcome=(raw.get("outcome") or "").strip(),
                prerequisites=list(raw.get("prerequisites") or []),
                hours_per_week=float(raw.get("hours_per_week") or 6),
                order=int(raw.get("order") or 0),
                modules=[
                    Module(
                        title=m["title"],
                        weeks=float(m.get("weeks") or 0),
                        hours=float(m.get("hours") or 0),
                        goal=(m.get("goal") or "").strip(),
                        concepts=list(m.get("concepts") or []),
                        practice=(m.get("practice") or "").strip(),
                    )
                    for m in (raw.get("modules") or [])
                ],
            )
        )
    return sorted(out, key=lambda lp: (lp.order, lp.id))
