from __future__ import annotations

import argparse
import json
import sys

from .parser import parse_frame, parse_hex


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Diagnose a Modbus RTU hexadecimal frame")
    parser.add_argument("frame", help='Hex frame, for example: "01 03 00 00 00 0A C5 CD"')
    parser.add_argument("--compact", action="store_true", help="Output one-line JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = parse_frame(parse_hex(args.frame))
    except ValueError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=None if args.compact else 2))
    return 0 if result["crc"]["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
