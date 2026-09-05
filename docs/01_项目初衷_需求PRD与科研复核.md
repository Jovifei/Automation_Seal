# 项目初衷、当前 PRD 与技术路线

**最后校准：2026-09-05**

## 1. 项目初衷

用户希望把自己的工程能力转化为可验证、可交付、可逐步商业化的数字产品，并用 AI/Codex 自动化调研、产品构建、测试、文档、商品候选、交付准备和复盘，减少重复劳动。

项目**不追求未经监管的自动交易**。真实账号、商业承诺、付款确认、最终交付、改价、退款与争议始终由 Jovi 控制，除非未来逐动作另行 Human Decision。

## 2. 当前第一产品线

第一真实 SKU 已从早期 Alpha 演进为独立产品仓：

`E:\project\jovi-modbus-diagnostic-toolkit-v1`

产品：**Modbus RTU Diagnostic Toolkit**。

C3 已完成：
- 产品源只读资格化；
- 40/40 reported product tests in sandbox；
- installer / portable ZIP SHA 绑定；
- 真实 SKU 的 Commerce Staging；
- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`；
- Runtime Promotion PASS。

当前 reported 版本：`0.2.0-dev`，installer 为 `UNSIGNED`。是否以 beta/dev 形式进入首轮真实 Pilot，还是先做 stable/signing，是 **Jovi 的商业决策**，不是 Agent 默认动作。

## 3. 当前 Commerce PRD

系统目标链：

`Product Source -> Qualification -> DigitalRelease -> Private Assets -> Deterministic DeliveryPackage -> Listing Candidate -> Order -> Human-confirmed Payment Fact -> Entitlement -> DeliveryReceipt -> DownloadGrant -> Human Delivery -> Support/KPI`

### 已完成技术能力
- Medusa v2.19.0 Commerce Core；
- Admin Cookie Session + Playwright；
- Product / Order / payment evidence；
- Jovi Entitlement / DeliveryReceipt；
- Redis replay / concurrency / restart recovery；
- deterministic digital package；
- DownloadGrant；
- Gitleaks / Syft / source-tree / sidecar；
- C2 Synthetic E2E independent PASS；
- C3 Real SKU independent PASS。

### 当前尚未完成
- C4 真实人工 Pilot；
- 商业转化/支持/退款数据；
- Pilot 后逐动作 permission expansion。

## 4. 当前技术路线（已冻结主线）

### Commerce Runtime
- **Medusa v2.19.0**：正式核心，不再重新比较 Saleor/Vendure 作为当前主线；
- PostgreSQL：交易/业务持久化；
- Redis：workflow / lock / replay / recovery；
- Docker：隔离运行与测试；
- Playwright：真实浏览器 Admin 验收。

### 数字交付
- immutable `DigitalRelease`；
- private `DeliveryAsset`；
- deterministic `DeliveryPackage`；
- `Entitlement` 与短时 `DownloadGrant` 分离；
- `DeliveryReceipt` 记录交付证据。

这一部分选择性借鉴 `makepay-apps/medusa-plugin-digital-downloads` commit `a5343ba18cee85b3eed674ed55d0de7e32aaa448` 的模式；**不让第三方插件接管付款、Entitlement、Receipt 或真实自动发货权威**。

### 安全/供应链
- Gitleaks v8.24.0；
- Syft v1.20.0；
- SHA256 / source-tree / sidecar；
- license / third-party notice；
- 历史 FAIL/stale evidence 保留；
- 实现 Agent 与 Independent Auditor 分离。

### 产品 Windows 打包
- PyInstaller / Inno Setup 只作为已有产品打包配方参考；
- C3/C4 不因为上游更新而升级已审计工具链；
- 当前 unsigned 状态必须诚实披露。

## 5. 当前渠道路线

首个商业验证渠道仍是闲鱼，但当前 C4 模式为：

- 系统生成 evidence-bound listing candidate；
- Jovi 人工发布；
- Jovi 人工沟通；
- Jovi 人工确认付款；
- 系统准备 Entitlement / Package / Receipt；
- Jovi 人工发送交付；
- Jovi 人工处理退款/争议。

不需要在 C4 前建设自动闲鱼后台能力。

## 6. 当前研究冻结

以下问题**不再作为当前主线重新研究**：
- 是否采用 Medusa；
- 是否改回纯 Python Commerce；
- 是否在 C4 前切 Saleor/Vendure；
- 是否为了 Pilot 引入 Storefront / S3 / n8n production；
- 是否重做闲鱼后台。

只有版本、安全公告、许可证、平台规则、产品事实与本机事实允许做窄范围刷新。

## 7. Backlog / 非当前主线

以下方向仍可保留，但全部属于 C4 商业验证之后的 backlog：
- 摄影数字产品；
- Ceedling / PlatformIO / Renode 等嵌入式产品工程增强；
- Trivy / harden-runner / dependency-review；
- SLSA / cosign release attestation；
- n8n production 内部编排；
- 多渠道 Storefront / CRM / BI。

**它们不得阻塞第一真实 SKU 的 C4 Pilot。**
