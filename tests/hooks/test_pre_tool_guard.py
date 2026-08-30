"""Offline regression tests for H0 structured guard decisions."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
GUARD_PATH = ROOT / "scripts" / "codex" / "pre_tool_guard.py"
SPEC = importlib.util.spec_from_file_location("h0_pre_tool_guard", GUARD_PATH)
assert SPEC and SPEC.loader
GUARD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GUARD)


class PreToolGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "Workspace Root"
        (self.root / "products").mkdir(parents=True)
        (self.root / ".codex").mkdir()
        (self.root / "scripts" / "codex").mkdir(parents=True)
        (self.root / "workspace" / "approvals").mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def payload(self, tool_name: str, tool_input: dict) -> dict:
        return {
            "hook_event_name": "PreToolUse",
            "cwd": str(self.root),
            "tool_name": tool_name,
            "tool_input": tool_input,
        }

    def decision(self, tool_name: str, tool_input: dict):
        return GUARD.evaluate_request(self.payload(tool_name, tool_input), self.root)

    def assert_denied(self, decision) -> None:
        self.assertIsInstance(decision, dict)
        self.assertEqual("PreToolUse", decision["hookSpecificOutput"]["hookEventName"])
        self.assertEqual("deny", decision["hookSpecificOutput"]["permissionDecision"])

    def patch_for(self, path: str) -> str:
        return f"*** Begin Patch\n*** Update File: {path}\n@@\n-old\n+new\n*** End Patch\n"

    def test_invalid_and_unknown_payloads_fail_closed(self) -> None:
        self.assert_denied(GUARD.evaluate_request({}, self.root))
        self.assert_denied(self.decision("mcp__unknown__write", {"path": "report.txt"}))
        self.assert_denied(self.decision("unclassified_tool", {"command": "noop"}))

    def test_safe_read_only_command_allows(self) -> None:
        self.assertIsNone(self.decision("Bash", {"command": "Get-Content README_FIRST.md"}))

    def test_protected_apply_patch_denied(self) -> None:
        self.assert_denied(
            self.decision("apply_patch", {"command": self.patch_for(".codex/hooks.json")})
        )
        self.assert_denied(
            self.decision(
                "apply_patch", {"command": self.patch_for("scripts/codex/pre_tool_guard.py")}
            )
        )

    def test_product_paths_without_track_p_all_deny(self) -> None:
        variants = [
            "products/sample.txt",
            ".\\products\\sample.txt",
            str(self.root / "products" / "sample.txt"),
            str(self.root / "PRODUCTS" / "sample.txt").replace("\\", "/"),
            "products\\..\\products\\sample.txt",
        ]
        for target in variants:
            with self.subTest(target=target):
                self.assert_denied(
                    self.decision("apply_patch", {"command": self.patch_for(target)})
                )

    def test_commerce_paths_without_track_p_all_deny(self) -> None:
        for root_name in (
            "docs/commerce",
            "schemas/commerce",
            "jovi_commerce",
            "tests/commerce",
            "data/commerce",
        ):
            target = f"{root_name}/sample.txt"
            with self.subTest(target=target):
                self.assert_denied(
                    self.decision("apply_patch", {"command": self.patch_for(target)})
                )

    def test_local_admin_unc_product_path_without_track_p_denied(self) -> None:
        drive = self.root.drive.rstrip(":")
        relative = str(self.root)[3:].replace("\\", "\\")
        unc = f"\\\\localhost\\{drive}$\\{relative}\\products\\sample.txt"
        self.assert_denied(self.decision("apply_patch", {"command": self.patch_for(unc)}))

    def test_nested_interpreters_and_encoded_shells_deny(self) -> None:
        commands = [
            "python -c \"from pathlib import Path; Path('.codex/hooks.json').write_text('{}')\"",
            "python temporary_writer.py",
            'cmd /c "echo unsafe > E:\\project\\xianyu-auto-reply\\global_config.yml"',
            "powershell -EncodedCommand ZQBjAGgAbwAgAHgA",
        ]
        for command in commands:
            with self.subTest(command=command):
                self.assert_denied(self.decision("Bash", {"command": command}))

    def test_known_powershell_mutators_protect_controls(self) -> None:
        protected = str(self.root / ".codex" / "hooks.json")
        for command in [
            f"Set-Content {protected} x",
            f"Out-File {protected}",
            f"Add-Content {protected} x",
            f"Copy-Item {protected} destination.txt",
            f"Move-Item {protected} destination.txt",
            f"Remove-Item {protected}",
        ]:
            with self.subTest(command=command):
                self.assert_denied(self.decision("Bash", {"command": command}))

    def test_external_sensitive_read_spellings_deny_without_access(self) -> None:
        external = r"E:\project\xianyu-auto-reply\browser_data\cookies.txt"
        for command in [f"gc {external}", f"Get-Content {external}", f"type {external}"]:
            with self.subTest(command=command):
                self.assert_denied(self.decision("Bash", {"command": command}))

    def test_ambiguous_write_target_denies(self) -> None:
        self.assert_denied(self.decision("Bash", {"command": "Set-Content $dynamicTarget value"}))


if __name__ == "__main__":
    unittest.main(verbosity=2)
