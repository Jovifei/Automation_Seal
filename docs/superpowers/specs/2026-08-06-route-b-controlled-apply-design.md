---
comet_change: route-b-qualification-controlled-apply
role: technical-design
canonical_spec: openspec
archived-with: route-b-qualification-controlled-apply
status: final
---

# Route B 受控 APPLY 计划 —— 深度技术设计

## 1. 概述与目标

本 Design Doc 是 open 阶段 `design.md` 的深化（非重写）。目标是把一个**受控、fail-closed 的 Route B 资格候选目标 APPLY 过程**落到可审计、可重算、零漂移的实现设计上。本 change 自身**不执行真实写入**；真实写入由未来用户显式授权触发。

## 2. 上下文与约束

- 上游真相：OpenSpec `proposal.md` / `design.md` / `specs/route-b-controlled-apply/spec.md` / `tasks.md`。
- 输入证据：`workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json`（10 目标 + 门标志全 false）、`reports/audit/JOVI_S1_ROUTE_B_FINAL_INDEPENDENT_AUDIT_RESULT_V1.md`（独立审核 PASS）。
- 硬约束：真实树零漂移（added / modified / deleted = 0）；fail-closed（门标志 false 时无任何真实写入）；Hook 保持 `DO_NOT_TRUST`。

## 3. 架构与数据流

```
JOVI_S1_RESTART_DECISION_V1.json (10 items)
        │  (读取，只读)
        ▼
[快照生成器] ──重算当前 SHA-256──比对──失配即中止──▶ APPLY_PLAN.md (change 目录)
        │                                                  │
        │                                          (逐项: 路径/决策SHA/实时SHA/动作/门条件)
        ▼
[校验 harness] ──robocopy /MIR 字节副本──▶ 隔离副本
        │                                        │
        │                             重跑 13 套回归 + package_validator DENY + A/B/回滚/零漂移
        ▼                                        ▼
VERIFICATION_EVIDENCE.json ◀──── PASS 复现 ◀──── 副本 (不写真实树)
```

数据流单向：只读读取 → 计划快照（change 目录） + 副本校验证据（change 目录）。真实树始终只读。

## 4. 组件设计

### 4.1 APPLY_PLAN.md 快照生成器

- 输入：`JOVI_S1_RESTART_DECISION_V1.json`。
- 处理：对每个 item：
  1. 读取 `path` 真实文件，计算 SHA-256；
  2. 与 item.`current_sha256` 比对；不一致 → 立即中止并报告（对应 Requirement "Missing target is rejected"）；
  3. 记录 `path`、`current_sha256`（决策）、实时 SHA、动作 `ACCEPT_CURRENT_BYTES_AS_QUALIFICATION_CANDIDATE_PENDING_INDEPENDENT_REVIEW`、门条件（逐项 false）。
- 输出：Markdown 表格 + 证据链注释（引用决策 item 与独立审核 PASS）。
- 落点：`docs/openspec/changes/route-b-qualification-controlled-apply/APPLY_PLAN.md`。

### 4.2 校验 harness（字节副本重跑）

- 步骤：
  1. `robocopy /MIR <repo> <copy>` 生成字节级副本（排除 .git / pycache）；
  2. 在副本上重跑 13 套回归套件（security_semantics_20、s2a2_24、s1_integrity_34_a/b、s2a1_42、batch_b_21、hook_subset_9、canonical_hook_28、modbus_12、static_smoke、package_validator、parser_json_utf8、guard_manifest_negative）；
  3. 断言 `package_validator` = DENY（fail-closed）；A/B 影子字节相同；回滚字节精确；前后全树 SHA 快照一致（零漂移）。
- 输出：`VERIFICATION_EVIDENCE.json`（复用独立审核 schemata）。
- 真实树零写入。

### 4.3 Build plan-ready 暂停机制

- build 阶段产出 `plan.md`（精确 APPLY 步骤）：隔离分支 / 工作树 → 字节备份 → 按门标志逐一写入 → 重跑 harness 确认。
- 设置 `build_pause: plan-ready`，在决策点暂停，呈现计划与门条件，等待用户显式授权（翻转对应门标志）后才执行真实写入。
- 未授权：保持零漂移，不进入真实写入。

## 5. 测试策略

- 单元级：13 套回归套件在副本上全 PASS（与独立审核一致）。
- 契约级：spec 5 项 Requirement 各 Scenario 映射为可验证检查：
  - 枚举 10 目标 + SHA → 计划含全部 10 item 且 SHA 一致；
  - fail-closed 门 → 门 false 时真实树净修改 FALSE；
  - 零漂移 → 前后全树 SHA 一致；
  - 可重算证据 → harness 复现 PASS；
  - 决策可追溯 → 每目标可追溯到决策 item + 审核 PASS。
- 负向：`package_validator` DENY 维持；任一 SHA 失配即中止。

## 6. 边界与异常

- 目标文件缺失或 SHA 失配：中止，不允许部分应用。
- 门标志状态变化：仅在用户显式授权后于隔离环境执行对应写入。
- 副本校验失败：阻止进入真实写入，回退到 design 重新评估。

## 7. 风险登记

| 风险 | 缓解 |
|------|------|
| 真实 APPLY 未授权前无法落地 | 交付物即精确计划 + 证据，未来单次授权即可执行 |
| Hook 仍 `DO_NOT_TRUST` | 本 change 不写 Hook；TRUST 需未来新精确决定 |
| 计划与真实目标漂移 | 计划绑定 SHA，执行前重算比对，失配中止 |

## 8. 回滚

- 所有真实写入均伴随字节级备份；任一目标失配可字节精确回滚（独立审核已证明回滚机制有效）。
- 本 change 自身不写入真实字节，归档即关闭，无需回滚真实树。
