# 当前落地计划（2026-08-01）

## ROADMAP-DOC-20260801：落地总路线

- [x] 锁定当前事实：总体准备度约 35%、控制面 `S1/CLOSED/1`、两个 blocker、Alpha ZIP 12/13 源码一致。
- [x] 创建 Obsidian `05-项目落地总路线与分层验收计划.md`。
- [x] 完成长期/短期、8 个阶段、子阶段、15 个原子任务和逐级验证门。
- [x] 使用无历史上下文读者进行三轮可执行性与门禁边界审查；最终结果 `PASS`。
- [x] 修订后同步 Obsidian 导航、当前进度和任务台账。

### ROADMAP-DOC-20260801 Review

- 结果：`DONE`。
- 文档：`E:\AI_Tools\Obsidian\Data\notes-personal\codex_memory\03-项目记忆\jovi-automation\05-项目落地总路线与分层验收计划.md`。
- SHA-256：`8a1b727197fe45741ed07851cb5fb0c0f18fd47c410b2d2ed00318c50bee9843`。
- 自动校验：8 个阶段权重合计 100；检查点合计 100；15 个 S1 原子动作齐全；10 个正式清单失配路径齐全。
- 独立审阅：第三轮 `PASS`。
- `S1.1.1`：`DONE`。报告 `reports/remediation/S1_CONTROLLED_ENTRY_CURRENT_DRIFT_INVENTORY_V1.json`，SHA-256 `665ebafc42a4241c917902ebd1acf1c329ed7a858c855716fde8fcd678bb46c7`；21 条清单记录、10/10 `MISMATCH`、两项负向验证均 `FAIL_CLOSED`，报告/受保护输入复核 `PASS`。下一项为 `S1.1.2`，未开始。
- `S1.1.2`：`DONE`。报告 `reports/remediation/S1_CONTROLLED_ENTRY_HOOK_BINDING_INVENTORY_V1.json`，SHA-256 `b4f2aa7c9b3bb494bb2ee138db167d2f13277a97305e6c5301edcec2b4da0d69`；启动链 3/3、正式清单与控制面不变、2/2 负向 `FAIL_CLOSED`、发布后复核均 `PASS`。下一项为 `S1.1.3`，未开始。
- `S1.1.3`：`DONE`。报告 `reports/remediation/S1_CONTROLLED_ENTRY_DRIFT_CLASSIFICATION_V1.json`，SHA-256 `ae94e971e40d1a25bcb15f551d63d0e3f4b8a98f97710ba2dc63b4243eef273a`；10/10 与 S1.1.1 冻结字节一致，分类为 0 项 `EXPECTED_CHANGE`、5 项 `STALE_MANIFEST_CANDIDATE`、5 项 `UNKNOWN_UNPROVEN`，两项负向验证均通过且清单/控制面未变。此结论不接受漂移、不授权清单更新、Hook 信任、恢复或 APPLY；下一项为 `S1.2.1`，未开始。
- `S1-EXECUTION-20260801`：`BLOCKED_WITH_EVIDENCE`。Jovi 已要求连续完成 S1；`S1.2.1` 已证明本地没有任一正式期望 Hash 的直接字节来源，因此未创建 Shadow 候选或真实树写入。恢复必须先取得原始交付归档/逐路径字节，或取得逐项当前 Hash 与正式清单动作的独立精确决定；长期授权不替代 S1.4 的精确 Hash 审阅/决定契约。
- `S1-PROGRESS-REVIEW-20260804`：`DONE`。已生成审核包 `reports/remediation/review-packages/S1_PROGRESS_REVIEW_20260804/`，并发布 `E:\Claude_allow\Download\jovi-automation-s1-progress-review-20260804.zip`（SHA-256 `8595c53f18462d192e5e3923087ae0ed59e72104f7186d4ee4e9f98ce6dad0f0`）；6 个成员、证据 Hash 和 JSON 均复核通过。未改源码、Hook、正式清单、控制面、审批或闲鱼工程。

## 总体完成度

- 端到端商业落地准备度：约 `35%`；这是按交付阶段加权的计划指标，不是验收通过率。
- 已可验证：Modbus 主机侧 Alpha 12/12、CLI 示例、现有 Alpha ZIP 哈希；QH1 两目标的真实物化及其 30/30、20/20、24/24、34/34、42/42、21/21、9/9 回归。
- 尚不可宣称：目标机 Phase 0/A/X0、Track P 可发布产品包、Track I 部署/恢复、真实平台或付费验证。

## 每任务双账本规则

- [x] 每个非平凡任务开始时，在本文件创建可检查项，并在 Obsidian `jovi-automation/03-任务台账.md` 创建或更新对应条目。
- [x] 每个阶段性证据产生后，更新本文件的状态/证据路径和 Obsidian 条目。
- [x] 每个任务结束时，更新 `STATUS.md`、本文件、Obsidian `02-当前进度.md`；有用户纠正或可复用教训时再更新 `tasks/lessons.md`。

## 当前可执行计划

- [x] D0：核验 Modbus Alpha ZIP 哈希、运行 12/12 主机单元测试和 FC03 CLI 示例。
- [x] D1：核验当前 Alpha ZIP 与现有源码；发现 `parser.py` 归档/源码不一致（12/13 匹配），不得作为发布包。
- [x] D2：完成最小“受控入口恢复”候选的 S1.1 事实层：`S1.1.1` 当前差异清单、`S1.1.2` 启动链 Hash 锁定、`S1.1.3` 漂移分类均已完成；当前没有接受漂移、修改控制面或扩大权限。下一项为 `S1.2.1`，未开始。
- [x] D2.1：完成 S1.2.1 最小目标映射与本地源检索，结果 `FAIL_CLOSED`；报告 `reports/remediation/S1_CONTROLLED_ENTRY_RECOVERY_TARGET_MAP_V1.json`（SHA-256 `1c960180…78a0`）证明 10/10 缺少正式期望字节，允许写入路径为 0，真实树零写入。
- [ ] D2.2：被 S1.2.1 阻止；没有可验证候选时不得创建 Shadow、回滚包或运行候选测试。
- [ ] D2.3：被 S1.2.1 阻止；精确 Hook 审阅和 Hash 决定必须针对实际候选。
- [ ] D2.4：被 S1.2.1 阻止；不得在无可验证候选和精确决定时恢复受控入口。
- [ ] D3：Jovi 审阅精确 Hook 及恢复候选哈希；独立审核通过后，恢复受控入口。
- [ ] D4：运行统一 Phase 0/A/X0 只读审计，生成并核验 `reports/gates/GATE_A_PLAN.json`，在首轮停止点报告。
- [ ] D5：取得独立 `GATE_A.P` 批准后，在隔离副本重建 Modbus Alpha ZIP、SBOM、许可证和测试证据，完成本地用户试用包。
- [ ] D6：基于真实用户反馈完成 5 次访谈和付费验证；真实平台行为始终由 Jovi 手工控制。
- [ ] D7：仅在出现重复工作且取得独立 `GATE_A.I` 批准后，执行 Docker/n8n/PostgreSQL 的本地回环、备份和恢复验证。

# 历史 Batch B 交接计划

- [x] Read `AGENTS.md` and the minimum project handoff documents.
- [x] Read the latest relevant turns from Codex task `019f559c-f053-7150-853a-dbf5c6a04a1d`.
- [x] Search the configured Obsidian vaults for this project record.
- [x] Verify the current Batch B Revision V2 artifacts and real-workspace baseline hashes.
- [ ] Obtain Jovi's explicit approval for `B Revision V2 APPLY`.
- [ ] After approval, apply only the approved V2 patch to:
  - `scripts/common.ps1`
  - `scripts/new-review-item.ps1`
  - `tests/powershell/test_b_common_and_review_item.ps1`
- [ ] Run the approved 21-test verification, verify exact post-apply hashes, record the apply result, and stop.

## Review

## Medusa synthetic closure remediation R2 (2026-08-31)

- [x] R2-1: verify isolated source/runtime baseline, image digests, and container network boundaries.
- [x] R2-2: fix the Medusa 2.19 production Admin build path and prove backend/Admin health on loopback.
- [x] R2-3: run R2 unit and database integration tests, including strategy rejection and transaction rollback behavior.
- [x] R2-4: run synthetic X2 replay, 10-way concurrency, negative payment/asset/evidence cases, and database cardinality checks.
- [x] R2-5: add deterministic staging/package evidence and crash/recovery checks without public failure controls.
- [x] R2-6: generate complete R2 source/environment/test/oracle/license/SBOM evidence and SHA sidecars.
- [x] R2-7: update project docs, Obsidian checkpoints, and lessons; freeze an independent-audit package without issuing a PASS.

### R2 review

- Scope: isolated synthetic X2 only; no manual payment, real providers, Storefront, Xianyu, production, Git baseline, remote, or root import.
- Evidence: `workspace/review-queue/commerce-v1/medusa-v2-spike-remediation-r2/`, package manifest SHA `da31915c0fa11935ff262593ad06c926af927a6d4c23f73ecb65c95dd64145e3`, 103 members.
- Verified: source/fixture snapshot, fixed Node/Medusa container, loopback health/Admin shell, unit 12/12, integration 5/5, X2 replay, 10-way concurrency, negative 6/6, oracle manifest/file SHA 7/7, CycloneDX SBOM. The first independent audit then returned `MEDUSA_SPIKE_FAIL`; these are candidate results, not adoption proof.
- Remaining independent-review items: four Admin license Unknowns, process-kill windows beyond the DB transaction adapter, interactive browser smoke, and final PASS/PASS_WITH_GAPS/FAIL decision.
- Required final state: `SYNTHETIC_REPAIR_VERIFIED_PENDING_AUDIT`; production integration remains false.

### R2 independent audit R1 follow-up

- [x] Recorded the immutable R2 audit failure and preserved the original 103-member package.
- [x] Close workflow-only capability and service-side Medusa revalidation in a new isolated revision.
- [x] Bind runtime image/build/lock/source evidence and close all four Admin license Unknowns.
- [x] Add process-level kill/restart recovery evidence; interactive Admin browser smoke remains a documented low gap.
- [x] Re-freeze and obtain a new independent read-only audit; result is `MEDUSA_SPIKE_PASS_WITH_GAPS`, not an adoption PASS.

### R2-R1 candidate rerun (2026-09-01)

- [x] Rebuilt the isolated source with workflow capability, service-side Medusa revalidation, order-level lock and 120-second recovery wait.
- [x] Added SIGKILL-after-receipt, Backend restart and replay evidence; closed image ID/manifest/source-tree/lock binding and four Admin tarball/integrity/SBOM records.
- [x] Frozen package `workspace/review-queue/commerce-v1/medusa-v2-spike-remediation-r2-r1/`, SHA `748ec4bcc2eb7061b2280ef367e43fcc0458bb21ff46583aacf882e1cd90a4c6`, 117 members; source tree SHA `d15eb73e94a1fcf8b19ac2c8e03b317fa5ea94f7d8242548aa3eac4dec334e8d`.
- [x] Obtained second independent read-only audit; result `MEDUSA_SPIKE_PASS_WITH_GAPS` recorded in `docs/commerce/MEDUSA_R2_INDEPENDENT_AUDIT_R2_RESULT.md`. Remaining gates are Jest natural shutdown and interactive Admin smoke; `production_integration_allowed=false`.

## QH1 V1 Independent Audit Recovery

- [x] Reproduce the V1 Hook fixture writes in an owned TEMP Shadow.
- [x] Prove exact Shadow-only restoration of the two expected H0 fixture outputs.
- [x] Verify preexisting `__pycache__` entries are not new V1/V2 drift.
- [x] Record a hash-bound V2 recovery contract.
- [x] Run the V2 independent audit under the recovery contract.
- [x] Verify the V2 package and prepare the next human-only real-APPLY plan.
- [x] Apply the two hash-bound targets after Jovi's explicit authorization.
- [x] Verify exact target hashes, the 20-file baseline, and approved non-writing regressions.
- [x] Record the real APPLY result and rollback condition.

- Current state: `B_REVISION_V2_PREPARE` is complete; the V2 candidate is not applied to the real workspace.
- Approved candidate requested: `reports/remediation/B_REVISION_V2_PROPOSED_PATCH.diff`.
- Candidate SHA-256: `cf3064ad4883786c2651c38a13c6b8a0d26ccff699b27f6abd5577f136d02863`.
- Real baseline remains unchanged:
  - `scripts/common.ps1`: `aa1b93b40fbfa63465a263445b9e7a1db0ce0853249eac13891c9186da2d5c59`
  - `scripts/new-review-item.ps1`: `1ecc57a537fa31959de085ad1fc305aca5b5fed3cd29d34b1a82c8466584c9f2`
  - `tests/powershell/test_b_common_and_review_item.ps1`: absent

## S2A2 Current Execution (v4/v5 Fix + Dual-Shadow)

- [x] Read AGENTS and core context docs; confirm prior state and approval constraints.
- [x] Reconstruct S2A2 delta with hash-bound apply harness (v3→v5 fixes).
- [x] Fix harness insertion defects:
  - marker-aware insertion after `root = Path(args.root).resolve()` in `update_status`
  - proper `\n` escaping in test `COMMAND` payloads
  - `tests/test_s2a2_enforcement.py` newline quoting stability
- [x] Run dual-shadow application on two fresh copies of current baseline.
- [x] Verify target set and A/B hash equality for 8 S2A2 targets.
- [x] Run `tests/test_s2a2_enforcement` in Shadow A (10/10 pass).
- [x] Run `python scripts/run-static-tests.py` in both shadows (static smoke PASS for enforcement controls; expected framework manifest mismatches only due unchanged manifests).
- [x] Apply hash-locked S2A2 patch to real repository.
- [x] Re-run S2A2 gate checks on real tree and write completion evidence.

## S2A2 Review Notes

- S2A2 blocker resolved: harness defects corrected, dual-shadow hash equality verified, explicit real-tree apply completed.
- Real-tree validation status: completed and passing (`tests.test_s2a2_enforcement` 10/0, `tests.hooks.test_pre_tool_guard` 9/0, `tests.test_s2a1_control_plane` 42/0).
- Stop condition reached: explicit approval accepted, real-tree patched, validation evidence written.

## Commerce V1 execution (2026-08-09)

- [x] Task 0: lock the mainline to Commerce Core; keep OpenClaw and Modbus as separate projects/products; keep Hook `DO_NOT_TRUST` and all real-platform actions false.
- [x] Task 1 pre-gate: create review-queue-only architecture, Decision V2 review summary, ten strict schemas and synthetic positive/negative fixtures.
- [x] Candidate validation: 17 JSON files parse, 10 schemas enforce `additionalProperties:false`, 20-file candidate manifest verifies, expected negative-fixture scan recorded.
- [ ] Gate A.P: absent; no Commerce runtime code, formal Commerce paths, `products/` writes or human-only scripts may run.
- [ ] Tasks 2-11: blocked until independent governance review passes and Jovi provides the exact Gate A.P receipt.

## Commerce review

- State: `COMMERCE_SPEC_CANDIDATE` / `BLOCKED_BEFORE_GATE_A_P`.
- Evidence: `workspace/review-queue/commerce-v1/`.
- Next action: Jovi/independent reviewer decides whether to advance governance; after a valid Gate A.P receipt, continue Task 2 with controlled Git baseline.

## Commerce V1 governance-to-X2 execution (authorized G1)

- [x] G0: verify exact Plan/Target Set authorization and create review-queue-only execution package.
- [x] G1.1: add Commerce path fail-closed guard and known `commerce-development` / `commerce-test` action labels.
- [x] G1.2: add the only bound `S1/CLOSED → C/APPLY` transition and fixture-tested four-file mirror synchronization.
- [x] G1.3: add fail-closed Commerce readiness validator and outer review-package manifest verification.
- [x] G1.4: correct the read-only entry and master prompt to Commerce mainline; preserve Hook DNT and no external Xianyu access.
- [x] G1.5: initial focused governance regression; historical result `116/116 PASS` (preserved for audit traceability).
- [x] G1.6: generate protected-tree-after snapshot, target-set after report and immutable G1 evidence sidecars.
- [x] G1.7: final governance regression; `118/118 PASS`; formal `tests/commerce` discovery remains `NOT_APPLICABLE_GATED_BEFORE_FORMAL_COMMERCE_TESTS`.
- [x] G1 V2 evidence correction: authoritative final result is `workspace/review-queue/commerce-v1/audit-remediation-v2/GOVERNANCE_TEST_RESULTS_V2.json`; its `passed/collected` fields are the only final count authority.
- [x] G1 V2 human-only cycle: old G1 history remains `NOT_VERIFIED`; new before/after evidence is required to prove only the V2 cycle.
- [ ] G3 independent Pre-Apply Audit: not started; Decision V3 remains candidate-only.
- [x] G3 attempt 1: `FAIL` — three mutable mirror SHA/byte records in `FINAL_CONTROL_TARGET_SET_V2.json` were stale; no Decision or Gate action was taken.
- [x] G3 RERUN1: regenerated human-only cycle, current-cycle pointer, V3/Controlled Baseline candidates and V4 package from one final tree.
- [ ] G3 attempt 2: pending a new independent Agent review.

### G1 review

- Current authority remains `config/control-plane-state.json` at `S1/CLOSED/1` with `HOOK_UNTRUSTED` and `FORMAL_MANIFEST_MISMATCH`.
- Readiness is `NOT_READY`; no Gate A plan, Decision V3, Manifest APPLY, Approval, product code or Git baseline was created. G1 stops for an independent pre-audit.

### Commerce D4 V7/V8 execution (2026-08-13)

- [x] Human Jovi Decision V7 issued: formal SHA `a7bafcdf4c3f26848338f8abd1c5773edbe18c4b8b447613b6acfb4d8a194204`.
- [x] V7 canonical-mirror preservation check passed with zero target writes; old mirror remains immutable.
- [x] V7 structural `--check` stopped fail-closed because the candidate exact diff declares `modified=7` while the V7 tool required `modified=2`; no formal bytes or receipt were written.
- [x] V8 candidate-only correction created under `workspace/review-queue/commerce-v1/d4-tool-remediation-v1/superseding-decision/v8-corrected/`; structural executor now requires the actual `0/19/7/40` diff shape and candidate-only synthetic `--check` passes for 13 targets.
- [x] V8 package self-verification: 122/122 package members and sidecars match; 10 candidate tests pass; PowerShell parser passes; V7 formal remains unchanged and V8 formal is absent.
- [x] Fresh independent V8 review: Luna-max performed an elevated read-only verification of the ACL-protected old canonical mirror and issued `PASS_READY_FOR_JOVI_DECISION_V8`; report SHA `c60738ed1aa8534607d85e5e8211d822b3109a81c1b475399bc9c84df3e673ca`.
- [ ] Human Decision V8: ready for Jovi issuance but not issued; formal V8 and sidecar remain absent.
- [ ] Structural V8 APPLY, Post-Apply Audit, Gate A.P, C/APPLY: not started.

### Commerce Governance Closure V9 execution (2026-08-13)

- [x] V9 execution plan saved: `tasks/plans/2026-08-13-commerce-governance-closure-v9.md`; plan SHA `27a237a0dcef4a7fe829b3c537ef1f38cc1bf250f1afb40e1d9e97e42ee7bfb3`.
- [x] Feasibility review completed: V8 cannot safely feed Post-Apply/closeout/Gate because its downstream tools are V3-era or unbound; V9 downstream-chain candidate is required.
- [ ] Task 0: V9 preflight and frozen inputs. Candidate inputs are frozen, but fresh read-only evidence for ACL-protected 14 transaction bytes and the 52-file canonical mirror is still required.
- [x] Task 1-2: V9 candidate tools, target set, Decision proposal, review package and manifest. PowerShell 5.1 StrictMode remediation frozen candidate SHA `ae6433a27fb5d372615fe1d0fd7537eef7dff4476e05c5f7a69c5bffcdd379f5`; package SHA `faa273896357d62fca1e28da88f05332eec6d94927a78ba3593bb76aa014483c`; 112/112 package members and bundled Python 3.12 tests 38/38 independently rechecked.
- [x] Task 3: fresh independent V9 pre-apply audit. Jovi-run E001 report SHA `2fb228f22b6c78d58882f26df052a2d8247ff750347fe8d1da663f31d570d396` and fresh Luna R2 `PASS_READY_FOR_JOVI_DECISION_V9` report SHA `e697c16ab143e27d95da1f15ef8f94bc4a911e857b37d196d0af76386c1a4caa` are sidecarred and independently rechecked; historical top-level FAIL remains preserved.
- [x] Task 4: Jovi-only Decision V9 issuance. Jovi issued formal V9 SHA `af24e7ce181d5f5520be4570351e3cfe243b07562625d80928a79c684122c1bb`; body/sidecar, source candidate, R2 audit and false policies were rechecked.
- [x] Task 5 check: Structural V9 `--check` returned 14 targets / 0 writes. The one V9 `--apply` attempt failed on a receipt-schema defect after temporary writes; automatic rollback completed and independent failure audit confirmed all 14/14 targets are restored to frozen before bytes, no structural receipt exists, and the V9 failure journal/backups are preserved.
- [x] V9 Tasks 5-9 are superseded by V10: do not retry or mutate signed V9. V10 plan SHA `dd09c58a9e6c7d60dff89ea425f3a053cadac4d04b5620f0f137d4387cec5e78` was built, independently pre-audited and Jovi-issued.
- [x] V10 Structural APPLY: `--check` passed (14 / 0 writes), then one bounded apply published a valid 14-row receipt and `APPLIED` journal. Independent Post-Apply audit SHA `96bb6de09aa80d676591373d4755305c1ab76f3128dfde6a477cd82b3ee5a25e` fail-closed on the installed S2A1/security-semantics contract mismatch.
- [x] V10 rollback: signed V10 rollback returned 14 targets to before bytes. Independent rollback audit SHA `5e49017a898989f0bfd15bb88d7c3eb32760a466c0103d33d22bb0a64657f682` is `PASS_ROLLBACK_RESTORED_BEFORE_STATE`; it is not a governance PASS.
- [x] V11 candidate R1 was independently pre-audited and fail-closed: report `workspace/review-queue/commerce-v1/governance-closure-v11/preapply-evidence/V11_INDEPENDENT_PREAPPLY_AUDIT.json` SHA `ad766bacaac95e0b8a4aec1d0b6b0bed8b3aa19e798ab8025bc2cccd6099dbfe` found that its frozen source package manifest was incorrectly rejected by the staged-root helper. No V11 Decision or real-root apply occurred; R1 cannot be signed.
- [x] V11 candidate R3 frozen after repairing the frozen-package stage helper: candidate SHA `70cff920259cc8c6ece5e1c201e17eb93749038d5f2316fc2eeb755f54e0745d`, package SHA `e4868b30911731ef2c4f7b1673e7b67a653395888733747cc110ae8edf638a80`, 354 manifested entries. Post-freeze suite `9/9 PASS` includes copied frozen-source validation, actual disposable V11 APPLY, seven installed contracts, and `SECURITY_SEMANTICS_PASS` 20/20. R1 FAIL and invalidated R2 manifest are retained as candidate history; no formal V11 or real-root apply occurred.
- [x] V11 R3 fresh independent pre-apply audit: `PASS_READY_FOR_JOVI_DECISION_V11`; report `workspace/review-queue/commerce-v1/governance-closure-v11/preapply-evidence/V11_INDEPENDENT_PREAPPLY_AUDIT.json` SHA `c34a3b46d7ce131f55cbc57ef24482f80438fb45d31776e8e209cb6e5e025741`. It independently verified package 354/354, sidecars 177/177, 13/13 restored before bytes, Framework 40/40, canonical mirror 52/52, and frozen-source actual staged APPLY plus seven installed contracts 9/9.
- [x] V11 Decision issued by Jovi: formal SHA `c0dd781bdd8801680dcb6fe6afca41629a01b82f770ca637b34460b72ddd816f`; the first bounded `--check` stopped fail-closed with `missing or malformed SHA-256: V11 executor self binding`. Receipt child was absent and no target bytes changed. V11 is now immutable historical state and must not be edited or retried.
- [ ] V12 superseding candidate: add the missing formal executor/runtime self-bindings, re-freeze, obtain a fresh independent pre-apply audit, then Jovi Decision V12 before any structural APPLY. V11 formal/check failure is mandatory history; no V12 formal exists yet. Plan: `tasks/plans/2026-08-14-commerce-governance-closure-v12-self-binding.md` (SHA `fa309c038b456f6345934fd268322ffcb166bd7fc266641a8eda5222aec407c5`).
- [x] V12 R1 candidate implementation and pre-freeze suite: 8/8 passed, including isolated check/apply and seven installed contracts; frozen package was then rejected by its own post-freeze staging helper, so no V12 Decision or apply was performed.
- [x] V12 R2 candidate revision: preserved R1, re-ran 9/9 pre-freeze tests, compileall and PS parser, and froze 1202/1202 package entries. Post-freeze full suite stopped fail-closed on the same helper path still invoking `--prepare`; no formal V12 or receipt was created.
- [x] V12 R3 candidate revision: preserved R1/R2 immutable, repaired the complete frozen-source fixture and safe-copy path, ran prefreeze 9/9 and postfreeze 9/9, compileall 564 and PS parser 28/28, then froze once. Candidate `6f11c504...63de`, package `59dac10a...2c7e8`, 2412 entries, 29 bindings, 13 targets and Framework 40/40; no formal V12 or receipt.
- [x] V12 R3 fresh independent pre-apply audit: new Luna reviewer report `preapply-evidence/V12_INDEPENDENT_PREAPPLY_AUDIT.json` SHA `e5d295aa2f38b4213e1646104c821a84adb80476ee1bd741b942c3a39eeac0b2`, verdict `PASS_READY_FOR_JOVI_DECISION_V12`; 2412/2412 manifest, 29 bindings, 13 before, Framework 40/40, 9 tests exit 0/OK.
- [ ] V12 human issuance: all exact parameters are now rehashed and formal V12 is absent; waiting for Jovi to run `Issue-DecisionV12.ps1` with confirmation `ISSUE DECISION V12 6f11c504dac1`.

### Commerce V12 Post-Apply → S1 Closeout execution (2026-08-15)

- [x] Verify formal V12 issuance, successful V12 structural receipt/journal, Framework 40/40, and independent V12 Post-Apply `PASS`.
- [x] Reconcile repository truth with the Obsidian Commerce mainline and Phase2B route; current authoritative state remains `S1/CLOSED/1` with the two historical blockers pending closeout.
- [x] Check downstream authority compatibility: formal V12 binds only the structural executor/runtime; the reviewed V9 closeout/Gate/import/transition tools require formal V9 and V9 receipts and therefore cannot be reused for V12.
- [x] Build and freeze the V12-bound downstream closeout candidate as V13 under `workspace/review-queue/commerce-v1/governance-closeout-v13/`; no human-only, Approval, Gate, import, C/APPLY, or real-platform action was run.
- [x] Run TDD RED→GREEN, candidate package rehash, isolated structural/closeout/Gate→C/APPLY tests, Python AST/compile checks and PowerShell 5.1 parser checks.
- [x] Stop at the exact Jovi issuance boundary: V13 candidate is ready, but formal V13 issuance remains a Jovi-only action; no V13 closeout/APPLY has been run.

#### V12 Post-Apply → S1 Closeout review

- Status: `READY_FOR_JOVI_V13_ISSUANCE`.
- Current evidence: `reports/remediation/COMMERCE_V1_POST_APPLY_AUDIT.json` (`PASS`, independent, V12-bound).
- V13 candidate evidence: candidate SHA `9a32bf22a72fb0fa3d3bd808174e8e3732b9529a0fdaa5e542bf89eeafe5dc85`; package SHA `b8a6984e1d999e0deaf19639e63f2780e091edce2f093c2d6628ee52ddd501f8`; 74/74 manifest entries, 26 bindings, 8 structural transaction targets, closeout 3/3, Framework 40/40, isolated tests 8/8.
- Current verification: root regression matrix passed Gate readiness 3/3, transition 2/2, S1 2/2, S2A1 43/43, S2A2 2/2, PreToolGuard 10/10, and security semantics 20/20.
- Safety boundary: no `scripts/human-only/`, no `workspace/approvals/` write, no external Xianyu access, no Commerce import, no Git initialization, no real platform action. V13 audit was explicitly waived by Jovi in the candidate contract; this is not an independent audit PASS.

### Commerce V13 downstream governance closeout candidate (2026-08-22)

- [x] Reconcile current V12 formal/Post-Apply state with the Obsidian Commerce mainline; V12 is structurally complete but cannot authorize V12-bound closeout/Gate because those tools were not bound into the V12 Decision.
- [x] Build a V12-bound V13 candidate that rebinds the three root Commerce facades/tests, Framework manifest, S1 closeout, import-scope, Gate plan/verification, chain verifier and C/APPLY transition with journal/backup/rollback/recover contracts.
- [x] Freeze candidate and package with self-exclusion rules; rehash 74/74 entries and all body/sidecars; verify 26 Decision bindings, 8 structural targets, 3 closeout targets, Framework 40/40 and exact diff 0 added/7 modified/0 removed.
- [x] Run candidate TDD RED→GREEN and frozen 9/9 contract tests, including Windows inventory separator normalization, structural apply/rollback, closeout rollback, synthetic Gate→C/APPLY, external Xianyu rejection, path attacks, strict Jovi Approval negative, and `SECURITY_SEMANTICS_PASS` 20/20.
- [x] Re-run root regression matrix and formal-boundary checks; formal V13, V13 receipts, Gate plan, Approval and Commerce import remain absent.
- [x] V13-R1 issuance attempt was preserved as fail-closed history: Windows PowerShell compared backslash inventory paths against forward-slash Manifest entries and wrote no formal bytes. V13-R2 normalized actual inventory separators, added a focused regression test, re-froze the candidate, and isolated-verified the real issuer path.
- [x] Jovi issued V13 formal SHA `cc277ffb4b9891785c00234adf4449fb65cb9e52e764474e075fb51876dddd7b`; the V13 Structural APPLY was rolled back after the installed-facade regression, so V13 closeout/Gate/import/C-APPLY remain unexecuted.
- [x] V13 was issued by Jovi and passed structural `--check`; one controlled APPLY wrote 8 targets but the installed Gate facade contract failed because `runpy` could not import sibling V13 modules. The signed V13 rollback restored all 8 before bytes; no V13 closeout, Gate, import, or C/APPLY occurred.
- [ ] V14 superseding candidate: add installed-facade sibling-import coverage, bind the corrected wrappers and formal V13 rollback history, re-freeze, and obtain a new Jovi Decision before retrying structural APPLY.

#### V13 issuance inputs

- Candidate: `8121b6eba0ed158c8799bf84f22013fd57f2bd84c8a1bda7eb858f5639f1a851`
- Package: `77ced60124c51068082e426d398c260a47c0e65f4714ebc3b0606a0f37927a67`
- Review package: `90f1b3f8fd106733440408ad1188746fbe61653111c1624212953987be71a023`
- Implementation report: `dd7086439d21a2a40e902c1cacdd7a975559ca2b66315985dd5042bb6d173524`
- Issue script: `aad1600ebf6142af1b9bd2d92349efad89328d0065e6570c2c2763974a2859ef`
- Formal V12: `a8f48a4ff19dcb975bfe95c3a0b982f190196aad140c9554fcfa8e5636724bf3`
- V12 candidate: `6f11c504dac12ed8e3e8be11c25a0209aead93bde7b1744e32389d30364d63de`
- V12 package: `59dac10a513aeb8dbc7b2d5c21624af287eda2b3364c2214a41096be5732c7e8`
- V12 pre-apply audit: `e5d295aa2f38b4213e1646104c821a84adb80476ee1bd741b942c3a39eeac0b2`
- V12 structural receipt: `e11d43d95e9d1617d2bb71e3d58f5d2dda814ae2a0ded5a2369a74378218b2bc`
- V12 Post-Apply audit: `79251f296b5330d28d5ecf85283bcee5385839984544c9ad53a1457716512c2c`
- Confirmation: `ISSUE DECISION V13 8121b6eba0ed`

Current governance stop state: `V10_ROLLED_BACK_INSTALLED_CONTRACT_REGRESSION`; formal V7/V9/V10 remain immutable historical decisions; V11 formal, Gate, Commerce import and main-project X2 are absent. Approval directory may exist, but `GATE_A.P.approval.json` is absent.

### Commerce V14 superseding facade-import remediation candidate (2026-08-22)

- [x] Preserve V13 formal, failed structural receipt and signed rollback evidence; verify all 8 target bytes are back to V13 before state.
- [x] Build V14 from an untouched V13 copy, add `sys.path` binding before every installed facade `runpy` call, and add a real-root-shaped three-facade integration test.
- [x] Freeze and verify V14: Manifest `82/82`, candidate tests `10/10`, AST `20/20`, PowerShell 5.1 parser PASS, isolated V14 issuer PASS.
- [x] Jovi issued formal V14 `0cca20f7d5eec1be88bf30938bc769617a765988f68ef2658d67df7130583a95`; no V13 retry, Gate, Approval, import, Git, or real-platform action was run.
- [x] Ran V14 structural `--check` (`7` structural + `1` Framework target, `0` writes) and signed `--apply` (`8` writes); receipt `33dcdb034ef3104406f283bd79d131d40b6a4e925ce96f4a20cd3e4b38429ab5` self-verified 8/8 after bytes and Framework 40/40.
- [x] Ran root regression matrix: Gate 2/2, Transition 1/1, S1 2/2, S2A1 43/43, S2A2 2/2, PreToolGuard 10/10, Security Semantics 20/20; all exit 0.
- [x] Ran V14 S1 closeout `--check` (`3` targets, `0` writes) and signed `--apply` (`3` writes); receipt `786839b8b6069439899b560657c9226ddead8d81119ecc9f74a2e16a4dcb501b` self-verified; control plane is `s1-closed-v14-closeout`, revision 2, blockers empty.
- [x] Do not retry formal V13. Gate A.P, Gate Plan, Approval, import, Git initialization, main-project X2, C/APPLY, and real-platform actions remain outside this execution.

#### V14 issuance inputs

- Candidate: `ba6004838fa37e03a4ef7b5dc0b50ec32c996d98e403288d093ee61d1d500774`
- Package: `a9fc1983fa1b72d9d1e6f993d3d7e8f3279a187ba550cf08b058997762449490`
- Formal V13 history: `cc277ffb4b9891785c00234adf4449fb65cb9e52e764474e075fb51876dddd7b`
- V13 failed structural receipt: `00aec23b225ac97a0feb4158402b829fbedcf39dc88a79afe3ceaf09f38d9cb7`
- V13 rollback audit: `91f15fb08e8938f2b72791d1f6b74a4b8f9076b278556db29633dda2ae045580`
- Confirmation: `ISSUE DECISION V14 ba6004838fa3`
- Formal V14: `0cca20f7d5eec1be88bf30938bc769617a765988f68ef2658d67df7130583a95`
- Structural receipt: `workspace/review-queue/commerce-v1/governance-closeout-v14-execution-receipts/structural/run-20260822-0cca20f7/STRUCTURAL_REBIND_RECEIPT_V14.json`
- S1 closeout receipt: `workspace/review-queue/commerce-v1/governance-closeout-v14-execution-receipts/closeout/run-20260822-0cca20f7/S1_CLOSEOUT_RECEIPT_V14.json`

### V8 independent review evidence

- Package manifest: `72187123c43d2673914891ecb89f8310ddb83b64118c8ec7e66bed58b8191333`, 122/122 exact.
- Decision V8 candidate: `5121a89a95bbdf4fedd3f95716fa24f3cb5b92363b4b383337385e553f64bf63`, 38/38 bindings exact.
- Prior canonical mirror: 52/52 exact, zero missing/extra, no replacement or write.
- Candidate verification: 10/10 tests PASS; PowerShell parser errors 0; formal Decision V7 unchanged at `a7bafcdf4c3f26848338f8abd1c5773edbe18c4b8b447613b6acfb4d8a194204`.
- Stop state: `PASS_READY_FOR_JOVI_DECISION_V8`; no Decision V8 issuance, structural APPLY, Gate, Approval, control-plane transition, human-only execution, or external Xianyu access was performed.

### Commerce V15 Git-object import-scope correction (2026-08-22)

- [x] Preserve formal V14 and its structural/closeout receipts; no V14 bytes were edited or retried.
- [x] Reproduce the V14 import-scope defect: the V14 tool rejects legitimate record-only files instead of recording them as excluded rows, so no V14 import-scope receipt was created.
- [x] TDD RED→GREEN: V15 source classification now handles the complete external 93-file Git tree as 32 implementation + 17 test IMPORT rows, 10 evidence IMPORT rows, and 34 `RECORD_ONLY_EXCLUDE` rows with null targets; explicit mappings, forbidden path forms, and target collisions are fail-closed.
- [x] Implement V15 Git-object-only selector and strict Gate A/P scope validator under `workspace/review-queue/commerce-v1/governance-closeout-v15/`; no checkout bytes, network, Approval, import, Git initialization, or platform action was used.
- [x] Freeze V15 candidate package: candidate `f4c7167c87ed7d9f5fc8b30f8cf0010c7a7c66774040912146ddfa457462cad1`, package manifest `45de7cb8d148d5038be765b1959a00a73623661fc0c30c28cd4a6bd755a726c2`, 116 manifest entries; V15 tests 9/9 PASS including disposable-root CLI scope→Gate flow, Python compile PASS, PowerShell 5.1 parser PASS.
- [ ] Human-only V15 Decision issuance: formal V15 is absent; do not run the V15-bound selector or Gate generator until Jovi issues the candidate.
- [ ] After issuance: one V15 import-scope generation, one bound Gate A/P plan, Jovi-only Gate approval, strict receipt verification, then the next approved phase. Commerce import, main-root X2, real pilot, and remote configuration remain NOT_STARTED.

### Commerce V15 formal scope and Gate Plan execution (2026-08-22)

- [x] Jovi issued formal V15: `c6c7f61c784a0b23a9cecb542f09f754e1fee1cf7af6526315111af969eb1c1c`; V14 lineage and all V15 self-bindings rechecked.
- [x] Generated the only V15 Git-object scope at `workspace/review-queue/commerce-v1/governance-closeout-v15-execution-receipts/import-scope/run-20260822-v15/`: 93 source rows, 59 IMPORT, 34 `RECORD_ONLY_EXCLUDE`, ten body/sidecar members; index SHA `abb4bddc07a3240f8fb89623ee77320010ba0874eab231619ccc6e4e0eaed612`.
- [x] Generated bound Gate A/P plan `reports/gates/GATE_A_PLAN.json`; SHA `7db47094bb256223840cc3c685e22d7b7e240d8365ccc60841c5a6e4c6c16bb7`, sidecar and `.sha256.txt` match; status `AWAITING_HUMAN_APPROVAL`.
- [x] Self-verification passed: scope validator 93 rows, plan bindings, control-plane validator, no Approval, no `jovi_commerce`, no Git baseline, external Commerce HEAD `3b31f0f2f240038aa261db5c57c43e5e14992dc5` clean/no remote.
- [x] Jovi issued the human Gate A.P Approval at `workspace/approvals/GATE_A.P.approval.json`; body SHA `bf3628fb1b74505947d6004f4a6e017555260866e3ee0284d9ee8d5947b0e38e`, gate/track/plan binding is `GATE_A/P` → `GATE_A_PLAN.json` SHA `7db47094bb256223840cc3c685e22d7b7e240d8365ccc60841c5a6e4c6c16bb7`. Do not use V14 strict verifier/transition tools; V16 formal issuance remains a separate Jovi-only boundary.

### Commerce V16 strict Gate A.P and C/APPLY candidate (2026-08-22) — current correction

- [x] V15 formal issuance and the single Git-object scope/Gate Plan were verified; V15 remains the current signed authority.
- [x] Built V16-bound strict Gate A.P verifier. It requires the canonical V15 plan, exact Jovi/GATE_A/P body-only Approval, canonical V14 closeout, canonical V15 scope directory, all body/sidecar bindings, and formal V16 self-binding.
- [x] Built V16-bound journaled C/APPLY tool. Root control-plane validation is authoritative; the state binding remains the exact five-field schema binding, while detailed evidence is receipt-bound. The only target set is `config/control-plane-state.json`, `PROJECT_STATE.json`, `STATUS.md`.
- [x] TDD verification: 8/8 candidate tests pass. The disposable-root integration proves strict Gate verification, `--check` with 0 writes, exact three-target `--apply`, APPLIED journal/receipt, and signed-path `--rollback` byte restoration.
- [x] PowerShell 5.1 parser and Python 3.12 compile checks pass. V16 package freeze is complete: candidate SHA `d1b3ceb8ca6665234a71445d450d1237b02f68d573fd8db6206c80ac90fa2fef`, package SHA `6980204a45182bf6a441a437c6ac219442a11bafec490702a84a4df9226bff55`, 84 manifest entries.
- [x] Root safety checks: control-plane validator PASS; Gate readiness 2/2, transition facade 1/1, S1 2/2, S2A2 2/2, and PreToolGuard 10/10. The existing S2A1/security contract is not fully green after the V14 revision-2 closeout: `test_10_initial_predecessor_fails` expects a revision-1 fixture but loads the current revision-2 state, so S2A1 is 42/43 and `run-security-semantics.py` fail-closes. V16 candidate tests remain 8/8; no V16 tool changes root bytes.
- [x] Formal V16 issued and self-verified: `workspace/decisions/JOVI_S1_RESTART_DECISION_V16.json`, SHA `363654c5cc8552190e0f7f5c044695984efe1c553eafced0bc117ef298680ee7`.
- [x] Strict V16 Gate A/P verification passed: `reports/gates/GATE_A_P_VERIFICATION_V16.json`, SHA `c53639fca3fb90804b0b8a8d5330b5172591dddc5d665235c85f2a5c1a9808d6`, status `GATE_A_P_VERIFIED`; transition `--check` returned `READY_TO_APPLY`, 3 targets, 0 writes.
- [x] Executed the single V16 C/APPLY: receipt `workspace/review-queue/commerce-v1/governance-closeout-v16-execution-receipts/transition/run-20260822-v16-apply-001/CONTROL_PLANE_TRANSITION_RECEIPT_V16.json`, SHA `10cba4e6315debc891d7bd787c79e6f779238d10b8581d5c92a828aa42a3b485`; exactly 3 targets/3 writes; backup and journal `APPLIED`.
- [x] Post-apply self-verification passed: receipt bindings, target after hashes, control-plane mirror, Framework 40/40, MANIFEST/Hook/Prompt/human-only protection, no root Git HEAD/config, no Commerce import paths, and external Commerce repo unchanged.
- [x] Post-apply regression recorded: S1 2/2, S2A2 2/2, PreToolGuard 10/10, control-plane PASS; legacy S2A1 41/43 and Security Semantics 19/20 fail only on old baseline fixtures that hard-code pre-C/APPLY state/revision; frozen pre-apply V16 suite remains 8/8.
- [ ] Commerce import, Git initialization, main-root X2, real pilot, and remote configuration remain NOT_STARTED.

### Safe repository slimming and child-agent lifecycle cleanup (2026-08-22)

- [x] Read `AGENTS.md`, `README_FIRST.md`, `PROJECT_STATE.json`, retention/manifest policy, current task ledger and completion context before any deletion.
- [x] Baseline captured before cleanup: root `.git` was an empty uninitialized directory, formal V15 SHA remained `c6c7f61c…1c1c`, control plane was `S1/CLOSED/revision 2`, and no Gate A.P Approval or formal V16 existed at that time.
- [x] Removed 32 unreferenced, unmanifested, superseded remediation/nightly draft files (33,343 bytes). They were explicitly marked draft/non-authorizing, had no repository references, and were not decision/receipt records.
- [x] Removed 11 Python/pytest cache directories (about 402 KiB). They were fully regenerable and outside source/evidence contracts.
- [x] Retained all source, configuration, product assets, formal decisions, receipts, candidate packages, historical evidence, backups/data, route-B packages, and the empty `.git` marker because its intent cannot be proven safe to remove.
- [x] Child-agent inventory: only the primary `/root` agent exists; no stale child agent was present to close.
- [x] Post-cleanup verification at cleanup time: V16 candidate suite `8/8 PASS`, control-plane validator PASS, zero cache directories, zero suspicious report drafts, core documents and V16 candidate files present, V15 SHA unchanged, external Commerce HEAD unchanged/clean, Approval absent at that historical checkpoint. `STATUS.md`, `CHANGELOG.md`, and frozen Obsidian notes were intentionally not edited before C/APPLY.
- [x] After V16 C/APPLY, synchronized the current authoritative facts into Obsidian `02-当前进度.md`, `03-任务台账.md`, `06-自动售卖Commerce主线.md`, `08-COMMERCE-DECISION-TO-MAIN-X2-PHASE2B.md` and handoff note `09-COMMERCE-GOVERNANCE-CURRENT-V15-V16.md`; historical sections remain preserved.

### Commerce Import Phase2C D9 Git baseline candidate (2026-08-22) — current

- [x] Saved the evidence-first Phase2C plan and sidecar: `tasks/plans/2026-08-22-commerce-import-phase2c.md`, SHA `5512831902447b1cfcb3f0d43765ff13fd5029c09e76b9ae55e6feb2741c2bbd`.
- [x] Implemented V16-bound `prepare_git_baseline_v16.py` with atomic review-queue-only publication, formal V16/C-APPLY/policy/sidecar checks, protected-tree snapshot, secret scan, exclusion set, Windows casefold/NFC collision guard, NUL path list and no-Git/no-root-write contract.
- [x] TDD RED→GREEN: 9/9 candidate tests pass, including sidecar drift, `.gitignore` before drift, non-C/APPLY state, valid Git metadata, secret-like content, exclusion, NUL termination and path identity collision.
- [x] Frozen D9 candidate revision r3: `workspace/review-queue/commerce-v1/import-phase2c/git-baseline-r3/`; 556/556 manifest paths (554 current files + 2 special targets), secret scan `PASS` with 0 findings, candidate Manifest SHA `d0df2009fb859b280dc55b0291829519830078e0239951d9a689b3e5769a71d5`.
- [x] Built package manifest r2: `GIT_BASELINE_PACKAGE_MANIFEST_V16_R2.json`, SHA `79f3ec04022cdf083be8816a7a88a4ee546e200911bcf0298e885feaec222169`; it binds the candidate, formal V16, C/APPLY receipt, policy, generator, tests and human approval script; no root writes, Git init or remote.
- [x] Prepared (not executed) `Approve-GitBaselineV16.ps1`; its exact interactive boundary is Jovi’s 16-character confirmation against candidate Manifest SHA `d0df2009fb859b280dc55b0291829519830078e0239951d9a689b3e5769a71d5`. The old r1 candidate is retained as superseded evidence; r2 failed before publication and produced no candidate directory.
- [ ] Jovi exact Git baseline confirmation: not executed by the control agent because it is a human-only approval boundary; no `workspace/approvals/GIT_BASELINE.V1.approval.json` exists.
- [ ] D10 Git baseline establishment/object import, D11 main-root synthetic X2, D12 independent Import Audit execution and D13 frozen merge-candidate execution remain `NOT_STARTED`; only their review-queue candidate tools are prepared below.

#### D9 current stop state

`GIT_BASELINE_CANDIDATE_FROZEN` / `AWAITING_JOVI_GIT_BASELINE_CONFIRMATION`; formal V16 and C/APPLY remain valid; Hook `DO_NOT_TRUST`; no Git HEAD, Commerce import, main-root X2, real pilot or remote repository.

### Commerce Import Phase2C D10 Git-object preparation (2026-08-22) — machine-only, not formal import

- [x] Confirmed the human `GATE_A.P` receipt exists and matches `GATE_A_PLAN.json` SHA `7db47094bb256223840cc3c685e22d7b7e240d8365ccc60841c5a6e4c6c16bb7`; approval body SHA is `bf3628fb1b74505947d6004f4a6e017555260866e3ee0284d9ee8d5947b0e38e`.
- [x] Ran the V16-bound, read-only Git-object selector against external HEAD `3b31f0f2f240038aa261db5c57c43e5e14992dc5`; index `workspace/review-queue/commerce-v1/import-phase2c/source-object-index-v16/IMPORT_SOURCE_OBJECT_INDEX_V16.json` SHA `ab759901f57832f4dcc4f0e2cdee1d6138f5274c5898922392e472d0a5e25614` records 93 source rows: 49 feature, 10 evidence review-only, 34 record-only; checkout bytes read `false`, root writes `0`, root Git initialized `false`.
- [x] Materialized the non-authoritative Git-object staging preview at `workspace/review-queue/commerce-v1/import-phase2c/import-staging-preview-v16-r6/`; manifest SHA `6962f7c58b2cea3a59c2c9772fdbad3c0b2722c69220ec301b3d2fd6671893a8`, review SHA `72657884efc1269e9997dbab93a1f52aa42a065fc5e675593d4b6b1fef0e415b`, 49 feature files plus 14 derived compatibility aliases. The preview explicitly remains `formal_import_applied=false` and `git_baseline_established=false`.
- [x] Preview verification passed: unit `99/99` with 4 skips, acceptance `8/8` with 1 skip; candidate suite `16/16 OK`; six Python tools AST-parsed and the human approval PowerShell script passed the Windows PowerShell 5.1 parser.
- [ ] Formal Git baseline establishment, root import, main-root synthetic X2, Import Audit and merge candidate remain not started. The 14 derived aliases require a future formal target/package binding; they are not silently promoted by this preview.

#### D10 current stop state

`D10_READ_ONLY_GIT_OBJECTS_VERIFIED` / `AWAITING_JOVI_GIT_BASELINE_CONFIRMATION`; no root Git initialization, no formal Commerce import, no main-root X2, no real pilot and no remote repository.

### Commerce Import Phase2C D10-D13 execution candidates (2026-08-22) — prepared, not authorized

- [x] Added the V17-bound Git-object importer candidate `tools/import_commerce_objects_v17.py` (current SHA `6816d6a9f0efc973137c61ed9ae336c5377ac4e3c92d2cc01c698bf1117e2d7a`). It requires an issued V17 Decision, exact baseline receipt, both Jovi approvals, frozen source index/package, clean root and clean external repo; it stages only in `root/.worktrees/commerce-import-phase2`, commits the feature worktree, writes implementation/evidence receipts, and supports check/apply/rollback/recover.
- [x] Corrected evidence-record target semantics: the ten bound evidence rows may name `workspace/review-queue/commerce-v1/decision-to-main-x2/external-evidence/**`, but they remain review-only and are never written into the feature worktree; an outside target now fails before worktree creation. The regression is covered by the frozen candidate tests.
- [x] Corrected source-history validation to allow the bound implementation/evidence commits (`fd2321d…`, `7dbe080…`) even though the observed external `main` bootstrap HEAD `3b31f0…` is a separate root; all source bytes still come from Git blob OIDs.
- [x] Generated explicit compatibility target candidate `workspace/review-queue/commerce-v1/import-phase2c/inputs/IMPORT_COMPATIBILITY_TARGET_SET_V17.json`, SHA `d702c49ba10c002fc64425475885ac75f01191047f22e2703ca1c044e297eb7c`; 14 derived aliases, source index binding `ab759901…25614`, `requires_v17_binding=true`.
- [x] Added the V17-bound synthetic runner `tools/run_main_project_x2_v17.py` (SHA `f4dfb81dfffdfaa890912e9213a8da7b459e97bb206356ce21890963f6224e63`). It binds import receipts to the issued Decision and feature HEAD/tree, runs unit/acceptance/X2 outside the feature tree, and requires synthetic PASS, `READY_FOR_HUMAN_DELIVERY`, all real actions false and pilot not started.
- [x] Isolated preview X2 execution passed: `X2_STAGING_COMMERCE_FLOW_PASS`, order/payment/entitlement/delivery counts `1/1/1/1`, final order `READY_FOR_HUMAN_DELIVERY`, artifact manifest SHA `02fd1738a8966f8cdef559612c33b112e980f43071251ced17484a969d23d708`.
- [x] Candidate suite after D10/D11/D12/D13 additions: `29/29 OK`; all 12 source Python tools AST-parse and all 7 shipped Phase2C CLIs return help successfully. The frozen r9 package is independently self-contained: 9 shipped Python tools AST-parse, 29/29 tests pass, and both human-bound PowerShell scripts pass the Windows PowerShell 5.1 parser.
- [ ] Formal V17 issuance, Git baseline establishment, root import, feature worktree import, D11 main-root X2, D12 Import Audit and D13 merge candidate remain unexecuted. The compatibility target set is a candidate only and must be bound by V17 before use.

#### D10-D13 candidate stop state

`D10_D11_EXECUTORS_PREPARED` / `AWAITING_JOVI_GIT_BASELINE_CONFIRMATION_AND_FORMAL_V17`; formal root Git, Commerce import, main-root X2, Import Audit and merge candidate are still `NOT_STARTED`.

### Commerce Import Phase2C V17 candidate package (2026-08-22) — current handoff

- [x] Built review-queue-only V17 revision r9 at `workspace/review-queue/commerce-v1/import-phase2c/governance-v17-r9/`; package inventory `52/52`, candidate/package/review bindings and all member hashes rechecked. r8, r7, r6, r5, r4, r3 and r2 are retained as historical superseded evidence.
- [x] V17 candidate SHA: `14104a3c48d7c1806cbcb062385afc44130d08822a8b63868e8d89b7ac388188`.
- [x] V17 package manifest SHA: `8317a5c1e60bcab98659998fc0877d7810ee9461bf1a2c453008e6d7d9d0bb1e`; review SHA: `5e25a144482049df37952a8e6264ccd02909cc6b9857c3df565cd9d29624e95a`.
- [x] r9 binds D12 `audit_import_phase2c_v17.py` (SHA `9cc253e4d1303a157c79b88f64748db90f4293a4f033ef7b438d645c91375191`) and D13 `build_merge_candidate_v17.py` (SHA `cf0cc1692bc2bd3c6b95c32189ff50793264072e7dd57e465fe883f757249b6a`), directly verifies formal V16/C/APPLY/Gate Plan lineage, derives exact Git diff counts instead of hard-coding them, keeps audit/merge outputs outside the package manifest, and includes the evidence-target regression. Source suite is `29/29`, frozen-package suite is `29/29`, source AST is `12/12`, package AST is `9/9`, all seven CLI help checks exit 0, and both PowerShell 5.1 parser checks pass.
- [x] D12/D13 candidate tools are prepared but intentionally have no PASS receipt yet: they require the future formal V17, D10 baseline/import receipts and D11 synthetic reports. No audit output or merge candidate has been fabricated.
- [x] Hardened `Issue-DecisionV17.ps1` SHA `13b86f761147b7f6bb63fc59f1891a7beef653d3b3bcbdbced653a7c8987d79`; Windows PowerShell 5.1 parser and disposable-root end-to-end issuance test passed. The issuer validates Gate A.P and future Git baseline approval bodies, requires exact `ISSUE DECISION V17 14104a3c48d7` for the current r9 candidate (12 characters), and writes formal V17 only when all bindings match.
- [x] Final current-state regression: Gate readiness `2/2`, transition facade `1/1`, S1 integrity `2/2`, S2A2 `2/2`, and PreToolGuard `10/10` pass. The protected legacy S2A1 baseline is `41/43`; its two stale C/APPLY expectations were reproduced in an unbound temporary edit, then reverted because `FRAMEWORK_MANIFEST.sha256` binds the test file. The protected `run-security-semantics.py` entrypoint currently fails closed with `child_timeout` at its 30-second guard (`0/20` collected); no V17/import/X2/Audit/merge bytes were written.
- [ ] No V17 issuance has occurred; no Git baseline Approval exists, no formal V17 exists, and no root Git/import/X2/Audit/merge action has been run.

#### V17 current stop state

`V17_CANDIDATE_FROZEN` / `AWAITING_JOVI_GIT_BASELINE_APPROVAL_THEN_V17_ISSUANCE`; next human prefix is the D9 candidate prefix `d0df2009fb859b28` (16 characters). After that approval exists, V17 issuance uses the current r9 candidate confirmation `14104a3c48d7` (12 characters).
