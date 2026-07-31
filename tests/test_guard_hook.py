"""The PreToolUse guard that denies hand-edits of generated files.

Two halves, and both need pinning, because the hook has already failed each way:

* It must **deny** every declared build product. Without that, a hand-edit of
  README.md survives until the next build and silently diverges the map from
  the text -- the drift this whole project exists to remove.
* It must **allow** the hand-written sources. The hook's content scan looks for
  the literal banner text that build.py stamps into its output, and a generator
  contains that banner as *data* -- it is what it writes. So render_readme.py,
  render_docs.py, render_paths.py and the hook itself all matched, and the hook
  denied edits to the exact files its own message says to edit. Undetected from
  Phase 0 until a new renderer was added in Phase 7.

The hook is driven the way the harness drives it: a JSON tool call on stdin, a
permission decision on stdout.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / ".claude" / "hooks" / "guard_generated.py"

BANNER = "GENERATED" + " FILE"   # split so this test file is not itself flagged


def run(file_path: str, tool: str = "Edit") -> dict:
    """Invoke the hook and return its decision, or {} when it stays silent."""
    payload = json.dumps({"tool_name": tool, "tool_input": {"file_path": file_path}})
    proc = subprocess.run(
        [sys.executable, str(HOOK)],
        input=payload, capture_output=True, text=True, cwd=str(ROOT),
    )
    if proc.returncode != 0:
        raise AssertionError(f"hook exited {proc.returncode}: {proc.stderr}")
    out = proc.stdout.strip()
    return json.loads(out)["hookSpecificOutput"] if out else {}


def denied(file_path: str, tool: str = "Edit") -> bool:
    return run(file_path, tool).get("permissionDecision") == "deny"


class DeniesGeneratedOutput(unittest.TestCase):
    GENERATED = (
        "README.md",
        "LEARNING-PATHS.md",
        "docs/mindmap.html",
        "docs/learning-paths.md",
        "docs/reference/index.md",
        "docs/reference/03-web-development.md",
        "dist/webtech.ttl",
        "site/index.html",
    )

    def test_every_build_product_is_denied(self) -> None:
        for rel in self.GENERATED:
            with self.subTest(rel):
                self.assertTrue(denied(rel), f"{rel} should be denied")

    def test_denial_names_what_to_edit_instead(self) -> None:
        reason = run("LEARNING-PATHS.md")["permissionDecisionReason"]
        self.assertIn("paths/*.yml", reason)
        self.assertIn("scripts/build.py", reason)

    def test_all_write_tools_are_watched(self) -> None:
        for tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
            with self.subTest(tool):
                self.assertTrue(denied("README.md", tool))

    def test_read_only_tools_are_ignored(self) -> None:
        self.assertEqual(run("README.md", "Read"), {})

    def test_absolute_paths_are_resolved(self) -> None:
        self.assertTrue(denied(str(ROOT / "README.md")))

    def test_paths_outside_the_repo_are_not_policed(self) -> None:
        self.assertEqual(run(str(Path.home() / "scratch.md")), {})


class AllowsHandWrittenSources(unittest.TestCase):
    """The regression. Every file here contains the banner text as data."""

    #: Renderers that carry the banner *inside the scan window*, so a content
    #: scan would flag them. These are the exact files the bug denied.
    GENERATORS = (
        "scripts/webtech/render_readme.py",
        "scripts/webtech/render_docs.py",
        "scripts/webtech/render_paths.py",
    )

    #: The hook carries the banner too, but its position drifts as the file is
    #: edited -- it currently sits past 2048 bytes. Position is incidental; the
    #: prefix exemption is what must hold, so this is checked separately.
    SELF = ".claude/hooks/guard_generated.py"

    def test_the_generators_carry_the_banner_in_the_scan_window(self) -> None:
        """Guard the premise: if these stop containing it, the test below stops
        proving anything and would pass for the wrong reason."""
        for rel in self.GENERATORS:
            with self.subTest(rel):
                head = (ROOT / rel).read_text(encoding="utf-8")[:2048]
                self.assertIn(BANNER, head, f"{rel} no longer carries the banner")

    def test_the_hook_carries_the_banner_somewhere(self) -> None:
        self.assertIn(BANNER, (ROOT / self.SELF).read_text(encoding="utf-8"))

    def test_generators_are_editable(self) -> None:
        for rel in (*self.GENERATORS, self.SELF):
            with self.subTest(rel):
                self.assertFalse(denied(rel), f"{rel} must remain editable")

    def test_source_trees_are_editable(self) -> None:
        for rel in (
            "concepts/03-web-development/typescript.yml",
            "paths/front-end-foundations.yml",
            "content/header.md",
            "scripts/build.py",
            "tests/test_paths.py",
            "docs/ROADMAP.md",
            "docs/index.md",
            "CLAUDE.md",
            "mkdocs.yml",
        ):
            with self.subTest(rel):
                self.assertFalse(denied(rel), f"{rel} must remain editable")


class SentinelScanStillWorks(unittest.TestCase):
    """Exempting the source trees must not disable the content scan itself.

    It is the safety net for a build product added to build.py but not yet to
    GENERATED_GLOBS, so it has to keep firing outside those trees.
    """

    def setUp(self) -> None:
        self.probe = ROOT / "docs" / "_guard_probe.md"
        self.probe.write_text(f"<!-- {BANNER} -->\n# probe\n", encoding="utf-8")
        self.addCleanup(self.probe.unlink)

    def test_unlisted_file_with_the_banner_is_denied(self) -> None:
        self.assertTrue(denied("docs/_guard_probe.md"))

    def test_same_file_without_the_banner_is_allowed(self) -> None:
        self.probe.write_text("# probe\n", encoding="utf-8")
        self.assertFalse(denied("docs/_guard_probe.md"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
