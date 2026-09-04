#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("c2ref", HERE / "c2_reference_builder.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
FIXTURE = HERE.parent / "fixture"
VECTOR = json.loads((HERE.parent / "test-vector.json").read_text(encoding="utf-8"))

def expect_error(fn, code):
    try:
        fn()
    except m.ContractError as exc:
        assert code in str(exc), (code, exc)
    else:
        raise AssertionError(f"expected ContractError containing {code}")

def main():
    manifest = json.loads((FIXTURE / "product-manifest.json").read_text(encoding="utf-8"))
    a, pm1 = m.build_package(FIXTURE, manifest)
    b, pm2 = m.build_package(FIXTURE, manifest)
    assert a == b
    assert m.sha256_bytes(a) == VECTOR["delivery_package_sha256"]
    assert m.sha256_bytes(m.canonical_json_bytes(pm1)) == VECTOR["package_manifest_sha256"]
    assert pm1 == pm2
    assert m.sha256_bytes(m.canonical_json_bytes(manifest)) == VECTOR["product_manifest_sha256"]

    expect_error(lambda: m.validate_relative_path("../escape.txt"), "DOT_OR_TRAVERSAL")
    expect_error(lambda: m.validate_relative_path("C:/escape.txt"), "ABSOLUTE_OR_DRIVE")
    expect_error(lambda: m.validate_relative_path("//server/share.txt"), "ABSOLUTE_OR_DRIVE")
    expect_error(lambda: m.validate_relative_path(r"dir\file.txt"), "BACKSLASH")

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for p in FIXTURE.iterdir():
            if p.is_file():
                (tmp / p.name).write_bytes(p.read_bytes())
        bad = json.loads((tmp / "product-manifest.json").read_text(encoding="utf-8"))
        target = tmp / bad["assets"][0]["relative_path"]
        target.write_bytes(target.read_bytes() + b"tamper")
        expect_error(lambda: m.build_package(tmp, bad), "ASSET_SHA_MISMATCH")
    print("C2_REFERENCE_TESTS_PASS")

if __name__ == "__main__":
    main()
