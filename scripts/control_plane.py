#!/usr/bin/env python3
"""Strict, non-authorizing S2A1 control-plane primitives."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any


STATE_PATH = "config/control-plane-state.json"
REGISTRY_PATH = "config/control-plane-registry.json"
STATE_KEYS = {
    "schema_version",
    "state_id",
    "state_revision",
    "previous_state_hash",
    "stage",
    "phase_status",
    "permission_class",
    "approval_binding",
    "blockers",
}
STAGES = {"S1", "S2A1", "S2A2", "S2B", "S3", "H1", "C"}
PHASES = {"PREPARE", "READY", "APPLY", "CLOSED", "BLOCKED"}
CLASSES = {"security-tightening", "compatibility-fix", "permission-expansion"}
CORE_CONTROLS = {
    "PROJECT_STATE.json",
    "STATUS.md",
    "CODEX_START_PROMPT.txt",
    REGISTRY_PATH,
    STATE_PATH,
    "scripts/control_plane.py",
    "scripts/validate-control-plane.py",
    ".codex/hooks.json",
    "scripts/codex/Invoke-PreToolGuard.ps1",
    "scripts/codex/pre_tool_guard.py",
    "FRAMEWORK_MANIFEST.sha256",
    "MANIFEST.sha256",
}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
LEGACY_READY_STATE = "READY_FOR_CODEX_PHASE_0_A_X0"
LEGACY_AWAITING_STATE = "AWAITING_GATE_A_TRACK_APPROVALS"
LEGACY_XIANYU_DECISION = "REUSE_AS_SEPARATE_ADAPTER"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def canonical_hash(value: dict[str, Any]) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    return hashlib.sha256(raw).hexdigest()


def normalized_relative(root: Path, value: str, *, reparse_probe=None) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise ValueError("control path is invalid")
    candidate = Path(value.replace("\\", "/"))
    if candidate.is_absolute() or os.path.splitdrive(value)[0]:
        raise ValueError("absolute control path is forbidden")
    root_resolved = root.resolve()
    target = (root_resolved / candidate).resolve(strict=False)
    try:
        target.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError("control path escapes root") from exc
    probe = reparse_probe or (lambda item: item.is_symlink())
    cursor = target
    while cursor != root_resolved:
        if cursor.exists() and probe(cursor):
            raise ValueError("reparse control path is forbidden")
        cursor = cursor.parent
    return target.relative_to(root_resolved).as_posix()


def validate_registry(registry: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    if registry.get("schema_version") != 2:
        errors.append("registry schema_version must be 2")
    if registry.get("canonical_state") != STATE_PATH:
        errors.append("registry canonical state is invalid")
    if registry.get("report_inputs_allowed") is not False:
        errors.append("reports must never be authority inputs")
    controls = registry.get("protected_controls")
    if not isinstance(controls, list):
        return errors + ["protected_controls must be a list"]
    try:
        normalized = [normalized_relative(root, item) for item in controls]
    except ValueError as exc:
        return errors + [str(exc)]
    folded = [item.casefold() for item in normalized]
    if len(set(folded)) != len(folded):
        errors.append("case-colliding control path")
    if not CORE_CONTROLS.issubset(set(normalized)):
        errors.append("required control is missing")
    if set(registry.get("control_classes", [])) != CLASSES:
        errors.append("control class registry mismatch")
    target_classes = registry.get("target_classes")
    if not isinstance(target_classes, dict):
        errors.append("target_classes must be an object")
    else:
        for target in {
            "PROJECT_STATE.json",
            "STATUS.md",
            "CODEX_START_PROMPT.txt",
            REGISTRY_PATH,
            STATE_PATH,
            "scripts/control_plane.py",
            "scripts/validate-control-plane.py",
        }:
            if target_classes.get(target) not in CLASSES:
                errors.append(f"unclassified control target: {target}")
    return errors


def binding_is_valid(binding: Any, permission_class: str) -> bool:
    if not isinstance(binding, dict):
        return False
    required = {"approval_kind", "stage", "plan_sha256", "patch_sha256", "target_set_sha256"}
    if set(binding) != required or binding.get("stage") not in STAGES:
        return False
    if any(
        not isinstance(binding.get(key), str) or not HEX64.fullmatch(binding[key])
        for key in {"plan_sha256", "patch_sha256", "target_set_sha256"}
    ):
        return False
    required_kind = (
        "permission-expansion" if permission_class == "permission-expansion" else "phase"
    )
    return binding.get("approval_kind") == required_kind


def validate_state(state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if set(state) != STATE_KEYS:
        errors.append("state keys are not strict")
    if state.get("schema_version") != 2:
        errors.append("state schema_version must be 2")
    if not isinstance(state.get("state_id"), str) or not state.get("state_id"):
        errors.append("state_id is required")
    if not isinstance(state.get("state_revision"), int) or state.get("state_revision", 0) < 1:
        errors.append("state_revision must be a positive integer")
    previous = state.get("previous_state_hash")
    if state.get("state_revision") == 1 and previous is not None:
        errors.append("initial state cannot name a predecessor")
    if state.get("state_revision", 0) > 1 and (
        not isinstance(previous, str) or not HEX64.fullmatch(previous)
    ):
        errors.append("state predecessor hash is invalid")
    if state.get("stage") not in STAGES or state.get("phase_status") not in PHASES:
        errors.append("unknown stage or phase status")
    if state.get("permission_class") not in CLASSES:
        errors.append("unknown permission class")
    if not isinstance(state.get("blockers"), list) or not all(
        isinstance(item, str) for item in state.get("blockers", [])
    ):
        errors.append("blockers must be a string list")
    if state.get("phase_status") == "APPLY" and not binding_is_valid(
        state.get("approval_binding"), state.get("permission_class")
    ):
        errors.append("APPLY requires a matching approval binding")
    if (
        state.get("phase_status") in {"CLOSED", "BLOCKED", "PREPARE", "READY"}
        and state.get("approval_binding") is not None
    ):
        errors.append("non-APPLY state cannot carry an approval binding")
    return errors


def validate_transition(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    errors = validate_state(before) + validate_state(after)
    if errors:
        return errors
    if after["state_revision"] != before["state_revision"] + 1:
        return ["state revision must advance exactly once"]
    if after["previous_state_hash"] != canonical_hash(before):
        return ["previous state hash does not bind the predecessor"]
    if after["state_id"] == before["state_id"]:
        return ["state_id must change for a new revision"]
    if (
        before["stage"] == "S1"
        and before["phase_status"] == "CLOSED"
        and after["stage"] == "C"
        and after["phase_status"] == "APPLY"
    ):
        if before.get("blockers"):
            return ["S1 closeout blockers must be empty before Commerce APPLY"]
        if after.get("permission_class") != "permission-expansion":
            return ["Commerce APPLY requires permission-expansion classification"]
        binding = after.get("approval_binding")
        if not isinstance(binding, dict) or binding.get("stage") != "C":
            return ["Commerce APPLY requires a stage-C approval binding"]
        return []
    if before["stage"] != after["stage"]:
        return ["core transition cannot change stage"]
    allowed = {
        "PREPARE": {"PREPARE", "READY", "BLOCKED"},
        "READY": {"READY", "APPLY", "BLOCKED"},
        "APPLY": {"APPLY", "CLOSED", "BLOCKED"},
        "BLOCKED": {"BLOCKED"},
        "CLOSED": {"CLOSED"},
    }
    if after["phase_status"] not in allowed[before["phase_status"]]:
        return ["illegal phase transition"]
    return []


def mirror_marker(state: dict[str, Any]) -> str:
    return f"{state['stage']}/{state['phase_status']}/{state['state_revision']}"


def compatibility_view(state: dict[str, Any]) -> dict[str, Any]:
    """Return the deterministic, non-authoritative view kept for S1 readers."""
    current_state = (
        LEGACY_READY_STATE
        if state.get("stage") == "S1" and state.get("phase_status") == "CLOSED"
        else LEGACY_AWAITING_STATE
    )
    return {
        "current_state": current_state,
        "decisions": {"xianyu_integration": LEGACY_XIANYU_DECISION},
    }


def validate_mirrors(root: Path, state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        project = load_json(root / "PROJECT_STATE.json")
        control = project.get("control_plane")
        if not isinstance(control, dict):
            errors.append("PROJECT_STATE control-plane mirror is missing")
        elif (
            any(
                control.get(key) != state[key]
                for key in ("state_id", "state_revision", "stage", "phase_status")
            )
            or control.get("canonical_state") != STATE_PATH
        ):
            errors.append("PROJECT_STATE drift")
        compat = compatibility_view(state)
        if project.get("current_state") != compat["current_state"]:
            errors.append("PROJECT_STATE compatibility view drift")
        decisions = project.get("decisions")
        if (
            not isinstance(decisions, dict)
            or decisions.get("xianyu_integration") != compat["decisions"]["xianyu_integration"]
        ):
            errors.append("PROJECT_STATE compatibility decision drift")
        marker = mirror_marker(state)
        if f"`{marker}`" not in (root / "STATUS.md").read_text(encoding="utf-8"):
            errors.append("STATUS drift")
        prompt_text = (root / "CODEX_START_PROMPT.txt").read_text(encoding="utf-8")
        if "CONTROL_PLANE_AUTHORITY=config/control-plane-state.json" not in prompt_text:
            errors.append("CODEX_START_PROMPT canonical authority pointer missing")
        if "CONTROL_PLANE_MIRROR=" in prompt_text:
            errors.append("CODEX_START_PROMPT contains mutable mirror marker")
        prompt = (root / "CODEX_START_PROMPT.txt").read_text(encoding="utf-8")
        if "B Revision V2 APPLY" in prompt or "S2A-APPLY" in prompt:
            errors.append("expired candidate entry")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"mirror validation failed safely: {exc}")
    return errors


def validate_root(root: Path) -> list[str]:
    try:
        registry = load_json(root / REGISTRY_PATH)
        state = load_json(root / STATE_PATH)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"control-plane source unavailable: {exc}"]
    return validate_registry(registry, root) + validate_state(state) + validate_mirrors(root, state)
