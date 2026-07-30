#!/usr/bin/env python3
"""Check every external link, reporting redirects as well as failures.

    python scripts/check_links.py                 # check all public links
    python scripts/check_links.py --only-new HEAD # only links absent from a git ref
    python scripts/check_links.py --json out.json

Why not lychee, which the plan named: the requirement here is to surface links
that *moved*, not only links that broke. Three MDN links in this repository
returned HTTP 200 through a redirect while their canonical URL had changed
underneath -- a 404-only checker passes those silently, and the content slowly
drifts away from the address being taught. lychee follows redirects and reports
OK; making it fail on 3xx (``--max-redirects 0``) would instead flag every
harmless http->https and trailing-slash normalisation.

So this walks each redirect chain itself and classifies the outcome:

  OK        final URL == requested URL, 2xx
  MOVED     2xx, but the final URL differs meaningfully -> update the link
  NORMALISED2xx, differs only by scheme upgrade or a trailing slash -> ignore
  DEAD      4xx / 5xx / connection failure

Restricted links are never checked: they have no URL by design.
Uses only the standard library, so CI needs no extra dependency.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent

# Tolerates one level of balanced parentheses: plenty of Wikipedia targets look
# like `..._(web_framework)`, and a naive [^)]+ truncates them.
LINK_RE = re.compile(r"\[[^\]]+\]\((https?://(?:[^()\s]|\([^()\s]*\))+)\)")

UA = "Mozilla/5.0 (compatible; WebTechMindMap-link-check/1.0)"
TIMEOUT = 25
WORKERS = 8

OK, MOVED, NORMALISED, DEAD = "OK", "MOVED", "NORMALISED", "DEAD"


def canonical(url: str) -> str:
    """Strip differences that carry no meaning for a reader."""
    p = urlsplit(url)
    scheme = "https" if p.scheme == "http" else p.scheme
    path = p.path.rstrip("/") or "/"
    return urlunsplit((scheme, p.netloc.lower(), path, p.query, ""))


class Redirects(urllib.request.HTTPRedirectHandler):
    """Record the chain rather than only the destination."""

    def __init__(self) -> None:
        self.chain: list[str] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        self.chain.append(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def check(url: str) -> dict:
    handler = Redirects()
    opener = urllib.request.build_opener(handler)
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with opener.open(req, timeout=TIMEOUT) as resp:
            final = resp.geturl()
            code = resp.status
    except urllib.error.HTTPError as e:
        # Some sites reject HEAD-ish traffic or bots; report the code as seen.
        return {"url": url, "status": DEAD, "code": e.code, "final": url,
                "detail": f"HTTP {e.code}"}
    except Exception as e:  # noqa: BLE001 - network failure of any kind
        return {"url": url, "status": DEAD, "code": None, "final": url,
                "detail": type(e).__name__}

    if final == url:
        return {"url": url, "status": OK, "code": code, "final": final, "detail": ""}
    if canonical(final) == canonical(url):
        return {"url": url, "status": NORMALISED, "code": code, "final": final,
                "detail": "scheme or trailing slash only"}
    return {"url": url, "status": MOVED, "code": code, "final": final,
            "detail": f"{len(handler.chain)} redirect(s)"}


def collect(paths: list[Path]) -> set[str]:
    urls: set[str] = set()
    for p in paths:
        if p.exists():
            urls |= set(LINK_RE.findall(p.read_text(encoding="utf-8")))
    return urls


def from_ref(ref: str, rel: str) -> set[str]:
    try:
        raw = subprocess.run(["git", "show", f"{ref}:{rel}"],
                             capture_output=True, check=True).stdout
        return set(LINK_RE.findall(raw.decode("utf-8")))
    except subprocess.CalledProcessError:
        return set()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only-new", metavar="GIT_REF",
                    help="check only links not already present in this ref's README")
    ap.add_argument("--json", metavar="PATH", help="write full results as JSON")
    ap.add_argument("--fail-on-moved", action="store_true",
                    help="exit non-zero for MOVED as well as DEAD")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    targets = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]
    urls = collect(targets)
    if args.only_new:
        urls -= from_ref(args.only_new, "README.md")

    print(f"checking {len(urls)} URL(s) with {WORKERS} workers\n")
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        results = list(pool.map(check, sorted(urls)))

    buckets: dict[str, list[dict]] = {OK: [], NORMALISED: [], MOVED: [], DEAD: []}
    for r in results:
        buckets[r["status"]].append(r)

    for status in (DEAD, MOVED, NORMALISED):
        rows = buckets[status]
        if not rows:
            continue
        print(f"{status} ({len(rows)}):")
        for r in rows:
            print(f"  {r['url']}")
            if status != DEAD:
                print(f"    -> {r['final']}   [{r['detail']}]")
            else:
                print(f"    {r['detail']}")
        print()

    print(f"summary: {len(buckets[OK])} ok, {len(buckets[NORMALISED])} normalised, "
          f"{len(buckets[MOVED])} moved, {len(buckets[DEAD])} dead")

    if args.json:
        Path(args.json).write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"wrote {args.json}")

    if buckets[DEAD]:
        return 1
    if args.fail_on_moved and buckets[MOVED]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
