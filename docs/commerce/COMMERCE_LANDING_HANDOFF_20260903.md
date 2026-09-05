# Commerce Landing 交接 — 2026-09-03（历史交接，已被后续执行推进）

**状态：COMPLETED / HISTORICAL HANDOFF**  
**不要把本文件的 R2-R3/C2/C3“下一步”当当前指令。**

本文件记录 2026-09-03 时从 R2-R3 向 C2/C3/C4 过渡的计划。此后项目已经实际完成：

- `R2R3_INDEPENDENT_AUDIT_PASS`
- `C2_INDEPENDENT_AUDIT_PASS`
- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`
- Jovi Runtime C3 Promotion Decision
- `C3_RUNTIME_PROMOTION_AUDIT_PASS`

当前真实停点已更新为：

`C4_HUMAN_PILOT_DECISION`

请改读：

- `docs/CURRENT_PROJECT_GUIDE.md`
- `docs/commerce/README.md`
- `docs/commerce/C3_LOCAL_AUDIT_CLOSURE_MIRROR_20260905.md`
- `docs/commerce/C4_HUMAN_PILOT_PLAN_V1.md`
- `docs/commerce/C4_PILOT_PRIVACY_MINIMIZATION_V1.md`
- `docs/commerce/C4_HUMAN_PILOT_DECISION_CANDIDATE_V1.md`

当前 Candidate 仍 `issued_from_human=false`，真实 Pilot 尚未授权。

## 本历史交接仍然有效的设计结论

1. Medusa 是 Commerce Core，不再恢复 Python legacy Commerce；
2. `makepay-apps/medusa-plugin-digital-downloads` 只选择性吸收 immutable release / private asset / DownloadGrant / idempotent delivery 模式；
3. Gitleaks / Syft 保留；
4. Trivy / Storefront / S3 / n8n production 非当前阻断；
5. 实现 Agent 到独立审核门必须停止；
6. 真实平台动作始终 Human-controlled。

## 已失效的当时状态

以下当时事实已经过时：
- Runtime `main=8290392...`；
- R2-R3 仍待本地验证；
- C2 尚未开始；
- C3 尚未开始；
- Runtime 一定 `remote=none` 的假设。

这些现在必须现场重查，不得从本历史文件继承。

## 当前商业目标

项目现在不再需要证明“Commerce Runtime 能否工作”。当前需要证明：

**已经通过技术审计的真实 Modbus SKU，能否在所有平台动作由 Jovi 手工控制、买家数据最小化的情况下完成 5–10 单或固定时间窗的真实商业 Pilot。**
