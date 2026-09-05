# Commerce 专题文档导航

**最后校准：2026-09-05**  
**当前停点：`C4_HUMAN_PILOT_DECISION`**

> 本目录同时保存当前 C4 文档和从 Medusa spike/R2/R6/C2/C3 以来的完整历史。新 Agent 不要因为文件很多就逐份按时间重跑；先按本索引分类。

## 1. CURRENT / LIVING — 当前应读

### 当前状态与架构
- [`COMMERCE_PROJECT_TOPOLOGY_AND_AUTHORITY_V1.md`](COMMERCE_PROJECT_TOPOLOGY_AND_AUTHORITY_V1.md) — 四仓角色与权威边界
- [`C3_LOCAL_AUDIT_CLOSURE_MIRROR_20260905.md`](C3_LOCAL_AUDIT_CLOSURE_MIRROR_20260905.md) — C3 本地独立审计索引（mirror，不替代原件）
- [`JOVI_RUNTIME_C3_PROMOTION_DECISION_V1.md`](JOVI_RUNTIME_C3_PROMOTION_DECISION_V1.md) — C3 audited closure 提升 Runtime main 的 Human Decision
- [`C3_POST_AUDIT_RUNTIME_PROMOTION_PLAN_V1.md`](C3_POST_AUDIT_RUNTIME_PROMOTION_PLAN_V1.md) — Promotion 规则/回滚参考

### C4 当前执行
- [`C4_HUMAN_PILOT_PLAN_V1.md`](C4_HUMAN_PILOT_PLAN_V1.md)
- [`C4_PILOT_PRIVACY_MINIMIZATION_V1.md`](C4_PILOT_PRIVACY_MINIMIZATION_V1.md)
- [`C4_HUMAN_PILOT_DECISION_CANDIDATE_V1.md`](C4_HUMAN_PILOT_DECISION_CANDIDATE_V1.md) — **`issued_from_human=false`，不是授权**
- [`C4_PILOT_OPERATIONAL_KIT_V1.md`](C4_PILOT_OPERATIONAL_KIT_V1.md) — **Pre-Publish Draft；本地 claim evidence QA 后才能发布**

### Governance / Git
- [`COMMERCE_RUNTIME_REMOTE_GOVERNANCE_PLAN_V1.md`](COMMERCE_RUNTIME_REMOTE_GOVERNANCE_PLAN_V1.md)
- [`GITHUB_GOVERNANCE_PLAN.md`](GITHUB_GOVERNANCE_PLAN.md)

### OSS
- [`oss-reuse/README.md`](oss-reuse/README.md)

## 2. COMPLETED STAGE — 已完成，供追溯

### Medusa / R2
以下记录 Medusa 从 spike 到可采用的证据。当前不再做框架选型：
- `MEDUSA_ADOPTION_FRAMEWORK.md`
- `MEDUSA_R2_REMEDIATION.md`
- `MEDUSA_R2_INDEPENDENT_AUDIT_R1_RESULT.md`
- `MEDUSA_R2_INDEPENDENT_AUDIT_R2_RESULT.md`
- `MEDUSA_R2R2_*`
- `MEDUSA_R2R3_*`

### R6 Controlled Adoption
- `JOVI_MEDUSA_R6_CONTROLLED_ADOPTION_DECISION_V1.md`
- `MEDUSA_R6_ADOPTION_DECISION_CANDIDATE.json`
- `R6_*` / Post-Import 相关资料

R6 已完成，当前不要重新创建 Commerce repo 或重复做 adoption。

### C2 Synthetic Digital Commerce
- `COMMERCE_C2_SYNTHETIC_E2E_DIGITAL_DELIVERY_PLAN.md`
- `C2_CLOUD_REFERENCE_*`
- `C2_LOCAL_AUDIT_CLOSURE_MIRROR_20260905.md`
- `OSS_DIGITAL_DELIVERY_ADOPTION_V1.md`

Reported verdict：`C2_INDEPENDENT_AUDIT_PASS`。

### C3 First Real SKU
- `C3_MODBUS_REAL_SKU_STAGING_PLAN_V1.md`
- `C3_REAL_SKU_READINESS_PACKAGE_20260905.md`
- `C3_PRODUCT_READONLY_EXECUTION_PATTERN_20260905.md`
- `C3_WINDOWS_RELEASE_CHECKLIST_20260905.md`
- `C3_OSS_AND_WINDOWS_RELEASE_ACCELERATION_20260905.md`
- `C3_LOCAL_AUDIT_CLOSURE_MIRROR_20260905.md`

Reported verdict：`C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`；Runtime Promotion reported `C3_RUNTIME_PROMOTION_AUDIT_PASS`。

## 3. HISTORICAL / DO NOT USE AS CURRENT INSTRUCTIONS

以下文档可以解释“为什么这样设计”，但不应被新 Agent 当作当前 TODO：

- `COMMERCE_POST_R6_MAINLINE_PLAN.md`
- `COMMERCE_LANDING_HANDOFF_20260903.md`
- `COMMERCE_LANDING_MAINLINE_C2_C4_V1.md` 中已经完成的 C2/C3 部分
- `INTEGRATION_PLAN.md`
- `MEDUSA_R2R2_INTEGRATION_POINTER.md`
- 旧 `*_DECISION_CANDIDATE*`（已由后续 Human Decision supersede 的）
- 早期 Medusa spike 计划/修复 Prompt

它们保留用于审计追溯，不必删除。

## 4. 当前 OSS 结论

### 已采用
- Medusa v2.19.0 — Commerce Core
- Playwright — real browser/Admin acceptance
- Gitleaks v8.24.0 — secret scan
- Syft v1.20.0 — source/image SBOM
- Redis/PostgreSQL/Docker — Runtime 基础设施

### 选择性借鉴
`makepay-apps/medusa-plugin-digital-downloads` commit `a5343ba18cee85b3eed674ed55d0de7e32aaa448`：
- immutable DigitalRelease
- private asset/storage
- short-lived DownloadGrant
- Entitlement/Grant separation
- idempotent digital delivery

不接管 Jovi payment/Entitlement/DeliveryReceipt authority，不启用其真实自动交付。

### 产品打包参考
- PyInstaller
- Inno Setup

只参考现有产品 recipe；C4 前不为追最新版本升级。

### 后续非阻断
Trivy、harden-runner、dependency-review、SLSA/cosign、n8n production、Storefront/S3。

## 5. 当前 C4 Pre-Publish 风险

当前 `C4_PILOT_OPERATIONAL_KIT_V1.md` 仍需：
- 删除/隔离 synthetic 示例订单；
- 逐条绑定本地 C3 claim evidence；
- 修 CRC“纠错”、SHA“签名”等不精确措辞；
- 核对实际交付是否包含源码/PDF/requirements/virtual-simulator；
- 刷新当前闲鱼数字商品/退款规则；
- 明确 `0.2.0-dev` + unsigned Pilot 的披露。

在这些完成以及 Jovi `issued_from_human=true` 前，不进入真实 Pilot。

## 6. 新 Agent 冲突处理

当本文与历史文档冲突：

1. 本地 Runtime/Product 原始 evidence；
2. 最新 Human Decision / Independent Audit；
3. `docs/CURRENT_PROJECT_GUIDE.md`；
4. 本 README；
5. completed/history docs。
