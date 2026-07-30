#!/usr/bin/env python3
"""PreToolUse hook: refuse hand-edits of generated files.

README.md and the site/RDF outputs in this repository are build products of
``scripts/build.py``, whose source of truth is ``concepts/**/*.yml``. A hand-edit
survives only until the next build, and silently diverges the map from the text --
exactly the drift this project's roadmap exists to remove.

The hook denies Edit/Write/NotebookEdit on a generated path and names what to edit
instead. Two independent checks, so a path added later is still caught:

1. Path match against GENERATED_GLOBS.
2. Sentinel scan -- any existing file whose head contains GENERATED_SENTINEL.

Reads the tool call as JSON on stdin, writes a PreToolUse permission decision as
JSON on stdout. Exits 0 even when denying: a non-zero exit means the hook itself
failed, which is a different signal.
"""

from __future__ import annotations

import json
import sys
from fnmatch import fnmatch
from pathlib import Path

# Paths whose contents are produced by scripts/build.py. Relative to repo root,
# forward slashes. Keep in sync with the "Generated" list in CLAUDE.md.
GENERATED_GLOBS: tuple[str, ...] = (
    "README.md",
    "LEARNING-PATHS.md",
    "docs/mindmap.html",
    "docs/reference/*",
    "docs/reference/**/*",
    "dist/*",
    "dist/**/*",
    "site/*",
    "site/**/*",
)

# Hand-written files that would otherwise be caught by a glob above.
ALLOWLIST: tuple[str, ...] = (
    "docs/ROADMAP.md",
    "docs/index.md",
)

# Marker that build.py writes into the head of every file it generates.
GENERATED_SENTINEL = "GENERATED FILE"
SENTINEL_SCAN_BYTES = 2048

GUIDANCE = {
    "README.md": (
        "edit the concept under concepts/**/*.yml (or a prose partial in content/), "
        "then run: python scripts/build.py"
    ),
    "LEARNING-PATHS.md": "edit paths/*.yml, then run: python scripts/build.py",
    "docs/mindmap.html": (
        "edit concepts/**/*.yml or scripts/webtech/render_mindmap.py, "
        "then run: python scripts/build.py"
    ),
}

WATCHED_TOOLS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}


def repo_root() -> Path:
    # .claude/hooks/guard_generated.py -> repo root is two levels up.
    return Path(__file__).resolve().parent.parent.parent


def relative_path(raw: str, root: Path) -> str | None:
    """Return *raw* as a repo-relative POSIX path, or None if outside the repo."""
    if not raw:
        return None
    try:
        candidate = Path(raw)
        if not candidate.is_absolute():
            candidate = root / candidate
        return candidate.resolve().relative_to(root).as_posix()
    except (ValueError, OSError):
        # Outside the repository, or an unresolvable path: not ours to police.
        return None


def has_sentinel(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            return GENERATED_SENTINEL in handle.read(SENTINEL_SCAN_BYTES)
    except OSError:
        return False


def reason_for(rel: str, root: Path) -> str | None:
    """Return a denial reason if *rel* is generated, else None."""
    if rel in ALLOWLIST:
        return None

    matched = any(fnmatch(rel, pattern) for pattern in GENERATED_GLOBS)
    if not matched and not has_sentinel(root / rel):
        return None

    hint = GUIDANCE.get(rel, "edit the source under concepts/ or scripts/webtech/, then rebuild")
    return (
        f"{rel} is a GENERATED file and must not be hand-edited -- the next "
        f"`python scripts/build.py` would overwrite the change.\n\n"
        f"To make this change stick: {hint}\n\n"
        f"See the golden rule in CLAUDE.md. Do not bypass this by shelling out to "
        f"sed/Set-Content; if the generated output is wrong, the generator or its "
        f"source data is wrong."
    )


def emit(decision: str, reason: str = "") -> None:
    # Windows consoles default to cp1252; a non-ASCII character in a reason string
    # would otherwise raise UnicodeEncodeError and fail the hook open.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
        }
    }
    if reason:
        out["hookSpecificOutput"]["permissionDecisionReason"] = reason
    json.dump(out, sys.stdout)
    sys.stdout.write("\n")


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        # Malformed input: stay out of the way rather than blocking all edits.
        return 0

    if payload.get("tool_name") not in WATCHED_TOOLS:
        return 0

    tool_input = payload.get("tool_input") or {}
    raw = tool_input.get("file_path") or tool_input.get("notebook_path") or ""

    root = repo_root()
    rel = relative_path(raw, root)
    if rel is None:
        return 0

    reason = reason_for(rel, root)
    if reason:
        emit("deny", reason)
    return 0


if __name__ == "__main__":
    sys.exit(main())
