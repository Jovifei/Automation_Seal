#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPOS = [
    ("codex", "openai/codex", "main", "CORE"),
    ("openai_plugins", "openai/plugins", "main", "REFERENCE"),
    ("spec_kit", "github/spec-kit", "main", "PRODUCT_SPEC_OPTION"),
    ("n8n", "n8n-io/n8n", "master", "TRACK_I"),
    ("changedetection", "dgtlmoon/changedetection.io", "master", "TRACK_I_OPTION"),
    ("xianyu_adapter", "GuDong2003/xianyu-auto-reply-fix", "main", "REUSE_STAGED"),
    ("promptfoo", "promptfoo/promptfoo", "main", "EVALUATION"),
    ("gitleaks", "gitleaks/gitleaks", "master", "SECURITY"),
    ("trivy", "aquasecurity/trivy", "main", "SECURITY"),
    ("docling", "docling-project/docling", "main", "RESEARCH_OPTION"),
    ("paperqa", "Future-House/paper-qa", "main", "RESEARCH_OPTION"),
    ("platformio", "platformio/platformio-core", "develop", "EMBEDDED_OPTION"),
    ("ceedling", "ThrowTheSwitch/Ceedling", "master", "EMBEDDED_OPTION"),
    ("renode", "renode/renode", "master", "EMBEDDED_OPTION"),
    ("syft", "anchore/syft", "main", "SUPPLY_CHAIN_OPTION"),
    ("cosign", "sigstore/cosign", "main", "SUPPLY_CHAIN_LATER"),
]


def request_json(url: str, timeout: int = 15):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Jovi-Automation-Narrow-Version-Refresh/3.0",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read(2_000_000).decode("utf-8"))


def resolve(item):
    name, repo, branch, decision = item
    base = f"https://api.github.com/repos/{repo}"
    result = {
        "name": name,
        "repo": repo,
        "decision": decision,
        "formal_release": None,
        "branch_snapshot": None,
        "license_spdx": None,
        "security_policy_url": f"https://github.com/{repo}/security/policy",
        "status": "NOT_VERIFIED_CURRENT",
        "errors": [],
    }
    try:
        meta = request_json(base)
        result["license_spdx"] = (meta.get("license") or {}).get("spdx_id")
        result["archived"] = bool(meta.get("archived"))
        result["default_branch"] = meta.get("default_branch")
    except Exception as exc:
        result["errors"].append(f"metadata: {type(exc).__name__}: {exc}")
    try:
        release = request_json(base + "/releases/latest")
        result["formal_release"] = {
            "tag": release.get("tag_name"),
            "name": release.get("name"),
            "published_at": release.get("published_at"),
            "prerelease": bool(release.get("prerelease")),
            "url": release.get("html_url"),
        }
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            result["errors"].append(f"release: HTTP {exc.code}")
    except Exception as exc:
        result["errors"].append(f"release: {type(exc).__name__}: {exc}")
    try:
        commit = request_json(base + f"/commits/{branch}")
        result["branch_snapshot"] = {
            "branch": branch,
            "commit": commit.get("sha"),
            "committed_at": (((commit.get("commit") or {}).get("committer") or {}).get("date")),
            "url": commit.get("html_url"),
        }
    except Exception as exc:
        result["errors"].append(f"branch: {type(exc).__name__}: {exc}")
    if result["formal_release"] or result["branch_snapshot"]:
        result["status"] = "REFRESHED"
    return name, result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    resolved = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(resolve, item) for item in REPOS]
        for future in concurrent.futures.as_completed(futures):
            name, value = future.result()
            resolved[name] = value
            print(f"{name}: {value['status']}")
    ordered = {name: resolved[name] for name, *_ in REPOS}
    refreshed = sum(1 for value in ordered.values() if value["status"] == "REFRESHED")
    report = {
        "schema_version": 2,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "NARROW_VOLATILE_FACT_REFRESH_ONLY",
        "overall_status": "REFRESHED" if refreshed == len(ordered) else "PARTIAL",
        "refreshed_count": refreshed,
        "total_count": len(ordered),
        "policy": {
            "does_not_redo_market_research": True,
            "formal_release_and_branch_snapshot_are_separate": True,
            "target_deployment_must_pin_tag_commit_or_digest": True,
            "network_failure_uses_frozen_sources_and_marks_not_verified": True,
        },
        "repositories": ordered,
    }
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
