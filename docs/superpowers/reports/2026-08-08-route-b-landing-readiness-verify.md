# Route B 落地就绪准备 — 验证报告（Verify Report）— 2026-08-08

> 受控载体验证。本 change 为 fail-closed 准备载体，不写真实字节、不翻门、不伪造 approval。
> 验证目标：确认 4 份就绪产物齐备且诚实、证据链已重锚、所有门仍 false。

## 验证项（7 项全 PASS）

### V1 — OpenSpec 结构一致性
- `proposal.md` / `design.md` / `specs/route-b-landing-readiness/spec.md` / `tasks.md` 语言均为 `zh-CN`，与配置一致。
- `applyRequires: [tasks]` 满足；`tasks.md` 全勾（含 verify/archive 关闭路径）。
- **结果：PASS**

### V2 — 证据链重新锚定（只读 pre-flight）
- 复跑 `workspace/review-queue/route_b_preflight.py` → `ROUTE_B_PREFLIGHT_2026-08-08.json`。
- 断言：`matched=10/10`、`mismatched=[]`、`gate_all_false=true`、`audit_pass=true`、`verdict=PASS`、退出码 0。
- 自归档（`2026-08-06`）以来真实树**零漂移**。
- **结果：PASS**

### V3 — 4 份就绪产物齐备且非空
| 产物 | 路径 | 状态 |
|---|---|---|
| GATE_A 计划草稿 | `workspace/review-queue/ROUTE_B_GATE_A_PLAN_DRAFT_V1.json` | ✅ 非空 |
| 目标机验证清单 | `workspace/review-queue/ROUTE_B_TARGET_MACHINE_VERIFICATION_V1.md` | ✅ 非空 |
| Modbus parser.py 修复提案 | `workspace/review-queue/ROUTE_B_MODBUS_PARSER_FIX_PROPOSAL_V1.md` | ✅ 非空 |
| Track P/I 步骤序列 | `workspace/review-queue/ROUTE_B_TRACK_PI_STEP_SEQUENCE_V1.md` | ✅ 非空 |
- **结果：PASS**

### V4 — GATE_A 草稿诚实标 BLOCKED
- `ROUTE_B_GATE_A_PLAN_DRAFT_V1.json` 中 Track P 与 Track I `status` 均为 `BLOCKED`，blockers 列出真实阻塞（approval 缺失、Hook 未信任、形式清单缺口、包静态门）。
- 头部注明：草稿非 `generate_gate_a_plan.py` 产出（其 3/4 输入缺失，运行会掩盖 blocker），正式回执只能由用户运行 `Approve-Gate.ps1` 生成。
- **结果：PASS**（无伪造 `AWAITING_HUMAN_APPROVAL`）

### V5 — Modbus parser.py 分析准确
- 实测 diff：当前源（175 行）与 ZIP（167 行）差异仅 4 处 warning 字符串的换行风格（相邻字符串字面量连接），运行时字符串内容逐字符相同，**行为零差异**。
- 提案定性「纯 cosmetic 重格式化，非功能缺陷」成立。
- **结果：PASS**

### V6 — Track P/I 步骤序列门闸正确
- `ROUTE_B_TRACK_PI_STEP_SEQUENCE_V1.md` 首步判定 `workspace/approvals/GATE_A.P/I.approval.json` 存在，缺失即中止。
- 严禁项（闲鱼真实动作、未 TRUST 前 APPLY、无回执执行、推送远程）明确列出。
- **结果：PASS**

### V7 — 安全边界未被破坏
- 10 目标真实字节未变（pre-flight `current_sha256` 与决策 JSON 逐字节一致）。
- 所有门（`real_apply` / `formal_manifest_real_write` / `hook_trust` / `track_p` / `track_i` / `publish`）仍为 false。
- `workspace/approvals/` 无新增回执文件。
- `MANIFEST` 清单哈希未改。
- `.codex/hooks.json` 信任态仍为 `DO_NOT_TRUST`。
- **结果：PASS**

## 结论

- **verdict：PASS**（7/7）
- 本 change 作为 fail-closed 落地就绪载体已就绪，可进入 archive 关闭。
- 真实落地仍被阶段门挡着：需用户本人运行 `Approve-Gate.ps1` 生成 `GATE_A.P/I.approval.json` + 显式 Hook 信任 + 独立审计决策。
