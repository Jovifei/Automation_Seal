# JOVI-AUTOMATION-COMMERCE-DECISION-TO-MAIN-X2-PHASE2B V2

> **交给 Luna：** 使用 `executing-plans` 执行 D0-D8；主工程 Git baseline 和独立 worktree 建立后，D9-D13 改用 `subagent-driven-development`。涉及实现或适配的任务使用 `test-driven-development`，任何完成声明使用 `verification-before-completion`。
>
> **主工程：** `E:\project\jovi-automation`
>
> **外置对象仓：** `E:\project\jovi-commerce-engine-v1`（只用于读取 Git objects；当前工作树 HEAD 不是 evidence HEAD）。
>
> **外置 evidence worktree：** `E:\project\jovi-commerce-engine-v1\.worktrees\landing-phase1`
>
> **本计划替代范围：** 替代 `2026-08-10-commerce-import-phase2.md` 中尚未完成的 I2-I13；保留并复用已完成 I0/I1/G3 原始证据，不改写或重做原 G3。D2 只对新发现的 static-Prompt structural remediation 做 fresh independent audit。
>
> **最终出口：** `COMMERCE_IMPORT_CANDIDATE_PASS` + `MAIN_PROJECT_X2_SYNTHETIC_PASS`。不 merge、不 push、不进入真实 SKU 试点。
>
> **V2 修正：** 2026-08-11 可执行性复核证明旧顺序存在确定性循环：当前 Framework 候选封存 `CODEX_START_PROMPT.txt`，但 S1 closeout 和 `S1/CLOSED -> C/APPLY` 又会更新它。仅把 Prompt 移出 Framework 也不安全，因为现有 mirror validator 只检查 marker，保留 marker 的正文篡改可能漏检。本版把 Prompt 改成不含 revision 的静态 canonical-state 指针并继续纳入 Framework 全字节保护；closeout/C-APPLY 只更新 canonical state、`PROJECT_STATE.json` 和 `STATUS.md` 三文件。

---

## 1. 当前真实状态

### 1.1 已完成且不得重做

- G3 独立审核：`PASS_READY_FOR_JOVI_DECISION`。
- G3 报告：`workspace/review-queue/commerce-v1/governance-v2/G3_PREAPPLY_AUDIT_PASS_RERUN1.md`。
- G3 SHA-256：`c92682c9d58f702ac5249cb2387f87999c41a8d17d79b20a0ec210e125a36686`；sidecar 匹配。
- Final Target Set：13/13 bytes/SHA 匹配。
- V4 review package：18/18。
- RERUN1 human-only：`PASS_ZERO_DRIFT`。
- Pre-Decision validator：`PREDECISION_READY_FOR_INDEPENDENT_AUDIT`。
- Hook：`DO_NOT_TRUST`；`hook_runtime_dependency=false`、`hook_restore_allowed=false`、`hook_trust_allowed=false`。
- 外置对象仓 observed HEAD：`3b31f0f2f240038aa261db5c57c43e5e14992dc5`；它只是对象仓当前工作树 HEAD，不得冒充 evidence HEAD。
- 外置 Commerce Engine evidence worktree HEAD：`7dbe080c907c1da2eef1c16b79e677e6a1d49470`，worktree clean，remote 为空。
- 外置 implementation HEAD：`fd2321d5a3f12aa923014cadbc397849903fd97c`。
- `fd2321d5a3f12aa923014cadbc397849903fd97c` 是 `7dbe080c907c1da2eef1c16b79e677e6a1d49470` 的祖先；两个commit均可由外置对象仓读取。
- 外置 implementation snapshot 共83项：49项待导入、34项明确排除；Git object bytes 83/83 与 manifest 匹配，Windows checkout bytes 仅60/83匹配，因此不得从 checkout 复制。
- 外置 `IMPORT_CANDIDATE_MANIFEST.json` body SHA-256=`4090c6963b19705cc401336df6f3a0f7a31a97a650cff517cc9cb7d83c94a4f0`，Git blob OID=`dd4a55426771c4fb10bb55e6ff1e84fc8001b953`；`155f01b83211275b560c3482f8e98cea24e5e889367b87468c03d33d5325854e`只是其内部绑定的Commerce candidate manifest SHA，二者不得混用。
- 外置 unit/general discovery：99 run、95 passed、4个有说明的Windows symlink/platform skipped；acceptance必须另行执行，当前为8 run、7 passed、1个有说明的Windows symlink skipped；X2 47/47 artifacts、8/8 evidence，Xianyu validator PASS。

### 1.2 当前即时阻塞与已证实的结构缺口

以下对象当前不存在：

```text
workspace/decisions/JOVI_S1_RESTART_DECISION_V3.json
workspace/decisions/JOVI_S1_RESTART_DECISION_V3.json.sha256.sidecar
reports/remediation/COMMERCE_V1_POST_APPLY_AUDIT.json
reports/gates/GATE_A_PLAN.json
workspace/approvals/GATE_A.P.approval.json
```

控制面仍为：

```text
S1/CLOSED/1
blockers = HOOK_UNTRUSTED, FORMAL_MANIFEST_MISMATCH
```

当前精确状态：

```text
G3_PASS_READY_FOR_JOVI_DECISION
BLOCKED_PROMPT_MANIFEST_CYCLE_AND_WEAK_INTEGRITY
WAITING_FOR_PHASE2B_EXECUTION_AMENDMENT
```

原 G3 PASS 仍是有效的当前树审阅证据，但**不能直接用于签发旧 Decision proposal**。原因不是 G3 造假或 SHA 漂移，而是其已审核的 Framework V2 candidate 同时把 `CODEX_START_PROMPT.txt` 当成不可变框架字节和 revisioned mirror。下一步必须先形成一个精确、独立审核的静态 Prompt 结构修正包；正式 Decision V3 同时绑定原 G3 与该修正审核。

### 1.3 已冻结的关键绑定

```text
G3 report                            c92682c9d58f702ac5249cb2387f87999c41a8d17d79b20a0ec210e125a36686
Decision V3 candidate                c5cc3d0f6c3a60287b79becf401bc66ff8b626af4d10f9dd57926c0cc81b71ff
Controlled Baseline candidate        3a85bf26729d874f28f6874f7ed76781fba4fdde265e61a22701f6719898e190
Framework Manifest V2 candidate      00550de6fabff131298168d33e3ace04440cd4b5bbe1bcc021c4b31cfa2b8e8e
V4 Review Package Manifest           6acd9e1998eb60bc6d69d7a3fd9d06837bd2d79fc991fc028a77c2a968dcaa79
Final Target Set file                1ee1dcd0e41fc9d822ae6839a60d96c284d8d184ce3141e81547ffc00c67ad5a
Final Target Set declared binding    c3d0e9b2a3749b2750e3bbbf8cd07fb8feda4b64e4ac6d4009e4e21f8507428e
Commerce Candidate Manifest          155f01b83211275b560c3482f8e98cea24e5e889367b87468c03d33d5325854e
```

任何一个 SHA 漂移都使后续人类签发包失效。

### 1.4 当前完成度（计划估算，不是 Gate 结论）

| 范围 | 当前证据 | 估算 |
|---|---|---:|
| 外置 Commerce Engine + X2 staging | implementation/evidence已冻结；unit/general 99 run/95 passed/4 skipped，acceptance单独8 run/7 passed/1 skipped；X2 47/47 + 8/8 | 100% |
| G3 原治理候选审阅 | G3 receipt 已落盘并匹配 | 100% |
| Phase2B 治理解锁 | 已发现并定位 Prompt/Manifest loop 与弱 marker 校验；结构补丁/Decision/APPLY/Gate 尚未执行 | 35% |
| 主工程 Git baseline 与 Commerce import | 尚未授权、尚未开始 | 0% |
| 主工程 X2 与 Import Audit | 尚未开始 | 0% |
| 最终人工商业闭环 | 无真实 SKU、无真实成交、无试点 | 约 40%-45% |

百分比只用于排期。唯一权威状态仍是本计划第4节的离散阶段状态。

---

## 2. 最终项目效果与本阶段边界

最终项目要实现：

```text
原创数字产品资产
→ 人工审核商品草稿
→ 匿名本地订单
→ Jovi 人工付款确认
→ Entitlement 与可验证交付包
→ Jovi 人工发送
→ 脱敏售后
→ 聚合商业指标
→ 单 SKU 人工商业验证
```

本阶段只完成：

```text
治理解锁
→ 主工程受控导入
→ 主工程纯合成 X2
→ 独立 Import Audit
→ 可合并候选冻结
```

本阶段永久禁止：

- Hook TRUST、恢复或成为运行依赖；
- 修改 `MANIFEST.sha256`；
- Track I；
- 外部闲鱼仓访问；
- Cookie、Token、平台消息、订单库、支付信息或客户 PII；
- 自动发布、消息、收款、发货、改价、退款或验证；
- 修改 `products/modbus-rtu-toolkit/`；
- 真实 SKU 或客户数据；
- Git remote、push、merge、tag、发布。

---

## 3. 人类动作压缩设计

为了避免再次卡在“需要 Jovi 手工制作 JSON”，本计划把后续 human-only 动作压缩为三次，且全部由经过独立审核的脚本生成回执：

1. **Jovi运行一次 Decision V3 交互式签发脚本。** Luna只生成候选、验证器和测试；独立 Agent先审核。脚本由 Jovi运行，Luna永不运行。
2. **Jovi运行现有 `Approve-Gate.ps1`。** Luna只生成 Gate Plan并验证 receipt。
3. **Jovi运行一次 Git baseline 确认脚本。** 原因是 C/APPLY state 必须绑定 Gate Plan SHA，导致该状态文件的最终字节在 Gate Plan 生成前无法确定；不得用算法假设冒充 exact-byte 人工确认。

Decision V3 同时绑定：

- G3 与现有治理候选；
- 原 G3 receipt 与新的 static-Prompt structural remediation 独立审核；
- 精确十二目标 structural migration + 唯一 Framework Manifest apply工具与candidate SHA；
- 精确 S1 closeout target/patch/tool SHA；
- `Post-Apply Audit PASS` 作为 closeout 的强制前置。

因此不再额外要求一轮聊天式 closeout 授权。Decision 仍保持 Track P/I 和真实平台动作全部为 false；Gate A.P 仍是唯一 Track P 批准。D1 只写 review queue 候选，不改任何正式控制字节，因此 Jovi下发本计划即可授权 Luna 准备 D1；真正改变正式治理或 Git 状态仍只能由三次 Jovi human-only 动作触发。

---

## 4. 状态晋级

```text
G3_PASS_READY_FOR_JOVI_DECISION
→ STATIC_PROMPT_STRUCTURAL_REMEDIATION_REVIEW_PASS
→ HUMAN_ACTION_PACKAGE_REVIEW_PASS
→ DECISION_V3_ISSUED
→ FRAMEWORK_MANIFEST_V2_1_APPLIED
→ POST_APPLY_AUDIT_PASS
→ S1_CLOSED_CLEAN
→ GATE_A_P_VERIFIED
→ CONTROL_PLANE_C_APPLY
→ MAIN_GIT_BASELINE_ESTABLISHED
→ COMMERCE_IMPORT_IMPLEMENTED
→ MAIN_PROJECT_X2_SYNTHETIC_PASS
→ IMPORT_AUDIT_PASS
→ COMMERCE_IMPORT_CANDIDATE_PASS
```

---

## 5. Luna 执行台账

Luna在 `workspace/review-queue/commerce-v1/decision-to-main-x2/EXECUTION_LEDGER.md` 维护以下清单；它是D0-D13唯一允许跨阶段追加的**非权威进度元数据例外**。Ledger只追加阶段、UTC、状态和已经存在的证据SHA，不作为任何PASS的替代证据、不纳入D0原子证据事务、不得重写历史行；本计划与 sidecar 保持冻结：

- [ ] D0：重验 G3、13/13、V4、外置 X2，并机器证明 Prompt/Manifest 循环和 marker-only 篡改缺口。
- [ ] D1：生成静态 Prompt 结构补丁、V2.1 Framework、Decision/S1-closeout 人类动作包及 Shadow 测试。
- [ ] D2：独立审核静态 Prompt 修正与人类动作包为 PASS。
- [ ] D3：Jovi运行签发脚本，正式 Decision V3 只读验证通过。
- [ ] D4：canonical governance mirror 和 Decision-bound exact Structural+Manifest APPLY 完成。
- [ ] D5：新的独立 Post-Apply Audit 为 PASS。
- [ ] D6：Decision 授权的 S1 closeout 应用，blockers 为空。
- [ ] D7：Gate readiness PASS；Jovi Gate A.P receipt 验证通过。
- [ ] D8：控制面完成 `S1/CLOSED → C/APPLY`。
- [ ] D9：主工程本地 Git baseline 与 feature worktree 建立。
- [ ] D10：外置 Commerce Engine 精确导入并完成命名空间适配。
- [ ] D11：主工程治理回归和 X2 合成复验通过。
- [ ] D12：独立 Import Audit PASS，finding 修复闭合。
- [ ] D13：证据冻结、状态/知识库同步和 feature branch 停点完成。

---

## 6. Track A：从 G3 PASS 到 C/APPLY

### D0 — Resume Preflight

**目的：** 确保不复用漂移后的 G3 或外置来源。

**业务证据只写：**

```text
workspace/review-queue/commerce-v1/decision-to-main-x2/preflight/
├── run_phase2b_resume_preflight.py
├── test_phase2b_resume_preflight.py
├── PREDECISION.json
├── RESUME_PREFLIGHT.json
├── PROMPT_MANIFEST_LOOP_AND_TAMPER_PROOF.json
├── PROTECTED_TREE_BEFORE.json
├── EXTERNAL_SOURCE_BEFORE.json
└── 每个body对应sidecar
```

唯一写范围例外是上一节的append-only `decision-to-main-x2/EXECUTION_LEDGER.md`：D0业务证据事务全部成功后才能追加一行`D0=RESUME_PREFLIGHT_PASS`及RESUME SHA；事务失败只追加`D0=BLOCKED`和失败报告SHA（若存在），不得把ledger行当作业务证据或留下部分preflight发布。

D0没有可复用的现成总控脚本，因此不得只运行现有validator后声称四份报告已产生。Luna先在上述唯一允许目录内，以TDD实现`run_phase2b_resume_preflight.py`：RED测试必须覆盖plan sidecar错误、G3漂移、13/13漂移、Prompt marker-only篡改证明缺失、外置commit/blob不可达和输出半成品；GREEN后脚本才可生成报告。runner及其test也必须生成sidecar。`RESUME_PREFLIGHT.json`是本次run的外层索引，必须包含唯一`run_id`、真实UTC，并逐项绑定：本计划body+sidecar、runner body+sidecar、test body+sidecar、`PREDECISION.json` body+由runner补写的sidecar，以及`PROMPT_MANIFEST_LOOP_AND_TAMPER_PROOF.json`、`PROTECTED_TREE_BEFORE.json`、`EXTERNAL_SOURCE_BEFORE.json`三份body+sidecar。RESUME自身再由sidecar绑定。D1的Human Action Package必须逐项复核并绑定这份索引及全部成员，D0脚本永不安装为正式安全入口。

**检查：**

- 本计划 `tasks/plans/2026-08-11-commerce-decision-to-main-x2.md` 与同名 sidecar 精确匹配；执行ledger、Human Action Package、Decision proposal及D2 audit均必须引用该plan body SHA，后续不得静默换计划；
- G3 body/sidecar；
- Final Target Set 13/13；
- V4 18/18；
- human-only RERUN1 zero drift；
- current Framework mismatch 集合仍精确为 11 项；
- `CODEX_START_PROMPT.txt` 同时存在于 Framework V2 candidate 与 control-plane mirror 集合；
- Shadow 执行 closeout 或 C/APPLY 后旧 Framework candidate 必然失配该文件；
- 保留 marker 的 Prompt 正文篡改当前不会被 `validate_root()` 完整检测；
- Decision、Post-Apply、Gate Plan、Approval 仍不存在；
- state 仍为 `S1/CLOSED/1`；
- 外置对象仓存在并可读取`fd2321d5a3f12aa923014cadbc397849903fd97c`与`7dbe080c907c1da2eef1c16b79e677e6a1d49470`；对象仓observed HEAD记录为`3b31f0f2f240038aa261db5c57c43e5e14992dc5`，但不要求它等于evidence HEAD；
- evidence worktree HEAD为`7dbe080c907c1da2eef1c16b79e677e6a1d49470`、clean、remote empty；
- implementation为`fd2321d5a3f12aa923014cadbc397849903fd97c`，且它是`7dbe080c907c1da2eef1c16b79e677e6a1d49470`祖先；
- implementation manifest body SHA=`4090c6963b19705cc401336df6f3a0f7a31a97a650cff517cc9cb7d83c94a4f0`、blob OID=`dd4a55426771c4fb10bb55e6ff1e84fc8001b953`，83/83 Git blobs匹配；
- 外置unit/general 99 run/95 passed/4 skipped、acceptance单独8 run/7 passed/1 skipped、X2 47/47、8/8。

**命令：**

```powershell
$planPath = (Resolve-Path .\tasks\plans\2026-08-11-commerce-decision-to-main-x2.md).Path
$planSidecar = "$planPath.sha256.sidecar"
$expectedPlanSha = ((Get-Content -Raw -Encoding ASCII $planSidecar).Trim() -split '\s+')[0].ToLowerInvariant()
if ((Get-FileHash -LiteralPath $planPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expectedPlanSha) { throw 'Phase2B plan sidecar mismatch' }
$preflightRoot = (Resolve-Path .\workspace\review-queue\commerce-v1\decision-to-main-x2\preflight).Path
py -3.12 -B .\scripts\validate_commerce_predecision_readiness.py `
  --root . `
  --package .\workspace\review-queue\commerce-v1\governance-v2 `
  --output "$preflightRoot\PREDECISION.json"
if ($LASTEXITCODE -ne 0) { throw 'resume predecision validation failed' }
py -3.12 -B "$preflightRoot\test_phase2b_resume_preflight.py"
if ($LASTEXITCODE -ne 0) { throw 'resume preflight TDD tests failed' }
py -3.12 -B "$preflightRoot\run_phase2b_resume_preflight.py" `
  --root . `
  --plan $planPath `
  --expected-plan-sha256 $expectedPlanSha `
  --predecision "$preflightRoot\PREDECISION.json" `
  --g3 .\workspace\review-queue\commerce-v1\governance-v2\G3_PREAPPLY_AUDIT_PASS_RERUN1.md `
  --output-root $preflightRoot
if ($LASTEXITCODE -ne 0) { throw 'resume preflight evidence generation failed' }
```

**输出：** runner验证现有validator的`PREDECISION.json`后，原子生成`RESUME_PREFLIGHT.json`、`PROMPT_MANIFEST_LOOP_AND_TAMPER_PROOF.json`、`PROTECTED_TREE_BEFORE.json`、`EXTERNAL_SOURCE_BEFORE.json`及全部sidecar；任一失败时四份业务报告全部保持不存在，不接受“只生成其中一部分”。

原`workspace/review-queue/commerce-v1/import-phase2/`中的`PHASE2_INPUT_STATUS.json`、`CURRENT_FACTS_PHASE2.json`、`EXECUTION_LEDGER.md`仅保留为旧计划历史证据，本计划不更新、不补sidecar、不用它们表达当前状态。当前执行状态只追加到新的`decision-to-main-x2/EXECUTION_LEDGER.md`；除该非权威元数据例外外，D0严格只写上述preflight目录。

**成功状态：** `RESUME_PREFLIGHT_PASS`。

**失败：** `BLOCKED_INPUT_DRIFT`；不自动更新候选，不复制新字节，不重做 G3 以掩盖漂移。

---

### D1 — 生成可由 Jovi一次签发的 Human Action Package

#### D1.1 目录

```text
workspace/review-queue/commerce-v1/decision-to-main-x2/human-action/
├── STATIC_CONTROL_POINTER_POLICY_V1.json
├── FRAMEWORK_MANIFEST_V2_1_CANDIDATE.sha256
├── CONTROLLED_BASELINE_V2_1_CANDIDATE.json
├── CONTROLLED_BASELINE_V2_1_CANDIDATE.sha256
├── V2_TO_V2_1_EXACT_DIFF.json
├── PHASE2B_STRUCTURAL_PATCH_TARGET_SET_V1.json
├── PHASE2B_STRUCTURAL_PATCH_V1.json
├── proposed-structural/
│   ├── CODEX_START_PROMPT.txt
│   ├── MANIFEST_POLICY.md
│   ├── config/control-plane-registry.json
│   ├── scripts/control_plane.py
│   ├── scripts/apply_commerce_control_plane_transition.py
│   ├── scripts/validate_commerce_gate_readiness.py
│   ├── scripts/run-static-tests.py
│   └── tests/
│       ├── test_s2a2_enforcement.py
│       ├── test_s2a1_control_plane.py
│       ├── test_control_plane_commerce_transition.py
│       ├── test_commerce_gate_readiness.py
│       └── test_s1_integrity.py
├── PRE_APPLY_AUDIT_INPUT_V4_AMENDED/
│   └── REVIEW_PACKAGE_MANIFEST.json
├── PHASE2B_EXACT_TARGET_SET_V1.json
├── DECISION_V3_PROPOSED.json
├── DECISION_V3_PROPOSED.json.sha256.sidecar
├── Issue-DecisionV3.ps1
├── verify_decision_v3.py
├── apply_phase2b_structural_patch.py
├── materialize_governance_canonical_mirror.py
├── apply_s1_closeout.py
├── apply_commerce_control_plane_transition_bound.py
├── verify_gate_a_p_bound.py
├── verify_phase2b_governance_chain.py
├── generate_gate_a_plan_bound.py
├── GIT_BASELINE_POLICY_V1.json
├── Approve-GitBaseline.ps1
├── verify_git_baseline_approval.py
├── prepare_git_baseline.py
├── apply_git_baseline_files.py
├── prepare_import_scope.py
├── prepare_import_source_selection.py
├── import_external_git_blobs.py
├── verify_expected_import_red.py
├── run_and_record.py
├── write_dual_root_binding.py
├── proposed-root/
│   ├── .gitignore
│   └── .gitattributes
├── S1_CLOSEOUT_TARGET_SET_V1.json
├── S1_CLOSEOUT_PATCH_V1.json
├── proposed/
│   ├── config/control-plane-state.json
│   ├── PROJECT_STATE.json
│   └── STATUS.md
├── tests/
│   ├── test_decision_issuer.py
│   ├── test_canonical_governance_mirror.py
│   ├── test_structural_manifest_apply.py
│   ├── test_s1_closeout.py
│   ├── test_bound_commerce_transition.py
│   ├── test_bound_gate_plan.py
│   ├── test_bound_gate_receipt.py
│   ├── test_git_baseline_approval.py
│   ├── test_import_source_selection.py
│   ├── test_external_git_blob_import.py
│   ├── test_expected_import_red.py
│   ├── test_run_and_record.py
│   └── test_dual_root_binding.py
├── HUMAN_ACTION_PACKAGE_MANIFEST.json
└── sidecars
```

所有脚本在D1都只是review-queue candidate，不安装到`scripts/human-only/`，D1本身不修改正式安全脚本。只有D4在Decision和D2独审双重绑定后，才可通过已审核apply工具写入十二个精确structural targets和一个Framework Manifest；除此之外不得修改正式安全脚本。

#### D1.2 Static Prompt structural remediation 与 Framework V2.1 candidate

`STATIC_CONTROL_POINTER_POLICY_V1.json` 必须固定：

- canonical state：`config/control-plane-state.json`；
- revisioned mirrors：`PROJECT_STATE.json`、`STATUS.md`；
- immutable pointer：`CODEX_START_PROMPT.txt`；
- Prompt 固定包含 `CONTROL_PLANE_AUTHORITY=config/control-plane-state.json` 和只读验证入口，不再包含 `CONTROL_PLANE_MIRROR=<stage/status/revision>`；
- Prompt 全文字节继续由 Framework Manifest 保护；
- state/mirror integrity：`previous_state_hash` + `state_revision` + `mirror_marker` + `scripts/control_plane.py::validate_root`；
- closeout/transition 只能写 canonical state 与两份 revisioned mirrors；
- Hook、Manifest、Decision、Approval、human-only 和平台权限不属于 state mirror。

`PHASE2B_STRUCTURAL_PATCH_V1.json` 必须绑定十二个proposed formal targets：Prompt、`MANIFEST_POLICY.md`、registry、`control_plane.py`、现有transition脚本、Gate readiness、static-test runner和五份测试。精确语义：

1. registry 明确区分 `revisioned_mirrors` 与 `immutable_state_pointers`；
2. `validate_root()` 要求 Prompt 的 canonical authority pointer，但 Prompt 的任意正文篡改由 Framework 全字节校验拒绝；
3. `apply_commerce_control_plane_transition.py` 的 mirror documents 从四文件缩为三文件，不再读取、替换 Prompt；
4. S1 closeout 同样只生成/写三文件；
5. `test_s1_integrity.py` 移除旧 Framework body 的永久硬编码 SHA，改为逐项 Manifest→当前字节匹配；授权链由 Decision/apply receipt 检查；
6. `test_s2a2_enforcement.py` 不再断言live tree永远是`S1/CLOSED/1`、永远保留两个旧blocker或永远拒绝Commerce；改为临时fixture覆盖门前拒绝、DNT与阶段转换兼容性、human-only/Approval/Manifest/外部闲鱼始终拒绝。现有guard只提供粗粒度Commerce-root门禁，**不得**把该测试表述为target-set精确授权证明；D10正式写入只能经Decision/Gate-bound importer完成，任何直接写路径均不属于本计划；
7. `MANIFEST_POLICY.md` 仅新增一次性迁移条款：只有Decision V3 + D2独立PASS，且Decision绑定外置`FRAMEWORK_MANIFEST_V2_1_CANDIDATE.sha256`路径/body sidecar和apply tool时，才允许执行该候选迁移；Policy正文**不得嵌入新Framework Manifest body SHA、不得引用由自身字节派生的SHA**，以避免manifest↔policy自引用。迁移后恢复不可变策略；禁止通用重建、自动接受current bytes或修改`MANIFEST.sha256`；
8. tests 必须证明 state revision 改变时 Prompt SHA 不变、Prompt 任意正文篡改会被 Framework 拒绝、registry/pointer 缺失 fail-closed，并证明旧/新阶段测试均不依赖 live-state 常量。
9. `validate_commerce_gate_readiness.py` 增加显式`pre-gate`与`post-transition`模式：前者要求S1 closeout、Gate尚未批准；后者要求`C/APPLY`、strict Gate receipt与transition receipt，不再硬编码`S1/CLOSED`。CLI的`--phase`为required，缺失失败；为保持V2中不可变`generate_gate_a_plan.py::build_plan(root)`不变，库接口固定安全默认`readiness_errors(root, phase="pre-gate")`，只有调用方显式传`post-transition`才进入后阶段，其他值失败；
10. `run-static-tests.py` 移除`gate_satisfied=False`和live阶段硬编码，改用临时fixture或显式phase参数；
11. `test_commerce_gate_readiness.py` 同时覆盖CLI缺phase FAIL、库接口默认pre-gate、未修改的`build_plan(root)`在pre-gate成功、post-transition显式PASS及阶段证据互换FAIL；D11调用post-transition模式。

`FRAMEWORK_MANIFEST_V2_1_CANDIDATE.sha256` 从 G3 已审核 V2 candidate 加结构补丁生成：

1. 除Prompt和`MANIFEST_POLICY.md`外的19个旧path，其顺序和SHA与V2 candidate逐字节相同，禁止对旧路径重算后换值；
2. `CODEX_START_PROMPT.txt` 保留在 Framework，但 SHA 更新为 proposed static bytes；
3. 新增以下19个 immutable protector；其中属于 structural patch 的路径使用 proposed after SHA，其余使用当前 SHA：

```text
config/control-plane-registry.json
config/package-integrity-scope.json
scripts/control_plane.py
scripts/validate-control-plane.py
scripts/apply_commerce_control_plane_transition.py
scripts/validate_commerce_gate_readiness.py
scripts/validate_commerce_predecision_readiness.py
scripts/run-security-semantics.py
scripts/package_integrity.py
scripts/run-hook-tests.ps1
scripts/run-static-tests.py
scripts/static_test_support.py
tests/hooks/pre_tool_bootstrap.ps1
tests/hooks/test_pre_tool_guard.py
tests/test_s1_integrity.py
tests/test_s2a2_enforcement.py
tests/test_s2a1_control_plane.py
tests/test_control_plane_commerce_transition.py
tests/test_commerce_gate_readiness.py
```

4. 最终 active Framework target 必须为40项；
5. 输出 `V2_TO_V2_1_EXACT_DIFF.json`，差异只能是 `0 removed + 19 added + 2 modified(Prompt, MANIFEST_POLICY)`；
6. 对 structural patch 与新增 protector 在 Shadow 中运行完整治理测试并由 D2 独立审核，不把“当前存在”自动等同于“已接受”。

`CONTROLLED_BASELINE_V2_1_CANDIDATE.json` 保留原 V2 candidate 的21项历史记录：Prompt 标记为 `REPLACE_WITH_APPROVED_STATIC_POINTER_BYTES`，`MANIFEST_POLICY.md` 标记为 `REPLACE_WITH_APPROVED_ONE_TIME_MIGRATION_POLICY_BYTES`，其余19项处置不变；19个新增 protector 标记为 `NEW_IMMUTABLE_PROTECTOR_PENDING_HUMAN_DECISION`。Gate 所需 canonical baseline 稍后从 V2.1 候选物化，active targets为40项。

`PRE_APPLY_AUDIT_INPUT_V4_AMENDED/` 必须包含原 V4 的 18 项原字节、上述 execution amendment、exact diff、tools/tests manifest；新的 outer manifest 覆盖除自身外全部文件。原 `governance-v2/` 和 G3 receipt 保持不变，不把此次修正伪装成原 G3 已审核内容。

#### D1.3 Decision proposal

候选固定：

- `issued_from_human=false`；
- `authority=PROPOSED_FOR_JOVI_ISSUANCE`；
- Hook DNT + 三 false；
- `manifest_apply_scope=["FRAMEWORK_MANIFEST.sha256"]`；
- `structural_remediation_scope` 精确为D1.2的十二个formal targets，另加单独`manifest_apply_scope`一个文件；
- `s1_closeout_scope` 精确为三个 state/mirror path，`s1_closeout_prerequisite="POST_APPLY_AUDIT_PASS"`；
- `commerce_transition_scope` 只声明候选工具和 Gate A.P 前置，不使用任何 `*_allowed=true`；
- `git_baseline_scope` 只声明 Gate A.P + C/APPLY 后可由 Jovi exact receipt 解锁；
- Track P/I、real platform actions 均 false；
- 绑定第 1.3 节全部 SHA；
- 绑定本计划 body SHA、sidecar SHA和 canonical plan path；
- 绑定原 G3 receipt、原 V2 candidate、V2.1 candidate、structural patch/target set、exact diff 和 amended review-package manifest SHA；
- 绑定 `apply_phase2b_structural_patch.py` SHA；
- 绑定 canonical governance mirror writer SHA；
- 绑定 closeout tool/patch/target set SHA；
- 绑定 hash-bound C/APPLY wrapper SHA；
- 绑定 Phase2B chain verifier、bound Gate receipt verifier 和 import source-selection generator SHA；
- 绑定 bound Gate Plan generator、Git baseline policy、proposed `.gitignore`/`.gitattributes` SHA；
- 绑定 Git baseline prepare/apply/approval/verify 四个工具 SHA，但明确它们只有 Gate A.P + C/APPLY 后才可使用；
- 绑定 binary-safe external Git blob importer SHA；
- 绑定 import-scope generator、expected-RED verifier、machine test recorder和dual-root binding writer SHA；
- closeout 仅允许在 Post-Apply Audit 独立 PASS 后执行；
- 禁止修改 `MANIFEST.sha256`。

候选本身不得出现 `issued_from_human=true`。

#### D1.4 `Issue-DecisionV3.ps1`

脚本必须：

- 只接受绝对 root、candidate path、expected candidate SHA、expected G3 SHA、review SHA 和 approver；
- 重新验证所有绑定文件；
- candidate 必须为 `issued_from_human=false`；
- 拒绝任何 Hook/Track/platform true；
- 拒绝 Decision 已存在；
- 显示精确 scope、SHA 和禁止动作；
- 要求 Jovi输入 `ISSUE DECISION V3 <candidate-sha前16位>`；
- 只有交互输入正确才将 formal body 写为 `issued_from_human=true`；
- 添加 `approver=Jovi`、真实 UTC、source proposal SHA、原 G3 SHA、execution-amendment review SHA；
- 原子写入正式 Decision 和 sidecar；
- 不创建 Gate、Approval 或修改 Manifest/控制面。

Luna永远不得运行非 `-ValidateOnly` 模式。

#### D1.5 Structural patch + Framework atomic apply tool

`apply_phase2b_structural_patch.py` 必须：

- 默认只检查；显式 `--apply` 才写；
- 验证 formal Decision、sidecar、G3、V2.1 candidate、exact diff、amendment review 和 tool 自身 SHA；
- structural scope 必须精确为十二个目标，manifest scope 必须精确为 `FRAMEWORK_MANIFEST.sha256`；
- 创建十三个目标的 exact old-byte backup 和 before snapshot；
- 先在 Shadow 物化 proposed structural bytes + V2.1 Manifest，运行全部 D1 tests、Security 20/20、S2A1、Commerce control transition、S1 integrity；
- `--apply` 时为十三个目标准备同目录临时文件，再受控替换；
- 逐项复算 Framework 40/40，运行 `validate-control-plane.py --root .`；
- Prompt 必须为 static pointer，canonical state仍为 `S1/CLOSED/1`；
- 验证 `MANIFEST.sha256`、Hook、Decision、Approval、canonical state、human-only 未变；
- 任一写入/验证失败恢复全部十三个 old bytes并输出 `ROLLED_BACK`。

#### D1.6 S1 closeout candidate/tool

基于 current state 生成精确三文件 after bytes：

- `state_revision=2`；
- 新 `state_id`；
- `previous_state_hash` 绑定当前 canonical state；
- 保持 `S1/CLOSED`、`permission_class=security-tightening`、`approval_binding=null`；
- blockers 变为 `[]`；
- `FORMAL_MANIFEST_MISMATCH` 由 Framework 40/40 + Post-Apply PASS 关闭；
- `HOOK_UNTRUSTED` 只改为 receipt 中的 accepted limitation，Hook 本体仍 DNT；
- canonical state、PROJECT_STATE、STATUS 具有一致 marker；Prompt SHA 必须保持 structural patch 后值。

`apply_s1_closeout.py` 必须检查：

- formal Decision 精确授权 closeout tool/patch/target；
- Framework 40/40；
- `MANIFEST.sha256` 未变；
- Post-Apply report/sidecar、`verdict=PASS`、`independent=true`；
- before SHA 仍匹配；
- Shadow 中 `control_plane.validate_transition` 和 mirror tests PASS；
- 仅三个目标原子写入；部分写失败恢复全部 before bytes。

因为 `CODEX_START_PROMPT.txt` 已变为 immutable pointer，closeout 完成后必须同时满足 Framework 40/40、Prompt SHA unchanged 和 control-plane mirrors PASS。禁止在 closeout 后再次重写 Framework Manifest。

#### D1.7 Hash-bound C/APPLY wrapper

现有 `apply_commerce_control_plane_transition.py` 只验证传入的 target/patch SHA 是 64 位十六进制，不读取对应对象；本计划不得直接把它作为最终写入口。新增 candidate wrapper `apply_commerce_control_plane_transition_bound.py`：

- 固定调用 canonical Gate Plan 和 canonical Gate A.P receipt；
- 接受并严格解析 target-set、control-evidence-target-set、scope-patch、source-selection、baseline-policy 及各自 sidecar，而不是裸 SHA；
- 拒绝未知字段、非 canonical path、sidecar 格式错误或任一对象缺失；
- 逐项断言上述对象、proposed `.gitignore`/`.gitattributes` SHA、83-file manifest body SHA/blob OID、object-repo observed HEAD、implementation/evidence commit 都与**已获批 Gate Plan 的 bindings 完全相等**；不得把调用者提供的新对象 SHA写入状态冒充已批准对象；
- target set 只允许 D7.2 列出的 Commerce 本地路径；control evidence target只允许 control root的 review-queue精确前缀；
- scope patch 只能描述 `S1/CLOSED -> C/APPLY`；
- receipt 必须先由现有 `verify-gate-approval.py` 和新增 `verify_gate_a_p_bound.py` 同时验证；bound verifier要求 `schema_version=2`、exact keys、gate=`GATE_A`、track=`P`、approver=`Jovi`、canonical absolute plan path、plan SHA、可解析带时区时间、P=`AWAITING_HUMAN_APPROVAL`、I.status=`BLOCKED`、I.next_phase=`NOT_AUTHORIZED`、全部 real actions=false；
- wrapper 必须从 Plan bindings 派生传给底层的 target/patch SHA，禁止直接采用 CLI 裸值；同时绑定 current state SHA、S1 closeout receipt SHA 和唯一 transition tuple；
- 调用现有 `build_transition()` / `apply_transition_files()`，不复制状态机逻辑；
- dry-run 输出 exact before/after；`--apply` 后输出 transition receipt；
- 写后要求 Framework 40/40、Prompt SHA unchanged、control-plane mirrors PASS；
- 任一失败恢复三个 state/mirror before bytes。

#### D1.8 Bound Gate Plan generator 与 Git baseline policy

现有 `generate_gate_a_plan.py` 不绑定 import target/patch 或 Git baseline，而且在 Approval 不存在时可覆盖已有 plan。本计划新增 candidate wrapper `generate_gate_a_plan_bound.py`：

- 在同一稳定读取窗口先显式运行Gate readiness的`pre-gate`模式，再调用保持原字节的现有`build_plan(root)`；其内部`readiness_errors(root)`按受审库接口安全默认仍为pre-gate。随后强制运行`verify_phase2b_governance_chain.py --phase post-closeout`；三者任一失败不得生成 Plan；
- 冻结 `GATE_CHAIN_INPUT_SNAPSHOT.json` + sidecar，绑定 chain verifier自身 SHA、chain report SHA、输入快照 SHA；生成前后任一输入 SHA变化即失败；
- 仅当 canonical Gate Plan 和 sidecar都不存在时写入；使用同目录临时 body/sidecar、双重复算和受控 replace，写第二个文件失败时清理临时文件并恢复到“两者均不存在”，不得留下永久半成品；
- 把 `COMMERCE_IMPORT_TARGET_SET_V1.json`、`CONTROL_EVIDENCE_TARGET_SET_V1.json`、`COMMERCE_IMPORT_SCOPE_PATCH_V1.json`、`IMPORT_SOURCE_SELECTION_V1.json`、`GIT_BASELINE_POLICY_V1.json`、proposed `.gitignore`、proposed `.gitattributes`、外置 object-repo observed HEAD、evidence/implementation commit、83-file manifest body SHA/blob OID加入 `bindings`；
- Track P actions 明确包含“local no-remote Git baseline”“hash-bound Commerce import”“synthetic X2”；
- Track I的 `status` 必须为 `BLOCKED`、`next_phase` 必须为 `NOT_AUTHORIZED`，从而当前 human-only脚本即使误传 `-Track I` 也会拒绝；五项真实平台动作必须 false；
- 生成 canonical plan + sidecar 后立即只读冻结。

`GIT_BASELINE_POLICY_V1.json` 在 Decision 前冻结规则；具体 `GIT_BASELINE_FILES_V1.txt` 和 manifest 在 C/APPLY 后根据最终真实树生成。proposed `.gitignore`/`.gitattributes` 字节在 D1 冻结，`.gitattributes` 固定 `* -text`，避免再次发生 checkout 换行改变审计字节。Policy必须把当前 `.gitignore` 记录为 `REPLACE_WITH_APPROVED_BYTES`、before SHA=`6879e1723cf111c34377003f5f0d1c3da0167768b174b9efeaee8a3475216bf4`、before length=284、after为D1 proposed bytes；`.gitattributes` 记录为 `CREATE_FROM_APPROVED_BYTES`、before=`ABSENT`、after=`* -text`的精确 proposed bytes。

`prepare_import_source_selection.py` 必须从外置 Git objects构造严格清单，而不是读取checkout bytes：

- `source_object_repo=E:\project\jovi-commerce-engine-v1`，单独记录object repo observed HEAD=`3b31f0f2f240038aa261db5c57c43e5e14992dc5`；
- `source_evidence_worktree=E:\project\jovi-commerce-engine-v1\.worktrees\landing-phase1`，要求HEAD=`7dbe080c907c1da2eef1c16b79e677e6a1d49470`、clean、remote empty；
- implementation commit=`fd2321d5a3f12aa923014cadbc397849903fd97c`、evidence commit=`7dbe080c907c1da2eef1c16b79e677e6a1d49470`，并证明祖先关系；
- 83项 implementation snapshot逐项记录 `record_id/source_role/group/disposition/source_commit/source_path/source_blob_oid/source_mode/source_size/source_sha256/target_root_role/target_relative_path/expected_target_sha256/reason`，精确49项 `IMPORT`（17 tests + 32 implementation）、34项 `RECORD_ONLY_EXCLUDE`；
- evidence commit仅允许10个 `reports/product` body/sidecar新增 blobs进入 `evidence` group，逐项使用同样字段，target root role固定为 `CONTROL_ROOT_REVIEW_QUEUE`；不得导入该commit修改的 `CHANGELOG.md`、`CURRENT_STATUS.md` 或 `tasks/todo.md`；
- group只能为 `tests`、`implementation`、`evidence`；34个排除项target字段必须为null；所有import行必须被三个互斥group全量覆盖；
- 绑定external manifest body SHA=`4090c6963b19705cc401336df6f3a0f7a31a97a650cff517cc9cb7d83c94a4f0`、blob OID=`dd4a55426771c4fb10bb55e6ff1e84fc8001b953`与内部candidate binding=`155f01b83211275b560c3482f8e98cea24e5e889367b87468c03d33d5325854e`，字段语义不得互换。

`import_external_git_blobs.py` 的任何 group 在解析、打开或创建任一 target path **之前**，必须在同一稳定读取窗口完成以下前置校验；任一失败时 `target_access_count=0`、`target_write_count=0`，且不创建 staging 目录：

1. importer 自身 SHA 等于 formal Decision 与 Gate Plan 中的同名 binding；
2. 现有 `verify-gate-approval.py --gate GATE_A --track P` 和新的 `verify_gate_a_p_bound.py` 均 PASS；
3. canonical control plane 已是 `C/APPLY`，`CONTROL_PLANE_TRANSITION_RECEIPT.json` body/sidecar匹配，并绑定当前 Gate Plan SHA；
4. Gate Plan 中的 source selection、import target、scope patch、control evidence、baseline policy、`.gitignore`、`.gitattributes`、外置 commits和blob manifest bindings均与传入对象逐项相等；
5. `GIT_BASELINE_ESTABLISHMENT.json` body/sidecar、root commit、index/tree、feature branch ancestry、clean state与无remote约束均匹配；
6. 校验前后 Decision、Plan、Gate receipt、transition receipt、baseline establishment和selection SHA保持稳定。

只有这六项全部成立，importer 才能检查该 group 的 target absence/允许状态并进入临时 staging。不能用调用方已运行过 validator 代替 importer 自身的 fail-closed 前置。

`Approve-GitBaseline.ps1` 必须只接受 absolute root、exact baseline manifest path/SHA、policy SHA 和 approver；交互显示文件数、排除项、秘密扫描结论、remote-empty 约束和 SHA 前16位。Jovi精确确认后，它只写 `workspace/approvals/GIT_BASELINE.V1.approval.json`，不得运行 `git init` 或写任何被纳入 baseline 的文件。`verify_git_baseline_approval.py` 重新复算 manifest/policy/receipt。

#### D1.9 Phase2B chain verifier

`verify_phase2b_governance_chain.py` 是 Gate readiness 的附加 fail-closed 校验，不替代现有 validator。它提供 `pre-decision`、`post-closeout`、`post-transition` 三个明确模式，必须核验 G3 sidecar、V2→V2.1 exact diff、amendment review sidecar、formal Decision bindings、Framework 40/40、Post-Apply report sidecar、S1 closeout receipt、Hook DNT。`post-closeout` 不再错误要求原 Final Target Set 13/13 当前字节不变，而是要求所有差异都由 Decision-bound closeout before/after SHA 和 receipt 解释；`post-transition` 再要求 strict Gate receipt、Gate Plan bindings和transition receipt解释三个 state/mirror文件的第二次变化。任何额外差异仍失败。Decision必须显式绑定该verifier SHA。D4之后所有会写正式树、Git或import目标的review-queue executor，启动后必须先读取Decision/Plan binding并自验自身SHA；D1/D2的pre-Decision validate-only测试则由Human Action Package manifest和D2 audit绑定，不错误要求尚不存在的formal Decision。

#### D1.10 TDD

```powershell
py -3.12 -B -m unittest discover `
  -s .\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action\tests `
  -v
if ($LASTEXITCODE -ne 0) { throw 'Human Action Package tests failed' }
```

必须覆盖：

- 错误/缺失 G3；
- candidate SHA 漂移；
- candidate 伪造 `issued_from_human=true`；
- Hook/Track/platform 任一 true；
- Decision 重复签发；
- Manifest scope 扩大；
- V2.1 与 V2 的差异不是精确 `0 removed + 19 added + 2 modified(Prompt, MANIFEST_POLICY)`；
- Prompt 仍含 revision marker、未由 Framework 全字节保护或 static authority pointer 缺失；
- Framework candidate 漂移；
- `MANIFEST.sha256` 改变；
- Post-Apply 缺失/FAIL/非独立；
- closeout before 漂移；
- 部分写回滚；
- exact replay fail-closed；
- target/patch 只有裸 SHA、不存在对应对象；
- target set 多出 `products/`、human-only 或外部路径；
- C/APPLY 后 Framework 或 mirror 任一失配；
- Gate Plan 未绑定 import target/patch/baseline；
- Gate Plan 已存在时被覆盖；
- `Approve-Gate.ps1` 被计划成 Track I 或任意非 P track；
- Gate receipt存在未知字段、非Jovi approver、非canonical plan path、时间非法、I未BLOCKED或real action不为false；
- chain report未在Gate生成的同一稳定读取窗口重算并绑定；
- source selection不是83项完整disposition + 10项精确evidence blobs，或混淆object repo/evidence worktree；
- Policy嵌入新Framework body SHA或形成任何manifest↔policy自引用；
- canonical mirror writer目标半成品、overwrite或source→target SHA不一致；
- expected-RED存在缺包以外错误却被接受；
- dual-root binding在最终feature commit前生成、漏绑tested/final两个HEAD或允许审核后feature变化；
- baseline 在 proposed `.gitignore`/`.gitattributes` 写入后漂移；
- baseline receipt 缺失、错误 SHA、非 Jovi 或重复创建；
- Git index blob 与 approved baseline 任一不一致；
- importer 从 Windows checkout 而不是固定 commit object 取字节；
- importer 遇到缺失/过期 Gate receipt、非 `C/APPLY`、错误 transition receipt、错误 Gate Plan binding或错误 baseline establishment时，在任何target resolve/open/write之前失败且目标树零变化；
- importer 各group receipt缺失、重放payload不同、group越界或receipt与实际写入集合不一致；
- expected-RED只检查unit而漏掉acceptance，或任一suite未收集测试却被判合格；
- Gate readiness CLI缺少phase却通过、库接口默认不是pre-gate、或未修改的`build_plan(root)`无法在pre-gate fixture生成候选。

`HUMAN_ACTION_PACKAGE_MANIFEST.json`在D1最后生成，覆盖本目录中除自身及其sidecar外的全部候选文件、相对路径、长度和SHA；它的顶层bindings必须包含本计划body/sidecar SHA、G3 receipt SHA、D0 `RESUME_PREFLIGHT.json` body/sidecar SHA，以及RESUME索引列出的plan、runner、test、PREDECISION和另外三份报告全部body/sidecar SHA。Package generator必须重新计算每一成员，禁止只信RESUME内的字符串。随后以单独sidecar绑定manifest body。D2必须先验证plan sidecar和Package Manifest，再开始语义审核；计划body变化会使整个人类动作包与D2结论立即失效。

**成功状态：** `HUMAN_ACTION_PACKAGE_CANDIDATE_READY`。

---

### D2 — Fresh Phase2B Pre-Decision Amendment Audit

由未参与 D1 的新 Agent只读审核并写：

```text
workspace/review-queue/commerce-v1/decision-to-main-x2/human-action/
PHASE2B_PREDECISION_AMENDMENT_AUDIT.json
PHASE2B_PREDECISION_AMENDMENT_AUDIT.json.sha256.sidecar
```

结论仅允许 `PASS_READY_FOR_JOVI_DECISION_V3` 或 `FAIL`。

审核至少确认：

- 本计划body/sidecar、D0 runner/test及四份preflight报告均匹配Human Action Package bindings，D0不存在部分发布或伪造当前输入；
- 原 G3/V4/候选 SHA 未漂移，原报告没有被改写；
- V2→V2.1 精确为 `0 removed + 19 added + 2 modified(Prompt, MANIFEST_POLICY)`；Prompt变成 immutable static pointer，Policy只增加一次性、精确 old→new、Decision+独审绑定的迁移例外；
- amended review package 全量 SHA 匹配；
- registry/validator 明确区分 immutable Prompt 与 revisioned mirrors，Framework 对 Prompt 任意字节篡改真实 fail-closed；
- proposed Decision 仍为 false；
- human script 只能交互式写正式 Decision；
- Luna无法用 `-ValidateOnly` 产生正式 Decision；
- structural apply精确写十二个受审字节，Manifest portion仅写一个`FRAMEWORK_MANIFEST.sha256`；
- closeout tool 仅写三文件且强制 Post-Apply PASS；
- bound transition 读取并验证 target/patch 对象，不接受裸 SHA 冒充授权；
- bound transition逐项要求 target/patch/source-selection/control-evidence/baseline-policy/dotfiles/blob-manifest/commits等于获批 Plan bindings；
- bound Gate Plan在同一稳定读取窗口运行并绑定Phase2B chain verifier、chain report和输入快照，并在Jovi批准前绑定import scope和Git baseline policy；
- strict Gate receipt verifier要求P-only、Jovi、schema 2、exact keys、canonical path、I BLOCKED/NOT_AUTHORIZED和real actions false；
- canonical mirror writer no-overwrite、原子发布、source→target全量SHA和失败零半成品；
- Git baseline approval script 只确认 C/APPLY 后生成的 exact manifest，不执行 Git；
- source selection为83项完整 disposition（49 import/34 exclude）+ 10项精确 evidence blobs，且object repo与evidence worktree语义分离；
- machine recorder、expected-RED verifier和dual-root writer均使用精确输入、sidecar、非零fail-closed且不修改feature；
- rollback、重复执行、错误 SHA 均 fail-closed；
- 没有 Track P/I、Hook trust 或平台授权。

**成功结论只允许：** `PASS_READY_FOR_JOVI_DECISION_V3` 或 `FAIL`。

**成功状态：** `STATIC_PROMPT_STRUCTURAL_REMEDIATION_REVIEW_PASS` + `HUMAN_ACTION_PACKAGE_REVIEW_PASS`。

FAIL 时仅修复精确 finding，重跑全套测试并由同一 reviewer scoped re-review；任何字节变化使旧 review SHA 失效。

---

### D3 — Jovi一次签发 Decision V3

#### D3.1 Jovi命令

Luna输出以下变量已解析后的命令，但不运行。Jovi在主工程 PowerShell 中运行：

```powershell
$actionRoot = Resolve-Path .\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action
$candidateSha = ((Get-Content -Raw -Encoding ASCII `
  "$actionRoot\DECISION_V3_PROPOSED.json.sha256.sidecar").Trim() -split '\s+')[0]
$reviewSha = (Get-FileHash -Algorithm SHA256 `
  "$actionRoot\PHASE2B_PREDECISION_AMENDMENT_AUDIT.json").Hash.ToLowerInvariant()

powershell -NoProfile -File "$actionRoot\Issue-DecisionV3.ps1" `
  -Root (Get-Location).Path `
  -CandidatePath "$actionRoot\DECISION_V3_PROPOSED.json" `
  -ExpectedCandidateSha256 $candidateSha `
  -ExpectedG3Sha256 c92682c9d58f702ac5249cb2387f87999c41a8d17d79b20a0ec210e125a36686 `
  -ExpectedReviewSha256 $reviewSha `
  -Approver Jovi
if ($LASTEXITCODE -ne 0) { throw 'Jovi Decision V3 issuance failed' }
```

Jovi输入脚本显示的精确确认短语。

#### D3.2 Luna只读验证

```text
workspace/decisions/JOVI_S1_RESTART_DECISION_V3.json
workspace/decisions/JOVI_S1_RESTART_DECISION_V3.json.sha256.sidecar
```

运行 candidate `verify_decision_v3.py` 和 Gate validator 的 Decision 子检查。必须确认：

- body/sidecar；
- `issued_from_human=true`；
- approver/UTC；
- G3、original V2、V2.1、proposal、amendment review、tool、patch、target、baseline policy bindings；
- manifest scope 只有 Framework；
- Hook 三 false；
- Track P/I、platform false。

**成功状态：** `DECISION_V3_ISSUED`。

失败状态 `BLOCKED_DECISION_V3_INVALID`；Luna不得修补人类 Decision。

---

### D4 — Canonical mirror 与 exact Structural+Manifest APPLY

#### D4.1 Canonical mirror

当前 `workspace/review-queue/commerce-v1/governance/` 不存在，Gate validator却固定读取它。本任务显式创建，不再假设存在。

从 D1/D2 已审核的 V2.1/amended package 物化到 validator 要求的 canonical 文件名：

```text
CONTROLLED_BASELINE_V2_CANDIDATE.json
CONTROLLED_BASELINE_V2_CANDIDATE.sha256
PRE_APPLY_AUDIT_INPUT_V4/**
```

映射固定为：V2.1 baseline → canonical V2 filename；`PRE_APPLY_AUDIT_INPUT_V4_AMENDED/**` → canonical V4 directory。原`governance-v2/`只作为历史G3输入保持不变。物化只能使用Decision-bound `materialize_governance_canonical_mirror.py`：它先自验tool SHA、Decision、D2 audit和source sidecars；目标已存在时只允许完整集合100%相同，不一致即拒绝覆盖；目标不存在时先写独占临时目录、全量复算，再一次rename发布，禁止逐文件暴露半成品。

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$actionRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action").Path
py -3.12 -B "$actionRoot\materialize_governance_canonical_mirror.py" `
  --root $controlRoot `
  --decision "$controlRoot\workspace\decisions\JOVI_S1_RESTART_DECISION_V3.json" `
  --source "$actionRoot" `
  --target "$controlRoot\workspace\review-queue\commerce-v1\governance" `
  --apply
if ($LASTEXITCODE -ne 0) { throw 'canonical governance mirror materialization failed' }
```

输出`CANONICAL_MIRROR_MATERIALIZATION.json`和sidecar，逐项记录source→target path/SHA/size及“canonical name retained for existing validator compatibility”。失败时目标必须保持不存在或保持原有完全相同字节。

#### D4.2 APPLY

先运行 `apply_phase2b_structural_patch.py --check`；PASS 后再运行同一工具 `--apply`。这是 Decision 精确列出的十二文件 structural remediation + 单文件 Manifest apply，不是 Track P 产品写入，也不得扩展到第十四个目标。

**验收：**

```text
FRAMEWORK_MANIFEST 40/40
CODEX_START_PROMPT immutable static pointer and byte-matched
structural patch targets 12/12 exact proposed bytes
MANIFEST.sha256 unchanged
Hook unchanged and DNT
Decision unchanged
Approval absent
control plane still S1/CLOSED/1
```

输出 apply report、old-byte backup、before/after snapshot、sidecars。

**成功状态：** `PHASE2B_STRUCTURAL_REMEDIATION_APPLIED` + `FRAMEWORK_MANIFEST_V2_1_APPLIED`。

---

### D5 — 全新 Post-Apply Audit

由新的独立 Agent直接审核真实树，不信任 Luna 的 PASS 汇总。它必须写：

```text
reports/remediation/COMMERCE_V1_POST_APPLY_AUDIT.json
reports/remediation/COMMERCE_V1_POST_APPLY_AUDIT.json.sha256.sidecar
```

最低要求：

- `verdict=PASS`；
- `independent=true`；
- Framework 40/40；
- Prompt 位于 Framework 中且 static authority pointer/全文 SHA 匹配；
- structural patch 12/12 与 Decision/amendment audit bytes一致；
- `MANIFEST.sha256` unchanged；
- Hook DNT；
- Decision/G3/amendment review/V2.1/apply report SHA 链；
- state 仍 S1/CLOSED/1；
- Gate/Approval/Commerce runtime 尚不存在；
- real platform actions false。

**成功状态：** `POST_APPLY_AUDIT_PASS`。

FAIL 时只修复报告精确 finding；涉及 Framework 字节时重新 APPLY、重新 Post-Apply，不复用旧 PASS。

---

### D6 — 应用 Decision 授权的 S1 closeout

运行 `apply_s1_closeout.py --check`；必须同时验证 Decision、Post-Apply、Framework、before state、patch 和 tool SHA。

CHECK PASS 后运行 `--apply`。工具只允许且必须恰好写：

```text
config/control-plane-state.json
PROJECT_STATE.json
STATUS.md
```

`CODEX_START_PROMPT.txt` 必须保持 structural patch 后 SHA完全不变。工具若尝试打开Prompt写句柄、Prompt SHA变化或receipt把Prompt计入changed targets，立即回滚三个文件并失败。

输出 `S1_CLOSEOUT_RECEIPT.json`，绑定 Decision、Post-Apply、before/after state、三文件 before/after SHA、`changed_target_count=3`、`prompt_disposition=VERIFIED_UNCHANGED`、Prompt unchanged SHA和accepted Hook limitation。

随后运行：

```powershell
py -3.12 -B .\scripts\validate-control-plane.py --root .
if ($LASTEXITCODE -ne 0) { throw 'control-plane mirror validation failed after closeout' }
py -3.12 -B .\tests\test_s2a1_control_plane.py
if ($LASTEXITCODE -ne 0) { throw 'S2A1 control-plane tests failed after closeout' }
py -3.12 -B .\tests\test_control_plane_commerce_transition.py
if ($LASTEXITCODE -ne 0) { throw 'Commerce transition tests failed after closeout' }
```

closeout 后额外运行 `validate_commerce_gate_readiness.py --phase pre-gate` 的 Framework 子检查，必须仍为 40/40；不得再产生 Manifest refresh 或第二次 re-baseline。

**成功状态：**

```text
S1_CLOSED_CLEAN
CONTROL_PLANE_BLOCKERS_EMPTY
HOOK_DNT_ACCEPTED_LIMITATION
```

---

### D7 — Gate readiness 与第二次人工作用 Gate A.P

#### D7.1 Readiness

```powershell
$actionRoot = (Resolve-Path .\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action).Path
py -3.12 -B "$actionRoot\verify_phase2b_governance_chain.py" `
  --root . `
  --phase post-closeout `
  --output .\workspace\review-queue\commerce-v1\decision-to-main-x2\PHASE2B_CHAIN.json
if ($LASTEXITCODE -ne 0) { throw 'Phase2B post-closeout chain verification failed' }

py -3.12 -B .\scripts\validate_commerce_gate_readiness.py `
  --root . `
  --phase pre-gate `
  --output .\workspace\review-queue\commerce-v1\decision-to-main-x2\GATE_READINESS.json
if ($LASTEXITCODE -ne 0) { throw 'Commerce Gate readiness failed' }
```

两者必须同时 PASS。现有 Gate validator 的 PASS 不能替代 Phase2B chain verifier 对 G3、Decision bindings、Post-Apply sidecar 和 V2.1 amendment 的检查。

#### D7.2 在 Gate Plan 前冻结 import scope

生成并冻结：

```text
workspace/review-queue/commerce-v1/decision-to-main-x2/import-scope/
├── COMMERCE_IMPORT_TARGET_SET_V1.json
├── COMMERCE_IMPORT_TARGET_SET_V1.json.sha256.sidecar
├── CONTROL_EVIDENCE_TARGET_SET_V1.json
├── CONTROL_EVIDENCE_TARGET_SET_V1.json.sha256.sidecar
├── COMMERCE_IMPORT_SCOPE_PATCH_V1.json
├── COMMERCE_IMPORT_SCOPE_PATCH_V1.json.sha256.sidecar
├── IMPORT_SOURCE_SELECTION_V1.json
└── IMPORT_SOURCE_SELECTION_V1.json.sha256.sidecar
```

不得手工拼接这些对象。使用D1/D2已审核的scope generator；它内部调用`prepare_import_source_selection.py`并原子写完整目录：

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$actionRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action").Path
$importScopeRoot = "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope"
if (Test-Path -LiteralPath $importScopeRoot) { throw "import-scope target already exists: $importScopeRoot" }
py -3.12 -B "$actionRoot\prepare_import_scope.py" `
  --root $controlRoot `
  --source-object-repo E:\project\jovi-commerce-engine-v1 `
  --source-evidence-worktree E:\project\jovi-commerce-engine-v1\.worktrees\landing-phase1 `
  --implementation-commit fd2321d5a3f12aa923014cadbc397849903fd97c `
  --evidence-commit 7dbe080c907c1da2eef1c16b79e677e6a1d49470 `
  --external-manifest-sha256 4090c6963b19705cc401336df6f3a0f7a31a97a650cff517cc9cb7d83c94a4f0 `
  --external-manifest-blob-oid dd4a55426771c4fb10bb55e6ff1e84fc8001b953 `
  --baseline-policy "$actionRoot\GIT_BASELINE_POLICY_V1.json" `
  --baseline-policy-sidecar "$actionRoot\GIT_BASELINE_POLICY_V1.json.sha256.sidecar" `
  --output $importScopeRoot
if ($LASTEXITCODE -ne 0) { throw 'import scope generation failed' }
```

Generator必须把全部body/sidecar写到同目录临时树，验证集合、schema和SHA后再rename发布；失败时`import-scope`保持不存在。

允许目标仅为：

```text
jovi_commerce/**
docs/commerce/**
docs/commerce/evidence/import-phase2/**
schemas/commerce/**
tests/commerce/**
tests/fixtures/commerce/synthetic-digital-checklist/**
pyproject.toml
.gitignore
.gitattributes
```

`COMMERCE_IMPORT_TARGET_SET_V1.json` 明确排除 products、Hook、Manifest、Decision、Approval、human-only、外部闲鱼、runtime DB和真实数据。`CONTROL_EVIDENCE_TARGET_SET_V1.json` 不是Track P正式路径授权，只允许 control root中的：

```text
workspace/review-queue/commerce-v1/decision-to-main-x2/external-evidence/**
```

`IMPORT_SOURCE_SELECTION_V1.json` 必须由已审核 generator从Git objects生成，总计93行并100%覆盖：

```text
83 implementation snapshot rows
  = 49 IMPORT
      = 17 tests
      + 32 implementation
    + 34 RECORD_ONLY_EXCLUDE

10 evidence IMPORT rows
  = 5 body/sidecar pairs
```

10个 evidence source path固定为：

```text
reports/product/IMPORT_CANDIDATE_MANIFEST.json
reports/product/IMPORT_CANDIDATE_MANIFEST.json.sha256.sidecar
reports/product/S9_INDEPENDENT_REVIEW.md
reports/product/S9_INDEPENDENT_REVIEW.md.sha256.sidecar
reports/product/SOURCE_NONMUTATION.json
reports/product/SOURCE_NONMUTATION.json.sha256.sidecar
reports/product/TEST_RESULTS.json
reports/product/TEST_RESULTS.json.sha256.sidecar
reports/product/X2_ACCEPTANCE.json
reports/product/X2_ACCEPTANCE.json.sha256.sidecar
```

每行必须包含：

```text
record_id
source_role
group
disposition
source_commit
source_path
source_blob_oid
source_mode
source_size
source_sha256
target_root_role
target_relative_path
expected_target_sha256
reason
```

`group` 只能为 `tests/implementation/evidence`；34个排除项target字段必须为null；tests/implementation只允许`FEATURE_ROOT`，evidence只允许`CONTROL_ROOT_REVIEW_QUEUE`。重复target、大小写碰撞、非普通blob mode、未知字段、路径逃逸或计数不符均失败。

全部import scope对象还必须绑定：object repo observed HEAD `3b31f0f2f240038aa261db5c57c43e5e14992dc5`、evidence worktree/commit `7dbe080c907c1da2eef1c16b79e677e6a1d49470`、implementation commit `fd2321d5a3f12aa923014cadbc397849903fd97c`、祖先关系、83-file manifest body SHA `4090c6963b19705cc401336df6f3a0f7a31a97a650cff517cc9cb7d83c94a4f0`、blob OID `dd4a55426771c4fb10bb55e6ff1e84fc8001b953`、内部candidate binding `155f01b83211275b560c3482f8e98cea24e5e889367b87468c03d33d5325854e`和`GIT_BASELINE_POLICY_V1.json`。

#### D7.3 Bound Gate Plan

```powershell
$actionRoot = (Resolve-Path .\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action).Path
$targetSet = (Resolve-Path .\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope\COMMERCE_IMPORT_TARGET_SET_V1.json).Path
$controlEvidenceSet = (Resolve-Path .\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope\CONTROL_EVIDENCE_TARGET_SET_V1.json).Path
$scopePatch = (Resolve-Path .\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope\COMMERCE_IMPORT_SCOPE_PATCH_V1.json).Path
$sourceSelection = (Resolve-Path .\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope\IMPORT_SOURCE_SELECTION_V1.json).Path
py -3.12 -B "$actionRoot\generate_gate_a_plan_bound.py" `
  --root . `
  --target-set $targetSet `
  --control-evidence-target-set $controlEvidenceSet `
  --scope-patch $scopePatch `
  --source-selection $sourceSelection `
  --baseline-policy "$actionRoot\GIT_BASELINE_POLICY_V1.json" `
  --baseline-policy-sidecar "$actionRoot\GIT_BASELINE_POLICY_V1.json.sha256.sidecar" `
  --source-object-repo E:\project\jovi-commerce-engine-v1 `
  --source-object-repo-observed-head 3b31f0f2f240038aa261db5c57c43e5e14992dc5 `
  --external-evidence-commit 7dbe080c907c1da2eef1c16b79e677e6a1d49470 `
  --external-implementation-commit fd2321d5a3f12aa923014cadbc397849903fd97c `
  --external-manifest-sha256 4090c6963b19705cc401336df6f3a0f7a31a97a650cff517cc9cb7d83c94a4f0 `
  --external-manifest-blob-oid dd4a55426771c4fb10bb55e6ff1e84fc8001b953
if ($LASTEXITCODE -ne 0) { throw 'bound Gate Plan generation failed' }
```

只生成一次：

```text
reports/gates/GATE_A_PLAN.json
reports/gates/GATE_A_PLAN.sha256.txt
```

Luna验证 Track P=`AWAITING_HUMAN_APPROVAL`、Track I.status=`BLOCKED`、Track I.next_phase=`NOT_AUTHORIZED`、real actions=false，并复算 target set、control evidence set、scope patch、source selection、baseline policy、chain input snapshot、chain report和external object bindings。禁止直接调用未绑定这些对象的原 `generate_gate_a_plan.py` 写 canonical plan。

#### D7.4 Jovi运行现有 human-only

```powershell
$gateSha = (Get-Content -Raw -Encoding ASCII `
  .\reports\gates\GATE_A_PLAN.sha256.txt).Trim()

powershell -NoProfile -File .\scripts\human-only\Approve-Gate.ps1 `
  -Gate GATE_A `
  -Track P `
  -PlanPath .\reports\gates\GATE_A_PLAN.json `
  -ExpectedSha256 $gateSha `
  -Approver Jovi
if ($LASTEXITCODE -ne 0) { throw 'Jovi Gate A.P approval script failed' }
```

Jovi输入 Gate SHA 前 16 位；Luna不得运行。

#### D7.5 Luna验证

```powershell
py -3.12 -B .\scripts\verify-gate-approval.py `
  --root . --gate GATE_A --track P
if ($LASTEXITCODE -ne 0) { throw 'legacy Gate receipt verification failed' }

$actionRoot = (Resolve-Path .\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action).Path
py -3.12 -B "$actionRoot\verify_gate_a_p_bound.py" `
  --root . `
  --plan .\reports\gates\GATE_A_PLAN.json `
  --receipt .\workspace\approvals\GATE_A.P.approval.json
if ($LASTEXITCODE -ne 0) { throw 'strict bound Gate receipt verification failed' }
```

**成功状态：** `GATE_A_P_VERIFIED`。

---

### D8 — 哈希绑定转换到 C/APPLY

先 dry-run：

```powershell
$actionRoot = (Resolve-Path .\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action).Path
$importScopeRoot = (Resolve-Path .\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope).Path
$targetSet = Join-Path $importScopeRoot 'COMMERCE_IMPORT_TARGET_SET_V1.json'
$controlEvidenceSet = Join-Path $importScopeRoot 'CONTROL_EVIDENCE_TARGET_SET_V1.json'
$scopePatch = Join-Path $importScopeRoot 'COMMERCE_IMPORT_SCOPE_PATCH_V1.json'
$sourceSelection = Join-Path $importScopeRoot 'IMPORT_SOURCE_SELECTION_V1.json'
$targetSetSidecar = "$targetSet.sha256.sidecar"
$controlEvidenceSetSidecar = "$controlEvidenceSet.sha256.sidecar"
$scopePatchSidecar = "$scopePatch.sha256.sidecar"
$sourceSelectionSidecar = "$sourceSelection.sha256.sidecar"
py -3.12 -B "$actionRoot\apply_commerce_control_plane_transition_bound.py" `
  --root . `
  --plan .\reports\gates\GATE_A_PLAN.json `
  --receipt .\workspace\approvals\GATE_A.P.approval.json `
  --target-set $targetSet `
  --target-set-sidecar $targetSetSidecar `
  --control-evidence-target-set $controlEvidenceSet `
  --control-evidence-target-set-sidecar $controlEvidenceSetSidecar `
  --scope-patch $scopePatch `
  --scope-patch-sidecar $scopePatchSidecar `
  --source-selection $sourceSelection `
  --source-selection-sidecar $sourceSelectionSidecar `
  --baseline-policy "$actionRoot\GIT_BASELINE_POLICY_V1.json" `
  --baseline-policy-sidecar "$actionRoot\GIT_BASELINE_POLICY_V1.json.sha256.sidecar"
if ($LASTEXITCODE -ne 0) { throw 'bound C/APPLY dry-run failed' }
```

dry-run为`READY_TO_APPLY`后，使用独立变量重新解析的apply代码块：

```powershell
$actionRoot = (Resolve-Path .\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action).Path
$importScopeRoot = (Resolve-Path .\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope).Path
$targetSet = Join-Path $importScopeRoot 'COMMERCE_IMPORT_TARGET_SET_V1.json'
$controlEvidenceSet = Join-Path $importScopeRoot 'CONTROL_EVIDENCE_TARGET_SET_V1.json'
$scopePatch = Join-Path $importScopeRoot 'COMMERCE_IMPORT_SCOPE_PATCH_V1.json'
$sourceSelection = Join-Path $importScopeRoot 'IMPORT_SOURCE_SELECTION_V1.json'
py -3.12 -B "$actionRoot\apply_commerce_control_plane_transition_bound.py" `
  --root . `
  --plan .\reports\gates\GATE_A_PLAN.json `
  --receipt .\workspace\approvals\GATE_A.P.approval.json `
  --target-set $targetSet `
  --target-set-sidecar "$targetSet.sha256.sidecar" `
  --control-evidence-target-set $controlEvidenceSet `
  --control-evidence-target-set-sidecar "$controlEvidenceSet.sha256.sidecar" `
  --scope-patch $scopePatch `
  --scope-patch-sidecar "$scopePatch.sha256.sidecar" `
  --source-selection $sourceSelection `
  --source-selection-sidecar "$sourceSelection.sha256.sidecar" `
  --baseline-policy "$actionRoot\GIT_BASELINE_POLICY_V1.json" `
  --baseline-policy-sidecar "$actionRoot\GIT_BASELINE_POLICY_V1.json.sha256.sidecar" `
  --apply
if ($LASTEXITCODE -ne 0) { throw 'bound C/APPLY failed' }
```

写后必须原子生成`workspace/review-queue/commerce-v1/decision-to-main-x2/CONTROL_PLANE_TRANSITION_RECEIPT.json`及sidecar，并运行`validate-control-plane.py --root .`、Framework 40/40、strict Gate receipt verifier和Phase2B chain verifier的post-transition模式；`CODEX_START_PROMPT.txt` SHA必须完全不变。

**成功状态：** `CONTROL_PLANE_C_APPLY`。

---

## 7. Track B：主工程导入与 X2

### D9 — 主工程本地 Git baseline

**前置：** Gate A.P verified + C/APPLY。

当前 `.git` 为空且无有效 HEAD；不得把它称为现有仓库。

#### D9.1 C/APPLY 后生成 exact baseline candidate

生成：

```text
workspace/review-queue/commerce-v1/decision-to-main-x2/git-baseline/
├── GIT_BASELINE_FILES_V1.txt
├── GIT_BASELINE_PATHS_V1.nul
├── GIT_BASELINE_MANIFEST_V1.json
├── GIT_BASELINE_MANIFEST_V1.json.sha256.sidecar
├── SECRET_SCAN_REPORT_V1.json
├── GIT_BASELINE_REVIEW.md
└── PROTECTED_TREE_BEFORE_GIT.json
```

由 D1 已审核的 `prepare_git_baseline.py` 生成，不得手工拼接。排除 Approval、review queue、runtime DB、reports、logs、cache、backup、临时包和秘密文件；正式 Decision、Framework Manifest和C/APPLY state必须包含。Manifest逐项记录current/desired bytes，并对两个root control files固定：

```text
.gitignore
  before_state=PRESENT
  before_sha256=6879e1723cf111c34377003f5f0d1c3da0167768b174b9efeaee8a3475216bf4
  before_size=284
  disposition=REPLACE_WITH_APPROVED_BYTES

.gitattributes
  before_state=ABSENT
  disposition=CREATE_FROM_APPROVED_BYTES
```

两者还必须记录 `after_sha256/after_size/proposed_source_path/proposed_source_sha256`，并与 Decision/Gate policy binding相同。Approval、baseline manifest/receipt自身和review queue必须排除于Git baseline，避免自引用。

秘密扫描只记录脱敏路径/行号/分类，不复制值。

首次生成命令如下；此时`.git`必须仍无有效HEAD：

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$actionRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action").Path
$baselineRoot = "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\git-baseline"
if (git -C $controlRoot rev-parse --verify HEAD 2>$null) { throw 'valid Git HEAD exists before approved baseline' }
if (Test-Path -LiteralPath $baselineRoot) { throw "baseline candidate target already exists: $baselineRoot" }
py -3.12 -B "$actionRoot\prepare_git_baseline.py" `
  --root $controlRoot `
  --policy "$actionRoot\GIT_BASELINE_POLICY_V1.json" `
  --policy-sidecar "$actionRoot\GIT_BASELINE_POLICY_V1.json.sha256.sidecar" `
  --output $baselineRoot
if ($LASTEXITCODE -ne 0) { throw 'exact Git baseline candidate generation failed' }
```

工具以临时目录生成全部candidate文件，`GIT_BASELINE_PATHS_V1.nul`必须使用**UTF-8 without BOM**编码、以单个NUL字节分隔literal repo-relative paths、末项后是否保留NUL须由policy固定并由测试逐字节验证；全量校验后才rename发布，失败时target保持不存在。

#### D9.2 Jovi第三次 human-only：确认 exact baseline

```powershell
$actionRoot = (Resolve-Path .\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action).Path
$baselineRoot = (Resolve-Path .\workspace\review-queue\commerce-v1\decision-to-main-x2\git-baseline).Path
$baselineManifest = "$baselineRoot\GIT_BASELINE_MANIFEST_V1.json"
$baselineSha = ((Get-Content -Raw -Encoding ASCII `
  "$baselineManifest.sha256.sidecar").Trim() -split '\s+')[0]
$policySha = (Get-FileHash -Algorithm SHA256 `
  "$actionRoot\GIT_BASELINE_POLICY_V1.json").Hash.ToLowerInvariant()

powershell -NoProfile -File "$actionRoot\Approve-GitBaseline.ps1" `
  -Root (Get-Location).Path `
  -ManifestPath $baselineManifest `
  -ExpectedManifestSha256 $baselineSha `
  -ExpectedPolicySha256 $policySha `
  -Approver Jovi
if ($LASTEXITCODE -ne 0) { throw 'Jovi exact Git baseline approval failed' }
```

Luna不得运行。Jovi输入脚本显示的 SHA 前16位。随后 Luna运行`verify_git_baseline_approval.py`；receipt、manifest、policy、当前树或proposed bytes任一不匹配即停止。自Jovi批准起 `GIT_BASELINE_MANIFEST_V1.json` 和文件清单完全冻结：任何漂移只能生成新candidate并重新请Jovi批准，禁止写后重生成或更新SHA。

#### D9.3 字节策略与初始化

- `apply_git_baseline_files.py --apply` 只把 D1 已审核的 `.gitignore`/`.gitattributes` proposed bytes 写到根目录；
- apply前再次验证`.git`为空、全树before快照、`.gitignore` before SHA/size和`.gitattributes` absent；
- `.gitignore` 包含 `.worktrees/`、Approval/review-queue 和 Commerce runtime 输出；
- `.gitattributes` 固定 `* -text`，保留审计字节；
- `git config --local core.autocrlf false`；
- 写入后只用已批准manifest的desired bytes逐项验证100%；禁止调用generator、写回manifest或“写后重新接受新SHA”。

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$actionRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action").Path
$baselineRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\git-baseline").Path
$baselineManifest = Join-Path $baselineRoot 'GIT_BASELINE_MANIFEST_V1.json'
py -3.12 -B "$actionRoot\apply_git_baseline_files.py" `
  --root $controlRoot `
  --manifest $baselineManifest `
  --receipt "$controlRoot\workspace\approvals\GIT_BASELINE.V1.approval.json" `
  --apply
if ($LASTEXITCODE -ne 0) { throw 'approved baseline root-file apply failed' }
git -C $controlRoot init -b main
if ($LASTEXITCODE -ne 0) { throw 'git init failed' }
git -C $controlRoot config --local core.autocrlf false
if ($LASTEXITCODE -ne 0) { throw 'git config failed' }
$remoteLines = @(git -C $controlRoot remote -v)
if ($LASTEXITCODE -ne 0 -or $remoteLines.Count -ne 0) { throw 'remote must remain empty' }
$pathspec = (Resolve-Path "$baselineRoot\GIT_BASELINE_PATHS_V1.nul").Path
git -C $controlRoot --literal-pathspecs add --pathspec-from-file="$pathspec" --pathspec-file-nul
if ($LASTEXITCODE -ne 0) { throw 'literal baseline staging failed' }
git -C $controlRoot diff --cached --check
if ($LASTEXITCODE -ne 0) { throw 'cached diff check failed' }
py -3.12 -B "$actionRoot\prepare_git_baseline.py" `
  --root $controlRoot `
  --verify-index-against $baselineManifest `
  --read-only
if ($LASTEXITCODE -ne 0) { throw 'index does not match approved baseline' }
git -C $controlRoot commit -m "chore: establish audited jovi automation baseline"
if ($LASTEXITCODE -ne 0) { throw 'baseline commit failed' }
```

禁止 `git add .`。

提交后立即生成并冻结 `GIT_BASELINE_ESTABLISHMENT.json` + sidecar，至少绑定：baseline manifest SHA、Jovi Git-baseline approval receipt SHA、Git tree OID、root commit OID、`parent_count=0`、`branch=main`、`remote_empty=true`、`index_matches_manifest=true`。该报告位于被忽略的control-root review queue，不进入commit：

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$actionRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action").Path
$baselineRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\git-baseline").Path
$baselineCommit = (git -C $controlRoot rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve baseline commit' }
$treeOid = (git -C $controlRoot rev-parse 'HEAD^{tree}').Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve baseline tree' }
py -3.12 -B "$actionRoot\prepare_git_baseline.py" `
  --root $controlRoot `
  --write-establishment "$baselineRoot\GIT_BASELINE_ESTABLISHMENT.json" `
  --manifest "$baselineRoot\GIT_BASELINE_MANIFEST_V1.json" `
  --approval "$controlRoot\workspace\approvals\GIT_BASELINE.V1.approval.json" `
  --expected-root-commit $baselineCommit `
  --expected-tree-oid $treeOid
if ($LASTEXITCODE -ne 0) { throw 'baseline establishment report failed' }
```

工具必须生成sidecar并重新验证root commit无parent、tree与approved index一致；不得修改Git index或manifest。

随后执行精确 worktree 创建；代码块必须独立解析变量：

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$featureRoot = 'E:\project\jovi-automation\.worktrees\commerce-import-phase2'
$baselineCommit = (git -C $controlRoot rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve baseline commit before worktree creation' }
if (Test-Path -LiteralPath $featureRoot) { throw "feature worktree target already exists: $featureRoot" }
git -C $controlRoot worktree add -b feature/commerce-import-phase2 $featureRoot $baselineCommit
if ($LASTEXITCODE -ne 0) { throw 'feature worktree creation failed' }
$featureHead = (git -C $featureRoot rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $featureHead -ne $baselineCommit) { throw 'feature HEAD does not equal baseline commit' }
$rootLine = (git -C $controlRoot rev-list --parents -n 1 $baselineCommit).Trim()
if ($LASTEXITCODE -ne 0 -or $rootLine.Split(' ').Count -ne 1) { throw 'baseline commit is not a root commit' }
$remoteLines = @(git -C $controlRoot remote -v)
if ($LASTEXITCODE -ne 0 -or $remoteLines.Count -ne 0) { throw 'remote must remain empty' }
```

创建并验证：

```text
branch: feature/commerce-import-phase2
worktree: E:\project\jovi-automation\.worktrees\commerce-import-phase2
```

此后每个feature提交都必须证明baseline root commit是其祖先；control-root main和feature-root在各自阶段结束时均须clean，remote始终为空。

**成功状态：** `MAIN_GIT_BASELINE_ESTABLISHED`。

---

### D10 — 精确导入 Commerce Engine

#### D10.1 来源复核

导入前再次要求：

- source object repo=`E:\project\jovi-commerce-engine-v1`，observed HEAD=`3b31f0f2f240038aa261db5c57c43e5e14992dc5`；只要求两个固定commit objects可读，不要求其工作树HEAD等于evidence HEAD；
- source evidence worktree=`E:\project\jovi-commerce-engine-v1\.worktrees\landing-phase1`，HEAD=`7dbe080c907c1da2eef1c16b79e677e6a1d49470`、clean、remote empty；
- implementation commit=`fd2321d5a3f12aa923014cadbc397849903fd97c`且为`7dbe080c907c1da2eef1c16b79e677e6a1d49470`祖先；
- source 20/20、22/22、protected 40/40；
- evidence sidecar 全部 PASS；
- implementation commit的83个Git blobs与外置`IMPORT_CANDIDATE_MANIFEST.json` 83/83；manifest body SHA=`4090c6963b19705cc401336df6f3a0f7a31a97a650cff517cc9cb7d83c94a4f0`、blob OID=`dd4a55426771c4fb10bb55e6ff1e84fc8001b953`；
- source selection精确93行：49 import + 34 exclude + 10 evidence import；
- 禁止把 Windows checkout bytes 当来源：当前已知 checkout 只有 60/83 与 Git blob 字节相同。

#### D10.2 映射

| 外置来源 | 主工程目标 | 规则 |
|---|---|---|
| `jovi_commerce/**` | `jovi_commerce/**` | 从 `fd2321d5a3f12aa923014cadbc397849903fd97c` Git blob写入；适配另提交 |
| 三份正式产品文档 | `docs/commerce/**` | 从`fd2321d5a3f12aa923014cadbc397849903fd97c` blob导入；排除外置`docs/commerce/STATUS.md` |
| `schemas/commerce/**` | `schemas/commerce/**` | 10份从`fd2321d5a3f12aa923014cadbc397849903fd97c` blob导入 |
| `tests/unit/**` | `tests/commerce/unit/**` | 先保持 blob bytes，再单独路径适配 |
| `tests/acceptance/**` | `tests/commerce/acceptance/**` | 先保持 blob bytes，再单独路径适配 |
| 合成 fixture | `tests/fixtures/commerce/synthetic-digital-checklist/**` | 从`fd2321d5a3f12aa923014cadbc397849903fd97c` blob导入 |
| `pyproject.toml` | `pyproject.toml` | 从`fd2321d5a3f12aa923014cadbc397849903fd97c` blob导入；标准库，无新依赖 |
| 外置证据 | control root的`workspace/review-queue/commerce-v1/decision-to-main-x2/external-evidence/**` | 从`7dbe080c907c1da2eef1c16b79e677e6a1d49470`的10个精确evidence blobs导入，不进入feature/runtime/tracked docs |

明确不导入外置 `.git`、`.worktrees`、AGENTS、tasks、runtime DB、receipts、临时 ZIP、human-only 或真实数据。

禁止 `Copy-Item` 直接复制外置checkout。Importer必须先用`git ls-tree`核验blob mode/OID，再用Python subprocess binary stdout执行`git cat-file blob <blob_oid>`；拒绝非普通blob mode、reparse ancestor、大小写碰撞、未知字段和目标已存在；每个group使用临时staging，整组成功才发布，失败只回滚本组创建的精确目标。

三个group必须分别执行，且每个代码块自包含变量。

第一组只导入tests/fixtures到feature root：

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$featureRoot = (Resolve-Path 'E:\project\jovi-automation\.worktrees\commerce-import-phase2').Path
$objectRepo = (Resolve-Path 'E:\project\jovi-commerce-engine-v1').Path
$actionRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action").Path
$sourceSelection = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope\IMPORT_SOURCE_SELECTION_V1.json").Path
$baselineEstablishment = Get-Content -Raw -Encoding UTF8 "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\git-baseline\GIT_BASELINE_ESTABLISHMENT.json" | ConvertFrom-Json
$baselineCommit = [string]$baselineEstablishment.root_commit_oid
if ((git -C $featureRoot rev-parse HEAD).Trim() -ne $baselineCommit) { throw 'tests import must start at exact baseline HEAD' }
$beforeStatus = @(git -C $featureRoot status --short)
if ($LASTEXITCODE -ne 0 -or $beforeStatus.Count -ne 0) { throw 'tests import requires clean feature worktree' }
py -3.12 -B "$actionRoot\import_external_git_blobs.py" `
  --control-root $controlRoot `
  --source-object-repo $objectRepo `
  --selection $sourceSelection `
  --group tests `
  --target-root $featureRoot `
  --gate-plan "$controlRoot\reports\gates\GATE_A_PLAN.json" `
  --gate-receipt "$controlRoot\workspace\approvals\GATE_A.P.approval.json" `
  --transition-receipt "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\CONTROL_PLANE_TRANSITION_RECEIPT.json" `
  --baseline-establishment "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\git-baseline\GIT_BASELINE_ESTABLISHMENT.json" `
  --require-feature-head $baselineCommit `
  --require-clean `
  --receipt-output "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope\IMPORT_TESTS_RECEIPT.json" `
  --apply
if ($LASTEXITCODE -ne 0) { throw 'tests Git-object import failed' }
```

立即运行tests-group RED。唯一允许的失败根因是目标实现包`jovi_commerce`尚不存在；路径、fixture、语法、selection或导入错误均不是合格RED。由已审核verifier启动测试、解析全部failure并写机器JSON：

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$featureRoot = (Resolve-Path 'E:\project\jovi-automation\.worktrees\commerce-import-phase2').Path
$actionRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action").Path
$redReport = "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope\TESTS_GROUP_EXPECTED_RED.json"
py -3.12 -B "$actionRoot\verify_expected_import_red.py" `
  --cwd $featureRoot `
  --suite-root tests/commerce/unit `
  --suite-root tests/commerce/acceptance `
  --expected-missing-module jovi_commerce `
  --output $redReport
if ($LASTEXITCODE -ne 0) { throw 'tests-group RED was not exclusively caused by missing jovi_commerce runtime' }
```

Verifier必须分别启动unit与acceptance，要求两个test process均非零、每个suite至少收集一项、所有error root cause均为`ModuleNotFoundError: jovi_commerce`、无syntax/path/fixture/selection failure，并为report生成sidecar。任一suite零收集、误通过或出现其他根因都不是合格RED。

第二组导入implementation/contracts到feature root：

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$featureRoot = (Resolve-Path 'E:\project\jovi-automation\.worktrees\commerce-import-phase2').Path
$objectRepo = (Resolve-Path 'E:\project\jovi-commerce-engine-v1').Path
$actionRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action").Path
$sourceSelection = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope\IMPORT_SOURCE_SELECTION_V1.json").Path
py -3.12 -B "$actionRoot\import_external_git_blobs.py" `
  --control-root $controlRoot `
  --source-object-repo $objectRepo `
  --selection $sourceSelection `
  --group implementation `
  --target-root $featureRoot `
  --gate-plan "$controlRoot\reports\gates\GATE_A_PLAN.json" `
  --gate-receipt "$controlRoot\workspace\approvals\GATE_A.P.approval.json" `
  --transition-receipt "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\CONTROL_PLANE_TRANSITION_RECEIPT.json" `
  --baseline-establishment "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\git-baseline\GIT_BASELINE_ESTABLISHMENT.json" `
  --require-existing-group tests `
  --require-no-other-changes `
  --receipt-output "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope\IMPORT_IMPLEMENTATION_RECEIPT.json" `
  --apply
if ($LASTEXITCODE -ne 0) { throw 'implementation Git-object import failed' }
```

第三组只把10个evidence blobs写入control-root review queue：

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$featureRoot = (Resolve-Path 'E:\project\jovi-automation\.worktrees\commerce-import-phase2').Path
$objectRepo = (Resolve-Path 'E:\project\jovi-commerce-engine-v1').Path
$actionRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action").Path
$sourceSelection = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope\IMPORT_SOURCE_SELECTION_V1.json").Path
py -3.12 -B "$actionRoot\import_external_git_blobs.py" `
  --control-root $controlRoot `
  --source-object-repo $objectRepo `
  --selection $sourceSelection `
  --group evidence `
  --target-root $controlRoot `
  --feature-root $featureRoot `
  --gate-plan "$controlRoot\reports\gates\GATE_A_PLAN.json" `
  --gate-receipt "$controlRoot\workspace\approvals\GATE_A.P.approval.json" `
  --transition-receipt "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\CONTROL_PLANE_TRANSITION_RECEIPT.json" `
  --baseline-establishment "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\git-baseline\GIT_BASELINE_ESTABLISHMENT.json" `
  --require-control-tracked-clean `
  --require-target-absent `
  --receipt-output "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope\IMPORT_EVIDENCE_RECEIPT.json" `
  --apply
if ($LASTEXITCODE -ne 0) { throw 'evidence Git-object import failed' }
```

每项source blob OID、source SHA-256、target SHA-256必须一致。逐组before-state固定为：tests前feature clean且HEAD=baseline；implementation前只能存在selection中tests group的精确变化；evidence前control tracked tree clean且精确evidence target不存在。任何checkout fallback、CRLF转换、未知变化、目标已存在、group越界或target root role不匹配即fail-closed。

三组均成功后，由同一importer只读复算并冻结**原始导入映射**；不得重新导入：

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$featureRoot = (Resolve-Path 'E:\project\jovi-automation\.worktrees\commerce-import-phase2').Path
$actionRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action").Path
$sourceSelection = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope\IMPORT_SOURCE_SELECTION_V1.json").Path
$finalRoot = "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\final"
py -3.12 -B "$actionRoot\import_external_git_blobs.py" `
  --selection $sourceSelection `
  --feature-root $featureRoot `
  --control-root $controlRoot `
  --receipt "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope\IMPORT_TESTS_RECEIPT.json" `
  --receipt "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope\IMPORT_IMPLEMENTATION_RECEIPT.json" `
  --receipt "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope\IMPORT_EVIDENCE_RECEIPT.json" `
  --finalize-raw-mapping "$finalRoot\RAW_IMPORT_MAPPING_MANIFEST.json"
if ($LASTEXITCODE -ne 0) { throw 'raw import mapping finalization failed' }
```

`RAW_IMPORT_MAPPING_MANIFEST.json`及sidecar绑定93项disposition、三组receipt、每个source blob到**刚发布的raw target bytes**以及未导入排除项；任何缺项、额外target或receipt漂移失败。它不宣称后续namespace适配后的target仍与source blob相同。

#### D10.3 TDD 适配

1. tests group写入后确认因runtime缺失而RED，并冻结RED机器报告；
2. implementation group写入runtime/contracts blobs；evidence group始终只写control root review queue；
3. 将 unit fixture root 从旧层级调整到主工程 `tests/fixtures/commerce`；
4. 将 acceptance root 调整到主工程 root；
5. 把外置 staging 专属 `G3_RECEIPT_NOT_BOUND`/`main_import_authorized` 字段从 Commerce Core 结果移除，改为通用 `X2_SYNTHETIC_COMMERCE_FLOW_PASS`；主工程 Gate/C-APPLY 事实只写在 D11 外层验收报告，禁止产品代码自我授权；
6. 在本阶段先以RED建立并提交 `tests/commerce/unit/test_import_safety.py`，检查正式代码无外部闲鱼路径、无真实平台动作API、无human-only入口、无客户PII字段、runtime输出全部ignored、Modbus SKU SHA未变、remote为空；它必须进入后续unit suite，不能等D11测试完成后才创建；
7. 每个变化记录 source SHA、raw target SHA、final target SHA、`MAIN_TEST_NAMESPACE_ADAPTATION`及对应commit；
8. focused GREEN；
9. unit与acceptance分别full GREEN；
10. 独立规格/质量审核；
11. 使用显式pathspec提交三个小提交；每次提交后工作树clean、remote empty，禁止把control-root raw evidence提交进feature；
12. 最后只读生成从raw bytes到适配后bytes的最终转换映射。

提交：

```text
docs: import reviewed commerce contracts
feat: import commerce engine x2 candidate
test: adapt commerce tests to main project namespace
```

三个提交完成且feature worktree clean后，生成最终转换映射；该步骤不修改feature：

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$featureRoot = (Resolve-Path 'E:\project\jovi-automation\.worktrees\commerce-import-phase2').Path
$actionRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action").Path
$finalRoot = "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\final"
$baseline = Get-Content -Raw -Encoding UTF8 "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\git-baseline\GIT_BASELINE_ESTABLISHMENT.json" | ConvertFrom-Json
$adaptationBase = [string]$baseline.root_commit_oid
$adaptationHead = (git -C $featureRoot rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve adaptation HEAD' }
$featureStatus = @(git -C $featureRoot status --short)
if ($LASTEXITCODE -ne 0 -or $featureStatus.Count -ne 0) { throw 'final transformation mapping requires clean feature worktree' }
py -3.12 -B "$actionRoot\import_external_git_blobs.py" `
  --control-root $controlRoot `
  --feature-root $featureRoot `
  --raw-mapping "$finalRoot\RAW_IMPORT_MAPPING_MANIFEST.json" `
  --adaptation-base $adaptationBase `
  --adaptation-head $adaptationHead `
  --require-clean `
  --finalize-transformation-mapping "$finalRoot\FINAL_IMPORT_MAPPING_MANIFEST.json"
if ($LASTEXITCODE -ne 0) { throw 'final transformation mapping generation failed' }
```

`FINAL_IMPORT_MAPPING_MANIFEST.json`及sidecar逐项绑定source blob、raw target SHA、final target SHA、`UNCHANGED`或受控 transformation reason、产生变化的精确commit OID、`adaptation_base`、`adaptation_head`和该HEAD tree OID。它必须覆盖RAW mapping全部import行，且不得把证据group伪装成feature transformation。D11.1的机器测试报告必须证明其测试HEAD仍精确等于这里的`adaptation_head`。

---

### D11 — 主工程治理回归与 X2

#### D11.1 Commerce

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$featureRoot = (Resolve-Path 'E:\project\jovi-automation\.worktrees\commerce-import-phase2').Path
$actionRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action").Path
$finalRoot = "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\final"
Push-Location $featureRoot
$previousPythonPath = $env:PYTHONPATH
try {
  $env:PYTHONPATH='.'
  py -3.12 -B "$actionRoot\run_and_record.py" `
    --cwd $featureRoot `
    --suite commerce-unit `
    --record-git-state `
    --require-git-clean `
    --output "$finalRoot\MAIN_COMMERCE_UNIT_RESULTS.json" `
    -- py -3.12 -B -m unittest discover -s tests/commerce/unit -p 'test_*.py' -v
  if ($LASTEXITCODE -ne 0) { throw 'Commerce unit suite failed' }
  py -3.12 -B "$actionRoot\run_and_record.py" `
    --cwd $featureRoot `
    --suite commerce-acceptance `
    --record-git-state `
    --require-git-clean `
    --output "$finalRoot\MAIN_COMMERCE_ACCEPTANCE_RESULTS.json" `
    -- py -3.12 -B -m unittest discover -s tests/commerce/acceptance -p 'test_*.py' -v
  if ($LASTEXITCODE -ne 0) { throw 'Commerce acceptance suite failed' }
  py -3.12 -B -m compileall -q jovi_commerce tests/commerce
  if ($LASTEXITCODE -ne 0) { throw 'Commerce compileall failed' }
}
finally {
  $env:PYTHONPATH = $previousPythonPath
  Pop-Location
}
```

`run_and_record.py`必须保留stdout/stderr SHA、exit code、命令数组/command SHA、UTC和suite name，解析并记录collected/passed/failed/errors/skipped且生成sidecar；解析失败也判失败。`--record-git-state --require-git-clean`要求记录执行前后HEAD、tree OID和porcelain status，二者必须完全相等且status均空；否则即使测试为绿也失败。unit/general来源证据为99 run/95 passed/4 skipped，acceptance来源证据为单独8 run/7 passed/1 skipped；主工程也必须分别记录。不得再把99项描述为已覆盖acceptance。新增适配测试计数只从机器JSON读取；skip只有原因和平台条件完全相同才允许保留。

#### D11.2 治理

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$actionRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action").Path
$finalRoot = "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\final"
py -3.12 -B "$actionRoot\run_and_record.py" `
  --cwd $controlRoot `
  --suite phase2b-governance `
  --preset phase2b-governance `
  --output "$finalRoot\MAIN_SECURITY_REGRESSION.json"
if ($LASTEXITCODE -ne 0) { throw 'Phase2B governance regression failed' }
```

`phase2b-governance` preset固定顺序运行`run-security-semantics.py`、S2A2、S1 integrity、S2A1、pre-tool guard、`validate_commerce_gate_readiness.py --phase post-transition`和Commerce transition；每个子命令非零立即终止，机器报告记录各自command SHA/exit/stdout/stderr SHA与计数，生成sidecar。

不得扩大 allowlist 掩盖回归。

#### D11.3 X2

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$featureRoot = (Resolve-Path 'E:\project\jovi-automation\.worktrees\commerce-import-phase2').Path
$actionRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action").Path
$finalRoot = "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\final"
$runId = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssfffffffZ')
$x2Root = Join-Path $featureRoot ".runtime\commerce\x2\$runId"
if (Test-Path -LiteralPath $x2Root) { throw "fresh X2 root already exists: $x2Root" }
Push-Location $featureRoot
$previousPythonPath = $env:PYTHONPATH
try {
  $env:PYTHONPATH='.'
  py -3.12 -B "$actionRoot\run_and_record.py" `
    --cwd $featureRoot `
    --suite commerce-x2-run `
    --record-git-state `
    --require-git-clean `
    --output "$finalRoot\MAIN_X2_RUN.json" `
    -- py -3.12 -B -m jovi_commerce x2 run --work-dir $x2Root
  if ($LASTEXITCODE -ne 0) { throw 'main X2 runner failed' }
  $bundlePath = Join-Path $x2Root 'xianyu\bundle.json'
  if (-not (Test-Path -LiteralPath $bundlePath -PathType Leaf)) { throw 'X2 bundle missing' }
  py -3.12 -B "$controlRoot\scripts\xianyu\validate_xianyu_bundle.py" `
    --bundle $bundlePath `
    --schema "$controlRoot\deploy\xianyu\xianyu_bundle.schema.json"
  if ($LASTEXITCODE -ne 0) { throw 'main Xianyu bundle validation failed' }
  $x2Acceptance = Join-Path $x2Root 'X2_ACCEPTANCE.json'
  if (-not (Test-Path -LiteralPath $x2Acceptance -PathType Leaf)) { throw 'X2 acceptance artifact missing' }
  py -3.12 -B "$actionRoot\run_and_record.py" `
    --freeze-artifact $x2Acceptance `
    --feature-root $featureRoot `
    --record-git-state `
    --require-git-clean `
    --expected-git-head-from "$finalRoot\MAIN_X2_RUN.json" `
    --output "$finalRoot\MAIN_X2_ACCEPTANCE.json"
  if ($LASTEXITCODE -ne 0) { throw 'X2 acceptance freeze failed' }
}
finally {
  $env:PYTHONPATH = $previousPythonPath
  Pop-Location
}
```

必须重新证明：

- 恰好一个订单、付款、Entitlement、交付包；
- 最终 `READY_FOR_HUMAN_DELIVERY`；
- 幂等重放无第二份效果；
- event chain/receipts/DB 一致；
- artifacts/evidence 全量 SHA；
- 未付款、阻塞权利、非法跳级、链断裂、路径逃逸和包篡改 fail-closed；
- Xianyu 五项动作 false；
- 无 PII、秘密、真实付款或外部访问。

主工程Xianyu validator已在同一代码块对该次精确`$x2Root`执行，禁止通过“选择最新目录”猜测运行证据。`MAIN_X2_RUN.json`记录实际runner执行前后相同且clean的HEAD/tree；`run_and_record.py --freeze-artifact`必须先验证该HEAD绑定、原X2 sidecar、47项artifact manifest和8项evidence，再按原字节冻结control-root raw report并生成新sidecar。unit、acceptance、X2 run和X2 freeze四份报告的git before/after必须是同一HEAD/tree。

#### D11.4 Safety test

复核已在D10.3通过RED→GREEN并随适配提交的 `tests/commerce/unit/test_import_safety.py`；D11不得在测试完成后才新增或修改该文件。它使用标准库检查：

- 正式代码无外部闲鱼路径；
- 无真实平台动作 API；
- 无 human-only 入口；
- 无客户 PII字段；
- runtime 输出全部 ignored；
- Modbus SKU SHA 与 before snapshot 一致；
- Git remote empty。

`MAIN_COMMERCE_UNIT_RESULTS.json`必须证明该测试在同一`TESTED_IMPLEMENTATION_HEAD`中被实际收集和执行。若本节发现需修改测试或实现，立即使D11.1-D11.3全部报告失效，回到D10.3完成新提交后重跑；不得在本节留下未提交测试。

随后由已审核recorder复算D0保护树、外置source before、current control/feature tree和remote状态：

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$featureRoot = (Resolve-Path 'E:\project\jovi-automation\.worktrees\commerce-import-phase2').Path
$actionRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action").Path
$finalRoot = "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\final"
py -3.12 -B "$actionRoot\run_and_record.py" `
  --suite phase2b-source-nonmutation `
  --preset phase2b-source-nonmutation `
  --cwd $controlRoot `
  --feature-root $featureRoot `
  --before "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\preflight\PROTECTED_TREE_BEFORE.json" `
  --output "$finalRoot\MAIN_SOURCE_NONMUTATION.json"
if ($LASTEXITCODE -ne 0) { throw 'source nonmutation verification failed' }
```

Preset只允许Decision-bound治理变化和selection-bound Commerce feature变化；Hook、`MANIFEST.sha256`、Modbus SKU、human-only、外部evidence worktree及禁止目标任一额外变化都失败。报告生成sidecar。

#### D11.5 Pre-audit tracked evidence 与最终 feature commit

在独立Import Audit前完成所有feature tracked写入。生成并提交：

```text
docs/commerce/evidence/import-phase2/
├── README.md
├── CURRENT_STATUS.md
├── EVIDENCE_INDEX.json
├── IMPORT_MAPPING_SUMMARY.json
├── TEST_SUMMARY.json
├── X2_SUMMARY.json
└── SHA256SUMS.txt
```

同步feature worktree中的`tasks/todo.md`和`CHANGELOG.md`；产品导入状态写入`docs/commerce/evidence/import-phase2/CURRENT_STATUS.md`。根`STATUS.md`是控制面revisioned mirror，必须保持baseline/C-APPLY字节不变；不得用feature文档更新破坏mirror链。不得写`INDEPENDENT_AUDIT_SUMMARY.json`，因为独立审核尚未发生。提交：

`IMPORT_MAPPING_SUMMARY.json`必须从已验证的`FINAL_IMPORT_MAPPING_MANIFEST.json`生成，并同时引用`RAW_IMPORT_MAPPING_MANIFEST.json` SHA；不得从工作树重新猜测source bytes或丢失raw→final transformation。`TEST_SUMMARY.json`和`X2_SUMMARY.json`只引用机器报告，不手填计数或HEAD。

```text
docs: freeze commerce import phase2 candidate evidence
```

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$featureRoot = (Resolve-Path 'E:\project\jovi-automation\.worktrees\commerce-import-phase2').Path
$finalRoot = "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\final"
$unit = Get-Content -Raw -Encoding UTF8 "$finalRoot\MAIN_COMMERCE_UNIT_RESULTS.json" | ConvertFrom-Json
$acceptance = Get-Content -Raw -Encoding UTF8 "$finalRoot\MAIN_COMMERCE_ACCEPTANCE_RESULTS.json" | ConvertFrom-Json
$x2Run = Get-Content -Raw -Encoding UTF8 "$finalRoot\MAIN_X2_RUN.json" | ConvertFrom-Json
$x2 = Get-Content -Raw -Encoding UTF8 "$finalRoot\MAIN_X2_ACCEPTANCE.json" | ConvertFrom-Json
$mapping = Get-Content -Raw -Encoding UTF8 "$finalRoot\FINAL_IMPORT_MAPPING_MANIFEST.json" | ConvertFrom-Json
$testedHead = [string]$unit.git_before.head
$testedTree = [string]$unit.git_before.tree
foreach ($report in @($unit,$acceptance,$x2Run,$x2)) {
  if ([string]$report.git_before.head -ne $testedHead -or [string]$report.git_after.head -ne $testedHead) { throw 'unit/acceptance/X2 were not run on one tested HEAD' }
  if ([string]$report.git_before.tree -ne $testedTree -or [string]$report.git_after.tree -ne $testedTree) { throw 'unit/acceptance/X2 tree binding mismatch' }
  if (@($report.git_before.status).Count -ne 0 -or @($report.git_after.status).Count -ne 0) { throw 'test report recorded dirty feature state' }
}
if ([string]$mapping.adaptation_head -ne $testedHead -or [string]$mapping.adaptation_tree -ne $testedTree) { throw 'final transformation mapping does not bind tested implementation HEAD/tree' }
$currentHead = (git -C $featureRoot rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $currentHead -ne $testedHead) { throw 'feature HEAD changed after tests' }
git -C $featureRoot diff --check
if ($LASTEXITCODE -ne 0) { throw 'pre-audit feature diff check failed' }
git -C $featureRoot --literal-pathspecs add -- `
  docs/commerce/evidence/import-phase2 `
  tasks/todo.md `
  CHANGELOG.md
if ($LASTEXITCODE -ne 0) { throw 'pre-audit evidence staging failed' }
git -C $featureRoot diff --cached --check
if ($LASTEXITCODE -ne 0) { throw 'pre-audit cached diff check failed' }
git -C $featureRoot commit -m "docs: freeze commerce import phase2 candidate evidence"
if ($LASTEXITCODE -ne 0) { throw 'pre-audit evidence commit failed' }
$finalHead = (git -C $featureRoot rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve final import candidate HEAD' }
$parents = @((git -C $featureRoot rev-list --parents -n 1 $finalHead).Trim() -split '\s+')
if ($LASTEXITCODE -ne 0 -or $parents.Count -ne 2 -or $parents[1] -ne $testedHead) { throw 'final candidate must be one docs-only child of tested HEAD' }
$changed = @(git -C $featureRoot diff --name-only "$testedHead..$finalHead")
if ($LASTEXITCODE -ne 0) { throw 'cannot enumerate tested-to-final diff' }
$unexpected = @($changed | Where-Object { $_ -ne 'CHANGELOG.md' -and $_ -ne 'tasks/todo.md' -and $_ -notlike 'docs/commerce/evidence/import-phase2/*' })
if ($unexpected.Count -ne 0) { throw "non-evidence path changed after tested HEAD: $($unexpected -join ', ')" }
$featureStatus = @(git -C $featureRoot status --short)
if ($LASTEXITCODE -ne 0 -or $featureStatus.Count -ne 0) { throw 'feature worktree is not clean after evidence commit' }
```

提交后不覆盖或重写D11机器报告。`TESTED_IMPLEMENTATION_HEAD`只能从unit、acceptance、X2 run、X2 freeze四份机器报告共同绑定的HEAD读取，禁止手填；`FINAL_IMPORT_CANDIDATE_HEAD`为docs-only提交后的HEAD。要求后者的唯一parent为前者，二者Git diff只能包含本节显式三个tracked target groups，根`STATUS.md`和两份control-plane state/mirror保持不变，且feature worktree clean、remote empty、baseline root commit仍为祖先。Dual-root writer和D12必须同时绑定/验证两个HEAD；D12后禁止再修改任何feature tracked byte。

#### D11.6 Dual-root binding

control root中的Gate、Approval、Decision、Post-Apply、transition和review evidence按policy不进入feature worktree；不得因feature中缺少这些对象而误判治理失败。使用D1/D2已审核writer生成：

```text
E:\project\jovi-automation\workspace\review-queue\commerce-v1\decision-to-main-x2\final\
├── DUAL_ROOT_BINDING_V1.json
└── DUAL_ROOT_BINDING_V1.json.sha256.sidecar
```

```powershell
$controlRoot = (Resolve-Path 'E:\project\jovi-automation').Path
$featureRoot = (Resolve-Path 'E:\project\jovi-automation\.worktrees\commerce-import-phase2').Path
$actionRoot = (Resolve-Path "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\human-action").Path
$finalRoot = "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\final"
if (Test-Path -LiteralPath "$finalRoot\DUAL_ROOT_BINDING_V1.json") { throw 'dual-root binding already exists' }
$unit = Get-Content -Raw -Encoding UTF8 "$finalRoot\MAIN_COMMERCE_UNIT_RESULTS.json" | ConvertFrom-Json
$acceptance = Get-Content -Raw -Encoding UTF8 "$finalRoot\MAIN_COMMERCE_ACCEPTANCE_RESULTS.json" | ConvertFrom-Json
$x2Run = Get-Content -Raw -Encoding UTF8 "$finalRoot\MAIN_X2_RUN.json" | ConvertFrom-Json
$x2 = Get-Content -Raw -Encoding UTF8 "$finalRoot\MAIN_X2_ACCEPTANCE.json" | ConvertFrom-Json
$testedHead = [string]$unit.git_before.head
$testedTree = [string]$unit.git_before.tree
foreach ($report in @($unit,$acceptance,$x2Run,$x2)) {
  if ([string]$report.git_before.head -ne $testedHead -or [string]$report.git_after.head -ne $testedHead) { throw 'test reports disagree on tested HEAD' }
  if ([string]$report.git_before.tree -ne $testedTree -or [string]$report.git_after.tree -ne $testedTree) { throw 'test reports disagree on tested tree' }
}
$finalHead = (git -C $featureRoot rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'cannot resolve final feature HEAD' }
py -3.12 -B "$actionRoot\write_dual_root_binding.py" `
  --control-root $controlRoot `
  --feature-root $featureRoot `
  --expected-tested-head $testedHead `
  --expected-final-head $finalHead `
  --baseline-establishment "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\git-baseline\GIT_BASELINE_ESTABLISHMENT.json" `
  --gate-plan "$controlRoot\reports\gates\GATE_A_PLAN.json" `
  --gate-receipt "$controlRoot\workspace\approvals\GATE_A.P.approval.json" `
  --transition-receipt "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\CONTROL_PLANE_TRANSITION_RECEIPT.json" `
  --source-selection "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope\IMPORT_SOURCE_SELECTION_V1.json" `
  --raw-import-mapping "$finalRoot\RAW_IMPORT_MAPPING_MANIFEST.json" `
  --final-import-mapping "$finalRoot\FINAL_IMPORT_MAPPING_MANIFEST.json" `
  --expected-red-report "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope\TESTS_GROUP_EXPECTED_RED.json" `
  --import-receipts-root "$controlRoot\workspace\review-queue\commerce-v1\decision-to-main-x2\import-scope" `
  --unit-report "$finalRoot\MAIN_COMMERCE_UNIT_RESULTS.json" `
  --acceptance-report "$finalRoot\MAIN_COMMERCE_ACCEPTANCE_RESULTS.json" `
  --x2-run-report "$finalRoot\MAIN_X2_RUN.json" `
  --x2-report "$finalRoot\MAIN_X2_ACCEPTANCE.json" `
  --security-report "$finalRoot\MAIN_SECURITY_REGRESSION.json" `
  --nonmutation-report "$finalRoot\MAIN_SOURCE_NONMUTATION.json" `
  --output "$finalRoot\DUAL_ROOT_BINDING_V1.json"
if ($LASTEXITCODE -ne 0) { throw 'dual-root binding generation failed' }
```

它必须绑定`control_root`、baseline root commit/establishment receipt、`feature_root`、机器报告共同证明的`TESTED_IMPLEMENTATION_HEAD`/tree、`FINAL_IMPORT_CANDIDATE_HEAD`、两HEAD间精确evidence-only diff、Gate Plan SHA、Gate receipt SHA、C/APPLY transition receipt SHA、source selection SHA、RAW与FINAL mapping SHA、expected-RED报告SHA、三份精确import receipt及sidecar、unit报告SHA、acceptance报告SHA、X2 run/freeze报告SHA、security报告SHA和source-nonmutation报告SHA。`--import-receipts-root`只能接受`IMPORT_TESTS_RECEIPT.json`、`IMPORT_IMPLEMENTATION_RECEIPT.json`、`IMPORT_EVIDENCE_RECEIPT.json`及各自sidecar，缺失或额外receipt失败。control root审核治理链和未跟踪证据；feature root审核tracked代码/测试/X2。两边HEAD/树/SHA在报告生成前后任一变化即失败；writer原子写body/sidecar且不修改feature。

**成功状态：** `MAIN_PROJECT_X2_SYNTHETIC_PASS`。

---

### D12 — 独立 Import Audit

新Agent必须直接只读审核两个根，并先验证`DUAL_ROOT_BINDING_V1.json` sidecar：

```text
CONTROL_ROOT = E:\project\jovi-automation
FEATURE_ROOT = E:\project\jovi-automation\.worktrees\commerce-import-phase2
```

不得从feature中缺少被忽略的Approval/Gate/review evidence推断治理未完成，也不得只审control root而漏掉feature实现。审核内容：

- Decision/Gate/C-APPLY 链；
- 外置来源和 83-file implementation snapshot；
- RAW import mapping、FINAL transformation mapping、三组receipt和每项 raw→final transformation；
- contracts/公共接口；
- SQLite hash chain、idempotency、ZIP；
- Xianyu actions false；
- 主工程治理回归；
- Modbus/Hook/Manifest/Approval 非预期变化为零；
- control root中的Decision/Gate/Approval/C-APPLY/Post-Apply链和raw evidence；
- feature root中的imported runtime/contracts/tests、机器报告共同绑定的TESTED_IMPLEMENTATION_HEAD、FINAL_IMPORT_CANDIDATE_HEAD、二者仅evidence-only精确差异、unit与acceptance独立结果和X2；
- baseline root commit是feature HEAD祖先，establishment report/sidecar与Git tree OID一致；
- remote empty；
- 无外部闲鱼访问。

允许结论：`PASS_IMPORT_CANDIDATE` 或 `FAIL`。

审核者将结论写入control root：

```text
workspace/review-queue/commerce-v1/decision-to-main-x2/final/
├── IMPORT_INDEPENDENT_AUDIT.json
└── IMPORT_INDEPENDENT_AUDIT.json.sha256.sidecar
```

报告绑定`DUAL_ROOT_BINDING_V1.json` SHA、FINAL_IMPORT_CANDIDATE_HEAD、control-root治理对象SHA和审核运行UTC；审核者不得修改feature。

只允许一轮 finding 修复和一次 scoped re-review。任何修复产生新 HEAD，旧审核立即失效。

**成功状态：** `IMPORT_AUDIT_PASS`。

---

### D13 — 证据冻结、知识库与停点

#### D13.1 Control-root raw evidence

```text
workspace/review-queue/commerce-v1/decision-to-main-x2/final/
├── RAW_IMPORT_MAPPING_MANIFEST.json
├── FINAL_IMPORT_MAPPING_MANIFEST.json
├── MAIN_COMMERCE_UNIT_RESULTS.json
├── MAIN_COMMERCE_ACCEPTANCE_RESULTS.json
├── MAIN_SECURITY_REGRESSION.json
├── MAIN_X2_RUN.json
├── MAIN_X2_ACCEPTANCE.json
├── MAIN_SOURCE_NONMUTATION.json
├── DUAL_ROOT_BINDING_V1.json
├── IMPORT_INDEPENDENT_AUDIT.json
└── sidecars
```

#### D13.2 Feature-root tracked summary

```text
docs/commerce/evidence/import-phase2/
├── README.md
├── CURRENT_STATUS.md
├── EVIDENCE_INDEX.json
├── IMPORT_MAPPING_SUMMARY.json
├── TEST_SUMMARY.json
├── X2_SUMMARY.json
└── SHA256SUMS.txt
```

上述feature-root summary已在D11.5、独立审核前提交并冻结；D13只读复算，绝不补写独立审核摘要。独立审核结论只存在control-root raw evidence与Obsidian。不得提交runtime DB、receipts、ZIP、客户/支付数据或秘密。

#### D13.3 状态同步

验证feature HEAD仍等于D12审核的`FINAL_IMPORT_CANDIDATE_HEAD`、worktree clean、remote empty、baseline ancestor成立；任何变化使D12失效并停止。control-root main也必须保持baseline tracked tree clean。

Obsidian `00/02/03/06/07/08` 是仓外知识库，由Luna在D13只同步事实，不进入Git提交；更新前记录before/after SHA。Obsidian必须明确“feature import candidate，尚未merge”，不得写成main已导入，并区分外置X2、主工程feature X2、真实试点三层证据。raw evidence、Approval和audit receipt只写control-root review queue。

#### D13.4 提交与停止

D12之后不再创建任何feature commit；若必须修正文档，则旧D12立即失效并回到D11.5重新冻结、重新绑定、重新独立审核。保留feature branch，不merge、不push、不tag。

最终只能报告：

```text
COMMERCE_IMPORT_CANDIDATE_PASS
MAIN_PROJECT_X2_SYNTHETIC_PASS
MERGE_NOT_AUTHORIZED
REAL_COMMERCE_PILOT_NOT_STARTED
REMOTE_REPOSITORY_NOT_CONFIGURED
HUMAN_ONLY_DECISION_GATE_AND_GIT_BASELINE_ACTIONS_COMPLETED_BY_JOVI
```

---

## 8. 每阶段统一回归

治理阶段每个写操作后：

```powershell
py -3.12 -B .\scripts\run-security-semantics.py
if ($LASTEXITCODE -ne 0) { throw 'security semantics regression failed' }
py -3.12 -B .\tests\test_s2a2_enforcement.py
if ($LASTEXITCODE -ne 0) { throw 'S2A2 regression failed' }
py -3.12 -B .\tests\test_s1_integrity.py
if ($LASTEXITCODE -ne 0) { throw 'S1 integrity regression failed' }
py -3.12 -B .\tests\test_s2a1_control_plane.py
if ($LASTEXITCODE -ne 0) { throw 'S2A1 regression failed' }
py -3.12 -B .\tests\hooks\test_pre_tool_guard.py
if ($LASTEXITCODE -ne 0) { throw 'pre-tool guard regression failed' }
```

Git阶段每个提交前：

```powershell
git diff --check
if ($LASTEXITCODE -ne 0) { throw 'git diff check failed' }
$statusLines = @(git status --short)
if ($LASTEXITCODE -ne 0 -or $statusLines.Count -ne 0) { throw 'worktree is not clean' }
$remoteLines = @(git remote -v)
if ($LASTEXITCODE -ne 0 -or $remoteLines.Count -ne 0) { throw 'remote must remain empty' }
```

每轮 Luna 报告：

```text
完成：
未完成：
测试：
证据：
风险：
下一步：
提交：
当前状态：
需要 Jovi 的动作：
```

测试数量只能引用机器 JSON。

---

## 9. 立即停止与回滚

立即停止：

- G3、13/13、V4、候选或外置 HEAD 漂移；
- D2 amendment audit 为 FAIL，或 V2.1 差异不再是精确 `0 removed + 19 added + 2 modified(Prompt, MANIFEST_POLICY)`；
- `CODEX_START_PROMPT.txt` 仍含 revision marker、离开 immutable Framework 或 static pointer失配；
- proposed Decision 提前变成 human=true；
- formal Decision 非 Jovi交互产生或 sidecar失配；
- Hook TRUST/恢复/依赖；
- `MANIFEST.sha256` 变化；
- structural migration超出Decision-bound十二个formal targets，或Framework Manifest apply超出唯一`FRAMEWORK_MANIFEST.sha256`；
- Post-Apply FAIL；
- closeout 超出三文件、修改 Prompt 或 before SHA 不匹配；
- Gate receipt 与 Plan SHA 不匹配；
- C/APPLY 不成立；
- Git baseline receipt 缺失、非 Jovi、与 exact manifest 不匹配；
- importer 回退到 Windows checkout bytes，或 83-file Git blob evidence 不匹配；
- 未知 worktree 变化；
- PII、秘密、真实付款或平台数据；
- remote 被配置；
-独立 Import Audit FAIL。

回滚：

- D4 structural+Framework：把十二个structural targets和一个Framework Manifest作为同一十三目标恢复单元，全部恢复exact old-byte backup后再验证；禁止只恢复Manifest或只恢复部分结构文件；
- 若V2.1 APPLY后失败：十三目标整体恢复V2周期before bytes；不得临时把Prompt/Policy hash写回清单伪造PASS；
- closeout：三文件原子恢复 before bytes；
- C/APPLY：不得改历史或 `reset --hard`，只能另行受控 revision；
- feature：使用 revert commit，不修改 main baseline；
- runtime：只清理当前任务创建、已解析确认的 ignored 绝对目录。

---

## 10. 下一阶段，不属于本计划

本计划完成后，下一阶段才是：

```text
COMMERCE-PILOT-PHASE3
```

它需要：Jovi选择原创 SKU、权利/定价/EULA/退款/支持范围确认、feature merge 单独批准、X3/X4 人工边界和真实成交证据。不得在本计划内提前执行。
