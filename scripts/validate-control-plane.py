#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from control_plane import validate_root


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the non-authorizing S2A1 control-plane core."
    )
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    errors = validate_root(args.root.resolve())
    if errors:
        print("\n".join(f"[FAIL] {error}" for error in errors))
        return 2
    print("[PASS] control-plane core is internally consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
