## Context

- 当前 10 个目标文件的字节为资格候选（`accepted_for_shadow_qualification=true`，`accepted_as_historical_original=false`）；本机无可验证的正式原始期望字节（S1.2.1 FAIL_CLOSED，有界检索 0 命中），历史来源 `UNKNOWN_UNPROVEN`。
- 独立审核已 PASS，证明：决策与目标映射 SHA 一致、A/B 影子字节相同、回滚字节精确、13 个回归套件全 PASS、`package_validator` DENY（fail-closed）、真实树零漂移（1053 文件 0 增 / 0 改 / 0 删）、Hook 为 `CANDIDATE_SEMANTICS_VERIFIED_BUT_UNTRUSTED`。
- 所有门标志为 false：真实 APPLY、Manifest 写入、Hook TRUST、Track P / I、发布均未被授权（见 `JOVI_S1_RESTART_DECISION_V1.json`）。

## Goals / Non-Goals

**Goals:**

- 产出可审计、可重算的精确 APPLY 计划（10 目标 + 当前 SHA + 动作 + 门条件）。
- 保留 fail-closed：未授权前不触碰真实字节 / Manifest / Hook / Track P-I / 发布。
- 在字节副本上重跑校验 harness，证明计划可重算、零漂移。

**Non-Goals:**

- 不执行真实写入；不将 Hook 置为 TRUST；不启用 Track P / Track I；不发布产品；不声称 S1 完成或历史原版已证明。

## Decisions

- **D1 以 comet-classic change 作为受控载体**：走 open→design→build→verify→archive 全流程；build 阶段 `plan-ready` 暂停，真实 APPLY 须由用户显式授权（翻转对应门标志）后才可执行。
  - 备选：直接写脚本落地 —— 否决，会绕过冻结门与审计纪律。
- **D2 计划产物置于 change 目录，不触碰 10 目标真实字节**：APPLY 计划文档与校验证据只写入 `docs/openspec/changes/...`，确保真实树零漂移。
  - 备选：就地修改目标文件 —— 否决，违反 fail-closed 与独立审核的零漂移约束。
- **D3 校验在字节副本上重跑**：复用独立审核的 robocopy 副本方式，避免污染真实树；harness 复用既有 13 套回归套件与 SHA 绑定逻辑。

## Risks / Trade-offs

- [Risk] 用户未授权前无法落地真实 APPLY → Mitigation：本 change 交付物即为精确计划 + 证据，未来用户单次精确授权（翻转门标志）即可执行，无需重做分析。
- [Risk] Hook 仍 `DO_NOT_TRUST`，仅允许只读审阅与影子负向测试 → Mitigation：本 change 不写 Hook；TRUST 需未来基于完整内容 / Hash / 命令 / matcher / timeout / statusMessage / 负向测试作新的精确决定。
- [Risk] 计划与真实目标未来出现字节漂移 → Mitigation：计划文档绑定各目标当前 SHA-256，执行前须重算比对，失配则中止并重新评估。

## Migration Plan

- 部署步骤：本 change archive 后，若用户授权，按 tasks 中的精确 APPLY 步骤在隔离分支 / 工作树上执行；执行后跑校验 harness 确认零漂移。
- 回滚策略：所有目标写入均伴随字节级备份；任一目标失配可字节精确回滚（独立审核已证明回滚机制有效）。

## Open Questions

<!-- 无需在本 change 内解决的未知项；Hook TRUST 与 Track P-I 的未来授权属独立决定，不改变本计划结构 -->
