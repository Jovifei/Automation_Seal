# C4 快速落地路线

**最后校准：2026-09-05**

旧“14 天 Alpha / Track P-I”路线已经完成/失效。当前最快落地路径不是继续开发基础设施，而是把已经通过 C3 独立审核的第一真实 SKU 安全推进到 C4 Human Pilot。

## 目标

用 5–10 个真实、人工控制订单或固定时间窗回答：
- 是否有人愿意付费；
- 哪些功能/文案真正驱动购买；
- 99 CNY 是否合适；
- `0.2.0-dev` / unsigned 是否影响转化；
- 每单人工沟通/交付耗时；
- support/refund/未成交原因；
- 下一项最值得自动化的动作。

## Step 1 — Pre-Publish QA

- 核 Governance PR #5 / CI / main；
- 核 Runtime C3 audit/promotion 原件；
- 核 Product HEAD / package SHA；
- 清 Pilot ledger 示例；
- 逐条 claim -> C3 evidence；
- 修 CRC / SHA256 / compatibility / source-delivery wording；
- 刷新当前闲鱼数字商品与退款规则；
- Jovi 选择 beta/dev/unsigned Pilot 或 stable-first。

## Step 2 — Pilot Package Freeze

冻结：
- final Listing Candidate SHA；
- SKU/version；
- DeliveryPackage SHA；
- price；
- pilot size/time window；
- human-only matrix；
- privacy ledger；
- delivery transport；
- stop/rollback checklist。

## Step 3 — Jovi Human Decision

只有 `issued_from_human=true` 才进入真实 Pilot。

## Step 4 — Human Pilot

Jovi 手工：publish / message / price / payment confirmation / final delivery / refund-dispute。

系统：order/payment fact / Entitlement / Receipt / Package/hash / support/KPI。

## Step 5 — 复盘

退出条件：
- duplicate Entitlement=0；
- duplicate Receipt=0；
- wrong-version=0；
- unauthorized action=0；
- package traceability=100%；
- 人工分钟/单、support、refund/未成交原因可量化。

结束：

`C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION`

## 当前不做

不重选 Commerce framework，不重做 C2/C3，不提前做 Storefront/S3/n8n production/CRM/多渠道自动化，不自动操作闲鱼。
