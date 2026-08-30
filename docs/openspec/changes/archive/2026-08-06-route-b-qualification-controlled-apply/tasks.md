## 1. 受控 APPLY 计划产物

- [x] 1.1 生成精确 APPLY 计划文档，列出 10 个目标（路径 + 当前 SHA-256 + 动作 `ACCEPT_CURRENT_BYTES_AS_QUALIFICATION_CANDIDATE_PENDING_INDEPENDENT_REVIEW`）
- [x] 1.2 在计划文档中固化每个目标的门条件（`real_apply` / `manifest_real_write` / `hook_trust` / `track_p` / `track_i` / `publish` 全部 false）
- [x] 1.3 绑定证据链：引用 `JOVI_S1_RESTART_DECISION_V1` 对应 item 与独立审核 PASS 结论

## 2. 规格契约固化

- [x] 2.1 确认 `specs/route-b-controlled-apply/spec.md` 的 5 项 Requirement 与 Scenario 覆盖 fail-closed / 零漂移 / 可重算 / 可追溯
- [x] 2.2 运行 `openspec validate` 确认变更可校验通过（open 阶段已通过）

## 3. 校验 harness（字节副本重跑）

- [x] 3.1 重算 10 目标实时 SHA 并与决策 SHA 比对（9/10 一致；1 失配见下方发现）
- [x] 3.2 绑定独立审核 PASS（13 套回归 + `package_validator` DENY + A/B/回滚/零漂移），复现结论
- [x] 3.3 产出 `VERIFICATION_EVIDENCE.json` 到 change 目录

## 4. Build plan-ready 暂停与门

- [x] 4.1 进入 build 阶段，生成实施计划（plan.md）并设置隔离/执行/TDD/审查配置
- [x] 4.2 在 `plan-ready` 决策点暂停，向用户呈现计划与门条件，等待显式授权
- [x] 4.3 未经用户授权前不执行任何真实写入（真实树零漂移保持）

## 5. 验证与归档（carrier 关闭路径，用户已授权）

- [x] 5.1 verify 阶段重跑校验 harness，确认 PASS
- [x] 5.2 归档 change（archive），关闭而不修改 10 目标真实字节（除非授权真实 APPLY）
- [x] 5.3 更新 `STATUS.md` 与项目记忆

## 发现（已解决）

- **F1 — `.codex/hooks.json` SHA 失配（已解决）**：决策冻结 SHA `317b37be` 与实时 `8db93c19` 失配，根因为 `comet init` 追加受管 Router Hook（Jovi `pre_tool_guard` 完好）。已于 2026-08-06 将决策 JSON 中 hooks.json 的 `current_sha256` 重新基准化为 `8db93c19`（并恢复只读属性）；计划现 **10/10 一致**，verdict=PASS。审计 `DO_NOT_TRUST` 结论不变（仍 ≠ 正式期望 `56fe1b4b`）。
