# Commerce 落地主线 C2-C4 V1

## 最终业务目标

让系统把一个经过验证的原创数字产品加工成：

`Product Source → Product Manifest → Release → Listing Candidate → Order → Human-confirmed Payment Evidence → Entitlement → Deterministic Delivery Package → DeliveryReceipt → Human-approved Platform Draft`

并保持真实平台发布、聊天、付款确认、退款和最终交付由 Jovi 控制。

## C2 — Synthetic Digital Commerce E2E

### 目的
证明 Commerce Runtime 本身可以完整处理数字商品，不引入真实 SKU 干扰。

### 输入
完全由本轮生成的 synthetic 产品与资产。

### 必须实现
- immutable DigitalRelease
- private DeliveryAsset
- deterministic DeliveryPackage
- short-lived DownloadGrant
- Listing Candidate
- synthetic Order + Payment Evidence
- exactly-one Entitlement / DeliveryReceipt
- loopback download SHA verification
- Xianyu Draft Bundle（candidate only）
- replay / concurrency / crash-recovery / 20+ negative tests

### Exit Gate
`C2_INDEPENDENT_AUDIT_PASS`

未通过前不得进入真实 SKU。

---

## C3 — Real SKU Staging

### 目的
把第一真实产品 `jovi-modbus-diagnostic-toolkit-v1` 作为只读产品源接入已通过 C2 的 Commerce Runtime。

### 原则
- 不修改 Modbus 产品仓来迎合 Commerce。
- 产品仓提供 release bytes / docs / license / test evidence；Commerce 负责包装、订单、Entitlement 和候选交付。
- 首轮仍然 synthetic order/payment，不触真实平台。

### Exit Gate
`C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`

---

## C4 — Human Pilot

### 目的
验证真实人工商业流程，而不是立即自动交易。

### Jovi 人工动作
- 发布商品
- 回复关键咨询
- 确认付款
- 确认交付
- 退款/争议处理

### 系统允许动作
- 生成 listing/reply/delivery candidate
- 生成订单/证据/Entitlement/Receipt
- 准备交付包和审计记录
- 记录指标

### Pilot Exit Gate
至少 5 个真实订单或明确的人工终止记录，并证明：
- 零重复 Entitlement/Receipt
- 零错误交付版本
- 零越权平台动作
- 所有交付 SHA 可追溯
- 售后边界可执行

---

## C5（未来）— Permission Expansion

只有 C4 证明人工流程稳定后，才逐项讨论：通知自动化、内部 n8n、有限自动交付等。每种权限单独 Decision，不允许一次性开放真实支付/发布/退款。