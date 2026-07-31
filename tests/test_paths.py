"""Learning paths: the curriculum layer over the concept map.

A path adds no content of its own -- it is an ordering over concept ids. That
is the property worth testing: the moment a path could name something the map
does not contain, or restate a definition in its own words, it becomes a second
source of truth that drifts from the first.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from webtech import checks, loader, render_paths  # noqa: E402
from webtech.model import LearningPath, MindMap, Module  # noqa: E402

MM = loader.load(ROOT)


class Loading(unittest.TestCase):
    def test_all_four_paths_load(self) -> None:
        self.assertEqual(
            [p.id for p in MM.paths],
            [
                "front-end-foundations",
                "back-end-with-python",
                "full-stack",
                "semantic-web-and-knowledge-graphs",
            ],
        )

    def test_ordered_by_order_then_id(self) -> None:
        orders = [p.order for p in MM.paths]
        self.assertEqual(orders, sorted(orders))

    def test_totals_are_derived_not_stored(self) -> None:
        for lp in MM.paths:
            self.assertEqual(lp.weeks, sum(m.weeks for m in lp.modules))
            self.assertEqual(lp.hours, sum(m.hours for m in lp.modules))

    def test_every_path_has_a_summary_and_an_outcome(self) -> None:
        for lp in MM.paths:
            self.assertTrue(lp.summary, f"{lp.id}: no summary")
            self.assertTrue(lp.outcome, f"{lp.id}: no outcome")


class Integrity(unittest.TestCase):
    def test_the_real_paths_are_clean(self) -> None:
        self.assertEqual([str(p) for p in checks.check_paths(MM)], [])

    def test_unknown_concept_is_an_error(self) -> None:
        mm = self._one(Module("M", 1, 6, concepts=["definitely-not-a-concept"]))
        self.assertIn("unknown concept", str(checks.check_paths(mm)))

    def test_repeated_concept_within_a_path_is_an_error(self) -> None:
        """Always a copy-paste slip in practice; a genuine second pass belongs
        in its own module with its own hours."""
        mm = self._one(
            Module("A", 1, 6, concepts=["javascript"]),
            Module("B", 1, 6, concepts=["javascript"]),
        )
        self.assertIn("appears in both", str(checks.check_paths(mm)))

    def test_the_same_concept_in_two_different_paths_is_fine(self) -> None:
        shared = set(MM.paths[0].concept_ids) & set(MM.paths[1].concept_ids)
        self.assertTrue(shared, "expected the paths to overlap somewhere")
        self.assertEqual([str(p) for p in checks.check_paths(MM)], [])

    def test_unknown_prerequisite_is_an_error(self) -> None:
        mm = self._one(Module("M", 1, 6, concepts=["javascript"]))
        mm.paths[0].prerequisites = ["no-such-path"]
        self.assertIn("unknown prerequisite", str(checks.check_paths(mm)))

    def test_prerequisite_cycle_is_caught(self) -> None:
        a = LearningPath(id="a", title="A", level="beginner", summary="",
                         prerequisites=["b"],
                         modules=[Module("M", 1, 6, concepts=["javascript"])])
        b = LearningPath(id="b", title="B", level="beginner", summary="",
                         prerequisites=["a"],
                         modules=[Module("M", 1, 6, concepts=["css3"])])
        mm = MindMap(sections=MM.sections, concepts=MM.concepts, prose={}, paths=[a, b])
        self.assertIn("prerequisite cycle", str(checks.check_paths(mm)))

    def test_zero_length_module_is_an_error(self) -> None:
        mm = self._one(Module("M", 0, 0, concepts=["javascript"]))
        self.assertIn("weeks and hours", str(checks.check_paths(mm)))

    def test_real_prerequisites_resolve(self) -> None:
        ids = {p.id for p in MM.paths}
        for lp in MM.paths:
            for pre in lp.prerequisites:
                self.assertIn(pre, ids)

    def _one(self, *modules: Module) -> MindMap:
        lp = LearningPath(
            id="probe", title="Probe", level="beginner", summary="",
            modules=list(modules),
        )
        return MindMap(
            sections=MM.sections, concepts=MM.concepts, prose={}, paths=[lp]
        )


class Rendering(unittest.TestCase):
    def setUp(self) -> None:
        self.root = render_paths.render(MM)
        self.site = render_paths.render_docs(MM)

    def test_both_versions_name_every_path(self) -> None:
        for lp in MM.paths:
            self.assertIn(lp.title, self.root)
            self.assertIn(lp.title, self.site)

    def test_site_version_links_concepts_to_their_anchors(self) -> None:
        c = MM.concepts["typescript"]
        self.assertIn(f"](reference/{c.section}.md#typescript)", self.site)

    def test_root_version_links_no_concepts(self) -> None:
        """GitHub does not parse the ``{#id}`` anchors the reference pages use,
        so a link into them would land on the page but not the concept. This
        project does not ship links it cannot verify."""
        self.assertNotIn("](reference/", self.root)

    def test_in_page_anchors_resolve(self) -> None:
        """The summary table links each path to its own section."""
        self.assertEqual([str(p) for p in checks.check_anchors(self.root)], [])

    def test_no_definition_is_restated(self) -> None:
        """A path sequences concepts; it must not paraphrase them. If a
        definition's text appears verbatim in a path file, the map has acquired
        a second source of truth."""
        sources = "\n".join(
            p.read_text(encoding="utf-8") for p in sorted((ROOT / "paths").glob("*.yml"))
        )
        for c in MM.concepts.values():
            if len(c.definition) < 60:
                continue
            self.assertNotIn(c.definition[:60], sources, f"{c.id} definition copied")

    def test_committed_output_matches_a_fresh_render(self) -> None:
        for rel, fresh in (
            ("LEARNING-PATHS.md", self.root),
            ("docs/learning-paths.md", self.site),
        ):
            with self.subTest(rel):
                self.assertEqual(
                    (ROOT / rel).read_text(encoding="utf-8"), fresh,
                    f"{rel} is stale -- run python scripts/build.py",
                )


class Coverage(unittest.TestCase):
    def test_coverage_is_reported_not_enforced(self) -> None:
        """Advisory by design: the map is a reference as well as a curriculum."""
        uncovered = checks.check_path_coverage(MM)
        self.assertTrue(uncovered, "expected some reference-only concepts")
        self.assertTrue(all(p.kind == "coverage" for p in uncovered))
        # And they are genuinely absent from every path, not a reporting bug.
        taught = {cid for lp in MM.paths for cid in lp.concept_ids}
        for p in uncovered:
            self.assertNotIn(p.detail.split(":")[0], taught)

    def test_a_majority_of_the_map_is_taught(self) -> None:
        taught = {cid for lp in MM.paths for cid in lp.concept_ids}
        self.assertGreater(len(taught) / len(MM.concepts), 0.6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
