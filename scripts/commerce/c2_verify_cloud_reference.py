#!/usr/bin/env python3
"""Verify the complete C2 cloud reference pack using only Python stdlib."""
from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    c2 = repo / "reference" / "commerce" / "c2"
    fixture = c2 / "fixture"
    expected = {}
    for line in (fixture / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        digest, name = line.split(None, 1)
        expected[name.strip()] = digest
    for name, digest in expected.items():
        actual = sha256(fixture / name)
        if actual != digest:
            print(f"FIXTURE_SHA_MISMATCH {name} expected={digest} actual={actual}", file=sys.stderr)
            return 2
    for test in ["test_c2_reference_builder.py", "test_download_grant_policy.py"]:
        cp = subprocess.run([sys.executable, str(c2 / "oracle" / test)], cwd=str(c2 / "oracle"), text=True, capture_output=True)
        if cp.returncode:
            sys.stderr.write(cp.stdout + cp.stderr)
            return cp.returncode
        print(cp.stdout.strip())
    vector = json.loads((c2 / "test-vector.json").read_text(encoding="utf-8"))
    print(json.dumps({
        "verdict": "C2_CLOUD_REFERENCE_PASS",
        "fixture_files": len(expected),
        "delivery_package_sha256": vector["delivery_package_sha256"],
        "package_format": vector["package_format"]
    }, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
