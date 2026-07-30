#!/usr/bin/env python3
"""Validate the concept tree and the artifacts generated from it.

    python scripts/validate.py           # errors fail, advisories are reported
    python scripts/validate.py --strict  # advisories fail too

Exit codes: 0 clean, 1 problems found, 2 could not load.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from webtech import checks, loader  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true", help="treat advisories as errors")
    args = ap.parse_args()

    try:
        mm = loader.load(ROOT)
    except loader.LoadError as exc:
        print(f"load failed: {exc}", file=sys.stderr)
        return 2

    errors: list[checks.Problem] = []
    errors += checks.check_schema(mm)
    errors += checks.check_graph(mm)

    artifacts = checks.collect_artifacts(ROOT)
    errors += checks.check_restricted_leak(mm, artifacts)
    if "README.md" in artifacts:
        errors += checks.check_anchors(artifacts["README.md"])
        errors += checks.check_duplicate_headings(artifacts["README.md"])

    advisories = checks.check_sources(mm)

    print(f"loaded {len(mm.concepts)} concepts in {len(mm.sections)} sections")
    print(f"scanned {len(artifacts)} artifact(s) for restricted leaks")
    restricted = mm.restricted_links
    print(f"restricted links declared: {len(restricted)}")

    if errors:
        print(f"\n{len(errors)} error(s):")
        for p in errors:
            print(f"  {p}")
    else:
        print("\nno errors")

    if advisories:
        print(f"\n{len(advisories)} advisory(ies) -- concepts without a primary source:")
        for p in advisories[:15]:
            print(f"  {p}")
        if len(advisories) > 15:
            print(f"  ... and {len(advisories) - 15} more")

    if errors:
        return 1
    if advisories and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
