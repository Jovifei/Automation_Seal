# Commerce 落地主线 C2-C4 V1

**状态：CURRENT ROADMAP / C2+C3 COMPLETED / C4 CURRENT**  
**最后校准：2026-09-05**

## 最终业务目标

让系统把经过验证的原创数字产品加工成：

`Product Source -> Product Manifest -> Release -> Listing Candidate -> Order -> Human-confirmed Payment Fact -> Entitlement -> Deterministic Delivery Package -> DeliveryReceipt -> DownloadGrant -> Human-controlled Delivery`

真实平台发布、消息、付款确认、改价、退款和最终交付由 Jovi 控制，除非未来逐动作 Human Decision。

---

## C2 — Synthetic Digital Commerce E2E — COMPLETED

### 目的
证明 Commerce Runtime 可以完整处理数字商品，不引入真实 SKU 干扰。

### 已完成
- immutable DigitalRelease；
- private DeliveryAsset；
- deterministic DeliveryPackage；
- short-lived DownloadGrant；
- Listing Candidate；
- synthetic Order + Payment Evidence；
- exactly-one Entitlement / DeliveryReceipt；
- loopback download SHA；
- Xianyu Draft candidate only；
- replay / concurrency / crash-recovery / negative tests；
- Python Oracle 与 TypeScript byte-for-byte package 对齐。

Exit Gate：

`C2_INDEPENDENT_AUDIT_PASS`

reported implementation：`82accb4173b34133dacc864d7f32c92fb26107ac`  
reported audit closure：`ce25c9e2a660b1f6b64ead3192ff861b3a8a19fa`

**不要重新执行 C2，除非本地锚点/原始 evidence 发生漂移。**

---

## C3 — Real SKU Staging — COMPLETED

### 产品
`E:\project\jovi-modbus-diagnostic-toolkit-v1`

### 已完成
- product source read-only qualification；
- `PASS_ZERO_WRITE`；
- product tests in isolated sandbox；
- installer / portable ZIP 原始 SHA 绑定；
- evidence-bound listing claims；
- immutable Release / deterministic wrapper；
- Real SKU + Synthetic Order/Payment；
- exactly-one Entitlement / Receipt；
- DownloadGrant + loopback verify；
- replay / restart recovery；
- 25 negative cases；
- Admin Playwright。

Exit Gate：

`C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`

reported implementation：`5b190edce6a530264560a6822b347255fba014ba`  
reported audit closure：`63db06e9fd2e1cbdf6e7926b48ba72d3fbe06cb1`

随后已经 Jovi Human Decision 进行 Runtime Promotion，reported：

`C3_RUNTIME_PROMOTION_AUDIT_PASS`

**不要重新做 C3。产品源码若后续变化，走新的产品资格化/delta audit。**

---

## C4 — Human Pilot — CURRENT

### 当前状态

`C4_HUMAN_PILOT_DECISION`

当前 Candidate：

`docs/commerce/C4_HUMAN_PILOT_DECISION_CANDIDATE_V1.md`

仍为：

`issued_from_human=false`

### C4 Pre-Publish QA

真实发布前：
1. 从本地 C3 claim evidence 审核最终 listing；
2. 清空/隔离 Pilot ledger synthetic 示例；
3. 修正 CRC/SHA256/compatibility/source-delivery/timing 文案；
4. 刷新当前闲鱼数字/虚拟商品及退款规则；
5. 明确 `0.2.0-dev` + unsigned beta Pilot 或 stable-first；
6. 冻结人工 delivery transport；
7. 复核 Runtime dedicated Git remote；
8. 收口 Governance PR/CI/main。

### Jovi 人工动作
- 发布商品；
- 回复关键咨询/商业承诺；
- 确认付款；
- 改价；
- 最终发送交付；
- 退款/争议。

### 系统动作
- listing/reply/delivery candidate；
- order/payment fact record；
- Entitlement / DeliveryReceipt；
- package/hash；
- support/KPI。

### Pilot Exit Gate

推荐 5–10 个真实订单或固定时间窗，并证明：
- 0 duplicate Entitlement/Receipt；
- 0 wrong-version delivery；
- 0 unauthorized platform action；
- package/release/payment traceability；
- 人工负担/support/refund/未成交原因可量化。

目标状态：

`C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION`

---

## C5（未来）— Permission Expansion

只有 C4 真实证据足够后，才逐项讨论：
- listing 自动化；
- reply suggestion；
- order metadata helper；
- delivery preparation；
- 有限平台动作。

每项权限独立 Decision。**绝不因为 C4 PASS 一次性开放真实支付、发布、消息、自动交付或退款。**

## 当前强制边界

在新的 Human Decision 之前至少保持：

`production_integration_allowed=false`  
`real_payment=false`  
`real_customer=false`  
`xianyu=false`  
`auto_delivery=false`  
`n8n_production=false`
