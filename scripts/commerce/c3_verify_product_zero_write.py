#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path, PurePosixPath, PureWindowsPath

class C3ZeroWriteError(RuntimeError):
    pass

def fail(msg: str) -> None:
    raise C3ZeroWriteError(msg)

def load(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        fail(f"JSON_INVALID {path}: {exc}")
    if not isinstance(data, dict):
        fail(f"JSON_ROOT_NOT_OBJECT {path}")
    return data

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def normalize(raw: str) -> str:
    if not isinstance(raw, str) or not raw or "\\" in raw:
        fail(f"UNSAFE_RELATIVE_PATH {raw!r}")
    p = PurePosixPath(raw)
    wp = PureWindowsPath(raw)
    if p.is_absolute() or wp.is_absolute() or wp.drive or raw.startswith("//") or ".." in p.parts:
        fail(f"UNSAFE_RELATIVE_PATH {raw}")
    return p.as_posix()

def artifact_map(items: object) -> dict[str, tuple[str, int]]:
    if not isinstance(items, list):
        fail("ARTIFACT_LIST_INVALID")
    result: dict[str, tuple[str, int]] = {}
    for item in items:
        if not isinstance(item, dict):
            fail("ARTIFACT_NOT_OBJECT")
        rel = normalize(item.get("relative_path"))
        sha = item.get("sha256")
        size = item.get("size_bytes")
        if not isinstance(sha, str) or len(sha) != 64 or not isinstance(size, int) or size < 1:
            fail(f"ARTIFACT_BINDING_INVALID {rel}")
        result[rel] = (sha, size)
    return result

def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    p = subprocess.run(["git", "-C", str(root), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        fail(f"GIT_FAILED git {' '.join(args)}: {p.stderr.strip()}")
    return p

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--product-root", required=True, type=Path)
    ap.add_argument("--qualification", required=True, type=Path)
    ap.add_argument("--proof", required=True, type=Path)
    args = ap.parse_args()

    root = args.product_root.resolve()
    q = load(args.qualification)
    proof = load(args.proof)

    if q.get("product_id") != "E01" or proof.get("product_id") != "E01":
        fail("PRODUCT_ID_MISMATCH")
    expected_head = q.get("source_git_head")
    actual_head = git(root, "rev-parse", "HEAD").stdout.strip()
    if expected_head != actual_head:
        fail(f"HEAD_MISMATCH expected={expected_head} actual={actual_head}")
    if proof.get("before_head") != expected_head or proof.get("after_head") != expected_head:
        fail("ZERO_WRITE_HEAD_DRIFT")

    for key in ("before_tracked_worktree_clean", "after_tracked_worktree_clean", "before_index_clean", "after_index_clean"):
        if proof.get(key) is not True:
            fail(f"ZERO_WRITE_CLEAN_FLAG_INVALID {key}")
    if proof.get("product_repo_write_attempts") != 0:
        fail("PRODUCT_REPO_WRITE_ATTEMPT_RECORDED")
    if proof.get("verdict") != "PASS_ZERO_WRITE":
        fail("ZERO_WRITE_VERDICT_INVALID")

    declared = artifact_map(q.get("qualified_untracked_release_artifacts", []))
    before = artifact_map(proof.get("before_qualified_untracked_artifacts", []))
    after = artifact_map(proof.get("after_qualified_untracked_artifacts", []))
    if declared != before or before != after:
        fail("QUALIFIED_ARTIFACT_SET_DRIFT")

    if git(root, "diff", "--quiet", check=False).returncode != 0:
        fail("TRACKED_WORKTREE_DIRTY_AFTER_C3")
    if git(root, "diff", "--cached", "--quiet", check=False).returncode != 0:
        fail("INDEX_DIRTY_AFTER_C3")

    actual_untracked = {
        normalize(line.strip())
        for line in git(root, "ls-files", "--others", "--exclude-standard").stdout.splitlines()
        if line.strip()
    }
    if actual_untracked != set(declared):
        fail(f"UNTRACKED_SET_DRIFT actual={sorted(actual_untracked)} expected={sorted(declared)}")

    for rel, (expected_sha, expected_size) in declared.items():
        path = (root / rel).resolve(strict=True)
        try:
            path.relative_to(root)
        except ValueError:
            fail(f"ARTIFACT_PATH_ESCAPE {rel}")
        if sha256_file(path) != expected_sha or path.stat().st_size != expected_size:
            fail(f"ARTIFACT_BYTES_DRIFT {rel}")

    print(f"C3_ZERO_WRITE_HEAD_OK {expected_head}")
    print(f"C3_ZERO_WRITE_ARTIFACTS_OK {len(declared)}")
    print("C3_PRODUCT_SOURCE_ZERO_WRITE_PASS")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except C3ZeroWriteError as exc:
        print(f"C3_PRODUCT_SOURCE_ZERO_WRITE_FAIL: {exc}", file=sys.stderr)
        raise SystemExit(2)
