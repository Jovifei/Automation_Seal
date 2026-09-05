# C4_HUMAN_PILOT_DECISION_CANDIDATE_V1

**Decision 类型：** Human Pilot Authorization Decision Candidate  
**状态：** `CANDIDATE_ONLY / PRE_PUBLISH_QA_REQUIRED`  
**issued_from_human：** `false`  
**候选日期：** 2026-09-05

> 这不是已经生效的批准。任何 Agent 不得把本文件中的第一人称正文当成 Jovi 已签发的 Human Decision。只有 Pre-Publish QA 完成、Jovi 本人审阅并明确把最终 Decision 签发为 `issued_from_human=true` 后，C4 Pilot 才可开始。

## 1. 已完成前置技术 Gate

reported：
- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`
- `C3_RUNTIME_PROMOTION_AUDIT_PASS`
- `C3_PRODUCT_SOURCE_ZERO_WRITE_PASS`

这些 Governance mirror 锚点不能替代本地 Runtime/Product 原始 evidence；最终签发前必须现场复算。

## 2. 签发前必须完成的 C4 Pre-Publish Gate

必须有明确 evidence：

- Runtime C3 audit/promotion 原件复核；
- Product HEAD / installer / portable ZIP / delivery package SHA 复核；
- `C4_LISTING_CLAIM_REVIEW`：最终商品文案每条技术 claim 均由本地 C3 claim evidence 支持；
- C4 Pilot ledger 从 0 条真实记录开始，不包含 synthetic “已完成订单”；
- CRC / SHA256 / compatibility / source-delivery / timing 文案已纠正；
- 当前闲鱼数字/虚拟商品、退款/争议规则已刷新；
- Jovi 已明确选择 `BETA_PILOT` 或 `STABLE_FIRST`；
- 人工 Delivery Transport 已冻结；
- privacy/minimization 检查完成；
- six real-action flags 仍为 false；
- Governance PR/CI 状态已核验。

任何一项未完成，本 Candidate 不应被签发。

## 3. 当前候选参数（不是最终商业承诺）

- **SKU：** Modbus RTU Diagnostic Toolkit
- **reported version：** `0.2.0-dev`
- **installer signing：** `UNSIGNED`
- **reported C3 delivery package SHA256：** `4bd5703ae80fcea9c1dcf7d5d1ea2a02fe282a5cf6ef3f04a2c9703db5188e59`
- **内部验证包 reported name：** `SYNTH-C3-MODBUS-RTU-0.2.0-dev.zip`
- **渠道：** 闲鱼，Jovi 手工发布
- **试点规模候选：** 5–10 单或 Jovi 指定固定时间窗
- **参考价格候选：** `99.00 CNY`（尚未经过真实市场验证）

注意：客户可见文件名可以在不改变 bytes/SHA 的前提下使用更合适 alias，但必须建立 alias -> audited package 的映射。

## 4. 若 Jovi 选择 BETA_PILOT

最终商品必须透明披露：
- `0.2.0-dev` / beta 试点性质；
- installer 当前 unsigned；
- 仅宣称 C3 evidence 已验证的功能/兼容范围；
- 不承诺 SmartScreen 信誉、所有设备兼容、永久更新或无限售后。

若 Jovi 选择 `STABLE_FIRST`，则停止 C4，返回产品仓独立完成 stable/signing 后再做必要资格化与 Commerce delta audit。

## 5. 拟签发正文模板

> 以下正文只有在 Jovi 本人最终审阅后才能成为正式 Decision。

我作为 Jovi，批准启动 **C4 Human Pilot（首个真实数字产品小规模人工试跑）**，并确认最终 Pilot Package 中绑定的 SKU、version、listing SHA、delivery package SHA、price、pilot size/time window、human-only action matrix 与 privacy rules。

### Human-only platform actions

Pilot 期间以下动作只由 Jovi 手工完成：
- 闲鱼发布；
- 买家沟通/商业承诺；
- 改价；
- 收款/付款事实确认；
- 最终交付物发送；
- 售后与退款争议处理。

### System-internal allowed work

系统可以：
- 生成/保存已人工审核的 listing candidate；
- 记录最小化 order/payment confirmation fact；
- 准备 Entitlement；
- 准备 DeliveryReceipt；
- 核验 DeliveryPackage SHA；
- 记录 support/KPI 分类。

系统不得自动执行平台写动作。

## 6. Privacy

首轮 Pilot 继续保持 `real_customer=false`：Runtime 不持久化买家原始 Profile/PII。

只保存完成审计所需最小字段，例如：
- `pilot_order_id`；
- 随机内部引用/必要时 keyed HMAC 平台引用；
- product/release/version；
- Jovi 人工付款确认事实；
- Entitlement ID；
- Package SHA；
- Receipt ID；
- support/refund 分类。

严禁保存 Cookie、Token、Browser Profile、真实姓名、手机号、地址、完整聊天或支付凭证明文。

## 7. Pilot Exit

至少要求：
- duplicate Entitlement = 0；
- duplicate Receipt = 0；
- wrong-version delivery = 0；
- unauthorized platform action = 0；
- package/release traceability = 100%；
- payment confirmation 可回溯到 order；
- 人工分钟/单、support、refund/未成交原因可量化。

目标结束状态：

`C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION`

Pilot PASS 不自动开放任何新权限；下一阶段仍需 Jovi 逐动作 Permission Expansion Decision。
