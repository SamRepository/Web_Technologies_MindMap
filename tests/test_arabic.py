"""The Arabic layer: a second definition, and links to Arabic Wikipedia.

Arabic is optional per concept and lands incrementally, so almost nothing here
asserts coverage. What it does assert is that when Arabic *is* present it is
well-formed everywhere it surfaces: the field round-trips through YAML, the
mind map carries it, and the RDF tags it with a language rather than emitting
two untagged definitions a SPARQL query cannot tell apart.

Encoding is the recurring hazard. These files are UTF-8 and the development
console is cp1252, so every read here is explicit about it -- a test that
passes only because it never managed to print the text is no test.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from webtech import checks, loader, render_mindmap, render_skos  # noqa: E402
from webtech.model import Concept, MindMap  # noqa: E402

MM = loader.load(ROOT)

#: Arabic script, matching webtech.checks.ARABIC_RE.
ARABIC = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿ]")

TRANSLATED = [c for c in MM.concepts.values() if c.definition_ar]
AR_LABEL = "Wikipedia (Ar)"


class Schema(unittest.TestCase):
    def test_some_concepts_are_translated(self) -> None:
        """Guards the premise of everything below."""
        self.assertGreater(len(TRANSLATED), 10)

    def test_every_translation_is_actually_arabic(self) -> None:
        for c in TRANSLATED:
            with self.subTest(c.id):
                self.assertRegex(c.definition_ar, ARABIC)

    def test_translation_never_stands_alone(self) -> None:
        """Arabic translates the English, so it cannot exist without it."""
        for c in TRANSLATED:
            with self.subTest(c.id):
                self.assertTrue(c.definition, f"{c.id}: Arabic but no English")

    def test_round_trips_through_yaml(self) -> None:
        for c in TRANSLATED[:5]:
            with self.subTest(c.id):
                self.assertEqual(c.to_yaml()["definition_ar"], c.definition_ar)

    def test_untranslated_concepts_omit_the_key(self) -> None:
        plain = next(c for c in MM.concepts.values() if not c.definition_ar)
        self.assertNotIn("definition_ar", plain.to_yaml())

    def test_the_real_tree_is_clean(self) -> None:
        arabic_problems = [
            str(p) for p in checks.check_schema(MM) if "definition_ar" in str(p)
        ]
        self.assertEqual(arabic_problems, [])

    # -- negative controls, so the checks are known to fire ---------------
    def test_arabic_without_english_is_rejected(self) -> None:
        mm = self._one(definition="", definition_ar="نص عربي")
        self.assertIn("definition_ar with no definition", str(checks.check_schema(mm)))

    def test_english_pasted_into_the_arabic_field_is_rejected(self) -> None:
        """The failure this catches renders as a left-to-right paragraph inside
        a right-to-left block, which looks broken rather than wrong."""
        mm = self._one(definition="A thing.", definition_ar="A thing, but again.")
        self.assertIn("contains no Arabic script", str(checks.check_schema(mm)))

    def test_a_correct_pair_passes(self) -> None:
        mm = self._one(definition="A thing.", definition_ar="شيء ما.")
        self.assertEqual([str(p) for p in checks.check_schema(mm)], [])

    def _one(self, **kw) -> MindMap:
        c = Concept(id="probe", label="Probe", section=MM.sections[0].id, **kw)
        return MindMap(sections=MM.sections, concepts={"probe": c}, prose={})


class Coverage(unittest.TestCase):
    def test_every_definition_is_translated(self) -> None:
        """Coverage is complete as of the second pass. Should a concept be added
        without Arabic this reports it -- as an advisory below, not a failure."""
        self.assertEqual(checks.check_translation_coverage(MM), [])

    def test_a_gap_is_reported_as_an_advisory(self) -> None:
        """The check still has to fire. Asserted against a synthetic gap rather
        than the real tree, so completing the translation cannot quietly turn
        this into a test of nothing."""
        c = Concept(
            id="probe", label="Probe", section=MM.sections[0].id,
            definition="An untranslated thing.",
        )
        mm = MindMap(sections=MM.sections, concepts={"probe": c}, prose={})
        pending = checks.check_translation_coverage(mm)
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].kind, "arabic")

    def test_coverage_never_fails_a_build(self) -> None:
        """Advisory by design: translation is authored content that lands over
        time, so a gap must never be an error."""
        c = Concept(
            id="probe", label="Probe", section=MM.sections[0].id,
            definition="An untranslated thing.",
        )
        mm = MindMap(sections=MM.sections, concepts={"probe": c}, prose={})
        self.assertEqual([str(p) for p in checks.check_schema(mm)], [])

    def test_counts_line_up(self) -> None:
        defined = [c for c in MM.concepts.values() if c.definition]
        self.assertEqual(len(defined), len(TRANSLATED))


class MindMapPayload(unittest.TestCase):
    def setUp(self) -> None:
        self.tree = render_mindmap.build_tree(MM)

    def test_translations_reach_the_detail_pane_data(self) -> None:
        found: dict[str, str] = {}

        def walk(n: dict) -> None:
            if "def_ar" in n:
                found[n["id"]] = n["def_ar"]
            for k in n.get("children", []):
                walk(k)

        walk(self.tree)
        self.assertEqual(found, {c.id: c.definition_ar for c in TRANSLATED})

    def test_the_committed_mindmap_carries_arabic(self) -> None:
        html = (ROOT / "docs" / "mindmap.html").read_text(encoding="utf-8")
        self.assertRegex(html, ARABIC)
        # The payload is JSON with ensure_ascii=False, so the Arabic must be
        # present as real characters rather than \u escapes.
        self.assertIn(TRANSLATED[0].definition_ar[:30], html)

    def test_the_pane_marks_direction_and_language(self) -> None:
        html = (ROOT / "docs" / "mindmap.html").read_text(encoding="utf-8")
        self.assertIn('class="def-ar" dir="rtl" lang="ar"', html)

    def test_a_toggle_exists_and_starts_on(self) -> None:
        html = (ROOT / "docs" / "mindmap.html").read_text(encoding="utf-8")
        self.assertIn('id="ar" aria-pressed="true"', html)


class SkosExport(unittest.TestCase):
    def setUp(self) -> None:
        self.ttl = (ROOT / "dist" / "webtech.ttl").read_text(encoding="utf-8")

    def test_arabic_definitions_are_language_tagged(self) -> None:
        """Two untagged definitions would be indistinguishable to a query; the
        language tag is what makes the export genuinely multilingual."""
        self.assertEqual(self.ttl.count("@ar"), len(TRANSLATED))

    def test_english_is_still_tagged_too(self) -> None:
        defined = sum(1 for c in MM.concepts.values() if c.definition)
        self.assertGreaterEqual(self.ttl.count("@en"), defined)

    def test_a_translated_concept_carries_both(self) -> None:
        g = render_skos.render(MM)
        c = TRANSLATED[0]
        self.assertIn(c.definition_ar[:25], g)
        self.assertIn(c.definition[:25], g)

    def test_the_graph_parses_and_queries_by_language(self) -> None:
        from rdflib import Graph
        from rdflib.namespace import SKOS

        g = Graph().parse(data=self.ttl, format="turtle")
        ar = [o for _, _, o in g.triples((None, SKOS.definition, None))
              if getattr(o, "language", None) == "ar"]
        self.assertEqual(len(ar), len(TRANSLATED))


class ArabicWikipediaLinks(unittest.TestCase):
    def setUp(self) -> None:
        self.links = [
            (c, ln) for c in MM.concepts.values()
            for ln in c.links if ln.label == AR_LABEL
        ]

    def test_the_resolver_added_a_substantial_number(self) -> None:
        self.assertGreater(len(self.links), 100)

    def test_all_point_at_arabic_wikipedia(self) -> None:
        for c, ln in self.links:
            with self.subTest(c.id):
                self.assertTrue(
                    ln.url.startswith("https://ar.wikipedia.org/wiki/"), ln.url
                )

    def test_none_is_restricted(self) -> None:
        """A public encyclopaedia link must never be marked restricted, which
        would strip it from every artifact for no reason."""
        self.assertEqual([c.id for c, ln in self.links if ln.is_restricted], [])

    def test_one_per_concept(self) -> None:
        seen: dict[str, int] = {}
        for c, _ in self.links:
            seen[c.id] = seen.get(c.id, 0) + 1
        self.assertEqual([k for k, v in seen.items() if v > 1], [])

    def test_each_sits_beside_an_english_article(self) -> None:
        """The resolver derives Arabic from English, so one cannot appear alone."""
        for c, _ in self.links:
            with self.subTest(c.id):
                self.assertTrue(
                    any(ln.type == "wikipedia" and ln.label != AR_LABEL
                        for ln in c.links),
                    f"{c.id}: Arabic article with no English one",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
