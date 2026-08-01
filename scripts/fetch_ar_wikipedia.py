#!/usr/bin/env python3
"""Resolve Arabic Wikipedia articles for concepts that link an English one.

    python scripts/fetch_ar_wikipedia.py            # report only
    python scripts/fetch_ar_wikipedia.py --write    # add the links to YAML

Two API calls per batch of 50: ``langlinks`` on en.wikipedia to find the Arabic
title, then ``info`` on ar.wikipedia for its byte length.

The length matters. Arabic Wikipedia's coverage of web technology is uneven --
some articles are thorough, others are two sentences and an infobox. Sending a
student to a stub is worse than sending them nowhere, so by default only
articles at or above ``--min-bytes`` are written, and the rest are listed for
the author to opt into deliberately.

Network at *tooling* time only. The resolved URLs are written into the concept
YAML, so nothing the published artifact does depends on this script ever
running again -- the same arrangement as scripts/check_links.py.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")  # Arabic titles on a cp1252 console

from webtech import loader  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

#: Wikipedia rejects the default urllib agent. Identify the project and a
#: contact, as the API etiquette guidelines ask.
UA = (
    "WebTechMindMap/1.0 "
    "(https://github.com/SamRepository/Web_Technologies_MindMap; "
    "samir.sellami@univ-constantine2.dz)"
)
BATCH = 50           # the API's limit for an unauthenticated titles= query
LABEL = "Wikipedia (Ar)"


def api(host: str, params: dict[str, str], tries: int = 4) -> dict:
    """One API call, retried on transport failure.

    A run makes only a handful of requests, but each covers 50 concepts, so a
    single dropped connection loses the whole batch. Retry with a widening
    delay rather than making the caller start over.
    """
    params = {**params, "format": "json", "formatversion": "2"}
    url = f"https://{host}/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(1, tries + 1):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except Exception as exc:                   # noqa: BLE001
            if attempt == tries:
                raise
            wait = 2 ** attempt
            print(f"  {type(exc).__name__} from {host}, retrying in {wait}s "
                  f"({attempt}/{tries - 1})", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError("unreachable")


def chunks(seq: list, n: int):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def en_title(url: str) -> str | None:
    """The article title out of an en.wikipedia URL, or None if it is not one."""
    p = urllib.parse.urlparse(url)
    if not p.netloc.endswith("en.wikipedia.org") or "/wiki/" not in p.path:
        return None
    return urllib.parse.unquote(p.path.split("/wiki/", 1)[1]).replace("_", " ")


def resolve(titles: list[str]) -> dict[str, str]:
    """English title -> Arabic title, for those that have one."""
    out: dict[str, str] = {}
    for group in chunks(titles, BATCH):
        data = api("en.wikipedia.org", {
            "action": "query", "prop": "langlinks", "lllang": "ar",
            "lllimit": "500", "redirects": "1", "titles": "|".join(group),
        })
        query = data.get("query", {})
        # A redirect means the URL in the YAML points at an alias; map the
        # resolved title back so the caller can still find its concept.
        alias = {r["to"]: r["from"] for r in query.get("redirects", [])}
        for page in query.get("pages", []):
            links = page.get("langlinks") or []
            if not links:
                continue
            title = page.get("title", "")
            out[alias.get(title, title)] = links[0]["title"]
        time.sleep(0.2)      # be polite; this is an anonymous API
    return out


def sizes(ar_titles: list[str]) -> dict[str, int]:
    """Arabic title -> article length in bytes."""
    out: dict[str, int] = {}
    for group in chunks(ar_titles, BATCH):
        data = api("ar.wikipedia.org", {
            "action": "query", "prop": "info", "titles": "|".join(group),
        })
        for page in data.get("query", {}).get("pages", []):
            if "missing" not in page:
                out[page["title"]] = int(page.get("length", 0))
        time.sleep(0.2)
    return out


def ar_url(title: str) -> str:
    return "https://ar.wikipedia.org/wiki/" + urllib.parse.quote(
        title.replace(" ", "_")
    )


def insert_link(path: Path, url: str) -> bool:
    """Append a ``Wikipedia (Ar)`` entry to a concept's links block."""
    text = path.read_text(encoding="utf-8")
    if url in text:
        return False
    lines = text.split("\n")
    entry = ["- type: wikipedia", f"  label: {LABEL}", f"  url: {url}"]

    if not any(l.startswith("links:") for l in lines):
        while lines and not lines[-1].strip():
            lines.pop()
        lines += ["links:"] + entry + [""]
    else:
        end = len(lines)
        while end > 0 and not lines[end - 1].strip():
            end -= 1
        lines = lines[:end] + entry + [""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true",
                    help="write the links into concepts/**.yml")
    ap.add_argument("--min-bytes", type=int, default=2000,
                    help="shortest Arabic article to link (default 2000)")
    ap.add_argument("--include-stubs", action="store_true",
                    help="write short articles too")
    args = ap.parse_args()

    mm = loader.load(ROOT)

    # A *list* per title, not one entry: four English articles are cited by two
    # concepts each (Algorithm by both `algorithms` and `algorithmic`, and so
    # on). Keying one concept per title silently drops the other.
    wanted: dict[str, list[tuple]] = {}
    for c in sorted(mm.concepts.values(), key=lambda c: c.id):
        if any(ln.label == LABEL for ln in c.links):
            continue                  # already resolved on a previous run
        for ln in c.links:
            t = en_title(ln.url) if (ln.type == "wikipedia" and ln.url) else None
            if t:
                hits = list((ROOT / "concepts").rglob(f"{c.id}.yml"))
                wanted.setdefault(t, []).append((c, hits[0]))
                break

    total = sum(len(v) for v in wanted.values())
    print(f"{total} concepts with an English Wikipedia link to resolve "
          f"({len(wanted)} distinct articles)")
    if not wanted:
        return 0

    try:
        found = resolve(list(wanted))
        length = sizes(sorted(set(found.values())))
    except Exception as exc:                       # noqa: BLE001
        print(f"API request failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    rows = []
    for en, ar in sorted(found.items()):
        for concept, path in wanted[en]:
            rows.append((concept.id, ar, length.get(ar, 0), path))
    rows.sort(key=lambda r: -r[2])

    solid = [r for r in rows if r[2] >= args.min_bytes]
    stubs = [r for r in rows if r[2] < args.min_bytes]
    missing = sorted(
        c.id for en, pairs in wanted.items() if en not in found for c, _ in pairs
    )

    print(f"  {len(rows)} have an Arabic article")
    print(f"  {len(solid)} at or above {args.min_bytes:,} bytes")
    print(f"  {len(stubs)} shorter (stubs)")
    print(f"  {len(missing)} have no Arabic article at all")

    if stubs:
        print("\nStubs -- not written unless you pass --include-stubs:")
        for cid, ar, n, _ in stubs:
            print(f"  {n:>6,}b  {cid:<28} {ar}")
    if missing:
        print("\nNo Arabic article:")
        print("  " + ", ".join(missing))

    if not args.write:
        print("\n(report only -- pass --write to add these to the YAML)")
        return 0

    chosen = rows if args.include_stubs else solid
    written = 0
    for cid, ar, n, path in chosen:
        if insert_link(path, ar_url(ar)):
            written += 1
    print(f"\nwrote {written} '{LABEL}' link(s); run python scripts/build.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
