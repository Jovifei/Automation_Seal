# route-b-landing-readiness Specification

## Purpose
为 Route B 真实落地建立 fail-closed 的就绪准备能力：在阶段门批准之前，预先产出受控分析产物（字节绑定决策、GATE_A 计划草稿、目标机验证清单、一致性修复提案、Track P/I 解锁即执行步骤序列），使门后执行延迟趋零且不提前写入任何真实字节。
## Requirements
### Requirement: Readiness artifacts MUST be fail-closed
所有落地就绪产物 SHALL 以 fail-closed 方式产出：不得写入 10 目标任何真实字节、不得翻转 `real_apply` / `formal_manifest_real_write` / `hook_trust` / `track_p` / `track_i` / `publish` 任一门、不得创建或修改 `workspace/approvals/*.approval.json`、不得修改 `MANIFEST` 清单哈希。

#### Scenario: Prep runs without touching gates or target bytes
- **WHEN** 执行就绪准备（生成 4 份产物 + 复跑 pre-flight）
- **THEN** 10 目标 `current_sha256` 与决策 JSON 逐字节一致、所有门仍为 false、`workspace/approvals/` 目录无新增回执文件

### Requirement: Byte-binding decision input is explicit
就绪产物 SHALL 显式给出「正式清单缺口」的本质：10 目标 `formal_expected_sha256` 全部来自 `OUTER_ARCHIVE_HASH_MISMATCH` 且无权威字节来源的包；并给出推荐绑定（方案 A：真实 APPLY 期望绑定到 `current_sha256`）及备选方案 B/C。

#### Scenario: Reviewer can locate the gap and the recommended binding
- **WHEN** 独立审计方或用户打开字节绑定提案
- **THEN** 能读到每个目标的 `current_sha256` 与 `formal_expected_sha256` 差异、被标 `requires_future_exact_apply_decision: true`，以及推荐方案 A 的依据

### Requirement: GATE_A plan draft reflects true track status
就绪产物 SHALL 产出一份供 `Approve-Gate.ps1` 消费的 GATE_A 计划 JSON 草稿，其中 track 状态 MUST 诚实反映当前 blocker（在独立审计决策 / Hook 信任 / 正式清单缺口未解除前标注 `BLOCKED`），不得伪造 `non-blocked` 状态以绕过脚本的 `throw "Track ... is blocked"` 守卫。

#### Scenario: Draft does not mask blockers
- **WHEN** 检查 GATE_A 计划草稿的 track 状态字段
- **THEN** Track P 与 Track I 均标注为 `BLOCKED`（或等价语义），且草稿头部注明「需用户本人运行 `Approve-Gate.ps1` 方可生成正式回执」

### Requirement: Target-machine verification list is enumerable
就绪产物 SHALL 给出逐项目标机核查清单，覆盖：真实树零漂移复算、回滚演练有效性、Windows / Codex / Hook 信任态 / Docker-WSL / GPU / 闲鱼本地状态 / 备份恢复 / 许可证边界，每项标注「目标机未验证 → NOT_VERIFIED」或已验证证据。

#### Scenario: Each item has a verifiable check
- **WHEN** 操作者按清单逐项核查
- **THEN** 每项存在可执行命令或判定条件，并能产出 pass / NOT_VERIFIED 结论

### Requirement: Modbus parser.py consistency fix is proposed, not applied
就绪产物 SHALL 分析 ZIP 与当前源码 12/13 一致（`parser.py` 不一致）的根因，并给出最小修复方案作为「受控入口解门」的前置输入；该修复 MUST 停留在提案态，真实修改仅在 Hook 经显式信任且门开后执行。

#### Scenario: Fix stays as proposal until gates open
- **WHEN** 一致性修复提案落盘
- **THEN** `products/Modbus*/*/parser.py`（或对应路径）真实字节未变，提案仅含根因分析与最小 diff 建议

### Requirement: Track P/I unlock step sequence is ordered with rollback points
就绪产物 SHALL 给出阶段门批准后按序执行的精确命令序列（Track I 部署 → 真实 APPLY → Track P 发布）及每步回滚点；序列 MUST 引用本载体证据链（`APPLY_PLAN.md` / `VERIFICATION_EVIDENCE.json` / pre-flight JSON），且明示「仅在 `workspace/approvals/` 出现真实回执后执行」。

#### Scenario: Sequence is gated on real approval receipt
- **WHEN** 操作者尝试按步骤序列执行
- **THEN** 序列首步判定 `workspace/approvals/GATE_A.P.approval.json` 与 `GATE_A.I.approval.json` 存在，缺失则中止并提示用户运行 `Approve-Gate.ps1`

### Requirement: Evidence chain is re-anchored by read-only pre-flight
就绪产物 SHALL 复用已归档载体（`route-b-qualification-controlled-apply`）的证据，并复跑只读 pre-flight 以断言：10/10 一致、零漂移、`gate_all_false=true`、`audit_pass=true`，输出可重算 JSON 到受管暂存区。

#### Scenario: Pre-flight re-asserts zero-drift and closed gates
- **WHEN** 复跑 `route_b_preflight.py`
- **THEN** 输出 `matched=10/10`、`mismatched=[]`、`gate_all_false=true`、`audit_pass=true`，且退出码为 0

