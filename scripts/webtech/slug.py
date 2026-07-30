"""Slug generation.

Two different slug rules live here and must not be conflated:

* :func:`github_slug` reproduces GitHub's heading-anchor algorithm. It exists so
  the generated table of contents can be checked against generated headings. The
  original README shipped four dead anchors because ``Web 1.0`` slugs to
  ``web-10``, not ``web-1.0`` -- the dot is stripped, not kept.
* :func:`concept_slug` produces concept ids and filenames. Shorter and friendlier
  than a heading slug, and stable across edits to the surrounding prose.
"""

from __future__ import annotations

import re
import unicodedata

_GITHUB_STRIP = re.compile(r"[^\w\s-]", re.UNICODE)
_PARENTHETICAL = re.compile(r"\s*\([^)]*\)")
_NON_WORD = re.compile(r"[^a-z0-9]+")


def github_slug(heading: str) -> str:
    """Slugify *heading* the way GitHub does for in-page anchors.

    Lowercase, drop everything that is not a word character / space / hyphen,
    then turn whitespace runs into single hyphens -- except that each individual
    whitespace character becomes its own hyphen, which is why ``Web 1.0 - Docs``
    yields three consecutive hyphens around the dash.
    """
    s = heading.strip().lower()
    s = _GITHUB_STRIP.sub("", s)
    return re.sub(r"\s", "-", s)


def concept_slug(label: str) -> str:
    """Return a kebab-case id for a concept *label*.

    A trailing parenthetical gloss is dropped, so ``XSS (Cross-Site Scripting)``
    becomes ``xss`` rather than ``xss-cross-site-scripting``. Callers are
    responsible for collision handling -- see :func:`unique_slug`.
    """
    s = _PARENTHETICAL.sub("", label).strip()
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = _NON_WORD.sub("-", s.lower()).strip("-")
    return s or "concept"


def unique_slug(label: str, taken: set[str], *, full_label: str | None = None) -> str:
    """Return a slug for *label* that is not already in *taken*.

    Falls back to the full label (parenthetical included) before resorting to a
    numeric suffix, so ids stay meaningful when two concepts share a short name.
    """
    base = concept_slug(label)
    if base not in taken:
        taken.add(base)
        return base

    if full_label:
        longer = _NON_WORD.sub("-", full_label.lower()).strip("-")
        if longer and longer not in taken:
            taken.add(longer)
            return longer

    n = 2
    while f"{base}-{n}" in taken:
        n += 1
    slug = f"{base}-{n}"
    taken.add(slug)
    return slug
