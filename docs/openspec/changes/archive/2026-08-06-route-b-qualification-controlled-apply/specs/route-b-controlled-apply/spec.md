## Purpose

定义 Route B 资格候选目标的受控、fail-closed APPLY 过程契约，使精确写入可由用户单次精确授权触发，且全程可审计、可重算、零漂移。

## ADDED Requirements

### Requirement: APPLY plan enumerates all 10 targets with current SHA

受控 APPLY 过程 SHALL 产出一份 APPLY 计划，列出全部 10 个 Route B 资格候选目标，每个目标包含路径、当前 SHA-256、以及动作 `ACCEPT_CURRENT_BYTES_AS_QUALIFICATION_CANDIDATE_PENDING_INDEPENDENT_REVIEW`。

#### Scenario: Plan lists every target with verified SHA

- **WHEN** 生成受控 APPLY 计划
- **THEN** 计划包含 `JOVI_S1_RESTART_DECISION_V1.json` 中全部 10 个 items，且每个目标的当前 SHA-256 与真实文件及冻结目标映射一致

#### Scenario: Missing target is rejected

- **WHEN** 任一目标缺失或 SHA 与真实文件不符
- **THEN** 计划生成失败并中止，不允许部分应用

### Requirement: Fail-closed gate retained

受控 APPLY 过程 SHALL NOT 执行真实目标写入、真实 Manifest 写入、Hook TRUST 写入、Track P / Track I 启用或产品发布，除非对应门标志被用户显式授权。

#### Scenario: No write without authorization

- **WHEN** 用户未显式授权（如 `real_apply_allowed=false`）
- **THEN** 过程仅产出计划与证据，真实树净修改保持 FALSE

#### Scenario: Authorized gate flips enable writes

- **WHEN** 用户显式授权对应门标志
- **THEN** 仅在被授权范围内执行精确写入，其余门仍保持 fail-closed

### Requirement: Zero-drift preserved

受控 APPLY 过程 SHALL NOT 修改计划声明输出之外的任何项目文件；真实树净修改 SHALL 保持 FALSE（零漂移）。

#### Scenario: Live tree unchanged by planning

- **WHEN** 仅执行计划与校验 harness（未授权真实 APPLY）
- **THEN** 前后全树 SHA 快照一致，added / modified / deleted 均为 0

### Requirement: Recomputable audit evidence

受控 APPLY 过程 SHALL 包含排练 / 校验 harness，在字节级副本上重跑独立审核式检查并复现 PASS 结论。

#### Scenario: Harness reproduces PASS on copy

- **WHEN** 在字节级副本上运行校验 harness
- **THEN** 13 个回归套件 PASS、`package_validator` DENY（fail-closed）、A/B 影子字节相同、回滚字节精确、真实树零漂移，复现独立审核 PASS

### Requirement: Decision traceability

每个被应用（或待应用）的目标 SHALL 引用其来源决策 `JOVI_S1_RESTART_DECISION_V1` 的对应 item 与独立审核 `JOVI_S1_ROUTE_B_FINAL_INDEPENDENT_AUDIT_RESULT_V1` 的 PASS 结论。

#### Scenario: Target links to decision and audit

- **WHEN** 查阅任一目标的 APPLY 条目
- **THEN** 可追溯到决策 item 的路径 / SHA 与独立审核 PASS 结论，形成完整证据链
