## Why

S1 Route B 资格决策 `ROUTE_B_DECISION_FROZEN_QUALIFICATION_READY_FOR_INDEPENDENT_REVIEW` 已完成**独立审核并 PASS**（`reports/audit/JOVI_S1_ROUTE_B_FINAL_INDEPENDENT_AUDIT_RESULT_V1.md`），证明 10 个资格候选目标的证据充分、当前且可重算。但决议仍处 **fail-closed 冻结态**：`real_apply_allowed=false`、`hook_trust_allowed=false`、`track_p_allowed=false`、`track_i_allowed=false`、`product_publish_allowed=false`，Hook 保持 `DO_NOT_TRUST`。

当前缺少一个**受控载体**把这些候选目标的精确 APPLY 计划与验证证据固化下来。需要一个 change，使后续真实 APPLY 可由用户**单次精确授权**触发，而本 change 自身不执行任何真实写入、不突破冻结门。

## What Changes

- 新建**受控 APPLY 计划文档**：精确到字节级别列出 10 个 Route B 资格候选目标（路径 + 当前 SHA-256 + 动作 `ACCEPT_CURRENT_BYTES_AS_QUALIFICATION_CANDIDATE_PENDING_INDEPENDENT_REVIEW` + 前置门条件）。
- 固化 **fail-closed 条件**：在用户显式授权前，不写真实目标字节、不写真实 Manifest、不置 Hook 为 TRUST、不启用 Track P / Track I、不发布产品。
- 提供**排练/校验 harness**：在字节级副本上重跑独立审核式检查，证明计划可重算、零漂移。
- 本 change 的产物仅为**计划与证据**，不修改 10 个目标文件的真实字节；build 阶段在 `plan-ready` 暂停，等待用户授权真实 APPLY。

## Capabilities

### New Capabilities

- `route-b-controlled-apply`: Route B 资格候选目标的受控、fail-closed APPLY 过程契约——精确字节 + 门条件 + 审计可重算 + 零漂移。

### Modified Capabilities

<!-- 无既有能力的需求变更；本 change 不修改任何产品能力的行为规范 -->

## Impact

- **产物位置**：`docs/openspec/changes/route-b-qualification-controlled-apply/`（计划与证据），不触碰 `E:\project\jovi-automation` 根下的 10 个目标真实字节。
- **引用证据**：`workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json`（10 目标 + 门标志）、`reports/audit/JOVI_S1_ROUTE_B_FINAL_INDEPENDENT_AUDIT_RESULT_V1.md`（独立审核 PASS）、`workspace/review-queue/route_b_qualification/` 下的候选清单与目标映射。
- **不影响的系统**：产品运行时代码、`.codex/hooks.json` 真实 Hook 语义、Track P / Track I 基础设施、发布流程。
