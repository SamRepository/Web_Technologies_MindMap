#!/usr/bin/env python3
"""Regenerate every published artifact from the concept tree.

    python scripts/build.py            # write outputs
    python scripts/build.py --check    # exit non-zero if committed output is stale

``--check`` is the CI gate. It is what stops a hand-edit of README.md from
silently diverging from the YAML it is supposed to be generated from.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from webtech import (  # noqa: E402
    checks,
    loader,
    render_docs,
    render_mindmap,
    render_readme,
    render_skos,
)

ROOT = Path(__file__).resolve().parent.parent


def outputs(mm) -> dict[str, str]:
    """Map of repo-relative path -> content for everything we generate."""
    out = {
        "README.md": render_readme.render(mm),
        "docs/mindmap.html": render_mindmap.render(mm),
        "dist/webtech.ttl": render_skos.render(mm),
    }
    out.update(render_docs.render_all(mm))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--check",
        action="store_true",
        help="do not write; fail if committed output differs from a fresh build",
    )
    args = ap.parse_args()

    try:
        mm = loader.load(ROOT)
    except loader.LoadError as exc:
        print(f"load failed: {exc}", file=sys.stderr)
        return 2

    built = outputs(mm)

    # The leak check runs against what we are about to publish, before it lands.
    leaks = checks.check_restricted_leak(mm, built)
    if leaks:
        print("RESTRICTED LEAK -- refusing to write:", file=sys.stderr)
        for p in leaks:
            print(f"  {p}", file=sys.stderr)
        return 3

    anchor_problems = checks.check_anchors(built["README.md"])
    if anchor_problems:
        print("dead anchors in generated README:", file=sys.stderr)
        for p in anchor_problems:
            print(f"  {p}", file=sys.stderr)
        return 4

    if args.check:
        stale = []
        for rel, content in built.items():
            path = ROOT / rel
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(rel)
        if stale:
            print("stale generated files (run: python scripts/build.py)", file=sys.stderr)
            for rel in stale:
                print(f"  {rel}", file=sys.stderr)
            return 1
        print(f"up to date: {', '.join(built)}")
        return 0

    for rel, content in built.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"wrote {rel} ({len(content):,} bytes)")

    print(f"\n{len(mm.concepts)} concepts, {sum(len(c.links) for c in mm.concepts.values())} links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
