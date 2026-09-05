# Jovi Automation / Automation_Seal

Jovi Automation 是一个本地优先、可审计、可回滚的数字产品 Commerce 与治理工程。它负责产品资格、Commerce 规格、Human Decision、审计索引、测试参考、商品候选与交付证据；真实平台账号、商业承诺、付款确认、最终交付和退款争议仍由 Jovi 控制。

## 当前状态 — 2026-09-05

技术主线已经完成：

`Governance -> Medusa R6 -> R2-R3 -> C2 Synthetic E2E PASS -> C3 First Real SKU PASS -> Runtime C3 Promotion PASS`

当前停点：

**`C4_HUMAN_PILOT_DECISION`**

第一真实 SKU：**Modbus RTU Diagnostic Toolkit**。

C4 Human Pilot Decision Candidate 已生成，但仍是 `issued_from_human=false`。因此当前只能进行 Pre-Publish QA、治理收口和 Pilot 资料准备；没有 Jovi 本人的新 Human Decision，不得开始真实平台 Pilot。

## 工程拓扑

| 本地路径 | 角色 |
|---|---|
| `E:\project\jovi-automation` | Governance / Decision / Audit mirror / Specs / Cloud reference |
| `E:\project\jovi-medusa-commerce-v1` | Formal Commerce Runtime / Medusa v2.19.0 |
| `E:\project\jovi-modbus-diagnostic-toolkit-v1` | First real SKU / Product source |
| `E:\project\jovi-commerce-engine-v1` | Legacy pure-Python Commerce / archive only |
| `E:\project\xianyu-auto-reply` | Independent external adapter; current real actions human-only |

Automation_Seal 不应承载 Runtime 业务源码。

## 已完成能力

### Medusa / Runtime
- Medusa v2.19.0 controlled adoption；
- Product / Variant / Order / payment evidence；
- Jovi Entitlement / DeliveryReceipt；
- Redis replay / locking / restart recovery；
- Admin Cookie Session + Playwright；
- Gitleaks / Syft / source-tree / sidecars / license / lockfile。

### C2 — Synthetic Digital Commerce
- immutable DigitalRelease；
- private DeliveryAsset；
- deterministic DeliveryPackage；
- Python ↔ TypeScript byte-for-byte Oracle；
- DownloadGrant 与 Entitlement 分离；
- replay/recovery/concurrency/negative；
- `C2_INDEPENDENT_AUDIT_PASS`。

### C3 — First Real SKU
- Modbus product source qualification；
- product `PASS_ZERO_WRITE`；
- sandbox product tests；
- installer / portable ZIP SHA binding；
- evidence-bound listing claims；
- Real SKU + Synthetic Order/Payment E2E；
- Entitlement=1 / Receipt=1 / DownloadGrant；
- 25 negative cases；
- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`；
- Human Runtime Promotion + `C3_RUNTIME_PROMOTION_AUDIT_PASS`。

## 当前 C4 工作

在 Jovi 签发 Pilot 前，优先：

1. 复核 Governance main / 当前 branch / PR #5 / CI；
2. 从本地 C3 claim evidence 审核 C4 listing；
3. 清理 Pilot ledger 的 synthetic/example completed rows；
4. 修正 CRC、SHA256、compatibility、源码交付、耗时等文案；
5. 核验当前闲鱼数字/虚拟商品与退款规则；
6. 明确 `0.2.0-dev` + unsigned beta Pilot 或 stable-first；
7. 冻结人工交付通道；
8. 核对 Runtime dedicated Git remote；
9. 准备最终 `issued_from_human=false` Decision Candidate 给 Jovi。

## 当前永久边界

未经新的 Human Decision：

```text
production_integration_allowed=false
real_payment=false
real_customer=false
xianyu=false
auto_delivery=false
n8n_production=false
```

C4 即使有真人买家，真实发布、消息、付款确认、发货、改价、退款也仍由 Jovi 手工完成；Runtime 只保存最小化、脱敏事实，不读取平台 Cookie/Token/Profile 或完整买家资料。

## OSS 复用路线

### 已采用
- Medusa v2.19.0 — Commerce Core；
- Playwright — browser/Admin acceptance；
- Gitleaks v8.24.0 — secret scanning；
- Syft v1.20.0 — source/image SBOM；
- Redis / PostgreSQL / Docker — Runtime infra。

### 选择性借鉴
- `makepay-apps/medusa-plugin-digital-downloads` commit `a5343ba18cee85b3eed674ed55d0de7e32aaa448` — immutable release/private asset/DownloadGrant/idempotent delivery；不接管 Jovi payment/Entitlement/Receipt authority。
- PyInstaller / Inno Setup — 只参考现有产品打包配方，不在 C4 前为追新升级。

### 非当前阻断项
Trivy、harden-runner、dependency-review、SLSA/cosign、n8n production、Storefront、S3、多渠道自动化。

## 新 Agent 文档入口

1. [Current Project Guide](docs/CURRENT_PROJECT_GUIDE.md)
2. [Historical Document Status](docs/HISTORICAL_DOCUMENT_STATUS.md)
3. [First Read](README_FIRST.md)
4. [Project State](PROJECT_STATE.json)
5. [Next Step Map](NEXT_STEP_MAP.md)
6. [Commerce Docs](docs/commerce/README.md)
7. [Docs Index](docs/README.md)
8. [Agent Rules](AGENTS.md)

历史 Medusa/Gate/OpenSpec/Superpowers 资料保留用于审计追溯，不代表当前下一步。

## 当前完成定义

技术 C0–C3 已高度成熟。商业 V1 还需要 C4 Human Pilot 的真实市场证据。

C4 目标结束状态：

`C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION`

之后仍由 Jovi 逐动作决定下一项自动化权限，而不是一次性“全自动闲鱼”。
