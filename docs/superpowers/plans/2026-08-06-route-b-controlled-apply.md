---
change: route-b-qualification-controlled-apply
design-doc: docs/superpowers/specs/2026-08-06-route-b-controlled-apply-design.md
base-ref: N/A (git rev-parse HEAD unavailable; tree snapshot anchors verification instead)
archived-with: route-b-qualification-controlled-apply
status: final
---

# 实施计划：Route B 受控 APPLY（精确步骤）

> 本计划是受控载体。**真实写入须用户在 plan-ready 暂停点显式授权后才执行**。当前所有门标志为 false（`real_apply` / `manifest_real_write` / `hook_trust` / `track_p` / `track_i` / `publish` 全 false），故默认不执行任何真实写入，真实树保持零漂移。

## 阶段 0：准备（已在 open / design 完成）

- 变更 `route-b-qualification-controlled-apply` 已创建：`proposal.md` / `design.md` / `specs/route-b-controlled-apply/spec.md` / `tasks.md` / Design Doc 就绪。
- 独立审核 PASS 证据已绑定（`reports/audit/JOVI_S1_ROUTE_B_FINAL_INDEPENDENT_AUDIT_RESULT_V1.md`，包 SHA 见 sidecar）。
- 输入决策：`workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json`（10 目标，门标志全 false）。

## 阶段 1：生成 APPLY_PLAN.md（落入 change 目录，真实树零漂移）

- **1.1** 运行只读快照生成器，读取决策 JSON 的 10 个 items（路径 + `current_sha256` + 动作）。
- **1.2** 对每个 item 重算目标文件当前 SHA-256，与 `current_sha256` 比对；**任一失配即中止**。
- **1.3** 生成 `APPLY_PLAN.md`，逐项列出：路径 / 决策 SHA / 实时 SHA / 动作 `ACCEPT_CURRENT_BYTES_AS_QUALIFICATION_CANDIDATE_PENDING_INDEPENDENT_REVIEW` / 门条件（全 false）。
- **1.4** 绑定证据链：每目标引用决策 item 与独立审核 PASS 结论。

## 阶段 2：校验 harness（字节副本重跑，真实树零漂移）

- **2.1** `robocopy /MIR` 生成字节级副本到隔离目录（排除 .git / pycache）。
- **2.2** 副本上重跑 13 套回归套件（security_semantics_20、s2a2_24、s1_integrity_34_a/b、s2a1_42、batch_b_21、hook_subset_9、canonical_hook_28、modbus_12、static_smoke、package_validator、parser_json_utf8、guard_manifest_negative）。
- **2.3** 断言 `package_validator` = DENY（fail-closed）、A/B 影子字节相同、回滚字节精确、前后全树 SHA 快照一致（零漂移）。
- **2.4** 产出 `VERIFICATION_EVIDENCE.json` 到 change 目录。

## 阶段 3：plan-ready 暂停（决策点 —— 本 change 默认停于此）

- **3.1** 向用户呈现 `APPLY_PLAN.md` 与门条件，等待显式授权。
- **3.2** 未授权 → 保持真实树零漂移，不进入真实写入；继续 verify → archive 关闭 change。

## 阶段 4（仅当用户授权后执行；当前门标志 false，默认不执行）

- **4.1** 在隔离分支 / 工作树，对 10 个目标做字节级备份。
- **4.2** 仅按被授权的门标志逐一写入（默认无）。
- **4.3** 重跑 harness 确认零漂移。
- **4.4** 更新对应 GATE / Track 状态与 Manifest（需用户显式授权）。

## 验收标准

- 计划含全部 10 目标且 SHA 与真实文件 / 冻结目标映射一致；
- 门条件明示全 false；
- 副本校验复现独立审核 PASS（13 套回归 PASS、`package_validator` DENY、零漂移）；
- 真实树净修改 = FALSE（零漂移）。
