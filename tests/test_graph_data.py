"""The data the graph view is drawn from.

The graph deliberately carries *two* edge kinds. Hierarchy edges are not emitted
at all -- the view derives them by walking the tree it already has -- so the only
thing added to the payload is the ``see_also`` cross-links, and these tests pin
that payload's shape.

They run without a browser, which matters: CI installs no Chromium, so the
Playwright suite in ``test_mindmap_ui.py`` skips there while these still run.
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from webtech import loader, render_mindmap  # noqa: E402

MM = loader.load(ROOT)
HTML = (ROOT / "docs" / "mindmap.html").read_text(encoding="utf-8")


def emitted_rel() -> list[list[str]]:
    """The ``REL`` array as it appears in the committed mind map."""
    m = re.search(r"^const REL = (\[.*?\]);$", HTML, re.M)
    assert m, "no REL array in docs/mindmap.html"
    return json.loads(m.group(1))


class RelatedEdges(unittest.TestCase):
    def setUp(self) -> None:
        self.rel = render_mindmap.build_related(MM)

    def test_every_endpoint_resolves_to_a_concept(self) -> None:
        for a, b in self.rel:
            self.assertIn(a, MM.concepts, f"dangling see_also endpoint {a!r}")
            self.assertIn(b, MM.concepts, f"dangling see_also endpoint {b!r}")

    def test_undirected_and_deduplicated(self) -> None:
        """``a.see_also: [b]`` and ``b.see_also: [a]`` are one edge, not two."""
        seen = set()
        for pair in self.rel:
            key = tuple(pair)
            self.assertNotIn(key, seen, f"duplicate edge {key}")
            seen.add(key)
            self.assertEqual(list(key), sorted(key), "edge endpoints not normalised")

    def test_no_self_edges(self) -> None:
        for a, b in self.rel:
            self.assertNotEqual(a, b, f"{a} is see_also to itself")

    def test_no_edge_restates_the_hierarchy(self) -> None:
        """A cross-link between a parent and its own child draws a dashed edge
        directly on top of a solid one and tells the reader nothing new."""
        redundant = [
            (a, b) for a, b in self.rel
            if MM.concepts[a].parent == b or MM.concepts[b].parent == a
        ]
        self.assertEqual(redundant, [])

    def test_matches_the_yaml(self) -> None:
        expected = {
            tuple(sorted((c.id, o)))
            for c in MM.concepts.values()
            for o in c.see_also
            if o in MM.concepts and o != c.id
        }
        self.assertEqual({tuple(p) for p in self.rel}, expected)

    def test_output_is_byte_stable(self) -> None:
        """``build.py --check`` diffs committed output against a fresh render;
        an unsorted set would make that comparison flap between runs."""
        self.assertEqual(self.rel, sorted(self.rel))
        self.assertEqual(self.rel, render_mindmap.build_related(MM))

    def test_committed_mindmap_carries_the_same_edges(self) -> None:
        self.assertEqual(emitted_rel(), self.rel)


class TreePayload(unittest.TestCase):
    def test_concepts_carry_their_cross_links(self) -> None:
        """The panel's Related list reads ``rel`` off the tree node."""
        tree = render_mindmap.build_tree(MM)
        found: dict[str, list[str]] = {}

        def walk(n: dict) -> None:
            if "rel" in n:
                found[n["id"]] = n["rel"]
            for c in n.get("children", []):
                walk(c)

        walk(tree)
        expected = {c.id: list(c.see_also) for c in MM.concepts.values() if c.see_also}
        self.assertEqual(found, expected)

    def test_restricted_links_still_carry_no_url(self) -> None:
        """Same rule as the README: the URL is absent, not hidden."""
        tree = render_mindmap.build_tree(MM)
        offenders: list[str] = []

        def walk(n: dict) -> None:
            for ln in n.get("links", []):
                if ln.get("restricted") and "url" in ln:
                    offenders.append(n["id"])
            for c in n.get("children", []):
                walk(c)

        walk(tree)
        self.assertEqual(offenders, [])


class SelfContained(unittest.TestCase):
    def test_no_external_script_or_stylesheet(self) -> None:
        """The graph view added physics, not a dependency."""
        self.assertEqual(re.findall(r"<(?:script|link)[^>]*\b(?:src|href)=", HTML), [])

    def test_both_views_are_present(self) -> None:
        for needle in ('id="tab-tree"', 'id="tab-graph"', 'id="view"', 'id="gview"'):
            self.assertIn(needle, HTML, f"missing {needle}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
