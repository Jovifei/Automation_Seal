#!/usr/bin/env python3
"""Canonical facade for the reviewed V14 bound C/APPLY transition."""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    candidate = root / "workspace/review-queue/commerce-v1/governance-closeout-v14/tools/apply_control_plane_transition_v14.py"
    if not candidate.is_file():
        print("BLOCKED_V14_CONTROL_PLANE_TRANSITION: reviewed V14 tool is absent", file=sys.stderr)
        return 2
    sys.path.insert(0, str(candidate.parent))
    sys.argv[0] = str(candidate)
    try:
        runpy.run_path(str(candidate), run_name="__main__")
    except SystemExit as exc:
        return int(exc.code or 0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
