# 文档状态与历史资料使用规则

**状态日期：2026-09-05**  
**目的：防止新 Agent 把历史计划、旧 Gate、旧技术选型或已完成阶段误当成当前指令。**

## 1. 当前/LIVING 文档

新 Agent 应优先依次阅读：

1. `docs/CURRENT_PROJECT_GUIDE.md`
2. `README_FIRST.md`
3. `PROJECT_STATE.json`
4. `NEXT_STEP_MAP.md`
5. `STATUS.md`
6. `docs/commerce/README.md`
7. `docs/commerce/C4_HUMAN_PILOT_PLAN_V1.md`
8. `docs/commerce/C4_PILOT_PRIVACY_MINIMIZATION_V1.md`
9. `docs/commerce/C4_HUMAN_PILOT_DECISION_CANDIDATE_V1.md`（**candidate，不是授权**）

当前执行停点：`C4_HUMAN_PILOT_DECISION`。

## 2. COMPLETED STAGE REFERENCE

以下资料记录已经完成的阶段，可以用于理解设计、测试与审计，但**不得据此重新执行旧阶段**：

- `docs/commerce/MEDUSA_ADOPTION_FRAMEWORK.md`
- `docs/commerce/MEDUSA_R2_REMEDIATION.md`
- `docs/commerce/MEDUSA_R2R2_INDEPENDENT_AUDIT_*`
- `docs/commerce/MEDUSA_R2R3_SESSION_COOKIE_ADOPTION_PLAN.md`
- `docs/commerce/JOVI_MEDUSA_R6_CONTROLLED_ADOPTION_DECISION_V1.md`
- `docs/commerce/COMMERCE_C2_SYNTHETIC_E2E_DIGITAL_DELIVERY_PLAN.md`
- `docs/commerce/C2_CLOUD_REFERENCE_*`
- `docs/commerce/C2_LOCAL_AUDIT_CLOSURE_MIRROR_20260905.md`
- `docs/commerce/C3_MODBUS_REAL_SKU_STAGING_PLAN_V1.md`
- `docs/commerce/C3_*READINESS*`
- `docs/commerce/C3_WINDOWS_RELEASE_CHECKLIST_20260905.md`
- `docs/commerce/JOVI_RUNTIME_C3_PROMOTION_DECISION_V1.md`
- `reference/commerce/c2/**`
- `reference/commerce/c3/**`

这些资料的当前意义是“已完成能力的证据与设计来源”，不是当前 TODO。

## 3. HISTORICAL / DO NOT USE AS CURRENT INSTRUCTIONS

### 早期 Track P / Track I / X0-X4 路线

以下概念曾用于早期 Governance / Product Alpha 阶段，但不再是当前 Commerce 主线：

- `Phase 0/A/X0`
- `GATE_A.P / GATE_A.I` 作为当前下一步
- `Track P / Track I` 作为当前执行轨道
- `X1/X2/X3/X4` 作为当前 Pilot 路线
- `READY_FOR_CODEX_PHASE_0_A_X0`
- 旧 Python SQLite Commerce C0-C6 路线

这些历史概念在旧报告、Prompt、OpenSpec、`context/` 和任务计划中仍会出现，用于审计追溯，不能覆盖当前事实。

### 工具归档

以下路径视为历史证据/工具状态，不因当前路线改变而重写：

- `docs/openspec/changes/archive/**`
- `docs/superpowers/**`
- `tasks/plans/**`（尤其带 `.sha256.sidecar` 的冻结计划）
- 历史 `MEDUSA_*AUDIT*` result/prompt
- stale/failed review package

除非发现证据完整性本身有问题，否则保持原字节。

## 4. DOCX 说明

`docs/00_*` 到 `docs/08_*` 的 `.docx` 是早期交付导出，**不再视为当前技术路线的权威副本**。本次路线更新以同名 Markdown 和新的 current guide 为准。

如未来确实需要重新生成 DOCX，应从最新 Markdown 单独生成，不能假定旧 DOCX 自动同步。

## 5. Commerce OSS 历史评估

`docs/commerce/oss-reuse/03-*` 到 `09-*` 中 OpenMeter / Kill Bill / Saleor / Vendure / Lago / Keygen / Lemon Squeezy 等主要是历史选型研究。

当前确定路线：
- Medusa v2.19.0 已采用；
- MakePay digital-downloads 只选择性借鉴数字交付模式；
- Playwright / Gitleaks / Syft 已采用；
- PyInstaller / Inno Setup 为产品打包参考；
- n8n production / Trivy / SLSA 等均为后续非阻断项。

## 6. 冲突处理

当文档互相冲突时：

1. 本地 Runtime/Product Git + 原始 evidence/sidecar
2. 最新 Human Decision / Independent Audit
3. `docs/CURRENT_PROJECT_GUIDE.md`
4. `STATUS.md` / `PROJECT_STATE.json`
5. 当前 Commerce 文档
6. 历史计划/报告

绝不能因为历史文档写着“下一步 X0 / Track P / Medusa adoption”就回退已经完成的 C2/C3。
