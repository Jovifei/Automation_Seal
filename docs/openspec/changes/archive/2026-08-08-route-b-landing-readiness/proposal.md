## Why

Route B 的 10 个资格候选目标已通过受控 APPLY 载体（`route-b-qualification-controlled-apply`，已归档）完成「计划 + 可重算证据」落盘，但真实落地仍被数道显式门控挡着（独立审计决策、Hook 信任、阶段门批准、正式清单缺口）。在门控解除之前，执行侧存在「门一开就要能立即、零差错地真实 APPLY / 部署 / 发布」的就绪缺口——若等到批准瞬间才现编步骤，会把可避免的人为风险带进门后执行期。

本变更建立一套 **fail-closed 的落地就绪准备载体**：把门后执行所需的计划草稿、验证清单、一致性修复提案、步骤序列，全部以「只读 / 受控分析」形式预先产出并落盘到受管暂存区，使阶段门一旦批准，执行延迟趋零、且全程不提前写入任何真实目标字节、不翻转任何门、不伪造 approval。

## What Changes

- 新增 4 份 fail-closed 就绪产物（均落盘于 `workspace/review-queue/`，不触碰 `workspace/approvals/`、不修改 10 目标真实字节）：
  1. **GATE_A 计划草稿** —— 供 `Approve-Gate.ps1` 消费的 GATE_A 计划 JSON 草稿（track 状态据当前 blocker 标注，诚实反映 `BLOCKED`）。
  2. **目标机验证清单** —— 真实树零漂移、回滚演练有效性、Windows / Codex / Hook / Docker-WSL / GPU / 闲鱼本地状态 / 备份恢复 / 许可证边界的逐项目标机核查表。
  3. **Modbus `parser.py` 一致性修复提案** —— 解决 ZIP 与当前源码 12/13 一致（`parser.py` 不一致）的根因分析与最小修复方案，作为受控入口解门的前置输入。
  4. **Track P / Track I 解锁即执行步骤序列** —— 阶段门批准后按序执行的精确命令序列与回滚点。
- 复用既有受控载体（`route-b-qualification-controlled-apply` 的 `APPLY_PLAN.md` / `VERIFICATION_EVIDENCE.json`）作为证据链锚点，新增只读 pre-flight 复算以确认 10/10 一致、零漂移、门全 false。
- 本变更**不**真实 APPLY、**不**部署、**不**发布、**不**翻转 Hook 信任、**不**创建或修改 `workspace/approvals/*.approval.json`。

## Capabilities

### New Capabilities
- `route-b-landing-readiness`: Route B 真实落地的 fail-closed 就绪准备能力。定义「门控前可预先产出的受控分析产物」契约：字节绑定决策输入、GATE_A 计划草稿、目标机验证清单、一致性修复提案、Track P/I 解锁即执行步骤序列；并约定这些产物必须 fail-closed（不写真实字节、不翻门、不伪造 approval）。

### Modified Capabilities
<!-- 无既有能力的需求级变更 -->

## Impact

- **代码**：无运行时代码变更；仅新增受管暂存区分析文档。
- **API / 依赖**：无。
- **系统**：不影响真实树、不影响 `workspace/approvals/`、不影响 Hook 信任态、不影响 `MANIFEST` 清单。
- **受众**：执行侧（未来的真实 APPLY / 部署 / 发布操作者）与独立审计方。
- **风险边界**：所有产物均为「建议 / 提案 / 清单」，不替代阶段门批准，不解锁任何门；真实执行仅在 `workspace/approvals/` 出现真实回执且 Hook 经显式信任后发生。
