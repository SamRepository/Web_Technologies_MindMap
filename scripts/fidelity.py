#!/usr/bin/env python3
"""Compare two READMEs semantically, to prove the extraction lost no content.

    python scripts/fidelity.py --before <git-ref>:README.md --after README.md

Byte-identity is not the goal and is not achievable: the source document mixes
2-, 4-, 5- and 6-space indentation for the same nesting level, has trailing
whitespace in some link bullets but not others, and varies blank-line usage
between sections. The generator normalises all of that.

What must be preserved exactly is the *content*: every concept label, every
definition's wording, and every link URL. This script compares those three sets
and reports anything present on one side and missing on the other. That is the
Phase 2 acceptance gate.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

BOLD_LABEL = re.compile(r"^\s*[-*]\s+\*\*(.+?)\*\*(?:\s*\*\(legacy\)\*)?\s*:?\s*(.*)$")
# The URL part must tolerate one level of balanced parentheses: plenty of
# Wikipedia targets look like `..._(web_framework)`, and a naive `[^)]+` stops at
# the first closing paren, silently comparing truncated URLs on both sides.
LINK = re.compile(
    r"\[([^\]]+)\]\((https?://(?:[^()\s]|\([^()\s]*\))+)\)"
)
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
WS = re.compile(r"\s+")


def norm(s: str) -> str:
    return WS.sub(" ", s).strip().rstrip(":").strip()


def read_source(spec: str) -> str:
    """Read a path, or ``<ref>:<path>`` from git.

    Decodes git's output as UTF-8 explicitly. ``subprocess`` with ``text=True``
    would use the locale encoding -- cp1252 on Windows -- turning every em-dash
    into mojibake and making identical content look like it diverged.
    """
    if ":" in spec and not Path(spec).exists():
        ref, _, path = spec.partition(":")
        raw = subprocess.run(
            ["git", "show", f"{ref}:{path}"],
            capture_output=True, check=True,
        ).stdout
        return raw.decode("utf-8")
    return Path(spec).read_text(encoding="utf-8")


def parse(md: str) -> dict[str, set[str]]:
    labels: set[str] = set()
    definitions: set[str] = set()
    urls: set[str] = set()
    headings: set[str] = set()

    for line in md.splitlines():
        if m := HEADING.match(line):
            headings.add(norm(m.group(2)))
            continue
        if m := BOLD_LABEL.match(line):
            labels.add(norm(m.group(1)))
            body = m.group(2)
            # A definition line may end with an inline link; keep only prose.
            prose = LINK.sub("", body)
            if norm(prose):
                definitions.add(norm(prose))
        for _, url in LINK.findall(line):
            urls.add(url.strip())

    return {
        "headings": headings,
        "labels": labels,
        "definitions": definitions,
        "urls": urls,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--show", type=int, default=12, help="max items to list per bucket")
    ap.add_argument(
        "--repr",
        dest="use_repr",
        action="store_true",
        help="print items with repr(), exposing whitespace and non-ASCII differences",
    )
    args = ap.parse_args()

    # Windows consoles are cp1252; without this, printing an em-dash renders as
    # U+FFFD and makes identical strings look like they differ.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    show = (lambda s: repr(s)) if args.use_repr else (lambda s: s)

    a = parse(read_source(args.before))
    b = parse(read_source(args.after))

    print(f"before: {args.before}")
    print(f"after : {args.after}\n")
    print(f"{'bucket':<12} {'before':>7} {'after':>7} {'lost':>6} {'added':>6}")
    print("-" * 44)

    def absorbed(item: str, others: set[str]) -> str | None:
        """Return the string that swallowed *item*, if any.

        The generator merges an unindented continuation paragraph into the
        definition it continues, so the text survives inside a longer string
        rather than disappearing. That is a relocation, not a loss.
        """
        for other in others:
            if item != other and item in other:
                return other
        return None

    failed = False
    absorptions: dict[str, list[tuple[str, str]]] = {}
    real_losses: dict[str, list[str]] = {}

    for bucket in ("headings", "labels", "definitions", "urls"):
        lost = a[bucket] - b[bucket]
        added = b[bucket] - a[bucket]

        merged: list[tuple[str, str]] = []
        truly_lost: list[str] = []
        for item in sorted(lost):
            host = absorbed(item, added)
            (merged.append((item, host)) if host else truly_lost.append(item))

        absorptions[bucket] = merged
        real_losses[bucket] = truly_lost
        print(
            f"{bucket:<12} {len(a[bucket]):>7} {len(b[bucket]):>7} "
            f"{len(truly_lost):>6} {len(added) - len(merged):>6}"
            + (f"   ({len(merged)} merged)" if merged else "")
        )
        if truly_lost:
            failed = True

    for bucket in ("headings", "labels", "definitions", "urls"):
        merged = absorptions[bucket]
        if merged:
            print(f"\nmerged in {bucket} ({len(merged)}) -- text preserved inside a longer string:")
            for item, host in merged[: args.show]:
                print(f"  ~ {show(item[:90])}")
                print(f"    now part of: {show(host[:120])}")

        lost = real_losses[bucket]
        if lost:
            print(f"\nLOST from {bucket} ({len(lost)}):")
            for item in lost[: args.show]:
                print(f"  - {show(item[:160])}")
            if len(lost) > args.show:
                print(f"  ... and {len(lost) - args.show} more")

        hosts = {h for _, h in merged}
        added = sorted(x for x in (b[bucket] - a[bucket]) if x not in hosts)
        if added:
            print(f"\nadded to {bucket} ({len(added)}):")
            for item in added[: args.show]:
                print(f"  + {show(item[:160])}")
            if len(added) > args.show:
                print(f"  ... and {len(added) - args.show} more")

    print("\nFIDELITY FAIL -- content was lost" if failed else "\nFIDELITY OK -- no content lost")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
