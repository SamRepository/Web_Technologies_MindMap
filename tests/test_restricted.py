"""The restricted-resource guarantee, under test.

This is the security-critical property of the whole generator: a link marked
``access: restricted`` must never have its URL or Drive folder id reach a public
artifact. Phase 2 verified it by hand once; these tests make it a standing check
so a future change to a renderer cannot quietly break it.

Runs under pytest or ``python -m unittest discover tests``.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from webtech import checks, render_mindmap, render_readme, render_skos  # noqa: E402
from webtech.model import Concept, Link, MindMap, Section, Subsection  # noqa: E402

SECRET_ID = "SECRET_DRIVE_FOLDER_ID_0123456789"
SECRET_URL = f"https://drive.google.com/drive/folders/{SECRET_ID}"


def fixture(*, restricted: bool = True) -> MindMap:
    """A minimal two-concept map, optionally carrying a restricted link."""
    links = [Link(type="official", label="Official Website", url="https://example.org/")]
    if restricted:
        links.append(
            Link(
                type="course",
                label="TP recordings",
                access="restricted",
                drive_folder_id=SECRET_ID,
                audience="webtech-students",
            )
        )

    parent = Concept(
        id="frameworks",
        label="Frameworks",
        section="03-web-development",
        subsection="back-end-development",
        order=1,
        definition="Group node.",
    )
    child = Concept(
        id="django",
        label="Django",
        section="03-web-development",
        subsection="back-end-development",
        parent="frameworks",
        order=2,
        definition="A high-level Python web framework.",
        links=links,
    )
    parent.children.append(child)

    section = Section(
        id="03-web-development",
        heading="Web Development",
        intro="Intro prose.",
        subsections=[Subsection(id="back-end-development", heading="Back-End Development")],
    )
    setattr(section, "outro", "")
    return MindMap(
        sections=[section],
        concepts={"frameworks": parent, "django": child},
        prose={"header": "# Test", "guide_intro": "", "footer": ""},
    )


class RestrictedLinksNeverLeak(unittest.TestCase):
    def setUp(self) -> None:
        self.mm = fixture()
        self.artifacts = {
            "README.md": render_readme.render(self.mm),
            "docs/mindmap.html": render_mindmap.render(self.mm),
            "dist/webtech.ttl": render_skos.render(self.mm),
        }

    def test_declared_in_the_model(self) -> None:
        """Sanity: the fixture really does declare a restricted link."""
        self.assertEqual(len(self.mm.restricted_links), 1)

    def test_no_artifact_contains_the_folder_id(self) -> None:
        for name, content in self.artifacts.items():
            with self.subTest(artifact=name):
                self.assertNotIn(SECRET_ID, content)

    def test_no_artifact_contains_the_url(self) -> None:
        for name, content in self.artifacts.items():
            with self.subTest(artifact=name):
                self.assertNotIn(SECRET_URL, content)
                self.assertNotIn("drive.google.com", content)

    def test_leak_check_agrees(self) -> None:
        """The output-side check must also find nothing."""
        self.assertEqual(checks.check_restricted_leak(self.mm, self.artifacts), [])

    def test_leak_check_actually_fires(self) -> None:
        """A negative control.

        If the leak check cannot detect a planted secret then its silence above
        means nothing. Plant one and require a LEAK problem.
        """
        tampered = dict(self.artifacts)
        tampered["README.md"] += f"\n<!-- oops {SECRET_URL} -->\n"
        problems = checks.check_restricted_leak(self.mm, tampered)
        self.assertTrue(problems, "leak check failed to notice a planted secret")
        self.assertEqual(problems[0].kind, "LEAK")

    def test_badge_is_rendered_instead(self) -> None:
        readme = self.artifacts["README.md"]
        self.assertIn("🔒 TP recordings", readme)
        self.assertIn("request access", readme)

    def test_public_link_still_rendered_normally(self) -> None:
        self.assertIn("https://example.org/", self.artifacts["README.md"])


class BadgeAnchorAlwaysResolves(unittest.TestCase):
    """The 🔒 badge points at an in-page anchor; that anchor must exist.

    This regression-tests a real bug: the badge originally linked to a section
    that was never emitted, so adding any restricted link produced a dead anchor
    and failed the build.
    """

    def test_access_section_emitted_when_a_badge_exists(self) -> None:
        readme = render_readme.render(fixture(restricted=True))
        self.assertIn(render_readme.ACCESS_HEADING, readme)
        self.assertEqual(checks.check_anchors(readme), [])

    def test_access_section_absent_when_no_badge(self) -> None:
        readme = render_readme.render(fixture(restricted=False))
        self.assertNotIn(render_readme.ACCESS_HEADING, readme)
        self.assertEqual(checks.check_anchors(readme), [])

    def test_external_form_url_replaces_the_in_page_section(self) -> None:
        mm = fixture(restricted=True)
        mm.prose["access_request_url"] = "https://forms.example.org/request"
        readme = render_readme.render(mm)
        self.assertIn("https://forms.example.org/request", readme)
        self.assertNotIn(render_readme.ACCESS_HEADING, readme)
        self.assertEqual(checks.check_anchors(readme), [])


class SchemaRejectsUnsafeInput(unittest.TestCase):
    def test_restricted_link_carrying_a_url_is_an_error(self) -> None:
        mm = fixture()
        mm.concepts["django"].links[-1].url = SECRET_URL
        problems = checks.check_schema(mm)
        self.assertTrue(
            any(p.kind == "restricted" for p in problems),
            "a restricted link with a url must be rejected at the schema level",
        )

    def test_restricted_link_without_folder_id_is_an_error(self) -> None:
        mm = fixture()
        mm.concepts["django"].links[-1].drive_folder_id = None
        problems = checks.check_schema(mm)
        self.assertTrue(any(p.kind == "schema" for p in problems))


if __name__ == "__main__":
    unittest.main(verbosity=2)
