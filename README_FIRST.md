# Jovi Automation — 首次阅读指南

**最后校准：2026-09-05**  
**当前主线：Commerce V1 / C4 Human Pilot**

> 这已经不是 2026-07 的“第一次解压后跑 Phase 0/A/X0”工程。Governance、Medusa adoption、C2、C3 都已经完成到独立审计/Promotion。新 Agent 不要重新从旧 Gate 开始。

## 1. 先知道当前状态

技术链：

`Governance -> Medusa R6 -> R2-R3 -> C2 PASS -> C3 PASS -> Runtime C3 Promotion PASS`

当前停点：

`C4_HUMAN_PILOT_DECISION`

当前存在 C4 Decision Candidate，但仍为：

`issued_from_human=false`

所以现在能做的是 C4 Pre-Publish QA 与 Human Decision 准备，**不能直接开始真实闲鱼 Pilot**。

## 2. 新 Agent 最小必读

按顺序：

```text
docs/CURRENT_PROJECT_GUIDE.md
docs/HISTORICAL_DOCUMENT_STATUS.md
PROJECT_STATE.json
NEXT_STEP_MAP.md
STATUS.md
AGENTS.md
CODEX_MASTER_TASK.md
docs/commerce/README.md
```

历史 `context/`、OpenSpec、Superpowers、Medusa audit 只在需要追溯时读取。

## 3. 当前四个核心工程

```text
E:\project\jovi-automation
  Governance / Decision / Audit mirror / Specs / Cloud reference

E:\project\jovi-medusa-commerce-v1
  Formal Medusa Commerce Runtime

E:\project\jovi-modbus-diagnostic-toolkit-v1
  First real SKU / product source

E:\project\jovi-commerce-engine-v1
  Legacy pure-Python Commerce / archive only
```

另有：

`E:\project\xianyu-auto-reply`

它仍是独立外部适配器。当前不读取它的 SQLite、Cookie、Token、Browser Profile，也不让 Runtime 直接执行真实平台动作。

## 4. 当前已验证的第一商品

产品：**Modbus RTU Diagnostic Toolkit**

reported C3 anchors：
- product HEAD：`25ef15386b21bcc53277c0d5af5973ad8ea272eb`
- version：`0.2.0-dev`
- installer：unsigned
- installer SHA256：`d86ccc3136bc2ed201622c5f961738e9e81762e74e71ac5772ea6d4b5a408e02`
- portable ZIP SHA256：`7525e4c8d4fd55900d46c51e075b92e47d61c7d8e1393383e2e92206855a9628`
- Commerce delivery package SHA256：`4bd5703ae80fcea9c1dcf7d5d1ea2a02fe282a5cf6ef3f04a2c9703db5188e59`
- C3 verdict：`C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`
- Runtime promotion：`C3_RUNTIME_PROMOTION_AUDIT_PASS`

这些是 governance mirror 中的 reported facts；开始 C4 前仍从本地 Runtime/Product 原件重算。

## 5. 当前第一件事不是“重新测试所有 C3”

当前 Pre-Publish QA：

1. 检查 Governance GitHub main / C3-C4 branch / PR #5 / CI；
2. 检查 Runtime main 与 C3 audit 原件；
3. 清理 C4 Operational Kit 中的 synthetic/example completed rows；
4. 从本地 C3 claim evidence 审核最终商品文案；
5. 修正 CRC / SHA256 / compatibility / delivery wording；
6. 刷新当前闲鱼数字/虚拟商品与退款规则；
7. Jovi 决定 beta/dev/unsigned Pilot 还是 stable-first；
8. 选择人工交付通道；
9. 准备 `issued_from_human=false` 的最终 Decision Candidate 给 Jovi。

## 6. C4 若获 Jovi 人工批准

首轮 5–10 单或固定时间窗。

Jovi 手工：
- 发布；
- 消息/承诺；
- 改价；
- 付款确认；
- 最终交付；
- 退款/争议。

系统负责：
- listing candidate；
- order/payment fact record；
- Entitlement；
- DeliveryReceipt；
- package/hash；
- support/KPI。

## 7. 当前真实权限

至少保持：

```text
production_integration_allowed=false
real_payment=false
real_customer=false
xianyu=false
auto_delivery=false
n8n_production=false
```

测试或 Pilot PASS 不会自动翻转它们。

## 8. 已采用 OSS

- Medusa v2.19.0 — Commerce Core；
- Playwright — Admin/browser E2E；
- Gitleaks v8.24.0 — secret scanning；
- Syft v1.20.0 — SBOM；
- Redis/PostgreSQL/Docker — Runtime infra；
- MakePay digital-downloads — 仅选择性借鉴 DigitalRelease/private asset/DownloadGrant/idempotent delivery；
- PyInstaller/Inno Setup — Windows 产品现有配方参考，不在 C4 前升级。

详见 `docs/commerce/oss-reuse/README.md`。

## 9. 不要再做的旧路线

除非发现 SHA/证据冲突，不要重新执行：
- `Phase 0/A/X0`；
- `Track P / Track I`；
- `X1-X4`；
- Medusa adoption；
- C2/C3 implementation；
- 纯 Python Commerce 主线；
- n8n production / Storefront / S3 作为 Pilot 前置。

## 10. 什么时候才叫完成

技术系统已经接近 V1 完成。

商业 V1 仍需真实 C4 Pilot：
- 5–10 单或固定窗口；
- 0 duplicate Entitlement/Receipt；
- 0 wrong-version delivery；
- 0 unauthorized action；
- package/release/payment fact 可追溯；
- 人工耗时、support/refund 数据可复盘。

结束：

`C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION`

之后再由 Jovi 逐项决定下一项自动化权限。
