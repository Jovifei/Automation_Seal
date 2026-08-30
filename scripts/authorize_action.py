#!/usr/bin/env python3
"""Fail-closed control-plane entry authorization for S2A2."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from control_plane import validate_root


KNOWN_ACTIONS = {
    "readonly-audit",
    "static-tests",
    "package-validation",
    "status-write",
    "commerce-development",
    "commerce-test",
}


def authorization_errors(
    root: Path, action: str, permission_class: str = "security-tightening"
) -> list[str]:
    """Return all authorization failures without performing an action."""
    errors = validate_root(root)
    if action not in KNOWN_ACTIONS:
        errors.append("unknown controlled action")
    if permission_class == "permission-expansion":
        errors.append("permission expansion requires a distinct authenticated S3/H1 approval")
    if errors:
        return errors
    state = json.loads((root / "config" / "control-plane-state.json").read_text(encoding="utf-8"))
    if state.get("phase_status") not in {"READY", "APPLY"}:
        errors.append("control-plane state is not READY or APPLY")
    if state.get("blockers"):
        errors.append("control-plane state has unresolved blockers")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail closed before controlled entry points run.")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--action", required=True)
    parser.add_argument("--permission-class", default="security-tightening")
    args = parser.parse_args()
    errors = authorization_errors(args.root.resolve(), args.action, args.permission_class)
    if errors:
        print("[DENY] " + "; ".join(errors), file=sys.stderr)
        return 2
    print("[ALLOW] controlled entry authorized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
