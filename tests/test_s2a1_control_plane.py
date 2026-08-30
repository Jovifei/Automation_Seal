#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from control_plane import (
    STATE_PATH,
    canonical_hash,
    compatibility_view,
    normalized_relative,
    validate_mirrors,
    validate_registry,
    validate_root,
    validate_state,
    validate_transition,
)  # noqa: E402


class S2A1CoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads(
            (ROOT / "config/control-plane-registry.json").read_text(encoding="utf-8")
        )
        cls.state = json.loads((ROOT / STATE_PATH).read_text(encoding="utf-8"))

    def transition(self, phase, binding=None):
        result = copy.deepcopy(self.state)
        result["state_id"] = "next-state"
        result["state_revision"] = self.state["state_revision"] + 1
        result["previous_state_hash"] = canonical_hash(self.state)
        result["phase_status"] = phase
        result["approval_binding"] = binding
        return result

    def test_01_registry_has_required_controls(self):
        self.assertEqual(validate_registry(self.registry, ROOT), [])

    def test_02_registry_missing_control_fails(self):
        item = copy.deepcopy(self.registry)
        item["protected_controls"].remove("scripts/control_plane.py")
        self.assertTrue(validate_registry(item, ROOT))

    def test_03_registry_self_classification_required(self):
        item = copy.deepcopy(self.registry)
        del item["target_classes"][STATE_PATH]
        self.assertTrue(validate_registry(item, ROOT))

    def test_04_absolute_control_path_fails(self):
        with self.assertRaises(ValueError):
            normalized_relative(ROOT, "E:/outside")

    def test_05_traversal_control_path_fails(self):
        with self.assertRaises(ValueError):
            normalized_relative(ROOT, "../outside")

    def test_06_case_collision_fails(self):
        item = copy.deepcopy(self.registry)
        item["protected_controls"].append("project_state.json")
        self.assertTrue(validate_registry(item, ROOT))

    def test_07_state_schema_is_valid(self):
        self.assertEqual(validate_state(self.state), [])

    def test_08_unknown_state_fails(self):
        item = copy.deepcopy(self.state)
        item["phase_status"] = "UNKNOWN"
        self.assertTrue(validate_state(item))

    def test_09_illegal_state_tuple_fails(self):
        item = copy.deepcopy(self.state)
        item["approval_binding"] = {}
        self.assertTrue(validate_state(item))

    def test_10_initial_predecessor_fails(self):
        item = copy.deepcopy(self.state)
        item["previous_state_hash"] = "a" * 64
        self.assertTrue(validate_state(item))

    def test_11_revision_replay_fails(self):
        item = self.transition("CLOSED")
        item["state_revision"] = self.state["state_revision"]
        self.assertTrue(validate_transition(self.state, item))

    def test_12_revision_rollback_fails(self):
        item = self.transition("CLOSED")
        item["state_revision"] = 0
        self.assertTrue(validate_transition(self.state, item))

    def test_13_closed_to_prepare_fails(self):
        self.assertTrue(validate_transition(self.state, self.transition("PREPARE")))

    def test_14_blocked_to_ready_fails(self):
        before = copy.deepcopy(self.state)
        before["phase_status"] = "BLOCKED"
        after = copy.deepcopy(before)
        after.update(
            {
                "state_id": "blocked-next",
                "state_revision": 2,
                "previous_state_hash": canonical_hash(before),
                "phase_status": "READY",
            }
        )
        self.assertTrue(validate_transition(before, after))

    def test_15_prepare_to_apply_without_approval_fails(self):
        before = copy.deepcopy(self.state)
        before.update(
            {
                "state_id": "prepare",
                "state_revision": 2,
                "previous_state_hash": "a" * 64,
                "phase_status": "PREPARE",
            }
        )
        self.assertTrue(validate_transition(before, copy.deepcopy(before)))

    def test_16_permission_expansion_requires_distinct_binding(self):
        item = copy.deepcopy(self.state)
        item.update(
            {
                "state_id": "apply",
                "state_revision": 2,
                "previous_state_hash": "a" * 64,
                "phase_status": "APPLY",
                "permission_class": "permission-expansion",
                "approval_binding": {
                    "approval_kind": "phase",
                    "stage": "S1",
                    "plan_sha256": "a" * 64,
                    "patch_sha256": "b" * 64,
                    "target_set_sha256": "c" * 64,
                },
            }
        )
        self.assertTrue(validate_state(item))

    def test_16b_s1_closed_to_c_apply_requires_bound_gate(self):
        before = copy.deepcopy(self.state)
        before["blockers"] = []
        after = copy.deepcopy(before)
        after.update(
            {
                "state_id": "commerce-apply",
                "state_revision": before["state_revision"] + 1,
                "previous_state_hash": canonical_hash(before),
                "stage": "C",
                "phase_status": "APPLY",
                "permission_class": "permission-expansion",
                "approval_binding": {
                    "approval_kind": "permission-expansion",
                    "stage": "C",
                    "plan_sha256": "a" * 64,
                    "patch_sha256": "b" * 64,
                    "target_set_sha256": "c" * 64,
                },
            }
        )
        self.assertEqual([], validate_transition(before, after))

    def test_17_project_state_is_mirror(self):
        self.assertEqual(validate_mirrors(ROOT, self.state), [])

    def test_18_status_only_tamper_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            self._fixture(Path(temp), "STATUS.md", "tampered", "STATUS drift")

    def test_19_project_only_tamper_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            self._fixture(Path(temp), "PROJECT_STATE.json", "{}", "PROJECT_STATE")

    def test_20_prompt_only_tamper_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            self._fixture(Path(temp), "CODEX_START_PROMPT.txt", "tampered", "CODEX_START_PROMPT")

    def test_21_legacy_entry_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            self._fixture(
                Path(temp),
                "CODEX_START_PROMPT.txt",
                "CONTROL_PLANE_MIRROR=S1/CLOSED/1\nB Revision V2 APPLY",
                "expired",
            )

    def test_22_report_path_cannot_be_authority(self):
        item = copy.deepcopy(self.registry)
        item["canonical_state"] = "reports/state.json"
        self.assertTrue(validate_registry(item, ROOT))

    def test_23_missing_registry_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            fixture = Path(temp)
            shutil.copytree(ROOT, fixture / "root")
            (fixture / "root/config/control-plane-registry.json").unlink()
            self.assertTrue(validate_root(fixture / "root"))

    def test_24_report_json_is_not_state_input(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self._minimal_control_root(Path(temp))
            report = self._write_report(root, {"phase_status": "READY"})
            self.assertEqual(validate_root(root), [])
            report.unlink()

    def test_25_reparse_probe_fails(self):
        with self.assertRaises(ValueError):
            normalized_relative(ROOT, "scripts/control_plane.py", reparse_probe=lambda _: True)

    def test_26_core_is_non_authorizing(self):
        self.assertTrue(validate_transition(self.state, self.transition("PREPARE")))

    def test_27_preexisting_reports_are_preserved_and_non_authoritative(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self._minimal_control_root(Path(temp))
            reports = root / "reports"
            reports.mkdir()
            sentinel = reports / "existing-unrelated-report.json"
            sentinel.write_text('{"keep":"unchanged"}', encoding="utf-8")
            before = sentinel.read_bytes()
            report = self._write_report(
                root,
                {
                    "phase_status": "CLOSED",
                    "state_revision": 999,
                    "previous_state": "forged",
                    "approval_binding": {"approved": True},
                    "blocked_stages": [],
                },
            )
            self.assertEqual(validate_root(root), [])
            self.assertEqual(sentinel.read_bytes(), before)
            report.unlink()
            self.assertEqual(sentinel.read_bytes(), before)

    def test_28_reports_file_is_rejected_by_fixture(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self._minimal_control_root(Path(temp))
            (root / "reports").write_text("not a directory", encoding="utf-8")
            with self.assertRaisesRegex(AssertionError, "unsafe reports fixture"):
                self._write_report(root, {"phase_status": "READY"})

    def test_29_reparse_reports_are_rejected_by_fixture(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self._minimal_control_root(Path(temp))
            (root / "reports").mkdir()
            with patch.object(self, "_is_reparse_point", return_value=True):
                with self.assertRaisesRegex(AssertionError, "unsafe reports fixture"):
                    self._write_report(root, {"phase_status": "READY"})

    def test_30_report_pseudo_states_do_not_change_authoritative_state(self):
        payloads = [
            {"phase_status": "READY"},
            {"phase_status": "CLOSED"},
            {"phase_status": "APPLY"},
            {
                "permission_expansion": "approved",
                "approval_binding": {"approved": True},
                "state_revision": 999,
                "previous_state": "forged",
                "blocked_stages": [],
            },
        ]
        with tempfile.TemporaryDirectory() as temp:
            root = self._minimal_control_root(Path(temp))
            canonical = (root / STATE_PATH).read_bytes()
            for payload in payloads:
                report = self._write_report(root, payload)
                self.assertEqual(validate_root(root), [])
                self.assertEqual((root / STATE_PATH).read_bytes(), canonical)
                report.unlink()

    def test_31_baseline_PROJECT_STATE_contract_is_preserved(self):
        project = json.loads((ROOT / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        for key in (
            "schema_version",
            "package_version",
            "generated_at",
            "current_state",
            "recommended_paths",
            "final_goal",
            "decisions",
            "completed",
            "not_verified_on_target_machine",
            "first_codex_command",
            "first_stop_condition",
            "approvals",
        ):
            self.assertIn(key, project)
        self.assertEqual(project["package_version"], "3.0.0")
        self.assertEqual(project["current_state"], "READY_FOR_CODEX_PHASE_0_A_X0")
        self.assertEqual(project["decisions"]["xianyu_integration"], "REUSE_AS_SEPARATE_ADAPTER")

    def test_32_canonical_state_is_single_authority(self):
        project = json.loads((ROOT / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(self.registry["canonical_state"], STATE_PATH)
        self.assertEqual(project["control_plane"]["canonical_state"], STATE_PATH)
        self.assertEqual(project["control_plane"]["state_id"], self.state["state_id"])

    def test_33_compatibility_view_is_derived_from_authority(self):
        project = json.loads((ROOT / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        view = compatibility_view(self.state)
        self.assertEqual(project["current_state"], view["current_state"])
        self.assertEqual(
            project["decisions"]["xianyu_integration"], view["decisions"]["xianyu_integration"]
        )

    def test_34_compatibility_view_cannot_override_authority(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self._minimal_control_root(Path(temp))
            project = json.loads((root / "PROJECT_STATE.json").read_text(encoding="utf-8"))
            project["control_plane"]["phase_status"] = "READY"
            (root / "PROJECT_STATE.json").write_text(json.dumps(project), encoding="utf-8")
            self.assertTrue(any("PROJECT_STATE drift" in error for error in validate_root(root)))

    def test_35_old_S1_reader_returns_machine_readable_state(self):
        project = json.loads((ROOT / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertTrue(
            project.get("package_version") == "3.0.0"
            and bool(project.get("current_state"))
            and project.get("decisions", {}).get("xianyu_integration")
            == "REUSE_AS_SEPARATE_ADAPTER"
        )

    def test_36_compatibility_fields_have_stable_types(self):
        project = json.loads((ROOT / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertIsInstance(project["current_state"], str)
        self.assertIsInstance(project["decisions"], dict)
        self.assertIsInstance(project["decisions"]["xianyu_integration"], str)

    def test_37_compatibility_view_revision_matches_authority(self):
        project = json.loads((ROOT / "PROJECT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(project["control_plane"]["state_revision"], self.state["state_revision"])
        self.assertEqual(project["control_plane"]["stage"], self.state["stage"])
        self.assertEqual(project["control_plane"]["phase_status"], self.state["phase_status"])

    def test_38_reports_JSON_cannot_override_compatibility_view(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self._minimal_control_root(Path(temp))
            before = (root / "PROJECT_STATE.json").read_bytes()
            report = self._write_report(
                root,
                {
                    "current_state": "B Revision V2 APPLY",
                    "control_plane": {"phase_status": "APPLY"},
                },
            )
            self.assertEqual(validate_root(root), [])
            self.assertEqual((root / "PROJECT_STATE.json").read_bytes(), before)
            report.unlink()

    def test_39_invalid_compatibility_view_fails_validation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self._minimal_control_root(Path(temp))
            project = json.loads((root / "PROJECT_STATE.json").read_text(encoding="utf-8"))
            project["decisions"]["xianyu_integration"] = "FORGED"
            (root / "PROJECT_STATE.json").write_text(json.dumps(project), encoding="utf-8")
            self.assertTrue(any("compatibility decision" in error for error in validate_root(root)))

    def test_40_legacy_B_or_V2_state_remains_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self._minimal_control_root(Path(temp))
            project = json.loads((root / "PROJECT_STATE.json").read_text(encoding="utf-8"))
            project["current_state"] = "B Revision V2 APPLY"
            (root / "PROJECT_STATE.json").write_text(json.dumps(project), encoding="utf-8")
            self.assertTrue(any("compatibility view" in error for error in validate_root(root)))

    def test_41_missing_compatibility_field_fails_validation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self._minimal_control_root(Path(temp))
            project = json.loads((root / "PROJECT_STATE.json").read_text(encoding="utf-8"))
            del project["current_state"]
            (root / "PROJECT_STATE.json").write_text(json.dumps(project), encoding="utf-8")
            self.assertTrue(any("compatibility view" in error for error in validate_root(root)))

    def test_42_reports_do_not_mutate_canonical_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self._minimal_control_root(Path(temp))
            before = (root / STATE_PATH).read_bytes()
            report = self._write_report(
                root, {"stage": "S2A1", "phase_status": "CLOSED", "state_revision": 999}
            )
            self.assertEqual(validate_root(root), [])
            self.assertEqual((root / STATE_PATH).read_bytes(), before)
            report.unlink()

    def _fixture(self, temp, relative, content, expected):
        fixture = temp / "root"
        shutil.copytree(ROOT, fixture)
        (fixture / relative).write_text(content, encoding="utf-8")
        self.assertTrue(any(expected in error for error in validate_root(fixture)))

    def _minimal_control_root(self, temp):
        root = temp / "root"
        for relative in (
            "CODEX_START_PROMPT.txt",
            "PROJECT_STATE.json",
            "STATUS.md",
            "config/control-plane-registry.json",
            "config/control-plane-state.json",
            "scripts/control_plane.py",
            "scripts/validate-control-plane.py",
        ):
            source = ROOT / relative
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        return root

    def _is_reparse_point(self, path):
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
        return path.is_symlink() or bool(attributes & 0x400)

    def _write_report(self, root, payload):
        reports = root / "reports"
        if reports.exists() or reports.is_symlink():
            if self._is_reparse_point(reports) or not reports.is_dir():
                raise AssertionError("unsafe reports fixture")
        else:
            reports.mkdir(parents=True)
        report = reports / ("s2a1-non-authoritative-" + uuid.uuid4().hex + ".json")
        report.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
        return report


if __name__ == "__main__":
    unittest.main(verbosity=2)
