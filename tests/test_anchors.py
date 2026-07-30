"""Anchor and slug behaviour.

The original README shipped four dead table-of-contents anchors for two years,
because ``Web 1.0 - Documents Web`` slugs to ``web-10---documents-web`` -- the dot
is stripped, not preserved. These tests pin that algorithm and the duplicate
disambiguation that goes with it, and assert the real README stays clean.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from webtech import checks, loader, render_readme  # noqa: E402
from webtech.slug import concept_slug, github_slug, unique_slug  # noqa: E402


class GitHubSlug(unittest.TestCase):
    def test_the_bug_that_started_this(self) -> None:
        # The dot is removed, and each of "space dash space" becomes a hyphen.
        self.assertEqual(github_slug("Web 1.0 - Documents Web"), "web-10---documents-web")
        self.assertNotEqual(github_slug("Web 1.0 - Documents Web"), "web-1.0-documents-web")

    def test_punctuation_dropped_hyphens_kept(self) -> None:
        self.assertEqual(github_slug("CSP (Content Security Policy)"), "csp-content-security-policy")
        self.assertEqual(github_slug("Front-End Development"), "front-end-development")
        self.assertEqual(github_slug("AI-Era Web"), "ai-era-web")

    def test_case_and_surrounding_space(self) -> None:
        self.assertEqual(github_slug("  Mixed Case  "), "mixed-case")


class ConceptSlug(unittest.TestCase):
    def test_parenthetical_gloss_dropped(self) -> None:
        self.assertEqual(concept_slug("XSS (Cross-Site Scripting)"), "xss")
        self.assertEqual(concept_slug("MCP (Model Context Protocol)"), "mcp")

    def test_kebab_case(self) -> None:
        self.assertEqual(concept_slug("ES Modules"), "es-modules")
        self.assertEqual(concept_slug("Node.js"), "node-js")

    def test_collision_falls_back_to_full_label_then_number(self) -> None:
        taken: set[str] = set()
        a = unique_slug("Databases", taken)
        b = unique_slug("Databases", taken)
        self.assertEqual(a, "databases")
        self.assertNotEqual(a, b)
        self.assertNotIn("", (a, b))


class DuplicateHeadingDisambiguation(unittest.TestCase):
    def test_second_identical_heading_gets_a_suffix(self) -> None:
        md = "## Web Security\ntext\n\n## Web Security\nmore\n\n[a](#web-security) [b](#web-security-1)\n"
        self.assertEqual(checks.check_anchors(md), [])

    def test_dead_anchor_is_reported(self) -> None:
        md = "## Real Heading\n\n[x](#not-a-heading)\n"
        problems = checks.check_anchors(md)
        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0].kind, "anchor")

    def test_duplicate_headings_reported_separately(self) -> None:
        md = "## Same\n\n## Same\n"
        self.assertTrue(checks.check_duplicate_headings(md))


class RealReadmeStaysClean(unittest.TestCase):
    """End-to-end: the committed README must have no dead anchors or duplicates."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.mm = loader.load(ROOT)
        cls.readme = render_readme.render(cls.mm)

    def test_no_dead_anchors(self) -> None:
        self.assertEqual(checks.check_anchors(self.readme), [])

    def test_no_duplicate_headings(self) -> None:
        self.assertEqual(checks.check_duplicate_headings(self.readme), [])

    def test_every_toc_subsection_has_a_heading(self) -> None:
        for section in self.mm.sections:
            if not section.in_toc:
                continue
            for ss in section.subsections:
                with self.subTest(subsection=ss.id):
                    self.assertIn(f"#### {ss.heading}", self.readme)

    def test_graph_and_schema_are_clean(self) -> None:
        self.assertEqual(checks.check_schema(self.mm), [])
        self.assertEqual(checks.check_graph(self.mm), [])

    def test_committed_readme_matches_a_fresh_render(self) -> None:
        """Guards against a hand-edit slipping past the PreToolUse hook."""
        on_disk = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertEqual(
            on_disk,
            self.readme,
            "README.md differs from a fresh build -- run: python scripts/build.py",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
