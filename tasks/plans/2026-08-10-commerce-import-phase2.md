# JOVI-AUTOMATION-COMMERCE-IMPORT-PHASE2

> **交给 Luna：** 先使用 `executing-plans` 逐任务执行；主工程形成有效 Git 基线并创建独立 worktree 后，再使用 `subagent-driven-development`。所有实现或适配任务必须使用 `test-driven-development`，所有阶段出口必须使用 `verification-before-completion`。独立审核 Agent 不得参与被审内容的生成或修复。
>
> **主工程：** `E:\project\jovi-automation`
>
> **外置已验证来源：** `E:\project\jovi-commerce-engine-v1\.worktrees\landing-phase1`
>
> **计划目标：** 完成治理人类门、把外置 X2 成果按 SHA 受控导入主工程、在主工程重新通过 X2 合成闭环；不进入真实 SKU 试点，不发布，不访问外部闲鱼仓。

---

## 0. 当前事实、最终目标与阶段判断

### 0.1 当前已完成

外置 Commerce staging 已完成 S1-S9：

- Feature 分支：`feature/commerce-landing-phase1`。
- 证据冻结 HEAD：`7dbe080c907c1da2eef1c16b79e677e6a1d49470`。
- 实现审阅 HEAD：`fd2321d5a3f12aa923014cadbc397849903fd97c`。
- Git 工作树干净，`git remote -v` 无输出。
- 全量单元/集成/验收测试：`99 PASS`，`4` 个已说明的 Windows symlink/platform skip。
- X2：`X2_STAGING_COMMERCE_FLOW_PASS`。
- X2 工件 Manifest：`47/47`；步骤证据：`8/8`。
- Xianyu 本地 validator：`PASS`；`publish/send_message/deliver/change_price/refund` 全为 `false`。
- 外置来源证据：Commerce 候选 `20/20`，source import `22/22`，主工程保护快照 `40/40`。
- 没有真实付款、真实客户、真实平台动作、远端仓库或 human-only 入口。

主工程当前事实：

- 控制面为 `S1/CLOSED/1`。
- blocker 为 `HOOK_UNTRUSTED`、`FORMAL_MANIFEST_MISMATCH`。
- Hook 必须继续保持 `DO_NOT_TRUST`，且不是运行依赖。
- `governance-v2` 候选包和 Pre-Decision validator 已存在。
- 当前不存在持久化 G3 PASS 回执、正式 Decision V3、Post-Apply Audit、Gate Plan、Gate A.P receipt。
- 主工程 `.git` 没有有效 HEAD。
- 主工程正式 `jovi_commerce/`、`docs/commerce/`、`schemas/commerce/`、`tests/commerce/` 尚不存在。
- Obsidian `07-JOVI-AUTOMATION-COMMERCE-LANDING-PHASE1.md` 已记录外置 X2；`00/02/03/06` 仍是治理冻结时的旧状态，不能在 G3/Decision 前擅自改写。

### 0.2 最终项目效果

项目最终要达到：

```text
原创数字产品资产
→ 人工审核的商品草稿
→ 本地匿名订单
→ Jovi 人工确认付款
→ 授权与可验证交付包
→ Jovi 人工发送
→ 脱敏售后
→ 聚合商业指标
→ 单 SKU 商业验证
```

Commerce Core 始终与渠道适配器分离；真实发布、消息、收款、交付、改价、退款和验证始终由 Jovi 控制。

### 0.3 当前进度口径

| 范围 | 当前状态 | 进度口径 |
|---|---|---:|
| 外置 Commerce Engine / X2 staging | 已验收 | 100% |
| 主工程治理准备 | 候选已冻结，缺人类门 | 约 90% |
| 主工程导入与复验 | 未授权、未开始 | 0% |
| 单 SKU 真实人工试点 | 未开始 | 0% |
| 最终商业闭环 | 管理估算，不是验收率 | 约 45% |

### 0.4 本阶段唯一出口

```text
COMMERCE_IMPORT_CANDIDATE_PASS
MAIN_PROJECT_X2_SYNTHETIC_PASS
MERGE_NOT_AUTHORIZED
REAL_COMMERCE_PILOT_NOT_STARTED
REMOTE_REPOSITORY_NOT_CONFIGURED
HUMAN_ONLY_ENTRYPOINTS_NOT_IMPLEMENTED
```

本阶段不得报告：

- 自动售卖已上线；
- 主工程已发布；
- 真实付款或交付已通过；
- `COMMERCE_V1_PILOT_PASS`；
- 无人值守商业系统已完成。

---

## 1. 角色、权限与永久边界

### 1.1 角色

- **Luna：** 只读核验、生成候选、运行测试、受授权应用精确字节、导入与适配、生成证据；不得签发人类 Decision/Approval，不得运行 human-only 脚本。
- **Jovi：** 签发 Decision V3、授权 S1 closeout 精确字节、运行 Gate A.P human-only 入口、授权主工程 Git 基线和精确导入集合。
- **G3 独立审核 Agent：** 审核当前未筛选真实树与 V4 包，生成真实报告及 sidecar；不得由 Luna 代写。
- **Post-Apply 独立审核 Agent：** 在 Framework Manifest APPLY 后只读审核；不得参与 APPLY。
- **Import 独立审核 Agent：** 审核 feature worktree 的导入映射、代码、测试和 X2 证据；不得参与导入实现。

### 1.2 永久禁止

- 不 TRUST、恢复、改写或依赖 Hook。
- 不修改 `MANIFEST.sha256`。
- 不伪造或代写 `workspace/approvals/` 和人类 Decision。
- Luna 不运行 `scripts/human-only/**` 或 `scripts/xianyu/human-only/**`。
- 不访问、读取或写入 `E:\project\xianyu-auto-reply`。
- 不读取 Cookie、Token、浏览器 Profile、平台消息、订单库、支付信息或客户 PII。
- 不自动发布、聊天、收款、发货、改价、退款或处理验证。
- 不修改遗留 `products/modbus-rtu-toolkit/`。
- 不配置 Git remote，不 push、merge、tag 或发布。
- 治理门通过前不写正式 Commerce 路径。

### 1.3 缺失输入的处理规则

人工或独立审核输入缺失时，Luna必须：

1. 输出精确 `WAITING_*` 状态；
2. 给出缺失文件、责任人和验真条件；
3. 保留已完成的技术结果；
4. 不把整个计划误报为工程失败；
5. 不自行补写、代签或绕过。

---

## 2. 现有可调用工具与不得假设的对象

### 2.1 已实测存在的治理脚本

```text
scripts/validate_commerce_predecision_readiness.py
scripts/validate_commerce_gate_readiness.py
scripts/generate_gate_a_plan.py
scripts/verify-gate-approval.py
scripts/apply_commerce_control_plane_transition.py
scripts/human-only/Approve-Gate.ps1
```

前五个可由 Luna 在对应阶段调用。最后一个只能由 Jovi 运行。

### 2.2 当前不存在，必须由对应任务生成

```text
workspace/review-queue/commerce-v1/governance-v2/G3_PREAPPLY_AUDIT_PASS_RERUN1.md
workspace/review-queue/commerce-v1/governance-v2/G3_PREAPPLY_AUDIT_PASS_RERUN1.md.sha256.sidecar
workspace/decisions/JOVI_S1_RESTART_DECISION_V3.json
workspace/decisions/JOVI_S1_RESTART_DECISION_V3.json.sha256.sidecar
reports/remediation/COMMERCE_V1_POST_APPLY_AUDIT.json
reports/remediation/COMMERCE_V1_POST_APPLY_AUDIT.json.sha256.sidecar
reports/gates/GATE_A_PLAN.json
workspace/approvals/GATE_A.P.approval.json
```

Luna不得把这些未来输出当作当前输入。

---

## 3. 总执行链

```text
I0 当前证据重验
→ I1 G3 回执落盘
→ I2 Jovi Decision V3
→ I3 Canonical mirror + Framework Manifest-only APPLY
→ I4 独立 Post-Apply Audit PASS
→ I5 S1 closeout 精确授权与应用
→ I6 Gate A.P 人工批准
→ I7 S1/CLOSED → C/APPLY
→ I8 主工程 Git 基线
→ I9 外置 Import Candidate 验真
→ I10 受控导入 feature worktree
→ I11 主工程测试与 X2 复验
→ I12 独立 Import Audit
→ I13 证据冻结与知识库同步
```

Track A（I0-I7）和 Track B 的来源复核可并行；正式导入 I10 必须等待 I7。

### 3.1 Luna 执行台账

计划正文与 sidecar 作为冻结输入，不在执行中直接改写。Luna在
`workspace/review-queue/commerce-v1/import-phase2/EXECUTION_LEDGER.md`
复制并维护以下清单：

- [ ] I0：主工程与外置来源 before snapshot 完成。
- [ ] I1：真实 G3 receipt 落盘、sidecar 与 13/13 目标验证通过。
- [ ] I2：Jovi Decision V3 已签发且 Luna 只读验证通过。
- [ ] I3：canonical mirror 完成，Framework Manifest-only APPLY 通过。
- [ ] I4：新的独立 Post-Apply Audit 为 PASS。
- [ ] I5：S1 closeout 精确候选经 Jovi 授权后应用，blockers 为空。
- [ ] I6：Gate readiness PASS，Jovi Gate A.P receipt 验证通过。
- [ ] I7：控制面完成 `S1/CLOSED → C/APPLY`。
- [ ] I8：主工程 Git baseline 与 feature worktree 建立，remote 为空。
- [ ] I9：外置 evidence HEAD、实现 HEAD 和 Import Candidate 复验通过。
- [ ] I10：精确导入和主工程测试命名空间适配完成。
- [ ] I11：Commerce、治理回归和主工程 X2 全部 PASS。
- [ ] I12：独立 Import Audit 为 `PASS_IMPORT_CANDIDATE`。
- [ ] I13：证据冻结、知识库同步和 feature branch 停点完成。

任一人类门等待时，在台账记录 `WAITING_FOR_*`，不得勾选后续项。

---

## 4. Track A：治理人类门解锁

### I0 — 建立 Phase 2 执行包与双侧快照

**目的：** 只记录事实，不改变治理结论。

**允许写入：**

```text
workspace/review-queue/commerce-v1/import-phase2/
```

**输出：**

```text
CURRENT_FACTS_PHASE2.json
MAIN_PROTECTED_TREE_BEFORE.json
EXTERNAL_SOURCE_BEFORE.json
PHASE2_INPUT_STATUS.json
每个 JSON 的 .sha256.sidecar
```

**主工程快照至少覆盖：**

- Hook 三组件；
- `FRAMEWORK_MANIFEST.sha256`、`MANIFEST.sha256`；
- `config/control-plane-state.json`、`PROJECT_STATE.json`、`STATUS.md`、`CODEX_START_PROMPT.txt`；
- Decision、Approval、Gate 目录文件集合；
- `governance-v2` 全文件；
- Commerce 候选 20 项；
- `products/modbus-rtu-toolkit/`；
- Obsidian `00/02/03/06/07`。

**外置来源快照至少覆盖：**

- 分支、HEAD、status、remote；
- `reports/product/` 的证据和 sidecar；
- `SOURCE_IMPORT_MANIFEST.json`；
- 实现 HEAD 的 83 个 tracked 文件；
- X2 acceptance 47/47 和 8/8。

**验收：**

```text
MAIN_PROTECTED_SNAPSHOT_CAPTURED
EXTERNAL_SOURCE_7DBE080_CLEAN
EXTERNAL_REMOTE_EMPTY
```

**失败状态：**

- 外置 HEAD 变化：`BLOCKED_EXTERNAL_SOURCE_HEAD_DRIFT`。
- 外置 dirty：`BLOCKED_EXTERNAL_SOURCE_DIRTY`。
- 主工程出现无法归因漂移：`BLOCKED_MAIN_UNATTRIBUTED_DRIFT`。

不清理、不覆盖、不自动重新复制新字节。

---

### I1 — G3 独立回执落盘与验证

#### I1.1 回执来源

优先由此前给出 `PASS_READY_FOR_JOVI_DECISION` 的原独立审核 Agent落盘同一次审核：

```text
workspace/review-queue/commerce-v1/governance-v2/G3_PREAPPLY_AUDIT_PASS_RERUN1.md
workspace/review-queue/commerce-v1/governance-v2/G3_PREAPPLY_AUDIT_PASS_RERUN1.md.sha256.sidecar
```

若原审核 Agent无法落盘，Luna停止为：

```text
WAITING_FOR_FRESH_G3_AUDIT
```

并由 Jovi 新开 lineage 外独立 Agent重新审核。Luna不得代写。

#### I1.2 报告最低字段

- `verdict=PASS_READY_FOR_JOVI_DECISION`；
- `independent=true`；
- 审核者未参与整改或候选生成；
- Final Target Set `13/13`；
- RERUN1 human-only `PASS_ZERO_DRIFT`；
- V4 Package `18/18`；
- Hook `DO_NOT_TRUST`；
- 三个 Hook 布尔值显式 `false`；
- Framework 11 项失配属于预期 APPLY 前集合；
- 未创建 Decision、Gate、Approval 或正式 Commerce runtime；
- 未访问外部闲鱼仓；
- 审核 UTC、Final Target Set SHA、V4 Manifest SHA。

#### I1.3 Luna只读验证

```powershell
py -3.12 -B .\scripts\validate_commerce_predecision_readiness.py `
  --root . `
  --package .\workspace\review-queue\commerce-v1\governance-v2 `
  --output .\workspace\review-queue\commerce-v1\import-phase2\PREDECISION_RECHECK.json
```

并独立复算：

- G3 body 与 sidecar；
- Final Target Set 13 项 live SHA/length；
- Decision candidate；
- Controlled Baseline candidate；
- Framework Manifest V2 candidate；
- V4 review package Manifest；
- Commerce candidate 20/20。

**出口：**

```text
G3_RECEIPT_BOUND
PREDECISION_READY
FINAL_CONTROL_TARGET_SET_13_OF_13
```

任一漂移则 `BLOCKED_G3_RECEIPT_OR_TARGET_DRIFT`，旧回执失效，重新独立审核。

---

### I2 — Decision V3 审阅包与 Jovi 人工签发

#### I2.1 Luna生成审阅包

输出：

```text
workspace/review-queue/commerce-v1/import-phase2/JOVI_DECISION_V3_SIGNING_INSTRUCTIONS.md
workspace/review-queue/commerce-v1/import-phase2/DECISION_V3_BINDINGS.json
对应 sidecar
```

必须列出当前精确 SHA、Manifest-only scope、回滚、Hook DNT 和全部禁止动作。

#### I2.2 Jovi人工创建

```text
workspace/decisions/JOVI_S1_RESTART_DECISION_V3.json
workspace/decisions/JOVI_S1_RESTART_DECISION_V3.json.sha256.sidecar
```

最低固定字段：

```json
{
  "issued_from_human": true,
  "hook_status": "DO_NOT_TRUST",
  "hook_runtime_dependency": false,
  "hook_restore_allowed": false,
  "hook_trust_allowed": false,
  "manifest_apply_scope": ["FRAMEWORK_MANIFEST.sha256"],
  "track_p_allowed": false,
  "track_i_allowed": false,
  "real_platform_actions_allowed": false
}
```

还必须绑定：

- G3 receipt SHA；
- Decision V3 candidate SHA；
- Controlled Baseline candidate SHA；
- Final Target Set SHA；
- Framework Manifest V2 candidate SHA；
- V4 Review Package Manifest SHA；
- Commerce Candidate Manifest SHA。

#### I2.3 Luna只读校验

- body SHA 等于 sidecar；
- `issued_from_human=true`；
- 三个 Hook 布尔值均为精确布尔 `false`；
- APPLY scope 只有 `FRAMEWORK_MANIFEST.sha256`；
- Track P/I、发布、平台动作没有隐藏 `true`；
- 所有 bindings 与 live 文件精确匹配。

失败：`BLOCKED_DECISION_V3_INVALID`。Luna不得修补人类 Decision。

---

### I3 — Canonical mirror 与 Manifest-only APPLY

**前置：** `DECISION_V3_ISSUED_AND_VERIFIED`。

#### I3.1 建立 Gate validator 所需 canonical 路径

当前脚本固定读取：

```text
workspace/review-queue/commerce-v1/governance/
```

仅从 `governance-v2/` 按字节复制：

```text
CONTROLLED_BASELINE_V2_CANDIDATE.json
CONTROLLED_BASELINE_V2_CANDIDATE.sha256
PRE_APPLY_AUDIT_INPUT_V4/**
```

目标若已存在则先比对；不一致时拒绝覆盖。复制后要求集合、长度、SHA 100% 一致。

#### I3.2 Manifest-only APPLY

允许修改的正式文件只有：

```text
FRAMEWORK_MANIFEST.sha256
```

执行前输出：

```text
MANIFEST_APPLY_BEFORE.json
FRAMEWORK_MANIFEST_BEFORE.backup
MANIFEST_ONLY_APPLY_PLAN.json
```

严格顺序：

1. 复算 Decision、G3、Final Target Set、candidate SHA；
2. 证明 Approval 尚不存在；
3. 证明 `MANIFEST.sha256` 当前 SHA；
4. 使用精确 candidate 字节替换 `FRAMEWORK_MANIFEST.sha256`；
5. 逐项复算 Framework Manifest，要求全部匹配；
6. 生成 APPLY 报告和 rollback SHA；
7. 证明 Hook、Decision、Approval、human-only、`MANIFEST.sha256`、控制面和外部仓未变化。

**出口：**

```text
CONTROLLED_BASELINE_V2_APPLIED
FRAMEWORK_MANIFEST_ALL_MATCHED
MANIFEST_SHA256_UNCHANGED
HOOK_DO_NOT_TRUST
```

任一失败立即使用已记录旧字节回滚 `FRAMEWORK_MANIFEST.sha256`，状态 `ROLLED_BACK_MANIFEST_APPLY_FAILURE`。

---

### I4 — 全新独立 Post-Apply Audit

由未参与 G3、APPLY 或候选生成的新 Agent只读审核，并由该 Agent生成：

```text
reports/remediation/COMMERCE_V1_POST_APPLY_AUDIT.json
reports/remediation/COMMERCE_V1_POST_APPLY_AUDIT.json.sha256.sidecar
```

最低字段：

```json
{
  "verdict": "PASS",
  "independent": true,
  "hook_status": "DO_NOT_TRUST",
  "framework_manifest_all_matched": true,
  "manifest_sha256_unchanged": true,
  "real_platform_actions": false
}
```

还必须绑定 Decision、G3、Final Target Set、Framework Manifest 和 APPLY report SHA。

**出口：** `POST_APPLY_AUDIT_PASS`。

FAIL 时只处理报告中的精确 finding；任何字节修复都要重新冻结和重新审核，不能复用旧 PASS。

---

### I5 — S1 blocker closeout（不假设现成脚本）

当前项目没有专用 S1 closeout 脚本。本任务不得假设它存在。

#### I5.1 生成精确候选

在 review queue 生成：

```text
workspace/review-queue/commerce-v1/import-phase2/s1-closeout/
├── S1_CLOSEOUT_PATCH_V1.json
├── S1_CLOSEOUT_TARGET_SET_V1.json
├── S1_CLOSEOUT_RECEIPT_CANDIDATE.json
├── proposed/config/control-plane-state.json
├── proposed/PROJECT_STATE.json
├── proposed/STATUS.md
└── proposed/CODEX_START_PROMPT.txt
```

规则：

- 读取 live revision，不硬编码；
- `state_revision + 1`；
- `previous_state_hash` 精确绑定 live canonical state；
- 保持 `stage=S1`、`phase_status=CLOSED`；
- blockers 变为 `[]`；
- `FORMAL_MANIFEST_MISMATCH` 的关闭证据为 Framework 全匹配 + Post-Apply PASS；
- `HOOK_UNTRUSTED` 不变为 TRUST，只作为 DNT 且 runtime dependency=false 的已接受限制写入 closeout receipt；
- `approval_binding` 仍为 `null`；
- 四份 authority/mirror 文件必须产生一致 marker；
- 不修改 Obsidian；冻结知识库在 C/APPLY 后再同步。

#### I5.2 Shadow 验证

- 在临时目录复制四文件；
- 用现有 `scripts/control_plane.py` 校验 before/after；
- 验证同阶段 `S1/CLOSED → S1/CLOSED` revision 递增合法；
- 运行 mirror 一致性和现有控制面回归；
- 验证只允许四个 target 变化。

#### I5.3 Jovi精确授权

Luna停止并请求：

```text
AUTHORIZE S1_CLOSEOUT_V1 <patch_sha256> <target_set_sha256>
```

收到完全匹配的授权后，Luna才按 proposed bytes 应用四文件，并生成正式 `S1_CLOSEOUT_RECEIPT.json`。

**出口：**

```text
S1_CLOSED_CLEAN
HOOK_DNT_ACCEPTED_LIMITATION
CONTROL_PLANE_BLOCKERS_EMPTY
```

任何未授权、before SHA 漂移或部分写入都要 fail-closed，并从 before snapshot 恢复四文件。

---

### I6 — Gate readiness、Gate Plan 与 Jovi Gate A.P

#### I6.1 Gate readiness

```powershell
py -3.12 -B .\scripts\validate_commerce_gate_readiness.py `
  --root . `
  --output .\workspace\review-queue\commerce-v1\import-phase2\GATE_READINESS_PHASE2.json
```

必须为 `PASS`，且同时证明：

- Decision V3 有效；
- canonical baseline/V4 包存在并匹配；
- Framework Manifest 全匹配；
- Post-Apply Audit 独立 PASS；
- state 为 `S1/CLOSED` 且 blockers 为空；
- Gate A.P 尚不存在；
- Track I、发布和五项平台动作仍为 false。

#### I6.2 生成一次 Gate Plan

```powershell
py -3.12 -B .\scripts\generate_gate_a_plan.py --root .
```

输出：

```text
reports/gates/GATE_A_PLAN.json
reports/gates/GATE_A_PLAN.sha256.txt
```

目标必须为 `Commerce V1 local product track`；Track P 为 `AWAITING_HUMAN_APPROVAL`，Track I 为 `NOT_AUTHORIZED`。

#### I6.3 Jovi运行 human-only Gate

仅 Jovi 运行：

```powershell
powershell -File .\scripts\human-only\Approve-Gate.ps1 `
  -Gate GATE_A `
  -Track P `
  -PlanPath .\reports\gates\GATE_A_PLAN.json `
  -ExpectedSha256 <GATE_A_PLAN_SHA256> `
  -Approver Jovi
```

Luna不得运行或模拟输入。

#### I6.4 Luna验证 receipt

```powershell
py -3.12 -B .\scripts\verify-gate-approval.py `
  --root . `
  --gate GATE_A `
  --track P
```

**出口：** `GATE_A_P_VERIFIED`。

---

### I7 — 哈希绑定转换到 C/APPLY

先生成：

```text
workspace/review-queue/commerce-v1/import-phase2/COMMERCE_IMPORT_TARGET_SET_V1.json
workspace/review-queue/commerce-v1/import-phase2/COMMERCE_IMPORT_SCOPE_PATCH_V1.json
```

Target Set 只允许后续正式路径：

```text
jovi_commerce/**
docs/commerce/**
schemas/commerce/**
tests/commerce/**
tests/fixtures/commerce/synthetic-digital-checklist/**
pyproject.toml
.gitignore
```

明确排除 `products/**`、Approval、Decision、Manifest、Hook、human-only、外部闲鱼、真实数据和 runtime DB。

先 dry-run：

```powershell
py -3.12 -B .\scripts\apply_commerce_control_plane_transition.py `
  --root . `
  --plan .\reports\gates\GATE_A_PLAN.json `
  --receipt .\workspace\approvals\GATE_A.P.approval.json `
  --target-set-sha256 <IMPORT_TARGET_SET_SHA256> `
  --patch-sha256 <IMPORT_SCOPE_PATCH_SHA256>
```

只有 dry-run 为 `READY_TO_APPLY` 才运行同一命令加 `--apply`。

转换必须为当前 live revision 的：

```text
S1/CLOSED → C/APPLY
```

**出口：** `CONTROL_PLANE_C_APPLY`。

Track I、发布和真实平台动作保持关闭。

---

## 5. Track B：主工程 Git 基线与受控导入

### I8 — 建立主工程受控本地 Git 基线

**前置：** `GATE_A_P_VERIFIED` + `CONTROL_PLANE_C_APPLY`。

#### I8.1 生成审阅材料

```text
workspace/review-queue/commerce-v1/import-phase2/git-baseline/
├── GIT_BASELINE_FILES_V1.txt
├── GIT_BASELINE_MANIFEST_V1.json
├── SECRET_SCAN_REPORT_V1.json
├── GIT_BASELINE_REVIEW_V1.md
└── sidecars
```

使用 `rg --files` 发现文件，再由显式排除规则生成清单。不要假设 `run-secret-scan.py` 存在。

排除：

- `.git/`、`.worktrees/`；
- `workspace/approvals/`、`workspace/review-queue/`；
- reports、logs、backups、runtime data、数据库、回执、缓存、临时 ZIP；
- `.env`、秘密、浏览器或平台数据；
- 外部项目。

秘密扫描只保存脱敏分类、路径和行号；不得把秘密值复制到报告。

#### I8.2 Jovi授权

```text
AUTHORIZE MAIN_GIT_BASELINE_V1 <file_list_sha256> <manifest_sha256>
```

#### I8.3 初始化

在暂存任何文件前：

- 把 `.worktrees/` 加入主工程 `.gitignore`；
- 新建 `.gitattributes`，采用 `* -text` 锁定工作树字节，防止 Windows CRLF 自动归一化再次破坏 provenance；
- 执行 `git config --local core.autocrlf false`；
- 将 `.gitignore`、`.gitattributes` 纳入精确 baseline 清单并重新计算清单 SHA。

```powershell
git init -b main
git config --local core.autocrlf false
git remote -v
git add --pathspec-from-file=<EXPLICIT_BASELINE_PATHSPEC_FILE>
git diff --cached --check
git commit -m "chore: establish audited jovi automation baseline"
```

禁止 `git add .`。

随后：

- 建立分支 `feature/commerce-import-phase2`；
- 建立 worktree `E:\project\jovi-automation\.worktrees\commerce-import-phase2`；
- 不配置 remote。

**出口：**

```text
MAIN_GIT_BASELINE_ESTABLISHED
MAIN_REMOTE_EMPTY
IMPORT_WORKTREE_READY
```

---

### I9 — 外置 Import Candidate 最终验真

在任何复制前复核外置仓：

```powershell
git -C E:\project\jovi-commerce-engine-v1\.worktrees\landing-phase1 status --short
git -C E:\project\jovi-commerce-engine-v1\.worktrees\landing-phase1 rev-parse HEAD
git -C E:\project\jovi-commerce-engine-v1\.worktrees\landing-phase1 remote -v
```

要求：

- HEAD 精确为 `7dbe080c907c1da2eef1c16b79e677e6a1d49470`；
- 工作树干净；
- remote 为空；
- `IMPORT_CANDIDATE_MANIFEST.json` 绑定实现 HEAD `fd2321d...`；
- 83 个实现 tracked files SHA 匹配；
- 证据 sidecar 100% 匹配；
- Test 99 PASS / 4 expected skips；
- X2 47/47、8/8；
- source 20/20、22/22、protected 40/40。

输出：

```text
workspace/review-queue/commerce-v1/import-phase2/EXTERNAL_IMPORT_RECHECK.json
workspace/review-queue/commerce-v1/import-phase2/EXTERNAL_IMPORT_RECHECK.json.sha256.sidecar
```

**出口：** `EXTERNAL_IMPORT_CANDIDATE_VERIFIED`。

---

### I10 — 精确导入与命名空间适配

#### I10.1 导入映射

| 外置来源 | 主工程目标 | 处理 |
|---|---|---|
| `jovi_commerce/**` | `jovi_commerce/**` | 首次导入保持字节；必要适配另提交 |
| `docs/commerce/AUTOMATED_COMMERCE_ARCHITECTURE.md`、`S7_SUPPORT_METRICS_CLI.md`、`S8_X2_WORKFLOW.md` | `docs/commerce/**` | 导入产品文档；明确排除外置 `docs/commerce/STATUS.md` |
| `schemas/commerce/**` | `schemas/commerce/**` | 10 份交换契约按字节导入 |
| `tests/unit/**` | `tests/commerce/unit/**` | 受控改路径后记录 source/target SHA |
| `tests/acceptance/**` | `tests/commerce/acceptance/**` | 受控改路径后记录 source/target SHA |
| `tests/fixtures/commerce/synthetic-digital-checklist/**` | `tests/fixtures/commerce/synthetic-digital-checklist/**` | 合成 fixture 按字节导入 |
| `pyproject.toml` | `pyproject.toml` | 新建，保持依赖为标准库 |
| 外置证据/provenance | `workspace/review-queue/commerce-v1/import-phase2/external-evidence/**` | 证据复制，不进入产品 runtime |

#### I10.2 明确不导入

- 外置 `.git/`、`.worktrees/`、AGENTS、README、tasks；
- 外置 runtime DB、receipts、临时包、缓存、logs；
- 外置 `reports/product/CURRENT_STATUS.md` 到正式产品路径；
- human-only 脚本；
- `products/` 内容；
- 外部闲鱼代码或数据；
- 任何真实客户或支付数据。

#### I10.3 必要的测试路径适配

因为测试从 `tests/unit` 移到 `tests/commerce/unit`：

- fixture path 从 `parents[1]` 调整为主工程真实 `tests/fixtures/commerce`；
- acceptance root 从原外置层级调整为主工程 root；
- 更新模块发现命令为 `unittest discover -s tests/commerce`；
- 每个改变记录 `source_sha256`、`target_sha256`、`reason=MAIN_TEST_NAMESPACE_ADAPTATION`；
- 不改变业务语义、fixture 内容和安全断言。

#### I10.4 TDD与小提交

1. 先复制测试到目标命名空间，确认因模块未导入/路径未适配而 RED；
2. 导入最小 runtime；
3. 只做命名空间和主工程兼容适配；
4. focused GREEN；
5. full Commerce 回归；
6. 主工程安全回归；
7. 独立规格与质量审核；
8. finding 修复；
9. 小提交。

建议提交：

```text
docs: import reviewed commerce contracts
feat: import commerce engine x2 candidate
test: adapt commerce tests to main project namespace
```

---

### I11 — 主工程全量验证与 X2 重跑

#### I11.1 Commerce 回归

```powershell
$env:PYTHONPATH='.'
py -3.12 -B -m unittest discover -s tests/commerce -v
py -3.12 -B -m compileall -q jovi_commerce tests/commerce
```

验收：原 99 项必须全部 PASS；4 个 Windows skip 只能在原因和条件完全相同的情况下继续记录为 expected。新增适配测试计数以机器报告为准，不手工硬编码。

#### I11.2 主工程治理回归

```powershell
py -3.12 -B .\scripts\run-security-semantics.py
py -3.12 -B .\tests\test_s2a2_enforcement.py
py -3.12 -B .\tests\test_s1_integrity.py
py -3.12 -B .\tests\test_s2a1_control_plane.py
py -3.12 -B .\tests\hooks\test_pre_tool_guard.py
py -3.12 -B -m unittest tests.test_commerce_gate_readiness -v
py -3.12 -B -m unittest tests.test_control_plane_commerce_transition -v
```

任何既有治理测试回归即停止导入，不扩大 allowlist 掩盖失败。

#### I11.3 主工程 X2

在被 `.gitignore` 排除的全新临时目录运行：

```powershell
py -3.12 -B -m jovi_commerce x2 run `
  --work-dir <MAIN_X2_TEMP_DIR>
```

必须重新证明：

- 一个订单、一个付款、一个 Entitlement、一个交付包；
- 最终 `READY_FOR_HUMAN_DELIVERY`；
- 幂等重放不增加效果；
- 事件链和 JSON receipt 一致；
- artifact Manifest 全匹配；
- 未付款、权利阻塞、非法跳级、链断裂、路径逃逸、包篡改均 fail-closed；
- Xianyu 五项动作全 false；
- 无 PII、秘密、真实付款或外部平台访问。

额外只读运行主工程现有 validator：

```powershell
py -3.12 -B .\scripts\xianyu\validate_xianyu_bundle.py `
  --bundle <MAIN_X2_BUNDLE_JSON> `
  --schema .\deploy\xianyu\xianyu_bundle.schema.json
```

#### I11.4 Git与来源卫生

```powershell
git diff --check
git status --short
git remote -v
```

测试运行后只允许预期、被忽略的 runtime 输出；tracked tree 不得被测试污染。

**出口：**

```text
MAIN_PROJECT_COMMERCE_TESTS_PASS
MAIN_PROJECT_SECURITY_REGRESSION_PASS
MAIN_PROJECT_X2_SYNTHETIC_PASS
```

---

### I12 — 独立 Import Audit

由未参与导入的新 Agent对 feature worktree 只读审核，至少检查：

- Gate A.P 与 `C/APPLY` 的有效性；
- 外置来源 HEAD、83 文件证据和导入 allowlist；
- source/target SHA 与每个适配差异；
- 正式路径中没有 products、human-only、真实数据或平台动作；
- 状态机、SQLite Hash 链、幂等和 ZIP；
- Xianyu 五项 false；
- 主工程治理回归；
- remote 为空；
- 外部闲鱼仓没有访问证据；
- Modbus SKU 未变化。

允许结论：

```text
PASS_IMPORT_CANDIDATE
FAIL
```

仅允许一轮 finding 修复和一次 scoped re-review。修复后重新跑受影响测试与全量回归；旧审核绑定的 commit 失效。

输出：

```text
workspace/review-queue/commerce-v1/import-phase2/IMPORT_INDEPENDENT_AUDIT.json
workspace/review-queue/commerce-v1/import-phase2/IMPORT_INDEPENDENT_AUDIT.json.sha256.sidecar
```

---

### I13 — 证据冻结、知识库同步与分支停点

#### I13.1 最终证据

原始运行工件继续留在被 Git 排除的 review queue：

```text
workspace/review-queue/commerce-v1/import-phase2/
├── IMPORT_MAPPING_MANIFEST.json
├── MAIN_COMMERCE_TEST_RESULTS.json
├── MAIN_X2_ACCEPTANCE.json
├── MAIN_SOURCE_NONMUTATION.json
├── MAIN_SECURITY_REGRESSION.json
├── IMPORT_INDEPENDENT_AUDIT.json
├── COMMERCE_IMPORT_PHASE2_STATUS.md
└── sidecars
```

同时生成不含 runtime 数据、可提交的证据索引：

```text
docs/commerce/evidence/import-phase2/
├── README.md
├── EVIDENCE_INDEX.json
├── IMPORT_MAPPING_SUMMARY.json
├── TEST_SUMMARY.json
├── X2_SUMMARY.json
├── INDEPENDENT_AUDIT_SUMMARY.json
└── SHA256SUMS.txt
```

可提交索引只记录状态、命令、计数、SHA 和 review-queue 相对证据标识；不得包含 SQLite、客户数据、运行包或秘密。

Manifest 必须绑定：

- main feature HEAD；
- baseline commit；
- Gate Plan/receipt；
- control-plane state；
- external evidence HEAD `7dbe080...`；
- implementation HEAD `fd2321d...`；
- 全部导入/适配文件 SHA；
-测试、X2、独立审核 SHA；
- remote 为空；
- real pilot `NOT_STARTED`。

#### I13.2 知识库同步

在 G3/Decision 前不得修改被冻结的 `00/02/03/06`。

达到 `CONTROL_PLANE_C_APPLY` 后，生成 `KNOWLEDGE_UPDATE_MANIFEST.json`，再同步：

```text
00-项目概览.md
02-当前进度.md
03-任务台账.md
06-自动售卖Commerce主线.md
07-JOVI-AUTOMATION-COMMERCE-LANDING-PHASE1.md
08-COMMERCE-IMPORT-PHASE2.md
```

知识库必须明确：

- 外置 X2 与主工程 X2 是两层不同证据；
- Feature branch 尚未 merge；
- 真实试点尚未开始；
- Hook 仍 DNT；
- Track I 和平台动作未授权；
- remote 为空；
- 下一阶段只能是 `COMMERCE-PILOT-PHASE3` 的人工批准准备。

#### I13.3 最终提交与停止

在 feature worktree 更新：

- `tasks/todo.md`；
- `STATUS.md`；
- `CHANGELOG.md`；
- `docs/commerce/evidence/import-phase2/**`。

建议最后提交：

```text
docs: freeze commerce import phase2 evidence
```

保留 `feature/commerce-import-phase2`，不 merge、不 push、不 tag。

---

## 6. 阶段测试矩阵

| 层级 | 必须证明 | 不得误报 |
|---|---|---|
| G3 | 候选与真实树可供人类 Decision | 不等于 Decision 已签发 |
| Manifest APPLY | Framework Manifest 精确匹配 | 不等于 Hook trusted |
| Post-Apply | 独立只读 PASS | 不等于 Gate 已批准 |
| Gate A.P | Track P 本地 Commerce 路径获批 | 不授权 Track I 或真实平台动作 |
| C/APPLY | 控制面允许精确本地导入 | 不等于 merge/release |
| Import tests | 主工程内实现通过 | 不等于真实客户/付款 |
| Main X2 | 纯合成闭环通过 | 不等于商业试点 |
| Import audit | Feature branch 可作为候选 | 不等于主分支上线 |

---

## 7. 每任务执行纪律

每个任务开始：

- 记录 live HEAD/state/SHA；
- 确认唯一 allowed paths；
- 确认不存在未知 dirty/untracked 变化；
- 把任务添加到当前执行台账；
- 非 Git 阶段不得声称有 commit。

每个实现或适配任务：

```text
RED
→ 验证失败原因正确
→ 最小实现
→ focused GREEN
→ full regression
→ spec review
→ quality review
→ finding remediation
→ fresh verification
→ small commit
```

每轮 Luna 固定报告：

```text
完成：
未完成：
测试：
证据：
风险：
下一步：
提交：
当前状态：
```

测试计数只能引用机器 JSON，不得从旧 Markdown 手工复制。

---

## 8. 立即停止条件

- G3 receipt/sidecar 不匹配或并非独立；
- Final Target Set 或 V4 包漂移；
- Decision 缺字段、sidecar 失配或出现隐藏权限 true；
- `MANIFEST.sha256` 被修改；
- Hook 被 TRUST、恢复或成为运行依赖；
- Post-Apply Audit 为 FAIL；
- Gate readiness 非 PASS；
- Gate A.P receipt 缺失、过期或与 Plan SHA 不匹配；
- 控制面不处于有效 `C/APPLY`；
- 外置 evidence HEAD、实现 HEAD 或 source Manifest 漂移；
- 主工程出现无法归因变化；
- 导入目标已存在不同字节；
- 发现 PII、秘密、真实付款或平台数据；
- 发生真实平台动作或访问外部闲鱼仓；
- Git remote 被配置；
- 独立 Import Audit 为 FAIL。

等待 Jovi 人工作用时使用 `WAITING_FOR_JOVI_*`，不得继续写入后续阶段。

---

## 9. 回滚策略

### 治理段

- Manifest-only APPLY：恢复 `FRAMEWORK_MANIFEST_BEFORE.backup`，复核其 SHA。
- S1 closeout：恢复四文件 before bytes，验证 canonical state 与镜像 marker。
- C/APPLY：保留状态哈希链，不使用 `git reset --hard`；任何回退必须另建受控状态 revision 与人类授权。

### Git/导入段

- baseline 后所有产品改动只在 feature worktree；回滚使用新的 revert commit，不破坏 main baseline。
- 不删除主工程历史、Approval、Decision 或审核证据。
- runtime 数据全部在 ignored 临时目录；清理只针对当前 X2 任务创建且已解析确认的绝对目录。

---

## 10. Luna 的首个动作

Luna接到本计划后只执行 I0 和 I1 的只读/证据检查。

如果 G3 回执仍不存在，必须停在：

```text
WAITING_FOR_G3_RECEIPT
EXTERNAL_X2_EVIDENCE_PRESERVED
MAIN_PROJECT_IMPORT_NOT_STARTED
```

并向 Jovi 给出原审核 Agent落盘回执的精确文件路径与验真要求。收到真实回执后从 I1.3 继续，不重做外置 Commerce Engine。
