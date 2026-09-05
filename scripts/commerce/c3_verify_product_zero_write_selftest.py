#!/usr/bin/env python3
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
def git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(root), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError(p.stderr)
    return p.stdout.strip()
def write_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
def run(script: Path, product: Path, q: Path, proof: Path, expected: int, needle: str) -> None:
    p = subprocess.run([sys.executable, str(script), "--product-root", str(product), "--qualification", str(q), "--proof", str(proof)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != expected or needle not in (p.stdout + p.stderr):
        raise AssertionError(f"expected rc={expected} needle={needle}\nOUT={p.stdout}\nERR={p.stderr}")

if len(sys.argv) != 2:
    raise SystemExit("usage: c3_verify_product_zero_write_selftest.py <zero-write-verifier.py>")

script = Path(sys.argv[1])
with tempfile.TemporaryDirectory() as td:
    root = Path(td)
    product = root / "product"; product.mkdir()
    (product / "README.md").write_text("baseline\n", encoding="utf-8")
    git(product, "init")
    git(product, "config", "user.email", "test@example.invalid")
    git(product, "config", "user.name", "C3 Zero Write Selftest")
    git(product, "add", "README.md")
    git(product, "commit", "-m", "baseline")
    (product / "dist").mkdir()
    artifact = product / "dist" / "tool.zip"
    artifact.write_bytes(b"release-bytes\n")
    head = git(product, "rev-parse", "HEAD")
    row = {"relative_path":"dist/tool.zip","sha256":sha(artifact),"size_bytes":artifact.stat().st_size}
    q = root / "qualification.json"
    proof = root / "proof.json"
    write_json(q, {"product_id":"E01","source_git_head":head,"qualified_untracked_release_artifacts":[row]})
    write_json(proof, {"schema_version":1,"product_id":"E01","before_head":head,"after_head":head,"before_tracked_worktree_clean":True,"after_tracked_worktree_clean":True,"before_index_clean":True,"after_index_clean":True,"before_qualified_untracked_artifacts":[row],"after_qualified_untracked_artifacts":[row],"product_repo_write_attempts":0,"verdict":"PASS_ZERO_WRITE"})
    run(script, product, q, proof, 0, "C3_PRODUCT_SOURCE_ZERO_WRITE_PASS")
    artifact.write_bytes(b"tampered\n")
    run(script, product, q, proof, 2, "ARTIFACT_BYTES_DRIFT")
print("C3_ZERO_WRITE_SELFTEST_PASS")
