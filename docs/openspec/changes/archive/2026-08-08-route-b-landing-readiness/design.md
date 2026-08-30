## Context

Route B 的 10 个资格候选目标已在 `route-b-qualification-controlled-apply`（已归档）中以 fail-closed 载体落盘：含 `APPLY_PLAN.md`（10 目标 SHA 绑定）、`VERIFICATION_EVIDENCE.json`（verdict=PASS、gate_all_false=true、audit_pass=true）、只读 pre-flight 脚本。真实落地却被数道显式门控挡着（独立审计决策、`DO_NOT_TRUST` Hook 信任、`GATE_A.P/I.approval.json` 缺失、正式清单缺口 `OUTER_ARCHIVE_HASH_MISMATCH`）。本设计说明如何在门控解除**之前**，把门后执行所需的分析产物以受控方式预先备齐。

关键约束（来自 `AGENTS.md` / `MANIFEST_POLICY.md` / `CODEX_START_PROMPT.txt`）：
- `workspace/approvals/*.approval.json` 只能由用户本人运行 `scripts/human-only/Approve-Gate.ps1` 生成；智能体不得创建或修改，也不得运行 `scripts/human-only/`。
- 包静态测试 `gate_track_p_match` / `gate_track_i_not_inherited` 在无匹配 approval 回执时 DENY 真实 APPLY。
- 真实树不得漂移；`MANIFEST` 清单按路径冻结。

## Goals / Non-Goals

**Goals:**
- 预先产出 4 份 fail-closed 就绪产物，使阶段门批准后执行延迟趋零。
- 复跑只读 pre-flight，重新锚定证据链（10/10 一致、零漂移、门全 false）。
- 诚实标注所有 blocker，不在草稿中掩盖 `BLOCKED` 状态。

**Non-Goals:**
- 不真实 APPLY、不部署、不发布、不翻转 Hook 信任、不创建/修改 approval 回执、不修改 `MANIFEST` 哈希、不改动 10 目标真实字节。
- 不替代独立人工审计或用户的显式决策。

## Decisions

**D1 — 产物落盘于 `workspace/review-queue/`，不污染已归档载体。**
归档载体是「计划+证据」的已冻结事实源；新准备产物是「门后执行输入」，二者职责不同，分离避免破坏归档完整性。复用归档载体的 `APPLY_PLAN.md` / `VERIFICATION_EVIDENCE.json` 作为锚点。

**D2 — 复用既有只读 pre-flight 脚本，输出写到新 JSON。**
`route_b_preflight.py` 已在 `review-queue/` 且 PASS；本次变更复用其 SHA-256 逻辑复算，输出 `ROUTE_B_PREFLIGHT_2026-08-08.json`，证明自上次归档以来真实树仍零漂移。

**D3 — GATE_A 计划草稿由 `scripts/generate_gate_a_plan.py`（受管生成器）产出，track 标 BLOCKED。**
该生成器若属受管脚本则可运行；草稿必须诚实反映 blocker，因为 `Approve-Gate.ps1` 在 track `BLOCKED` 时会 `throw` 拒绝——伪造 `non-blocked` 只会让用户在运行脚本时失败，毫无益处。

**D4 — Modbus `parser.py` 一致性修复停留在提案态。**
ZIP 与当前源码 12/13 一致（`parser.py` 不一致）受 `HOOK_UNTRUSTED` + `FORMAL_MANIFEST_MISMATCH` 双重挡。真实修改需 Hook 经显式信任且门开后才执行，故本变更只产提案。

**D5 — Track P/I 步骤序列首步判定 approval 回执存在性。**
序列以「检查 `workspace/approvals/GATE_A.P/I.approval.json` 存在」为门闸，缺失即中止，避免任何提前执行。

## Risks / Trade-offs

- **[风险] 用户误把本载体当「已落地」** → 缓解：每份产物头部与 `proposal.md` 均明示 fail-closed 与「未真实 APPLY」；状态文件 `STATUS.md` / 记忆同步标注。
- **[风险] `generate_gate_a_plan.py` 若非受管脚本则不可运行** → 缓解：若运行被项目规则禁止，则手写草稿并注明「未经生成器校验」，不在本变更内强行越权。
- **[风险] 目标机验证清单项无法在本地实跑** → 缓解：逐项标 `NOT_VERIFIED`，仅给出可执行命令/判定条件，供目标机执行。
- **[权衡] 不真实修复 `parser.py`** → 接受：门控未开前修复无合规意义，且会引入真实树漂移。

## Migration Plan

本变更为纯新增受管暂存区分析文档，无迁移/回滚需求。若将来真实落地，本载体产物作为执行输入被引用；本 change 本身在产物齐备后走 verify→archive 关闭为受控载体（不修改任何目标字节）。

## Open Questions

- 用户是否在决策中明确采用字节绑定方案 A（绑定到 `current_sha256`）或提供方案 C 的权威字节源？
- `generate_gate_a_plan.py` 在当前项目规则下是否可运行（受管脚本判定）？
