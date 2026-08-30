---
comet_change: route-b-landing-readiness
role: technical-design
canonical_spec: openspec
archived-with: 2026-08-08-route-b-landing-readiness
status: final
---

# Route B 落地就绪准备 — 技术设计（Design Doc）

## 概述

本 change 是 Route B 真实落地的 **fail-closed 就绪准备载体**，不写任何运行时代码、不翻转任何门、不创建/修改 `workspace/approvals/*.approval.json`、不改动 10 目标真实字节、不修改 `MANIFEST` 哈希。目标是把阶段门批准后门后执行所需的受控分析产物预先备齐，使执行延迟趋零且全程可审计。

## 上下文与锚点

- 决策 JSON：`workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json`（含 10 目标 `current_sha256` 与 `formal_expected_sha256`、统一 `requires_future_exact_apply_decision: true`）。
- 已归档受控载体：`docs/openspec/changes/archive/2026-08-06-route-b-qualification-controlled-apply/`（`APPLY_PLAN.md` / `VERIFICATION_EVIDENCE.json`）。
- 既有只读 pre-flight：`workspace/review-queue/route_b_preflight.py`（SHA-256 逻辑，输出 PASS）。

## 技术方法

### 产物 1 — GATE_A 计划草稿
- 优先运行 `scripts/generate_gate_a_plan.py`（若为受管脚本）；否则手写草稿并在头部标注「未经生成器校验」。
- Track P / Track I 状态诚实标 `BLOCKED`（反映独立审计决策 / Hook 信任 / 正式清单缺口未解除）。
- 输出 `workspace/review-queue/ROUTE_B_GATE_A_PLAN_DRAFT_V1.json`，头部注明「需用户本人运行 `scripts/human-only/Approve-Gate.ps1` 方可生成正式回执」。

### 产物 2 — 目标机验证清单
- 输出 `ROUTE_B_TARGET_MACHINE_VERIFICATION_V1.md`。
- 枚举 9 类核查：真实树零漂移复算、回滚演练有效性、Windows、Codex、Hook 信任态、Docker-WSL、GPU、闲鱼本地状态、备份恢复、许可证边界。
- 每项给可执行命令或判定条件，标注 `NOT_VERIFIED`（本地无法实跑）或已验证证据。

### 产物 3 — Modbus parser.py 一致性修复提案
- 输出 `ROUTE_B_MODBUS_PARSER_FIX_PROPOSAL_V1.md`。
- 分析 ZIP 与当前源码 12/13 一致（`parser.py` 不一致）的根因，给出最小修复 diff 建议。
- **真实字节不变**；作为受控入口（解 `HOOK_UNTRUSTED` + `FORMAL_MANIFEST_MISMATCH`）解门的前置输入，真实修改仅在 Hook 经显式信任且门开后执行。

### 产物 4 — Track P/I 解锁即执行步骤序列
- 输出 `ROUTE_B_TRACK_PI_STEP_SEQUENCE_V1.md`。
- 顺序：Track I 部署（Docker/PostgreSQL/n8n/changedetection/备份恢复）→ 真实 APPLY（10 目标）→ Track P 发布。每步含回滚点。
- 首步判定 `workspace/approvals/GATE_A.P.approval.json` 与 `GATE_A.I.approval.json` 存在，缺失即中止并提示用户运行 `Approve-Gate.ps1`。

### 证据重锚
- 复跑 `workspace/review-queue/route_b_preflight.py` → `ROUTE_B_PREFLIGHT_2026-08-08.json`，断言 matched=10/10、mismatched=[]、gate_all_false=true、audit_pass=true、零漂移、退出码 0。

## 关键权衡与风险

- **[风险] 误读为「已落地」** → 每份产物头部与 `proposal.md` 明示 fail-closed、未真实 APPLY；`STATUS.md` / 记忆同步标注。
- **[风险] `generate_gate_a_plan.py` 若非受管脚本则不可运行** → 手写草稿并标注「未经生成器校验」，不在本 change 内越权。
- **[风险] 目标机核查项本地无法实跑** → 逐项 `NOT_VERIFIED`，仅给命令/判定条件。
- **[权衡] 不真实修复 `parser.py`** → 门控未开前修复无合规意义且引入漂移，接受停留提案态。

## 测试策略

- 只读 pre-flight 复跑即本 change 的主要验证：断言 10/10 一致、零漂移、门全 false、独立审计 PASS、退出码 0。
- 各产物落盘后做存在性 + 非空校验。
- 不运行任何会触发真实写盘 / 部署 / 发布的命令。

## 边界

- 所有产物为「建议 / 提案 / 清单」，不替代阶段门批准，不解锁任何门。
- 真实执行仅在 `workspace/approvals/` 出现真实回执且 Hook 经显式信任后发生，由独立的 Track P/I 步骤序列承载。
- 本 change 在产物齐备后走 verify→archive 关闭为受控载体（不修改 10 目标真实字节）。
