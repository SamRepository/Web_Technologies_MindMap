"""Link-checker classification logic, tested without touching the network.

The reason this checker exists rather than lychee is the MOVED/NORMALISED
distinction: a link that still returns 200 but whose canonical URL has changed
needs updating, while one that differs only by an https upgrade or a trailing
slash does not. Three MDN links in this repository were in the first category and
a 404-only check passed them in silence.

That distinction lives entirely in :func:`canonical`, so it can be tested
offline. The network behaviour itself is exercised by the weekly CI workflow;
this environment sits behind a proxy that returns 403 for general web traffic,
so verdicts obtained here would be meaningless.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_links  # noqa: E402


class CanonicalForm(unittest.TestCase):
    def test_http_and_https_are_the_same_address(self) -> None:
        self.assertEqual(
            check_links.canonical("http://example.org/a"),
            check_links.canonical("https://example.org/a"),
        )

    def test_trailing_slash_is_insignificant(self) -> None:
        self.assertEqual(
            check_links.canonical("https://example.org/a"),
            check_links.canonical("https://example.org/a/"),
        )

    def test_host_case_is_insignificant(self) -> None:
        self.assertEqual(
            check_links.canonical("https://Example.ORG/a"),
            check_links.canonical("https://example.org/a"),
        )

    def test_fragment_is_dropped(self) -> None:
        self.assertEqual(
            check_links.canonical("https://example.org/a#frag"),
            check_links.canonical("https://example.org/a"),
        )

    def test_a_different_path_is_a_real_move(self) -> None:
        """The MDN case: same host, 200 response, different page."""
        self.assertNotEqual(
            check_links.canonical("https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP"),
            check_links.canonical("https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP"),
        )

    def test_query_string_is_significant(self) -> None:
        self.assertNotEqual(
            check_links.canonical("https://example.org/a?v=1"),
            check_links.canonical("https://example.org/a?v=2"),
        )


class UrlExtraction(unittest.TestCase):
    def test_parenthesised_url_captured_whole(self) -> None:
        md = "[Wikipedia](https://en.wikipedia.org/wiki/Django_(web_framework))"
        found = check_links.LINK_RE.findall(md)
        self.assertEqual(found, ["https://en.wikipedia.org/wiki/Django_(web_framework)"])

    def test_plain_url(self) -> None:
        self.assertEqual(
            check_links.LINK_RE.findall("[x](https://example.org/a)"),
            ["https://example.org/a"],
        )

    def test_restricted_badge_has_no_url_to_find(self) -> None:
        """A 🔒 badge must not be picked up as an external link."""
        md = "- 🔒 TP recordings — [request access](#requesting-access-to-restricted-resources)"
        self.assertEqual(check_links.LINK_RE.findall(md), [])

    def test_real_readme_urls_are_all_balanced(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        urls = check_links.LINK_RE.findall(readme)
        self.assertGreater(len(urls), 200)
        unbalanced = [u for u in urls if u.count("(") != u.count(")")]
        self.assertEqual(unbalanced, [], "URL extraction truncated a parenthesised link")


if __name__ == "__main__":
    unittest.main(verbosity=2)
