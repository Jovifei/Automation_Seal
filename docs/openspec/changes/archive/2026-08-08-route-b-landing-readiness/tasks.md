# Tasks — route-b-landing-readiness

> Fail-closed 落地就绪准备。所有任务均为受控/只读分析，不写真实字节、不翻门、不伪造 approval。

## 1. 证据链重新锚定（只读）
- [x] 1.1 复跑 `workspace/review-queue/route_b_preflight.py`，输出 `ROUTE_B_PREFLIGHT_2026-08-08.json`
- [x] 1.2 断言 matched=10/10、mismatched=[]、gate_all_false=true、audit_pass=true、零漂移

## 2. GATE_A 计划草稿
- [x] 2.1 运行 `scripts/generate_gate_a_plan.py`（若为受管脚本）或手写草稿，产出 GATE_A 计划 JSON 草稿
- [x] 2.2 Track P / Track I 状态诚实标 `BLOCKED`，头部注明「需用户本人运行 `Approve-Gate.ps1`」
- [x] 2.3 落盘 `workspace/review-queue/ROUTE_B_GATE_A_PLAN_DRAFT_V1.json`

## 3. 目标机验证清单
- [x] 3.1 枚举核查项：真实树零漂移复算、回滚演练有效性、Windows / Codex / Hook 信任态 / Docker-WSL / GPU / 闲鱼本地状态 / 备份恢复 / 许可证边界
- [x] 3.2 每项给出可执行命令或判定条件，标注 `NOT_VERIFIED` 或已验证证据
- [x] 3.3 落盘 `workspace/review-queue/ROUTE_B_TARGET_MACHINE_VERIFICATION_V1.md`

## 4. Modbus parser.py 一致性修复提案
- [x] 4.1 分析 ZIP 与当前源码 12/13 一致（`parser.py` 不一致）的根因
- [x] 4.2 给出最小修复 diff 建议，作为受控入口解门前置输入
- [x] 4.3 落盘 `workspace/review-queue/ROUTE_B_MODBUS_PARSER_FIX_PROPOSAL_V1.md`（真实字节不变）

## 5. Track P/I 解锁即执行步骤序列
- [x] 5.1 给出序：Track I 部署 → 真实 APPLY → Track P 发布，每步含回滚点
- [x] 5.2 首步判定 `workspace/approvals/GATE_A.P/I.approval.json` 存在，缺失即中止
- [x] 5.3 落盘 `workspace/review-queue/ROUTE_B_TRACK_PI_STEP_SEQUENCE_V1.md`

## 6. 验证与归档（受控载体关闭）
- [x] 6.1 verify 阶段重跑 pre-flight，确认 PASS
- [x] 6.2 archive 关闭 change，作为 fail-closed 计划+证据载体（不修改 10 目标真实字节）
- [x] 6.3 更新 `STATUS.md` 与项目记忆
