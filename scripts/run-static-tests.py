#!/usr/bin/env python3
"""Offline synthetic and structural test suite for the final Jovi handoff."""

from __future__ import annotations

import argparse
from authorize_action import authorization_errors
import hashlib
import importlib.util
import json
import os
import py_compile
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

from static_test_support import (
    capability_limitations,
    detect_capabilities,
    remove_runtime_caches,
    resolve_report_dir,
    run_clean_build_pair,
)

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
PARSER = argparse.ArgumentParser(description="Run offline static tests.")
PARSER.add_argument("--output-dir", type=Path, default=None)
PARSER.add_argument("--approved-output-root", type=Path, default=None)
PARSER.add_argument("--cleanup-runtime-caches", action="store_true")
PARSER.add_argument("--phase", choices=("pre-gate", "post-transition"), default="pre-gate")
ARGS = PARSER.parse_args()
authorization = authorization_errors(ROOT, "static-tests")
action_authorized = not authorization
try:
    OUT = resolve_report_dir(ROOT, ARGS.output_dir, ARGS.approved_output_root)
except ValueError as exc:
    PARSER.error(str(exc))
if OUT is not None:
    OUT.mkdir(parents=True, exist_ok=True)
checks: list[dict] = []


def record(name: str, passed: bool, detail: str = "") -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": str(detail)[:1200]})
    print(f"[{'PASS' if passed else 'FAIL'}] {name}: {detail}")


def control_plane_report() -> dict[str, object]:
    """Expose authorization facts without treating a denied action as allowed."""
    state_path = ROOT / "config" / "control-plane-state.json"
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError):
        state = {}
    return {
        "stage_closed": state.get("phase_status") == "CLOSED",
        "action_authorized": action_authorized,
        "blocker_present": bool(state.get("blockers")),
        "gate_satisfied": ARGS.phase == "post-transition",
        "authorization_errors": authorization,
    }


def run(
    command: list[str], cwd: Path = ROOT, input_text: str | None = None, env: dict | None = None
) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        cwd=cwd,
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=60,
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(root: Path) -> dict[str, str]:
    result = {}
    for file in sorted(p for p in root.rglob("*") if p.is_file()):
        result[file.relative_to(root).as_posix()] = sha256(file)
    return result


if ARGS.cleanup_runtime_caches:
    remove_runtime_caches(ROOT)


# 1. Package validator.
validation = run([PYTHON, "scripts/validate-package.py"])
record(
    "package_validator",
    validation.returncode == 0,
    validation.stdout.strip() or validation.stderr.strip(),
)

# 2. Compile every Python source separately.
python_files = sorted(
    p
    for p in ROOT.rglob("*.py")
    if not any(part in {"reports", "backups", "dist", "__pycache__"} for part in p.parts)
)
for file in python_files:
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            py_compile.compile(str(file), cfile=str(Path(temp_dir) / "compiled.pyc"), doraise=True)
        record(f"python_compile:{file.relative_to(ROOT)}", True, "compiled")
    except Exception as exc:
        record(f"python_compile:{file.relative_to(ROOT)}", False, exc)

# 3. PowerShell parser checks. They are not a substitute for behavioral execution.
ps_files = sorted(p for p in ROOT.rglob("*.ps1") if "reports" not in p.parts)
power_shell = shutil.which("powershell") or shutil.which("pwsh")
for file in ps_files:
    text = file.read_text(encoding="utf-8-sig", errors="replace")
    no_null = "\x00" not in text
    has_error_policy = "$ErrorActionPreference" in text or file.name in {
        "common.ps1",
        "Invoke-PreToolGuard.ps1",
    }
    if power_shell:
        escaped_file = str(file).replace("'", "''")
        parser_command = (
            "$tokens=$null; $errors=$null; "
            f"[System.Management.Automation.Language.Parser]::ParseFile('{escaped_file}', [ref]$tokens, [ref]$errors) | Out-Null; "
            "if($errors.Count -gt 0){$errors | ForEach-Object {$_.Message}; exit 1}"
        )
        parsed = run([power_shell, "-NoProfile", "-Command", parser_command])
        syntax_ok = parsed.returncode == 0
        detail = parsed.stdout.strip() or parsed.stderr.strip() or "parsed"
    else:
        syntax_ok = text.count("{") == text.count("}") and text.count("(") == text.count(")")
        detail = "powershell unavailable; lexical fallback"
    record(
        f"powershell_structure:{file.relative_to(ROOT)}",
        syntax_ok and no_null and has_error_policy,
        f"syntax={syntax_ok}, null_free={no_null}, error_policy={has_error_policy}; {detail}",
    )

# 4. Product Alpha tests and build.
product = ROOT / "products" / "modbus-rtu-toolkit"
product_env = os.environ.copy()
product_env["PYTHONDONTWRITEBYTECODE"] = "1"
product_tests = run(
    [PYTHON, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=product, env=product_env
)
record(
    "modbus_alpha_unittest",
    product_tests.returncode == 0,
    product_tests.stderr.strip() or product_tests.stdout.strip(),
)
build_pair = run_clean_build_pair(product, PYTHON, product_env)
facts = build_pair["archive_facts"][0]
record("modbus_alpha_build", build_pair["returncodes"] == [0, 0], build_pair["details"])
record(
    "modbus_alpha_independent_clean_outputs",
    build_pair["roots_distinct"] and build_pair["clean_starts"] == [True, True],
    build_pair["clean_starts"],
)
record(
    "modbus_alpha_archive_exists",
    build_pair["archives_exist"] == [True, True],
    build_pair["archives_exist"],
)
if facts is not None:
    names = set(facts["names"])
    record("modbus_alpha_zip_integrity", facts["bad_member"] is None, f"bad={facts['bad_member']}")
    record(
        "modbus_alpha_zip_required_files",
        {"README.md", "SBOM.cdx.json", "modbus_toolkit/parser.py", "tests/test_parser.py"}.issubset(
            names
        ),
        f"entries={len(names)}",
    )
    record("modbus_alpha_zip_deterministic_metadata", facts["fixed_times"], "fixed timestamps")
record("modbus_alpha_sha256", build_pair["sha_files"] == build_pair["hashes"], build_pair["hashes"])
record(
    "modbus_alpha_reproducible",
    build_pair["hashes"][0] is not None and len(set(build_pair["hashes"])) == 1,
    build_pair["hashes"],
)
record("modbus_alpha_no_shared_output", not build_pair["shared_output"], "independent output roots")
record("modbus_alpha_temp_roots_cleaned", build_pair["cleaned"], "temporary roots removed")

# 5. Hook behavior using synthetic tool payloads.
guard = ROOT / "scripts" / "codex" / "pre_tool_guard.py"
spec = importlib.util.spec_from_file_location("jovi_pre_tool_guard", guard)
assert spec and spec.loader
guard_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard_module)


def guard_case(name: str, payload: dict, should_block: bool, reason_fragment: str = "") -> None:
    data = guard_module.evaluate_request(payload, ROOT)
    output = data.get("hookSpecificOutput", {}) if isinstance(data, dict) else {}
    is_blocked = (
        output.get("hookEventName") == "PreToolUse" and output.get("permissionDecision") == "deny"
    )
    reason = str(output.get("permissionDecisionReason", ""))
    passed = is_blocked == should_block and (
        not reason_fragment or reason_fragment.lower() in reason.lower()
    )
    record(f"hook:{name}", passed, f"blocked={is_blocked}; reason={reason}")


# One CLI smoke verifies stdin/JSON behavior without paying process startup cost for every case.
def hook_payload(tool_name: str, tool_input: dict) -> dict:
    return {
        "hook_event_name": "PreToolUse",
        "cwd": str(ROOT),
        "tool_name": tool_name,
        "tool_input": tool_input,
    }


guard_cli = run(
    [PYTHON, str(guard)],
    input_text=json.dumps(
        hook_payload("Bash", {"command": "powershell scripts/human-only/Approve-Gate.ps1"})
    ),
)
record(
    "hook_cli_smoke",
    guard_cli.returncode == 0 and '"permissionDecision":"deny"' in guard_cli.stdout,
    guard_cli.stdout.strip() or guard_cli.stderr.strip(),
)

safe_payloads = {
    "readme_read": hook_payload("Bash", {"command": "Get-Content README_FIRST.md"}),
    "git_read": hook_payload("Bash", {"command": "git status --porcelain"}),
    "report_read": hook_payload(
        "Bash", {"command": "Get-Content reports\\phase-a\\preflight.json"}
    ),
}
for name, payload in safe_payloads.items():
    guard_case(name, payload, False)
product_without_gate_target = (
    ROOT / "products" / "modbus-rtu-toolkit" / "modbus_toolkit" / "parser.py"
).as_posix()
blocked_payloads = {
    "human_only": (
        hook_payload("Bash", {"command": "powershell scripts/human-only/Approve-Gate.ps1"}),
        "Nested",
    ),
    "dangerous_bypass": (
        hook_payload("Bash", {"command": "codex --dangerously-bypass-approvals-and-sandbox"}),
        "bypass",
    ),
    "xianyu_mutation": (
        hook_payload(
            "Bash",
            {"command": 'cmd /c "echo unsafe > E:\\project\\xianyu-auto-reply\\global_config.yml"'},
        ),
        "External",
    ),
    "xianyu_sensitive_read": (
        hook_payload(
            "Bash", {"command": "Get-Content E:\\project\\xianyu-auto-reply\\data\\xianyu_data.db"}
        ),
        "external",
    ),
    "slider": (
        hook_payload(
            "Bash", {"command": "Invoke-RestMethod http://localhost/api/captcha/slider-solve"}
        ),
        "verification",
    ),
    "external_reply": (
        hook_payload("Bash", {"command": "Invoke-RestMethod http://localhost/api/send_message"}),
        "platform",
    ),
    "approval_write": (
        hook_payload(
            "apply_patch",
            {
                "command": "*** Begin Patch\n*** Update File: workspace/approvals/GATE_A.P.approval.json\n*** End Patch"
            },
        ),
        "protected",
    ),
    "safety_edit": (
        hook_payload(
            "apply_patch",
            {"command": "*** Begin Patch\n*** Update File: .codex/hooks.json\n*** End Patch"},
        ),
        "protected",
    ),
    "product_without_gate": (
        hook_payload(
            "apply_patch",
            {
                "command": f"*** Begin Patch\n*** Update File: {product_without_gate_target}\n*** End Patch"
            },
        ),
        "Product writes require a valid GATE_A Track P approval receipt.",
    ),
    "infra_without_gate": (
        hook_payload("Bash", {"command": "powershell scripts/start-core.ps1"}),
        "Nested",
    ),
    "destructive_volume": (
        hook_payload("Bash", {"command": "docker compose down -v"}),
        "Infrastructure",
    ),
}
for name, (payload, fragment) in blocked_payloads.items():
    guard_case(name, payload, True, fragment)

# 6. Gate and track verification in a temporary root.
with tempfile.TemporaryDirectory() as temp_dir:
    temp = Path(temp_dir)
    (temp / "reports" / "gates").mkdir(parents=True)
    (temp / "workspace" / "approvals").mkdir(parents=True)
    plan = {
        "schema_version": 3,
        "gate": "GATE_A",
        "tracks": {
            "P": {"status": "AWAITING_HUMAN_APPROVAL"},
            "I": {"status": "AWAITING_HUMAN_APPROVAL"},
        },
    }
    plan_path = temp / "reports" / "gates" / "GATE_A_PLAN.json"
    plan_path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    digest = sha256(plan_path)
    (temp / "workspace" / "approvals" / "GATE_A.P.approval.json").write_text(
        json.dumps({"gate": "GATE_A", "track": "P", "plan_sha256": digest}), encoding="utf-8"
    )
    verify_p = run(
        [
            PYTHON,
            "scripts/verify-gate-approval.py",
            "--root",
            str(temp),
            "--gate",
            "GATE_A",
            "--track",
            "P",
        ]
    )
    record(
        "gate_track_p_match",
        verify_p.returncode == 0,
        verify_p.stdout.strip() or verify_p.stderr.strip(),
    )
    verify_i_missing = run(
        [
            PYTHON,
            "scripts/verify-gate-approval.py",
            "--root",
            str(temp),
            "--gate",
            "GATE_A",
            "--track",
            "I",
        ]
    )
    record(
        "gate_track_i_not_inherited",
        verify_i_missing.returncode != 0,
        verify_i_missing.stderr.strip(),
    )
    wrong_track = json.loads(
        (temp / "workspace" / "approvals" / "GATE_A.P.approval.json").read_text()
    )
    wrong_track["track"] = "I"
    (temp / "workspace" / "approvals" / "GATE_A.P.approval.json").write_text(
        json.dumps(wrong_track), encoding="utf-8"
    )
    verify_wrong = run(
        [
            PYTHON,
            "scripts/verify-gate-approval.py",
            "--root",
            str(temp),
            "--gate",
            "GATE_A",
            "--track",
            "P",
        ]
    )
    record("gate_wrong_track_rejected", verify_wrong.returncode != 0, verify_wrong.stderr.strip())
    wrong_track["track"] = "P"
    (temp / "workspace" / "approvals" / "GATE_A.P.approval.json").write_text(
        json.dumps(wrong_track), encoding="utf-8"
    )
    plan_path.write_text(json.dumps({**plan, "changed": True}), encoding="utf-8")
    verify_tamper = run(
        [
            PYTHON,
            "scripts/verify-gate-approval.py",
            "--root",
            str(temp),
            "--gate",
            "GATE_A",
            "--track",
            "P",
        ]
    )
    record("gate_plan_tamper_rejected", verify_tamper.returncode != 0, verify_tamper.stderr.strip())

# 7. Xianyu bundle contract tests from existing scripts.
builder_path = ROOT / "scripts" / "xianyu" / "new_xianyu_draft_bundle.py"
validator_path = ROOT / "scripts" / "xianyu" / "validate_xianyu_bundle.py"
validator_spec = importlib.util.spec_from_file_location("jovi_xianyu_validator", validator_path)
assert validator_spec and validator_spec.loader
validator_module = importlib.util.module_from_spec(validator_spec)
validator_spec.loader.exec_module(validator_module)
with tempfile.TemporaryDirectory() as temp_dir:
    temp = Path(temp_dir)
    package_dir = temp / "bundle"
    build_bundle = run(
        [
            PYTHON,
            str(builder_path),
            "--input",
            str(ROOT / "deploy/xianyu/synthetic_product_input.example.json"),
            "--output-dir",
            str(package_dir),
        ]
    )
    record(
        "xianyu_bundle_build",
        build_bundle.returncode == 0,
        build_bundle.stdout.strip() or build_bundle.stderr.strip(),
    )
    positive_errors = validator_module.validate_bundle(package_dir / "bundle.json")
    record("xianyu_bundle_positive", not positive_errors, "; ".join(positive_errors) or "valid")
    full_validator = validator_module.Draft202012Validator
    full_checker = validator_module.FormatChecker
    validator_module.Draft202012Validator = None
    validator_module.FormatChecker = None
    fallback_errors = validator_module.validate_bundle(package_dir / "bundle.json")
    record(
        "xianyu_bundle_stdlib_fallback",
        not fallback_errors,
        "; ".join(fallback_errors) or "valid without jsonschema",
    )
    validator_module.Draft202012Validator = full_validator
    validator_module.FormatChecker = full_checker
    if (package_dir / "bundle.json").is_file():
        base = json.loads((package_dir / "bundle.json").read_text(encoding="utf-8"))
        mutations = {
            "publish_true": lambda item: item["external_actions"].__setitem__("publish", True),
            "send_true": lambda item: item["external_actions"].__setitem__("send_message", True),
            "rights_pending": lambda item: item["rights"].__setitem__("status", "PENDING"),
            "delivery_nonempty": lambda item: item["payload"]["delivery_catalog"].append(
                {"demo": True}
            ),
            "unsafe_bundle_id": lambda item: item.__setitem__("bundle_id", "../../unsafe"),
            "embedded_approval": lambda item: item["approval"].__setitem__("status", "APPROVED"),
        }
        for case, mutate in mutations.items():
            case_dir = temp / f"negative-{case}"
            shutil.copytree(package_dir, case_dir)
            value = json.loads(json.dumps(base))
            mutate(value)
            bundle_case = case_dir / "bundle.json"
            bundle_case.write_text(
                json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            errors = validator_module.validate_bundle(bundle_case)
            record(f"xianyu_bundle_negative:{case}", bool(errors), "; ".join(errors[:3]))

# 8. Synthetic X0 audit must not mutate or disclose secrets/paths.
with tempfile.TemporaryDirectory() as temp_dir:
    temp = Path(temp_dir)
    fake = temp / "xianyu-auto-reply"
    (fake / "data").mkdir(parents=True)
    (fake / "browser_data").mkdir(parents=True)
    (fake / "docker-compose.yml").write_text(
        """services:\n  app:\n    image: demo/xianyu:latest\n    user: \"0:0\"\n    ports:\n      - \"9000:8090\"\n      - \"5900:5900\"\n    volumes:\n      - .:/app:rw\n    environment:\n      - ADMIN_PASSWORD=admin123\n      - JWT_SECRET_KEY=default-secret-key\n      - AUTO_REPLY_ENABLED=true\n      - AUTO_DELIVERY_ENABLED=true\n      - ENABLE_VNC=true\n""",
        encoding="utf-8",
    )
    (fake / "global_config.yml").write_text("SECRET_TOKEN=TOP_SECRET_VALUE\n", encoding="utf-8")
    (fake / "version.txt").write_text("v2.0.5\n", encoding="utf-8")
    (fake / "data" / "customer-private-name.db").write_bytes(b"SQLite format 3\x00TOP_SECRET_DB")
    (fake / "browser_data" / "private-profile.dat").write_text(
        "TOP_SECRET_BROWSER", encoding="utf-8"
    )
    (fake / "README.md").write_text("synthetic", encoding="utf-8")
    git_available = shutil.which("git") is not None
    if git_available:
        git_env = os.environ.copy()
        git_env["HOME"] = str(temp / "git-home")
        Path(git_env["HOME"]).mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init", "-q"], cwd=fake, env=git_env, check=True, timeout=10)
        subprocess.run(["git", "add", "README.md"], cwd=fake, env=git_env, check=True, timeout=10)
    record(
        "x0_git_fixture_optional",
        True,
        "git fixture enabled" if git_available else "git absent; non-git audit fixture used",
    )
    (fake / "buyer-phone-13800138000.txt").write_text("private", encoding="utf-8")
    before = tree_digest(fake)
    audit_dir = temp / "audit"
    audit_path = ROOT / "scripts" / "xianyu" / "xianyu_readonly_audit.py"
    audit_spec = importlib.util.spec_from_file_location("jovi_x0_offline_fixture", audit_path)
    assert audit_spec and audit_spec.loader
    audit_module = importlib.util.module_from_spec(audit_spec)
    audit_spec.loader.exec_module(audit_module)
    audit_module.run = lambda *args, **kwargs: {
        "ok": False,
        "error": "runtime probes disabled in offline static tests",
    }
    audit_module.urllib.request.urlopen = lambda *args, **kwargs: (_ for _ in ()).throw(
        AssertionError("network disabled in offline static tests")
    )
    original_argv = sys.argv
    try:
        sys.argv = [str(audit_path), "--repo", str(fake), "--output-dir", str(audit_dir)]
        audit_code = audit_module.main()
    finally:
        sys.argv = original_argv
    after = tree_digest(fake)
    output_text = "\n".join(
        p.read_text(encoding="utf-8") for p in audit_dir.glob("*") if p.is_file()
    )
    record("x0_audit_executes", audit_code == 0, "offline fixture; runtime probes disabled")
    record("x0_no_mutation", before == after, f"before={len(before)}, after={len(after)}")
    record(
        "x0_no_secret_values",
        all(
            token not in output_text
            for token in ["TOP_SECRET_VALUE", "TOP_SECRET_DB", "TOP_SECRET_BROWSER"]
        ),
        "secret markers absent",
    )
    record(
        "x0_no_git_paths", "buyer-phone-13800138000.txt" not in output_text, "changed path absent"
    )
    record(
        "x0_no_db_names", "customer-private-name.db" not in output_text, "database filename absent"
    )
    data = json.loads((audit_dir / "audit.json").read_text(encoding="utf-8"))
    record(
        "x0_db_not_opened_or_hashed",
        data["database_metadata"]["content_opened"] is False
        and data["database_metadata"]["hashes_computed"] is False,
        data["database_metadata"],
    )
    record(
        "x0_safe_version_parsed",
        data["safe_versions"]["version.txt"]["value"] == "v2.0.5",
        data["safe_versions"]["version.txt"],
    )
    record(
        "x0_compose_risks_boolean",
        data["compose"]["docker-compose.yml"]["structural_risks"]["root_user"] is True,
        data["compose"]["docker-compose.yml"]["structural_risks"],
    )

# 9. Context, research freeze and one-command path.
start = (ROOT / "CODEX_START_PROMPT.txt").read_text(encoding="utf-8")
record(
    "context_structured_summary_present",
    (ROOT / "context/04_CONVERSATION_CONTEXT.md").stat().st_size > 1000,
    "conversation summary",
)
record(
    "completed_work_present",
    (ROOT / "context/05_COMPLETED_WORK.md").stat().st_size > 500,
    "completed work",
)
record(
    "research_freeze_present",
    "不得重复" in (ROOT / "context/06_RESEARCH_FREEZE_POLICY.md").read_text(encoding="utf-8"),
    "freeze policy",
)
record(
    "start_prompt_single_entry",
    start.count("00-run-readonly-audit.ps1") == 1,
    f"count={start.count('00-run-readonly-audit.ps1')}",
)
record(
    "start_prompt_no_all_prd_load",
    "context/source_markdown/*.md" not in start,
    "progressive context",
)
state_data = json.loads((ROOT / "PROJECT_STATE.json").read_text(encoding="utf-8-sig"))
record(
    "project_state_machine_readable",
    state_data.get("package_version") == "3.0.0"
    and bool(state_data.get("current_state"))
    and state_data.get("decisions", {}).get("xianyu_integration") == "REUSE_AS_SEPARATE_ADAPTER",
    state_data.get("current_state"),
)
manifest_policy = (ROOT / "MANIFEST_POLICY.md").read_text(encoding="utf-8")
record(
    "manifest_policy_present",
    "FRAMEWORK_MANIFEST.sha256" in manifest_policy and "--verify-shipment" in manifest_policy,
    "two-level manifest policy",
)
first_run = (ROOT / "scripts/00-run-readonly-audit.ps1").read_text(encoding="utf-8-sig")
record(
    "first_run_verifies_shipment",
    "--verify-shipment" in first_run,
    "full snapshot verified before runtime writes",
)
validator_text = (ROOT / "scripts/validate-package.py").read_text(encoding="utf-8")
record(
    "validator_verifies_framework_manifest",
    "FRAMEWORK_MANIFEST.sha256" in validator_text and "ARGS.verify_shipment" in validator_text,
    "runtime-safe manifest behavior",
)

# 10. Compose policy checks.
compose = (ROOT / "deploy/docker-compose.core.yml").read_text(encoding="utf-8")
record("compose_no_latest", ":latest" not in compose, "mutable latest absent")
record("compose_loopback_n8n", "127.0.0.1:${N8N_PORT}:5678" in compose, "n8n loopback")
record(
    "compose_loopback_changedetection",
    "127.0.0.1:${CHANGEDETECTION_PORT}:5000" in compose,
    "changedetection loopback",
)
record(
    "compose_node_healthcheck",
    "fetch('http://127.0.0.1:5678/healthz')" in compose,
    "Node healthcheck",
)
record(
    "healthcheck_dynamic_ports",
    "N8N_PORT" in (ROOT / "scripts/healthcheck.ps1").read_text(encoding="utf-8")
    and ".env.runtime" in (ROOT / "scripts/healthcheck.ps1").read_text(encoding="utf-8"),
    "dynamic port lookup",
)
start_core_text = (ROOT / "scripts/start-core.ps1").read_text(encoding="utf-8-sig")
record(
    "start_core_runtime_digest_pin",
    all(
        token in start_core_text for token in [".env.runtime", "RepoDigest", "LOCKED_VERSIONS.json"]
    ),
    "runtime images are pinned before startup",
)
record(
    "env_files_written_without_bom",
    "UTF8Encoding($false)" in start_core_text
    and "UTF8Encoding($false)" in (ROOT / "scripts/bootstrap.ps1").read_text(encoding="utf-8-sig"),
    "Docker env files use UTF-8 without BOM",
)

passed = all(item["passed"] for item in checks)
capabilities = detect_capabilities()
report = {
    "schema_version": 3,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "mode": "OFFLINE_SYNTHETIC_AND_STRUCTURAL",
    "passed": passed,
    "check_count": len(checks),
    "passed_count": sum(1 for item in checks if item["passed"]),
    "failed_count": sum(1 for item in checks if not item["passed"]),
    "checks": checks,
    "capabilities": capabilities,
    "runtime_cache_cleanup_requested": ARGS.cleanup_runtime_caches,
    "limitations": capability_limitations(capabilities),
    "control_plane": control_plane_report(),
}
lines = [
    "# Package static test report",
    "",
    f"- Passed: {passed}",
    f"- Checks: {report['passed_count']}/{report['check_count']}",
    f"- Generated: {report['generated_at']}",
    "- Mode: offline, synthetic and structural",
    "",
    "| Check | Result | Detail |",
    "|---|---|---|",
]
for item in checks:
    detail = item["detail"].replace("|", "\\|").replace("\n", "<br>")
    lines.append(f"| {item['name']} | {'PASS' if item['passed'] else 'FAIL'} | {detail} |")
lines += ["", "## Limitations", ""] + [f"- {item}" for item in report["limitations"]]
if OUT is None:
    print(json.dumps(report, ensure_ascii=False, indent=2))
else:
    (OUT / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
raise SystemExit(0 if passed and action_authorized else 2)
