"""Browser tests for the interactive mind map.

These exist because of a real bug that static checks could not have caught: the
pan handler called ``setPointerCapture`` on *pointerdown*, which retargets every
subsequent pointer event -- and the click derived from them -- to the capturing
element. Clicking a node therefore never reached that node's own handler, and the
details panel never opened. The JavaScript parsed cleanly and every unit test
passed; only driving a real browser shows it.

Skipped automatically when Playwright or its Chromium build is unavailable, so
the rest of the suite still runs (CI does not install browsers).

    python -m pip install playwright && python -m playwright install chromium
    python -m pytest tests/test_mindmap_ui.py -v
"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MINDMAP = ROOT / "docs" / "mindmap.html"

try:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as _p:
        _b = _p.chromium.launch()
        _b.close()
    HAVE_BROWSER = True
    SKIP_REASON = ""
except Exception as exc:  # noqa: BLE001 - any failure means "cannot run these"
    HAVE_BROWSER = False
    SKIP_REASON = f"playwright/chromium unavailable: {type(exc).__name__}"


@unittest.skipUnless(HAVE_BROWSER, SKIP_REASON)
class MindMapInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._pw = sync_playwright().start()
        cls._browser = cls._pw.chromium.launch()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._browser.close()
        cls._pw.stop()

    def setUp(self) -> None:
        self.page = self._browser.new_page(viewport={"width": 1400, "height": 900})
        self.page.goto(MINDMAP.as_uri())
        self.page.wait_for_selector("g.node")

    def tearDown(self) -> None:
        self.page.close()

    # -- helpers ---------------------------------------------------------
    def node(self, label: str):
        """The <g> whose text is exactly *label*."""
        return self.page.locator("g.node").filter(
            has=self.page.locator(f'text="{label}"')
        ).first

    def panel_text(self) -> str:
        return self.page.locator("#panel").inner_text()

    def collapsed_node(self, label: str):
        """A collapsed node renders as "Label  (n)", so exact matching fails."""
        return self.page.locator("g.node text").filter(has_text=label).first

    # -- the regression --------------------------------------------------
    def test_clicking_a_leaf_shows_its_definition(self) -> None:
        """The bug: this panel stayed on its placeholder text forever."""
        self.assertIn("Select a node", self.panel_text())

        self.page.get_by_text("Agents", exact=True).click()

        text = self.panel_text()
        self.assertNotIn("Select a node", text)
        self.assertIn("Agents", text)
        self.assertIn("autonomous action", text)      # from the definition

    def test_panel_lists_resource_links(self) -> None:
        self.page.get_by_text("Agents", exact=True).click()
        links = self.page.locator("#panel a")
        self.assertGreater(links.count(), 0, "no resource links rendered")
        href = links.first.get_attribute("href")
        self.assertTrue(href.startswith("http"), f"unexpected href {href!r}")

    def test_clicking_a_collapsed_parent_shows_details_and_expands(self) -> None:
        # Subsections start collapsed; sections start open. Clicking an already
        # open node correctly *collapses* it, so expansion must be tested on one
        # that begins collapsed.
        before = self.page.locator("g.node").count()
        self.collapsed_node("Front-End Development").click()
        self.page.wait_for_timeout(150)

        self.assertIn("Front-End Development", self.panel_text())
        self.assertGreater(
            self.page.locator("g.node").count(), before,
            "clicking a collapsed parent did not reveal its children",
        )

    def test_clicking_an_open_parent_collapses_it(self) -> None:
        before = self.page.locator("g.node").count()
        self.page.get_by_text("Web Development", exact=True).first.click()
        self.page.wait_for_timeout(150)
        self.assertIn("Web Development", self.panel_text())
        self.assertLess(self.page.locator("g.node").count(), before)

    def test_collapse_then_expand_round_trip(self) -> None:
        start = self.page.locator("g.node").count()
        self.collapsed_node("Front-End Development").click()
        self.page.wait_for_timeout(150)
        expanded = self.page.locator("g.node").count()
        self.collapsed_node("Front-End Development").click()
        self.page.wait_for_timeout(150)
        self.assertGreater(expanded, start)
        self.assertEqual(self.page.locator("g.node").count(), start)

    # -- the fix must not break panning ----------------------------------
    def test_dragging_pans_and_does_not_select(self) -> None:
        """A drag must move the view and must NOT open the panel."""
        transform_before = self.page.locator("#view").get_attribute("transform") or ""

        box = self.page.get_by_text("Agents", exact=True).bounding_box()
        self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        self.page.mouse.down()
        self.page.mouse.move(box["x"] + 205, box["y"] + 105, steps=12)
        self.page.mouse.up()
        self.page.wait_for_timeout(120)

        transform_after = self.page.locator("#view").get_attribute("transform") or ""
        self.assertNotEqual(transform_before, transform_after, "drag did not pan the view")
        self.assertIn("Select a node", self.panel_text(),
                      "a drag ending on a node wrongly selected it")

    def test_tiny_movement_still_counts_as_a_click(self) -> None:
        """Below the drag threshold the gesture must remain a click."""
        box = self.page.get_by_text("Agents", exact=True).bounding_box()
        cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
        self.page.mouse.move(cx, cy)
        self.page.mouse.down()
        self.page.mouse.move(cx + 2, cy + 1)                 # 2px, under threshold
        self.page.mouse.up()
        self.page.wait_for_timeout(120)
        self.assertIn("Agents", self.panel_text())

    def test_whole_row_is_clickable_not_just_the_text(self) -> None:
        """Regression: only the 4px circle and the glyphs used to receive clicks,
        leaving the gap between them and the space past a short label dead."""
        text = self.page.get_by_text("Agents", exact=True).bounding_box()
        circle = self.node("Agents").locator("circle").bounding_box()

        gap_x = circle["x"] + circle["width"] + 1.5      # between circle and text
        mid_y = text["y"] + text["height"] / 2
        self.page.mouse.click(gap_x, mid_y)
        self.page.wait_for_timeout(150)
        self.assertIn("Agents", self.panel_text(), "gap between circle and label is dead")

        self.page.reload(); self.page.wait_for_selector("g.node")
        text = self.page.get_by_text("Agents", exact=True).bounding_box()
        past_x = text["x"] + text["width"] + 8           # past the end of the label
        self.page.mouse.click(past_x, text["y"] + text["height"] / 2)
        self.page.wait_for_timeout(150)
        self.assertIn("Agents", self.panel_text(), "area past the label is dead")

    # -- search ----------------------------------------------------------
    def test_search_filters_and_reveals_matches(self) -> None:
        self.page.fill("#search", "typescript")
        self.page.wait_for_timeout(200)
        self.assertIn("match", self.page.locator("#count").inner_text().lower())
        self.assertGreater(self.page.locator("g.node.hit").count(), 0)

    def test_search_result_is_clickable(self) -> None:
        self.page.fill("#search", "passkeys")
        self.page.wait_for_timeout(200)
        self.page.locator("g.node.hit").first.click()
        self.assertNotIn("Select a node", self.panel_text())

    def test_expand_all_then_collapse(self) -> None:
        self.page.click("#expand")
        self.page.wait_for_timeout(300)
        expanded = self.page.locator("g.node").count()
        self.page.click("#collapse")
        self.page.wait_for_timeout(300)
        collapsed = self.page.locator("g.node").count()
        self.assertGreater(expanded, collapsed)
        self.assertGreater(expanded, 200, "expand all should show every node")

    def test_no_console_errors(self) -> None:
        errors: list[str] = []
        page = self._browser.new_page()
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(MINDMAP.as_uri())
        page.wait_for_selector("g.node")
        page.get_by_text("Agents", exact=True).click()
        page.wait_for_timeout(200)
        page.close()
        self.assertEqual(errors, [])

    def test_page_makes_no_network_requests(self) -> None:
        """The map is self-contained; only the file itself may be fetched."""
        external: list[str] = []
        page = self._browser.new_page()
        page.on("request", lambda r: external.append(r.url)
                if not r.url.startswith("file:") else None)
        page.goto(MINDMAP.as_uri())
        page.wait_for_selector("g.node")
        page.wait_for_timeout(300)
        page.close()
        self.assertEqual(external, [], f"unexpected network requests: {external}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
