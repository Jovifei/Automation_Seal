# C4_HUMAN_PILOT_DECISION_CANDIDATE_V1

**Decision 类型：** Human Pilot Authorization Decision Candidate  
**状态：** `CANDIDATE_ONLY / READY_FOR_HUMAN_DECISION`  
**issued_from_human：** `false`  
**最后校准：** 2026-09-06

> 这不是已经生效的批准。Pre-Publish 技术与远端收口已经达到 `C4_PRE_PUBLISH_QA_READY_FOR_HUMAN_DECISION`，但只有 Jovi 本人明确绑定最终商业参数并签发 `issued_from_human=true` 后，真实 C4 Pilot 才可开始。

## 1. 已闭合技术与治理 Gate

已完成并有 evidence：

- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`
- `C3_RUNTIME_PROMOTION_AUDIT_PASS`
- `C3_PRODUCT_SOURCE_ZERO_WRITE_PASS`
- `C3_RUNTIME_GIT_RECONCILIATION_PASS`
- Product HEAD / installer / portable ZIP / delivery package SHA 复核
- `C4_LISTING_CLAIM_REVIEW_PASS`
- `C4_CUSTOMER_PACKAGE_INVENTORY_PASS`
- C4 Pilot ledger 从 0 条真实记录开始
- CRC / SHA256 / compatibility / delivery wording review
- `C4_MANUAL_DELIVERY_TRANSPORT_FROZEN`
- privacy/minimization ready
- `C4_PRE_PUBLISH_QA_READY_FOR_HUMAN_DECISION`

本地 Human-check evidence 还记录：

- release posture：`BETA_PILOT`
- Xianyu rule check：`C4_XIANYU_HUMAN_RULE_CHECK_PASS`

这些 Human-check 记录支持发布前 readiness，但不替代本文件的最终 Human Pilot Authorization。

## 2. Runtime 远端收口

Runtime 权威仓：

`Jovifei/jovi-medusa-commerce-v1`

C3 baseline：

`63db06e9628331982893929f39b1037077138480`

C4 readiness 已通过 Runtime PR #1 以 Fast-Forward 提升到 `main`：

`b7ec762f29092106ad10c88d72bc682b5f9e7ac2`

最终 Runtime CI：

- run：`34016366716`
- conclusion：PASS
- current audited `audit-source` SHA256：`3101604bf10c9c6ed3c9b67a23e5ef77a6704472835ccfd536c2cc0b6b8e568a`（94 files）
- unit：9/9 suites，41/41 tests PASS
- secret scan：0 findings
- TypeScript / License / SBOM：PASS
- X2 first/replay/concurrency/negative：PASS
- C2 first/replay/concurrency/negative/http-download：PASS
- terminal：`C4_RUNTIME_SYNTHETIC_REGRESSION_PASS`

Governance live binding：

`reference/commerce/c4/C4_RUNTIME_REMOTE_BINDING_20260906.json`

C4 CI 会使用 `git ls-remote` 重新核对 Runtime `main`，因此不允许再用短 SHA 推导完整 Git object ID。

## 3. 当前 Pilot 产品绑定

- **SKU：** Modbus RTU Diagnostic Toolkit
- **Version：** `0.2.0-dev`
- **Release posture：** `BETA_PILOT`（本地 Human-check 已记录，最终 Decision 再确认）
- **Installer signing：** `UNSIGNED`
- **Installer SHA256：** `d86ccc3136bc2ed201622c5f961738e9e81762e74e71ac5772ea6d4b5a408e02`
- **Portable ZIP SHA256：** `7525e4c8d4fd55900d46c51e075b92e47d61c7d8e1393383e2e92206855a9628`
- **权威 DeliveryPackage SHA256：** `4bd5703ae80fcea9c1dcf7d5d1ea2a02fe282a5cf6ef3f04a2c9703db5188e59`
- **客户可见 alias 候选：** `JoviModbusDiagnosticToolkit-0.2.0-dev-Windows-x64.zip`
- **Channel：** 闲鱼，Jovi 手工发布

alias 只允许改变展示文件名；权威 package bytes/SHA 不变。

## 4. 仍需 Jovi 明确绑定的最终商业参数

### 4.1 Pilot 价格

推荐候选：

`99 CNY`

当前仍是 proposal，必须由 Jovi 明确签发。

### 4.2 Pilot 停止条件

推荐候选：

**最多 10 个已付款 Pilot 订单，或自第一次真实商品发布起 14 个自然日，先到者为准。**

Jovi 可以签发其他精确订单上限或时间窗；未明确绑定前不得开始 Pilot。

### 4.3 Release posture 最终确认

本地 Human-check evidence 已记录：

`BETA_PILOT`

正式 Decision 应再次绑定这一值，或由 Jovi 明确改为 `STABLE_FIRST`。如果改为 `STABLE_FIRST`，则停止 C4，返回产品仓独立完成新 stable/signing release，并重新做必要资格化和 Commerce delta audit。

## 5. 拟签发正文模板

> 以下内容只有 Jovi 在当前 Human Decision 中明确确认后，才可落为 `issued_from_human=true` 的正式决策。

我作为 Jovi，批准启动 **C4 Human Pilot（首个真实数字产品小规模人工试点）**，并绑定：

- SKU：`Modbus RTU Diagnostic Toolkit`
- Version：`0.2.0-dev`
- Release posture：`BETA_PILOT`
- DeliveryPackage SHA256：`4bd5703ae80fcea9c1dcf7d5d1ea2a02fe282a5cf6ef3f04a2c9703db5188e59`
- Pilot price：`[JOVI_FINAL_PRICE_CNY]`
- Pilot stop condition：`[JOVI_FINAL_ORDER_LIMIT_OR_TIME_WINDOW]`
- Channel：闲鱼，人工发布

### Human-only platform actions

Pilot 期间以下动作只由 Jovi 手工完成：

- 闲鱼发布；
- 买家沟通与商业承诺；
- 改价；
- 真实付款事实确认；
- 最终交付物/受控链接发送；
- 退款与争议处理。

### System-internal allowed work

系统可以：

- 使用已人工审核、evidence-bound 的 listing candidate；
- 记录最小化、脱敏 order/payment-confirmation fact；
- 准备/校验 Entitlement；
- 准备/校验 DeliveryReceipt；
- 核验 DeliveryPackage SHA；
- 记录 support / KPI 分类。

系统不得自动执行任何真实平台写动作。

## 6. Privacy

首轮 Pilot 默认继续：

`real_customer=false`

这不禁止真人 Pilot；含义是 Runtime 不持久化买家原始 Profile/PII。

只保存完成审计所需的最小字段，例如：

- `pilot_order_id`
- 随机内部引用 / 必要时 keyed HMAC 平台引用
- product/release/version
- Jovi 人工付款确认事实
- Entitlement ID
- Package SHA
- Receipt ID
- support/refund 分类

严禁持久化：Cookie、Token、Browser Profile、真实姓名、手机号、地址、完整聊天或支付凭证明文。

## 7. 六项真实动作权限

最终 Human Decision 和首轮 Pilot 默认均不自动翻转以下权限：

- `production_integration_allowed=false`
- `real_payment=false`
- `real_customer=false`
- `xianyu=false`
- `auto_delivery=false`
- `n8n_production=false`

即使 C4 Pilot PASS，也必须另行逐动作 Permission Expansion Decision。

## 8. Pilot Exit

至少要求：

- duplicate Entitlement = 0
- duplicate Receipt = 0
- wrong-version delivery = 0
- unauthorized platform action = 0
- package/release traceability = 100%
- payment confirmation 可回溯到 order
- 无未经授权原始客户 PII/平台凭据进入 Runtime
- 人工分钟/单、support、refund/dispute、未成交原因可量化

目标结束状态：

`C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION`

## 9. 当前停止条件

在 Jovi 明确绑定最终 price、Pilot limit/time-window，并签发正式 Human Decision 之前：

`issued_from_human=false`

`NO_REAL_PILOT_START`
