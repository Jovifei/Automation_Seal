# Jovi 当前操作清单 — C4 Human Pilot

**最后校准：2026-09-05**

## A. 现在立即执行

1. 让 Agent 先读：
   - `docs/CURRENT_PROJECT_GUIDE.md`
   - `docs/HISTORICAL_DOCUMENT_STATUS.md`
   - `README_FIRST.md`
   - `PROJECT_STATE.json`
   - `NEXT_STEP_MAP.md`
2. 核对 GitHub：`Automation_Seal` main / 当前 C3-C4 branch / PR #5 / CI。
3. 核对本地 Runtime：`E:\project\jovi-medusa-commerce-v1` 的 C3 audit/promotion 原始 evidence。
4. 核对产品：`E:\project\jovi-modbus-diagnostic-toolkit-v1` 的 HEAD / installer / portable ZIP / package SHA。
5. 不直接发布当前 C4 Operational Kit。

## B. C4 Pre-Publish QA

让本地 Agent：

- 修 C3 governance mirror 中的文本编码/转义问题；
- 清空 C4 Pilot ledger 的 synthetic/example completed rows；
- 读取本地 `governance/c3/C3_LISTING_CLAIM_EVIDENCE.json`；
- 生成 C4 claim review；
- 删除无证据 claim；
- 修正 CRC、SHA256、兼容性、源码交付和时间承诺；
- 联网核验当前闲鱼数字/虚拟商品及退款规则；
- 输出一份干净的 Pilot Listing Candidate；
- 输出最终 `issued_from_human=false` 的 C4 Decision Candidate。

## C. Jovi 需要决定

### 1. Pilot 产品形态

当前 reported：
- version：`0.2.0-dev`
- installer：`UNSIGNED`

请选择：
- Beta/dev/unsigned 小规模 Pilot；
- 或先做 stable/signing。

### 2. Pilot price

当前 `99 CNY` 只是 candidate，不是已验证价格。

### 3. Pilot size/window

推荐：5–10 单或固定时间窗。

### 4. Delivery transport

选择人工交付渠道，并确保 package SHA 可复核。

## D. C4 Human Decision

只有你本人确认最终 Pilot Package 后，才把：

`C4_HUMAN_PILOT_DECISION_CANDIDATE`

签发为：

`issued_from_human=true`

Agent 不得代签。

## E. Pilot 期间你必须手工执行

- 闲鱼发布；
- 买家沟通/商业承诺；
- 改价；
- 付款确认；
- 最终发货/发送链接；
- 退款/争议。

系统只做：
- listing/order candidate；
- payment fact record；
- Entitlement；
- DeliveryReceipt；
- Package/hash；
- support/KPI。

## F. 永远不要交给 Agent/聊天/Git

- Cookie / Browser Profile / Token；
- 买家真实姓名、手机号、地址；
- 完整私聊；
- 银行/支付账号/凭证；
- 密钥/API Key；
- 公司/客户/雇主秘密代码；
- 未授权资源。

## G. Pilot 完成后

核对：
- 0 duplicate Entitlement；
- 0 duplicate Receipt；
- 0 wrong-version delivery；
- 0 unauthorized platform action；
- package/release traceability；
- 人工分钟/单；
- support/refund/未成交原因。

结束：

`C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION`

然后再由你本人决定下一项自动化权限，不一次性开放。
