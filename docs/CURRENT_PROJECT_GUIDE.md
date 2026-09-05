# Jovi Automation 当前项目指南

**状态日期：2026-09-05**  
**文档性质：CURRENT / LIVING / NEW-AGENT ENTRYPOINT**

> 新 Agent 先读本文件。仓库中保留了大量历史 Gate、Track P/I、X0-X4、Medusa spike 与审计资料；它们用于追溯，不代表当前执行状态。

## 1. 项目做什么

Jovi Automation 是一套本地优先、可审计、可回滚的数字产品 Commerce 系统。目标不是让 AI 无监管地操作真实交易，而是把产品资格、商品候选、订单、付款事实记录、Entitlement、DeliveryReceipt、确定性交付包、下载授权、测试和审计自动化，同时把真实平台账号、商业承诺、付款确认、最终交付和退款争议保留给 Jovi 人工控制。

当前第一真实 SKU：**Modbus RTU Diagnostic Toolkit**。

完整目标链：

`Product Source -> Qualification -> Immutable Release -> Private Assets -> Deterministic Delivery Package -> Listing Candidate -> Order -> Human-confirmed Payment Fact -> Entitlement -> DeliveryReceipt -> DownloadGrant/Delivery Preparation -> Human-controlled Delivery -> Support/KPI`

## 2. 当前真实阶段

技术链已经完成到：

`Governance -> Medusa R6 -> R2-R3 -> C2 Synthetic E2E PASS -> C3 First Real SKU PASS -> Runtime C3 Promotion PASS`

当前停点：

`C4_HUMAN_PILOT_DECISION`

C4 候选已经存在，但仍是 `issued_from_human=false`。**没有 Jovi 本人新的明确签发，不得开始真实平台 Pilot。**

## 3. 四个工程与权威边界

| 路径 | 角色 | 当前状态 |
|---|---|---|
| `E:\project\jovi-automation` | Governance / Decision / Audit mirror / Specs / Cloud reference | ACTIVE |
| `E:\project\jovi-medusa-commerce-v1` | 正式 Commerce Runtime（Medusa v2.19.0） | ACTIVE；本地 main reported 已提升至 audited C3 closure |
| `E:\project\jovi-modbus-diagnostic-toolkit-v1` | 第一真实 SKU 产品源 | ACTIVE；C3 作为 read-only product source |
| `E:\project\jovi-commerce-engine-v1` | 早期纯 Python Commerce 试验 | LEGACY / ARCHIVE ONLY |

另有 `E:\project\xianyu-auto-reply`：独立外部适配器。当前 C4 真实发布、消息、付款确认、发货、退款仍由 Jovi 手工执行；Runtime 不读取其 SQLite、Cookie、Token 或浏览器 Profile。

## 4. 已完成关键能力

### Commerce Runtime
- Medusa v2.19.0 正式采用；
- Product / Variant / Order / payment evidence；
- Jovi Entitlement / DeliveryReceipt；
- Redis replay / distributed locking / restart recovery；
- Admin Cookie Session + Playwright；
- Gitleaks / Syft；
- source-tree / sidecar / lockfile / license / SBOM 证据。

### C2 Synthetic Digital Commerce
- immutable DigitalRelease；
- private DeliveryAsset；
- `C2_DETERMINISTIC_ZIP_V1`；
- Python Oracle 与 TypeScript byte-for-byte 对齐；
- DownloadGrant 与 Entitlement 分离；
- replay / recovery / concurrency / negative tests；
- `C2_INDEPENDENT_AUDIT_PASS`。

### C3 First Real SKU
- Modbus 产品源资格化；
- product repo `PASS_ZERO_WRITE`；
- 40/40 product tests in sandbox；
- installer / portable ZIP 原始字节 SHA 绑定；
- 12 条 reported listing claims evidence-bound；
- Real SKU + Synthetic Order/Payment E2E；
- Entitlement=1 / Receipt=1 / DownloadGrant；
- 25 negative cases；
- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`；
- Jovi Human Runtime Promotion Decision；
- `C3_RUNTIME_PROMOTION_AUDIT_PASS`。

## 5. 当前关键锚点（新 Agent 必须重新核验）

Governance GitHub：`Jovifei/Automation_Seal`

- 当前远端 `main`（本指南更新前核验）：`7f64add4f59af3de7f257c5ac3370b4a1e69cd8b`
- 当前 C3/C4 分支：`commerce-c3-real-sku-readiness-20260905`
- 本分支在文档清理开始前 HEAD：`ad0e72db7fd21e368ec25b257a0bc9539718fe85`
- PR #5：open / mergeable；最终状态必须现场重查。

本地 Runtime reported：
- C3 implementation `5b190edce6a530264560a6822b347255fba014ba`
- C3 audited closure / promoted main `63db06e9fd2e1cbdf6e7926b48ba72d3fbe06cb1`
- C3 audit SHA256 `7123e18295895b84b7ed24c75628822db76dba2f7ba6a04f3ad004348e7b79b4`
- Product HEAD `25ef15386b21bcc53277c0d5af5973ad8ea272eb`
- Delivery package SHA256 `4bd5703ae80fcea9c1dcf7d5d1ea2a02fe282a5cf6ef3f04a2c9703db5188e59`

Governance mirror 不能替代本地 Runtime 原始 evidence；解锁下一阶段前必须现场重算。

## 6. 当前 C4 前置工作

在 Jovi 签发 C4 之前，优先完成：

1. 清理 C4 Pilot Draft Kit 中的示例订单，正式 ledger 必须从 0 条真实记录开始；
2. 从本地 `governance/c3/C3_LISTING_CLAIM_EVIDENCE.json` 对发布文案逐条做 claim/evidence 绑定；
3. 修正 CRC、SHA256、兼容性、源码交付、时间承诺等不精确措辞；
4. 重新核验当前闲鱼数字/虚拟商品与退款规则；
5. 明确 `0.2.0-dev` + unsigned installer 是 beta/dev Pilot，或由 Jovi 选择先做 stable/signing；
6. 核对 Runtime dedicated Git remote；
7. 清理并合并 PR #5，使 Governance main 与当前 C3/C4 状态一致；
8. 启用/规划 GitHub branch protection。

## 7. 当前强制安全边界

未经新的 Human Decision，至少以下保持 `false`：

- `production_integration_allowed`
- `real_payment`
- `real_customer`
- `xianyu`
- `auto_delivery`
- `n8n_production`

C4 即使出现真人买家，仍可保持 `real_customer=false`：Runtime 只保存最小化、脱敏的订单/交付事实，不持久化原始买家 PII、完整聊天、Cookie/Token 或支付凭据。

## 8. 当前采用的 OSS 路线

- **Medusa v2.19.0**：正式 Commerce Core；
- **Playwright**：Admin/UI 真实浏览器验收；
- **Gitleaks v8.24.0**：secret scan；
- **Syft v1.20.0**：source/image SBOM；
- **Redis / PostgreSQL / Docker**：Runtime persistence / DB / isolation；
- **makepay-apps/medusa-plugin-digital-downloads** commit `a5343ba18cee85b3eed674ed55d0de7e32aaa448`：只选择性借鉴 immutable release / private asset / DownloadGrant / idempotent delivery 模式，不接管 Jovi 的 payment/Entitlement/Receipt 权威；
- **PyInstaller / Inno Setup**：只参考现有 Windows 产品打包配方，C3 不因上游更新而升级已审计工具链。

Trivy、harden-runner、dependency-review、SLSA/cosign、n8n production 等均不是 C4 首单 Pilot 的前置条件。

## 9. 文档阅读规则

- 当前路线：本文件、`docs/commerce/README.md`、`STATUS.md`、`PROJECT_STATE.json`、`NEXT_STEP_MAP.md`；
- 已完成阶段的计划/审计：用于追溯，不当作当前执行 Prompt；
- `docs/openspec/changes/archive/**`、`docs/superpowers/**`、历史 `MEDUSA_*AUDIT*`：历史证据，不重写、不作为当前阶段入口；
- DOCX 是历史/人类阅读导出，**Markdown current docs 才是当前维护入口**。

详见 `docs/HISTORICAL_DOCUMENT_STATUS.md`。
