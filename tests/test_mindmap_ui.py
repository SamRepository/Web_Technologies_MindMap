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

import re
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
        page.click("#tab-graph")            # the force layout must not fetch either
        page.wait_for_timeout(1500)
        page.close()
        self.assertEqual(external, [], f"unexpected network requests: {external}")


@unittest.skipUnless(HAVE_BROWSER, SKIP_REASON)
class GraphView(unittest.TestCase):
    """The force-directed second view.

    The tree can only ever show the hierarchy. These tests are mostly about the
    thing it cannot show -- ``see_also`` edges reaching across sections -- and
    about the two highlight mechanisms (focus neighbourhood, search) coexisting.
    """

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
        self.page.click("#tab-graph")
        self.page.wait_for_selector("g.gnode")
        self.settle()

    def tearDown(self) -> None:
        self.page.close()

    # -- helpers ---------------------------------------------------------
    def settle(self, tries: int = 60) -> str:
        """Wait for the simulation to stop moving.

        Polling for a fixed positions snapshot rather than sleeping a guessed
        number of seconds: alpha decay is frame-rate dependent, so a wall-clock
        wait is a race on a slow machine.
        """
        prev = ""
        for _ in range(tries):
            cur = self.page.eval_on_selector_all(
                "g.gnode", 'els => els.map(e => e.getAttribute("transform")).join("|")'
            )
            if cur and cur == prev:
                return cur
            prev = cur
            self.page.wait_for_timeout(250)
        return prev

    def centre_of(self, prefix: str) -> dict:
        """Viewport centre of the node whose label starts with *prefix*.

        Labels are hidden when they would collide, so a Playwright text locator
        is not reliable here; go through the DOM instead.
        """
        box = self.page.evaluate(
            """(p) => {
                const t = [...document.querySelectorAll("g.gnode text")]
                    .find(e => e.textContent.startsWith(p));
                if (!t) return null;
                const r = t.parentNode.querySelector("circle").getBoundingClientRect();
                return {x: r.x + r.width / 2, y: r.y + r.height / 2};
            }""",
            prefix,
        )
        self.assertIsNotNone(box, f"no graph node labelled {prefix!r}")
        return box

    def lit(self) -> list[str]:
        """Labels of the nodes that are not dimmed."""
        return self.page.eval_on_selector_all(
            "g.gnode:not(.hushed) text", "els => els.map(e => e.textContent)"
        )

    def unhover(self) -> None:
        """Move off the graph, so only the click-focus drives the highlight."""
        self.page.mouse.move(5, 890)
        self.page.wait_for_timeout(200)

    # -- structure -------------------------------------------------------
    def test_node_and_edge_counts_match_the_concept_tree(self) -> None:
        nodes = self.page.locator("g.gnode").count()
        edges = self.page.locator("line.gedge").count()
        rel = self.page.locator("line.gedge.rel").count()

        # Every node except the root has exactly one parent, so hierarchy edges
        # are one fewer than nodes. This is what catches a node silently
        # dropping out of the graph while the tree still lists it.
        self.assertEqual(edges - rel, nodes - 1)
        self.assertGreater(rel, 0, "no see_also edges drawn")
        self.assertIn(f"{nodes} nodes", self.page.locator("#count").inner_text())

    def test_graph_holds_every_node_the_tree_does(self) -> None:
        self.page.click("#tab-tree")
        self.page.click("#expand")
        self.page.wait_for_timeout(400)
        tree = self.page.locator("g.node").count()
        self.page.click("#tab-graph")
        self.page.wait_for_timeout(200)
        self.assertEqual(self.page.locator("g.gnode").count(), tree)

    def test_layout_is_deterministic(self) -> None:
        """A seeded PRNG, so reopening the file gives the same picture back."""
        first = self.settle()
        other = self._browser.new_page(viewport={"width": 1400, "height": 900})
        try:
            other.goto(MINDMAP.as_uri())
            other.wait_for_selector("g.node")
            other.click("#tab-graph")
            other.wait_for_selector("g.gnode")
            prev = ""
            for _ in range(60):
                cur = other.eval_on_selector_all(
                    "g.gnode", 'els => els.map(e => e.getAttribute("transform")).join("|")'
                )
                if cur and cur == prev:
                    break
                prev = cur
                other.wait_for_timeout(250)
        finally:
            other.close()
        self.assertEqual(first, prev)

    # -- the point of the view -------------------------------------------
    def test_clicking_a_node_opens_the_panel_and_lights_its_neighbourhood(self) -> None:
        c = self.centre_of("RAG")
        self.page.mouse.click(c["x"], c["y"])
        self.unhover()

        text = self.page.locator("#panel").inner_text()
        self.assertNotIn("Select a node", text)
        self.assertIn("RAG", text)

        lit = self.lit()
        # RAG's parent, plus the three cross-section see_also targets. Those
        # three are precisely what the tree view cannot draw.
        for expected in ("AI-Era Web", "Embeddings", "Vector Databases", "Knowledge Graphs"):
            self.assertTrue(any(l.startswith(expected) for l in lit),
                            f"{expected} not lit; lit = {lit}")
        self.assertGreater(self.page.locator("g.gnode.hushed").count(), 100,
                           "focusing a node did not dim the rest of the graph")

    def test_neighbour_labels_are_never_suppressed(self) -> None:
        """Collision-hiding must not swallow the labels the reader asked for."""
        c = self.centre_of("RAG")
        self.page.mouse.click(c["x"], c["y"])
        self.unhover()
        hidden = self.page.eval_on_selector_all(
            "g.gnode:not(.hushed) text",
            'els => els.filter(e => e.style.display === "none").map(e => e.textContent)',
        )
        self.assertEqual(hidden, [], "a highlighted node lost its label")

    def test_related_list_is_symmetric(self) -> None:
        """``see_also`` is declared on one side only, because skos:related is
        symmetric and maintaining both halves in two YAML files is a trap. The
        reverse index has to make the panel show it from either end."""
        c = self.centre_of("SQL")
        self.page.mouse.click(c["x"], c["y"])
        self.page.wait_for_timeout(300)
        self.assertEqual(self.page.locator("#panel h2").inner_text(), "SQL")
        listed = self.page.eval_on_selector_all(
            "#panel button.jump", "els => els.map(e => e.textContent)"
        )
        # None of these are declared on sql.yml; every one points *at* SQL.
        for expected in ("SPARQL", "SQL Injection", "ORM (Object-Relational Mapping)"):
            self.assertIn(expected, listed, f"{expected} missing; listed = {listed}")

    def test_cross_links_can_be_hidden(self) -> None:
        """Teaching control: show the taxonomy alone, then reveal the links."""
        rel = self.page.locator("line.gedge.rel")
        self.assertTrue(rel.first.is_visible())
        before = self.page.locator("line.gedge").count()

        self.page.click("#xlinks")
        self.page.wait_for_timeout(200)
        self.assertFalse(rel.first.is_visible())
        # Hidden, not removed: the edges stay in the simulation so toggling
        # does not rearrange the graph under the reader.
        self.assertEqual(self.page.locator("line.gedge").count(), before)

        self.page.click("#xlinks")
        self.page.wait_for_timeout(200)
        self.assertTrue(rel.first.is_visible())

    def test_panel_related_list_jumps_to_the_other_concept(self) -> None:
        c = self.centre_of("RAG")
        self.page.mouse.click(c["x"], c["y"])
        self.page.wait_for_timeout(200)
        related = self.page.locator("#panel button.jump")
        self.assertGreater(related.count(), 0, "no Related entries in the panel")
        related.first.click()
        self.page.wait_for_timeout(300)
        self.assertNotIn("RAG (Retrieval", self.page.locator("#panel h2").inner_text())

    # -- the two highlight mechanisms must coexist -----------------------
    def test_search_hit_is_not_dimmed_by_an_active_focus(self) -> None:
        """Regression: focus-dimming used to override the search highlight, so
        typing a query while a node was selected greyed out its own match."""
        c = self.centre_of("RAG")
        self.page.mouse.click(c["x"], c["y"])
        self.unhover()
        self.page.fill("#search", "passkey")
        self.page.wait_for_timeout(300)

        hit = self.page.locator("g.gnode.hit")
        self.assertGreater(hit.count(), 0, "search produced no hit in the graph")
        self.assertEqual(hit.locator(".hushed").count(), 0)
        for cls in hit.evaluate_all("els => els.map(e => e.getAttribute('class'))"):
            self.assertNotIn("hushed", cls, "the search hit was dimmed")

    def test_search_reports_matches_in_graph_mode(self) -> None:
        self.page.fill("#search", "typescript")
        self.page.wait_for_timeout(300)
        self.assertIn("match", self.page.locator("#count").inner_text().lower())

    # -- interaction ------------------------------------------------------
    def test_dragging_a_node_moves_it_and_does_not_pan(self) -> None:
        before_cam = self.page.locator("#gview").get_attribute("transform")
        c = self.centre_of("Front-End Development")
        self.page.mouse.move(c["x"], c["y"])
        self.page.mouse.down()
        self.page.mouse.move(c["x"] + 120, c["y"] - 90, steps=10)
        self.page.mouse.up()
        self.page.wait_for_timeout(400)

        after = self.centre_of("Front-End Development")
        self.assertNotEqual((round(c["x"]), round(c["y"])),
                            (round(after["x"]), round(after["y"])),
                            "dragging a node did not move it")
        # Auto-fit may rescale, but a node drag must not be read as a pan
        # gesture that leaves the canvas in its grabbing state.
        self.assertNotIn("drag", self.page.locator("#canvas").get_attribute("class") or "")
        self.assertIsNotNone(before_cam)

    def test_a_press_without_movement_selects(self) -> None:
        c = self.centre_of("Front-End Development")
        self.page.mouse.move(c["x"], c["y"])
        self.page.mouse.down()
        self.page.mouse.move(c["x"] + 2, c["y"] + 1)      # under the drag threshold
        self.page.mouse.up()
        self.page.wait_for_timeout(300)
        self.assertIn("Front-End Development", self.page.locator("#panel").inner_text())

    def test_zooming_in_reveals_more_labels(self) -> None:
        """Labels are drawn at a constant screen size, so zoom buys room."""
        visible = 'els => els.filter(e => e.style.display !== "none").length'
        before = self.page.eval_on_selector_all("g.gnode text", visible)
        self.page.mouse.move(700, 450)
        for _ in range(8):
            self.page.mouse.wheel(0, -200)
        self.page.wait_for_timeout(400)
        self.assertGreater(self.page.eval_on_selector_all("g.gnode text", visible), before)

    def test_switching_back_to_the_tree_restores_it(self) -> None:
        self.page.click("#tab-tree")
        self.page.wait_for_timeout(300)
        self.assertGreater(self.page.locator("g.node").count(), 0)
        self.assertEqual(self.page.locator("g.gnode:visible").count(), 0)
        self.page.click("#tab-graph")
        self.page.wait_for_timeout(300)
        self.assertGreater(self.page.locator("g.gnode:visible").count(), 0)

    def test_tree_only_controls_are_hidden_in_graph_mode(self) -> None:
        self.assertFalse(self.page.locator("#expand").is_visible())
        self.assertTrue(self.page.locator("#relayout").is_visible())
        self.page.click("#tab-tree")
        self.assertTrue(self.page.locator("#expand").is_visible())
        self.assertFalse(self.page.locator("#relayout").is_visible())

    def test_no_console_errors(self) -> None:
        errors: list[str] = []
        page = self._browser.new_page(viewport={"width": 1400, "height": 900})
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(MINDMAP.as_uri())
        page.wait_for_selector("g.node")
        page.click("#tab-graph")
        page.wait_for_timeout(2500)
        page.click("#relayout")
        page.wait_for_timeout(800)
        page.click("#reset")
        page.click("#tab-tree")
        page.wait_for_timeout(300)
        page.close()
        self.assertEqual(errors, [])


#: Dispatch a two-finger gesture as real PointerEvents. Playwright's touchscreen
#: API only taps, so a pinch has to be synthesised -- which is fine here,
#: because the handler under test consumes pointer events and nothing else.
PINCH_JS = """
([x1, y1, x2, y2, x1b, y1b, x2b, y2b, steps]) => {
  const el = document.getElementById('canvas');
  const ev = (type, id, x, y) => el.dispatchEvent(new PointerEvent(type, {
    pointerId: id, pointerType: 'touch', isPrimary: id === 1,
    clientX: x, clientY: y, button: 0, buttons: 1, bubbles: true, cancelable: true
  }));
  ev('pointerdown', 1, x1, y1);
  ev('pointerdown', 2, x2, y2);
  for (let i = 1; i <= steps; i++){
    const t = i / steps;
    ev('pointermove', 1, x1 + (x1b - x1) * t, y1 + (y1b - y1) * t);
    ev('pointermove', 2, x2 + (x2b - x2) * t, y2 + (y2b - y2) * t);
  }
  ev('pointerup', 1, x1b, y1b);
  ev('pointerup', 2, x2b, y2b);
}
"""


@unittest.skipUnless(HAVE_BROWSER, SKIP_REASON)
class MobileGestures(unittest.TestCase):
    """Touch zoom, and the framing that made zooming necessary in the first place.

    Two defects, reported together from a phone. There was no pinch handler at
    all -- and `touch-action:none`, which the drag-to-pan needs, also suppresses
    the browser's own pinch, so on touch there was simply no way to zoom. And
    the tree fitted all 217 rows into the viewport, rendering labels at about
    4 CSS px, which is what made the missing zoom impossible to work around.
    """

    PHONE = {"width": 390, "height": 844}

    @classmethod
    def setUpClass(cls) -> None:
        cls._pw = sync_playwright().start()
        cls._browser = cls._pw.chromium.launch()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._browser.close()
        cls._pw.stop()

    def setUp(self) -> None:
        self.ctx = self._browser.new_context(
            viewport=self.PHONE, has_touch=True, is_mobile=True
        )
        self.page = self.ctx.new_page()
        self.page.goto(MINDMAP.as_uri())
        self.page.wait_for_selector("g.node")

    def tearDown(self) -> None:
        self.ctx.close()

    # -- helpers ---------------------------------------------------------
    def scale_of(self, sel: str) -> float:
        t = self.page.locator(sel).get_attribute("transform") or ""
        m = re.search(r"scale\(([-0-9.eE]+)\)", t)
        return float(m.group(1)) if m else 1.0

    def pinch(self, x1, x2, x1b, x2b, y=430, steps=12) -> None:
        self.page.evaluate(PINCH_JS, [x1, y, x2, y, x1b, y, x2b, y, steps])
        self.page.wait_for_timeout(120)

    def spread(self, **kw) -> None:
        """Fingers apart — zoom in."""
        self.pinch(140, 250, 60, 330, **kw)

    def squeeze(self, **kw) -> None:
        """Fingers together — zoom out."""
        self.pinch(60, 330, 150, 240, **kw)

    # -- framing ---------------------------------------------------------
    def test_tree_uses_the_window_model_on_a_narrow_screen(self) -> None:
        vb = self.page.locator("svg").get_attribute("viewBox").split()
        self.assertAlmostEqual(float(vb[2]), self.PHONE["width"], delta=2)

    def test_tree_labels_are_legible_without_zooming(self) -> None:
        """The regression: about 4 CSS px before this fix."""
        h = self.page.evaluate(
            '() => document.querySelector("g.node text").getBoundingClientRect().height'
        )
        self.assertGreater(h, 11, f"tree labels render at {h}px on a phone")

    def test_graph_labels_are_legible_without_zooming(self) -> None:
        self.page.click("#tab-graph")
        self.page.wait_for_timeout(4000)
        h = self.page.evaluate(
            """() => { const t = [...document.querySelectorAll("g.gnode text")]
                         .find(e => e.style.display !== "none");
                       return t ? t.getBoundingClientRect().height : 0; }"""
        )
        self.assertGreater(h, 11, f"graph labels render at {h}px on a phone")

    # -- the gesture -----------------------------------------------------
    def test_pinch_zooms_the_tree_in_and_out(self) -> None:
        start = self.scale_of("#view")
        self.spread()
        zoomed = self.scale_of("#view")
        self.assertGreater(zoomed, start * 1.4, "spreading two fingers did not zoom in")
        self.squeeze()
        self.assertLess(self.scale_of("#view"), zoomed * 0.85,
                        "pinching two fingers did not zoom out")

    def test_pinch_zooms_the_graph(self) -> None:
        self.page.click("#tab-graph")
        self.page.wait_for_selector("g.gnode")
        self.page.wait_for_timeout(4000)
        start = self.scale_of("#gview")
        self.spread()
        self.assertGreater(self.scale_of("#gview"), start * 1.4)

    def test_pinch_is_anchored_to_the_fingers(self) -> None:
        """Whatever is between the fingers must stay between them; scaling about
        the origin instead slides the map out from under the gesture."""
        probe = 'g.node text'
        before = self.page.locator(probe).nth(20).bounding_box()
        # Pinch centred on that label's own position.
        cx = before["x"] + before["width"] / 2
        cy = before["y"] + before["height"] / 2
        self.page.evaluate(
            PINCH_JS, [cx - 55, cy, cx + 55, cy, cx - 120, cy, cx + 120, cy, 12]
        )
        self.page.wait_for_timeout(150)
        after = self.page.locator(probe).nth(20).bounding_box()
        acx = after["x"] + after["width"] / 2
        acy = after["y"] + after["height"] / 2
        self.assertLess(abs(acx - cx), 40, "anchor drifted horizontally")
        self.assertLess(abs(acy - cy), 40, "anchor drifted vertically")

    def test_single_finger_still_pans(self) -> None:
        before = self.page.locator("#view").get_attribute("transform") or ""
        self.page.mouse.move(200, 400)
        self.page.mouse.down()
        self.page.mouse.move(200, 250, steps=10)
        self.page.mouse.up()
        self.page.wait_for_timeout(120)
        self.assertNotEqual(before, self.page.locator("#view").get_attribute("transform"))

    def test_a_tap_still_opens_the_panel(self) -> None:
        """The pinch bookkeeping runs in the capture phase for every pointer, so
        the ordinary one-finger tap has to survive it."""
        self.page.get_by_text("Agents", exact=True).tap()
        self.page.wait_for_timeout(200)
        self.assertIn("Agents", self.page.locator("#panel").inner_text())

    def test_a_pinch_does_not_register_as_a_tap(self) -> None:
        self.spread()
        self.assertIn("Select a node", self.page.locator("#panel").inner_text())


@unittest.skipUnless(HAVE_BROWSER, SKIP_REASON)
class WideScreenFramingUnchanged(unittest.TestCase):
    """The mobile fix must not alter what a desktop reader already had."""

    @classmethod
    def setUpClass(cls) -> None:
        cls._pw = sync_playwright().start()
        cls._browser = cls._pw.chromium.launch()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._browser.close()
        cls._pw.stop()

    def test_tree_still_fits_to_content(self) -> None:
        page = self._browser.new_page(viewport={"width": 1400, "height": 900})
        page.goto(MINDMAP.as_uri())
        page.wait_for_selector("g.node")
        vb = page.locator("svg").get_attribute("viewBox").split()
        page.close()
        self.assertEqual(float(vb[2]), 900.0, "wide-screen tree viewBox changed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
