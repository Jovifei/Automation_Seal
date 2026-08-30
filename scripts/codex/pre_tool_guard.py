#!/usr/bin/env python3
"""Fail-closed, project-local PreToolUse guard for Jovi Automation.

This guard is defense in depth only. Codex native workspace permissions and
explicit human approval remain the authority for all real actions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import socket
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
EVENT_NAME = "PreToolUse"
EXTERNAL_XIANYU_ROOT = os.path.normcase(os.path.normpath(r"E:\project\xianyu-auto-reply"))
COMMERCE_CONTROLLED_ROOTS = (
    "docs/commerce",
    "schemas/commerce",
    "jovi_commerce",
    "tests/commerce",
    "data/commerce",
)

WRITE_VERBS = re.compile(
    r"\b(?:set-content|add-content|out-file|copy-item|move-item|remove-item|"
    r"new-item|clear-content|ni|sc|cp|mv|rm|del|erase|rmdir|rd|touch|mkdir|"
    r"write_file|edit_file|git\s+(?:apply|checkout|reset|clean|merge|rebase))\b"
    r"|(?<!\d)>>?(?![&])",
    re.IGNORECASE,
)
READ_VERBS = re.compile(r"\b(?:get-content|gc|cat|type|more|sqlite3)\b", re.IGNORECASE)
NESTED_INTERPRETERS = re.compile(
    r"\b(?:py(?:thon(?:3)?)?|node|powershell|pwsh|cmd)(?:\.exe)?\b",
    re.IGNORECASE,
)
FORBIDDEN_ACTIONS = (
    (
        re.compile(r"dangerously-bypass|bypass-hook-trust", re.IGNORECASE),
        "Safety bypasses are forbidden.",
    ),
    (
        re.compile(r"slider-solve|x5sec|captcha|face[_ -]?verify", re.IGNORECASE),
        "Automated verification handling is forbidden.",
    ),
    (
        re.compile(r"(?:publish|send|deliver|refund|price|reply|order|message)", re.IGNORECASE),
        "External platform actions are forbidden.",
    ),
    (
        re.compile(
            r"docker\s+(?:compose\s+)?(?:up|down|restart|stop|start|build|pull)", re.IGNORECASE
        ),
        "Infrastructure actions require a separate approved phase.",
    ),
)


def deny(reason: str) -> dict[str, Any]:
    """Return the current documented PreToolUse deny shape."""
    return {
        "hookSpecificOutput": {
            "hookEventName": EVENT_NAME,
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def canonicalize_path(value: str, base: Path, *, resolve_links: bool = True) -> str | None:
    """Return a normalized path, or None when safe normalization is impossible."""
    if not isinstance(value, str):
        return None
    raw = value.strip().strip("\"'")
    if not raw or "\x00" in raw or any(ord(char) < 32 for char in raw):
        return None

    # Map local administrative UNC spellings to their drive form without querying a remote host.
    normalized_separators = raw.replace("/", "\\")
    if normalized_separators.lower().startswith("\\\\?\\"):
        normalized_separators = normalized_separators[4:]
        if normalized_separators.lower().startswith("unc\\"):
            normalized_separators = "\\\\" + normalized_separators[4:]
    hostnames = {"localhost", "127.0.0.1", "::1", socket.gethostname().lower()}
    unc_match = re.match(r"^\\\\([^\\]+)\\([A-Za-z])\$(?:\\(.*))?$", normalized_separators)
    if unc_match and unc_match.group(1).lower() in hostnames:
        normalized_separators = f"{unc_match.group(2)}:\\{unc_match.group(3) or ''}"

    try:
        candidate = Path(normalized_separators)
        if not candidate.is_absolute():
            candidate = base / candidate
        normalized = os.path.normpath(os.path.abspath(str(candidate)))
        if resolve_links:
            try:
                is_external = (
                    os.path.commonpath([os.path.normcase(normalized), EXTERNAL_XIANYU_ROOT])
                    == EXTERNAL_XIANYU_ROOT
                )
            except ValueError:
                is_external = False
            if not is_external:
                normalized = os.path.realpath(normalized)
        return os.path.normcase(os.path.normpath(normalized))
    except (OSError, TypeError, ValueError):
        return None


def is_within(candidate: str, parent: str) -> bool:
    """Containment check that rejects cross-volume and malformed comparisons."""
    try:
        return os.path.commonpath([candidate, parent]) == parent
    except (OSError, TypeError, ValueError):
        return False


def protected_domains(root: Path) -> tuple[set[str], tuple[str, ...], str]:
    root_path = canonicalize_path(str(root), root)
    if root_path is None:
        raise ValueError("project root is not canonical")
    protected_dirs = {
        canonicalize_path(str(root / relative), root)
        for relative in (
            ".codex",
            ".agents",
            "scripts/codex",
            "scripts/human-only",
            "scripts/xianyu/human-only",
            "workspace/approvals",
        )
    }
    protected_files = tuple(
        path
        for path in (
            canonicalize_path(str(root / "MANIFEST.sha256"), root),
            canonicalize_path(str(root / "MANIFEST_POLICY.md"), root),
            canonicalize_path(str(root / "PROJECT_STATE.json"), root),
            canonicalize_path(str(root / "STATUS.md"), root),
            canonicalize_path(str(root / "CODEX_START_PROMPT.txt"), root),
            canonicalize_path(str(root / "config" / "control-plane-registry.json"), root),
            canonicalize_path(str(root / "config" / "control-plane-state.json"), root),
        )
        if path is not None
    )
    return {path for path in protected_dirs if path is not None}, protected_files, root_path


def external_xianyu_root() -> str:
    """Return the lexical external protected root without touching that filesystem."""
    return EXTERNAL_XIANYU_ROOT


def is_protected_write(path: str, root: Path) -> bool:
    directories, files, _ = protected_domains(root)
    return (
        path in files
        or any(is_within(path, directory) for directory in directories)
        or is_within(path, external_xianyu_root())
    )


def is_sensitive_external_read(path: str) -> bool:
    return is_within(path, external_xianyu_root())


def extract_path_candidates(text: str) -> list[str]:
    """Extract explicit filesystem-looking arguments; dynamic expressions remain unresolved."""
    candidates: list[str] = []
    for quoted in re.findall(r"\"([^\"]+)\"|'([^']+)'", text):
        candidates.append(quoted[0] or quoted[1])
    path_pattern = re.compile(
        r"(?<![\w])(?:\\\\(?:[^\\\s]+)\\[^\\\s]+\\|[A-Za-z]:[\\/]|\.\.?[\\/]|"
        r"(?:\.codex|\.agents|products|workspace|scripts)[\\/])[^\s;|><\"']*",
        re.IGNORECASE,
    )
    candidates.extend(path_pattern.findall(text))
    for filename in ("MANIFEST.sha256", "MANIFEST_POLICY.md"):
        if re.search(rf"(?<![\w.]){re.escape(filename)}(?![\w.])", text, re.IGNORECASE):
            candidates.append(filename)
    return list(
        dict.fromkeys(candidate.strip("\"'") for candidate in candidates if candidate.strip("\"'"))
    )


def extract_patch_paths(command: str) -> list[str]:
    paths: list[str] = []
    for line in command.splitlines():
        stripped = line.strip()
        for prefix in ("*** Update File: ", "*** Add File: ", "*** Delete File: "):
            if stripped.startswith(prefix):
                paths.append(stripped[len(prefix) :].strip())
        if stripped.startswith("+++ ") or stripped.startswith("--- "):
            value = stripped[4:].strip()
            if value not in {"/dev/null", "a/dev/null", "b/dev/null"}:
                paths.append(re.sub(r"^[ab]/", "", value))
    return list(dict.fromkeys(path for path in paths if path))


def approval_valid(root: Path, gate: str, track: str) -> bool:
    """H0 preserves the existing hash binding; approval authenticity is H1 work."""
    plan = root / "reports" / "gates" / f"{gate}_PLAN.json"
    receipt = root / "workspace" / "approvals" / f"{gate}.{track}.approval.json"
    if not plan.is_file() or not receipt.is_file():
        return False
    try:
        digest = hashlib.sha256(plan.read_bytes()).hexdigest()
        plan_data = json.loads(plan.read_text(encoding="utf-8-sig"))
        receipt_data = json.loads(receipt.read_text(encoding="utf-8-sig"))
    except (OSError, TypeError, ValueError, json.JSONDecodeError):
        return False
    return (
        isinstance(plan_data, dict)
        and isinstance(plan_data.get("tracks"), dict)
        and isinstance(receipt_data, dict)
        and plan_data.get("gate") == gate
        and isinstance(plan_data["tracks"].get(track), dict)
        and receipt_data.get("gate") == gate
        and receipt_data.get("track") == track
        and str(receipt_data.get("plan_sha256", "")).lower() == digest
    )


def validate_payload(payload: Any, root: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not isinstance(payload, dict):
        return None, "Hook input must be a JSON object."
    required = ("hook_event_name", "cwd", "tool_name", "tool_input")
    if any(key not in payload for key in required):
        return None, "Hook input was incomplete."
    if payload["hook_event_name"] != EVENT_NAME:
        return None, "Unexpected hook event was denied."
    if (
        not isinstance(payload["cwd"], str)
        or not isinstance(payload["tool_name"], str)
        or not isinstance(payload["tool_input"], dict)
    ):
        return None, "Hook input had an invalid field type."
    canonical_cwd = canonicalize_path(payload["cwd"], root)
    canonical_root = canonicalize_path(str(root), root)
    if (
        canonical_cwd is None
        or canonical_root is None
        or not is_within(canonical_cwd, canonical_root)
    ):
        return None, "Hook working directory was outside the project."
    return payload, None


def evaluate_write_paths(paths: Iterable[str], root: Path) -> dict[str, Any] | None:
    canonical_root = canonicalize_path(str(root), root)
    product_root = canonicalize_path(str(root / "products"), root)
    commerce_roots = tuple(
        canonicalize_path(str(root / relative), root)
        for relative in COMMERCE_CONTROLLED_ROOTS
    )
    if canonical_root is None or product_root is None or any(item is None for item in commerce_roots):
        return deny("Project path normalization failed safely.")
    normalized_paths: list[str] = []
    for value in paths:
        path = canonicalize_path(value, root)
        if path is None:
            return deny("A write target could not be normalized safely.")
        normalized_paths.append(path)
    if not normalized_paths:
        return deny("A write request did not expose explicit file targets.")
    for path in normalized_paths:
        if is_protected_write(path, root):
            return deny("Writing a protected control domain is forbidden.")
        if not is_within(path, canonical_root):
            return deny("Writing outside the project workspace is forbidden.")
        if is_within(path, product_root) and not approval_valid(root, "GATE_A", "P"):
            return deny("Product writes require a valid GATE_A Track P approval receipt.")
        if any(is_within(path, commerce_root) for commerce_root in commerce_roots):
            if not approval_valid(root, "GATE_A", "P"):
                return deny("Commerce writes require a valid GATE_A Track P approval receipt.")
    return None


def evaluate_bash(command: str, root: Path) -> dict[str, Any] | None:
    if not isinstance(command, str) or not command.strip():
        return deny("Shell input was malformed.")
    for pattern, reason in FORBIDDEN_ACTIONS:
        if pattern.search(command):
            return deny(reason)
    if NESTED_INTERPRETERS.search(command):
        return deny("Nested interpreters and command shells require separate approval.")

    candidates = extract_path_candidates(command)
    canonical_candidates = [canonicalize_path(value, root) for value in candidates]
    if READ_VERBS.search(command):
        if any(path is None for path in canonical_candidates):
            return deny("A read target could not be normalized safely.")
        if any(
            path is not None and is_sensitive_external_read(path) for path in canonical_candidates
        ):
            return deny("Reading the external execution domain is forbidden.")
    if WRITE_VERBS.search(command):
        return evaluate_write_paths(candidates, root)
    return None


def evaluate_apply_patch(tool_input: dict[str, Any], root: Path) -> dict[str, Any] | None:
    command = tool_input.get("command")
    if not isinstance(command, str) or not command.strip():
        return deny("Patch input was malformed.")
    return evaluate_write_paths(extract_patch_paths(command), root)


def evaluate_request(payload: Any, root: Path = ROOT) -> dict[str, Any] | None:
    """Return a deny decision or None for an explicitly understood safe request."""
    try:
        valid_payload, failure = validate_payload(payload, root)
        if failure:
            return deny(failure)
        assert valid_payload is not None
        tool_name = valid_payload["tool_name"]
        tool_input = valid_payload["tool_input"]
        if tool_name == "Bash":
            return evaluate_bash(tool_input.get("command"), root)
        if tool_name == "apply_patch":
            return evaluate_apply_patch(tool_input, root)
        if tool_name.startswith("mcp__"):
            return deny("MCP tools are denied until their write capability is classified.")
        return deny("Unknown tool input was denied safely.")
    except Exception:
        return deny("Hook guard failed safely.")


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", type=Path, default=ROOT)
    args, _ = parser.parse_known_args()
    try:
        payload = json.loads(sys.stdin.buffer.read().decode("utf-8-sig"))
    except Exception:
        payload = None
    decision = evaluate_request(payload, args.root)
    if decision is not None:
        print(json.dumps(decision, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
