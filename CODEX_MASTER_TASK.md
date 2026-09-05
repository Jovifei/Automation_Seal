# Jovi Automation Commerce V1 主任务书

**最后校准：2026-09-05**  
**当前停点：`C4_HUMAN_PILOT_DECISION`**

## 1. 当前主线

本项目已经完成技术主线：

`Governance -> Medusa R6 -> R2-R3 -> C2 Synthetic E2E PASS -> C3 First Real SKU PASS -> Runtime C3 Promotion PASS`

当前目标不是继续建设 Commerce Core，而是安全完成第一真实 SKU 的 C4 Human Pilot，并用真实数据决定下一项自动化权限。

第一 SKU：**Modbus RTU Diagnostic Toolkit**。

## 2. 永久边界

未经新的 Jovi Human Decision：

- `production_integration_allowed=false`
- `real_payment=false`
- `real_customer=false`
- `xianyu=false`
- `auto_delivery=false`
- `n8n_production=false`

不读取/提交 Cookie、Token、Browser Profile、买家 PII、完整聊天、支付秘密。

不自动执行：发布、消息、付款确认、发货、改价、退款、平台验证。

## 3. 当前工程权威

- Governance：`E:\project\jovi-automation` / `Jovifei/Automation_Seal`
- Runtime：`E:\project\jovi-medusa-commerce-v1`
- Product Source：`E:\project\jovi-modbus-diagnostic-toolkit-v1`
- Legacy Commerce：`E:\project\jovi-commerce-engine-v1`（archive only）
- Xianyu Adapter：`E:\project\xianyu-auto-reply`（独立，不读写其秘密/DB）

## 4. 已完成阶段

### Medusa/R6/R2-R3
正式采用 Medusa v2.19.0，Post-Import、Cookie Session、Playwright、安全供应链均完成对应独立验证。

### C2
Synthetic Digital Commerce E2E：DigitalRelease、private asset、deterministic package、DownloadGrant、replay/recovery/concurrency、negative tests，结论 `C2_INDEPENDENT_AUDIT_PASS`。

### C3
Real Modbus SKU：product zero-write、sandbox tests、artifact SHA、evidence-bound claims、Real SKU Synthetic Commerce E2E、25 negative tests，结论 `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`。

Jovi 已完成 C3 Runtime Promotion，reported `C3_RUNTIME_PROMOTION_AUDIT_PASS`。

## 5. 当前唯一实施顺序

```text
C4-P0 Current Truth Verification
-> C4-P1 Pre-Publish QA
-> C4-P2 Jovi Product/Pilot Mode Choice
-> C4-P3 Delivery Transport Freeze
-> C4-P4 Jovi Human Pilot Decision
-> C4-P5 Human-controlled Pilot
-> C4-P6 Evidence + KPI Recap
-> C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION
```

## 6. C4-P0 / P1

必须：
- 核 Governance main/current branch/PR/CI；
- 核 Runtime C3 audit/promotion 原始 evidence；
- 核 Product HEAD / artifact SHA；
- 修 C3 governance mirror 文本编码；
- 清 C4 ledger 的 synthetic/example completed rows；
- 从本地 C3 claim evidence 对最终 listing 逐条 KEEP/REWRITE/REMOVE；
- 修正 CRC/SHA256/compatibility/source-delivery/timing wording；
- 刷新当前闲鱼数字商品/退款规则；
- 复核 Runtime Git remote。

此阶段不得真实发布。

## 7. C4-P2 / P3

当前 SKU reported：`0.2.0-dev`，installer unsigned。

Jovi 选择：
- `BETA_PILOT`：透明 beta/dev/unsigned；
- `STABLE_FIRST`：返回产品仓做 stable/signing，然后重新做必要资格化。

人工 Delivery Transport 只需满足：
- payload bytes 与 audited package 一致；
- SHA256 可复核；
- Jovi 手工发送；
- 可撤销/到期；
- 不收集不必要 PII。

C4 不为此提前建设 Storefront/S3。

## 8. C4-P4 Human Decision

当前 Decision Candidate 是 `issued_from_human=false`。

最终 Decision 必须由 Jovi 本人明确签发，并绑定：
- C3 audit SHA；
- Runtime main；
- SKU/version；
- final Listing Candidate SHA；
- DeliveryPackage SHA；
- pilot price；
- pilot size/time window；
- human-only action matrix；
- privacy rules。

缺失则保持 blocked。

## 9. C4-P5 Pilot

首轮 5–10 单或固定时间窗。

Jovi 手工：publish / message / price / payment confirmation / final delivery / refund-dispute。

Runtime：记录最小 order/payment fact，准备 Entitlement/Receipt/Package，生成 support/KPI。

## 10. C4-P6 Exit

至少：
- 0 duplicate Entitlement；
- 0 duplicate Receipt；
- 0 wrong-version delivery；
- 0 unauthorized platform action；
- package/release/payment traceability；
- 人工耗时、support、refund/未成交原因可量化。

结束：

`C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION`

之后停止，等待 Jovi 的逐动作 Permission Expansion Decision。

## 11. 不再执行的旧路线

以下只作历史追溯，不是当前任务：
- G0-G6 Governance remediation；
- Gate A.P / Track P/I；
- X0-X4；
- 旧 SQLite C0-C6；
- Medusa adoption；
- C2/C3 implementation。

## 12. 工作闭环

每轮：事实复核 -> 最小计划 -> 小范围修改 -> 聚焦测试 -> 回归 -> evidence -> `STATUS.md` -> 唯一下一动作。

实现 Agent 不得自审；Human Decision 不得伪造；历史 evidence 不得覆盖。
