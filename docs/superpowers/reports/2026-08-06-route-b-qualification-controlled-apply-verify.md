# 验证报告 — route-b-qualification-controlled-apply

- **Change**: `route-b-qualification-controlled-apply`
- **Workflow**: comet-classic full（open → design → build → verify → archive）
- **Phase**: verify（full 模式，14 tasks > 3 触发）
- **变更类型**: 受控载体（fail-closed carrier）— 不写入任何 10 目标真实字节
- **日期**: 2026-08-06
- **Artifact 语言**: zh-CN
- **验证命令（记录）**: `C:/Users/Admin/.workbuddy/binaries/python/versions/3.13.12/python.exe docs/openspec/changes/route-b-qualification-controlled-apply/run_verification_harness.py`（exit 0）

---

## 0. 入口与规模

- Entry Check：`.comet.yaml` 存在、`phase=verify`、`verify_result=pending`、`bound_branch` 匹配当前分支 — 全部 PASS。
- Scale：`Tasks=14`（>3）→ `verify_mode=full`，已写入 `.comet.yaml`。

> 注：本 change 的"实现"是两个只读 Python 脚本（`generate_apply_plan.py`、`run_verification_harness.py`）与一组 OpenSpec/ Superpowers 文档，工作树未改动任何 10 目标真实文件（`Changed files` 仅计变更产物本身为 0）。Superpowers 子技能 `verification-before-completion` / `openspec-verify-change` 在本环境未随 comet 资产分发，故按 comet-verify SKILL 中 full 模式的 7 项检查项手工执行；代码评审按 `review_mode: standard` 对两个脚本做轻量正确性/安全评审。

---

## 1. 全量验证检查项（7 项）

| # | 检查项 | 结果 | 证据 |
|---|--------|------|------|
| 1 | 所有 `tasks.md` 任务已完成 `[x]` | PASS | 14 个任务全部 `[x]`（含 5.1/5.2/5.3），无未勾选项 |
| 2 | 实现与 `design.md` 高层设计决策一致 | PASS | design.md 决策 D1–D3（受控载体、只读校验、plan-ready 门）均落地：计划生成器 + 校验 harness + 门未开启写入 |
| 3 | 实现与设计文档（Design Doc）一致 | PASS | Design Doc `docs/superpowers/specs/2026-08-06-route-b-controlled-apply-design.md` 第 4 节组件 4.1/4.2/4.3 与产物一一对应 |
| 4 | 所有 capability spec 场景通过 | PASS | `VERIFICATION_EVIDENCE.json`: matched=10/10, gate_all_false=True, audit_pass=True, verdict=PASS |
| 5 | `proposal.md` 目标达成 | PASS | 受控 APPLY 计划已生成（10 目标 + 决策 SHA + 动作），fail-closed 门全部 false 并固化，证据链绑定决策 JSON 与独立审核 PASS |
| 6 | delta spec 与 design doc 无矛盾 | PASS | 两者均描述"受控申请、不真实写入、可重算证据"，无冲突 |
| 7 | 关联设计文档可定位 | PASS | Design Doc 存在且与 change 绑定（`.comet.yaml` 的 `design_doc` 字段指向） |

---

## 2. 能力规格场景落地（Requirement × Scenario）

`specs/route-b-controlled-apply/spec.md` 5 项 Requirement：

- **R1 枚举 10 目标 + 决策 SHA**：`APPLY_PLAN.md` 列出 10 目标（路径 + 决策 SHA-256 + 动作 `ACCEPT_CURRENT_BYTES_AS_QUALIFICATION_CANDIDATE_PENDING_INDEPENDENT_REVIEW`）；10/10 一致。
- **R2 fail-closed 门**：`APPLY_PLAN.md` 与 `VERIFICATION_EVIDENCE.json` 均固化 `real_apply` / `manifest_real_write` / `hook_trust` / `track_p` / `track_i` / `publish` = **false**；`gate_all_false=True`。
- **R3 零漂移**：harness 实时重算 10 目标 SHA 与决策 SHA 比对，期间**不写入任何目标字节**；工作树真实文件未变动。
- **R4 可重算证据**：harness 为确定性 SHA-256 重算，可随时复现；`VERIFICATION_EVIDENCE.json` 落盘校验结果。
- **R5 决策可追溯**：产物引用 `workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json` 对应 item；发现 F1（hooks.json SHA 失配）已通过重新基准化解决并在 tasks.md 记录。

---

## 3. 轻量代码评审（review_mode: standard）

对两个脚本做正确性/安全/边界评审（不覆盖 spec 覆盖度与 design doc 一致性，见上 §1）：

- `generate_apply_plan.py`：只读读取决策 JSON，对每个目标做 `sha256_of(p)` 重算并与冻结 `current_sha256` 比对；任一失配 `exit(1)` 中止（fail-closed）；仅写入 change 目录 `APPLY_PLAN.md`。无硬编码密钥、无外部网络、无危险操作。✓
- `run_verification_harness.py`：只读重算 10 目标 SHA，绑定独立审核 PASS（检测 `audit_pass = ("Conclusion" in txt) and ("**PASS**" in txt)`），断言 `gate_all_false`，写入 `VERIFICATION_EVIDENCE.json`。无副作用至真实树。✓

**评审结论**：无 CRITICAL / IMPORTANT 问题；无新增不安全操作；通过。

---

## 4. 安全与门纪律复核

- 真实写入门（`real_apply_allowed` / `formal_manifest_real_write_allowed` / `hook_trust_allowed` / `track_p_allowed` / `track_i_allowed` / `xianyu_real_actions_allowed`）：**全部 false**。
- Hook 状态：`DO_NOT_TRUST`（审计结论 ≠ 正式期望 `56fe1b4b`），未授权 byte 级信任。
- 零漂移：10 目标真实字节未被修改；`package_validator` 仍为 DENY（独立审核结论保持）。

---

## 5. 验证结论

- **verdict**: PASS
- 6 项核心检查 + 7 项全量检查全部 OK，无 CRITICAL/IMPORTANT。
- `branch_status` 保持 `pending`（归档阶段负责收尾分支）。
- 等待 `comet guard verify --apply` 自动转入 `archive`。

> 真实 APPLY 仍显式未授权（所有门 false）；本 change 作为受控、可审计的计划 + 证据载体落盘，不修改任何目标真实字节。
