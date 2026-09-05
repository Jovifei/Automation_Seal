# C4 快速商业验证与 Codex 定时任务

**最后校准：2026-09-05**  
**说明：文件名保留“14天快速落地”仅为了兼容旧引用；原 Track P/I 14 天 Alpha 计划已经完成/失效。当前用途是首个真实 SKU 的 C4 快速商业验证。**

## 1. 当前目标

在不开放自动真实平台权限的前提下，用最短路径回答：

1. 真实用户是否愿意为 Modbus RTU Diagnostic Toolkit 付费；
2. 当前商品文案是否准确匹配需求；
3. `0.2.0-dev` / unsigned 交付是否可接受；
4. 每单人工沟通与交付成本是多少；
5. 售后/退款的主要原因是什么；
6. 下一项最值得自动化的动作是什么。

技术底座 C2/C3 已完成，不再用时间建设新的 Commerce framework。

## 2. 当前最快执行节奏

### Step 1 — Pre-Publish QA

优先完成：
- Governance PR #5 / CI / main 状态复核；
- C3 mirror 文本清理；
- C4 Pilot ledger 清空真实样式示例；
- 本地 C3 claim evidence -> C4 listing claim review；
- CRC/SHA256/兼容性/源码交付文案修正；
- 当前闲鱼数字商品、退款、售后规则刷新；
- 选择 beta/dev/unsigned Pilot 或 stable-first。

### Step 2 — Pilot Package Freeze

冻结：
- final Listing Candidate SHA；
- SKU/version；
- DeliveryPackage SHA；
- pilot price；
- 试点规模/时间窗；
- 人工交付通道；
- privacy ledger；
- rollback/stop checklist。

### Step 3 — Jovi Human Decision

只有 Jovi 将 C4 Decision 明确签发为 `issued_from_human=true`，才进入真实 Pilot。

### Step 4 — 真实人工 Pilot

建议目标：5–10 单，或预先定义固定时间窗。

所有平台动作仍人工：
- publish；
- message；
- price；
- payment confirmation；
- delivery；
- refund/dispute。

系统负责：
- candidate；
- order/payment fact record；
- Entitlement；
- Receipt；
- Package SHA；
- support 分类；
- KPI 汇总。

### Step 5 — 复盘

输出：
- inquiries；
- paid orders；
- conversion；
- average manual minutes/order；
- package preparation success；
- support categories；
- refunds/disputes；
- wrong-version / duplicate / unauthorized-action count；
- 未成交原因。

## 3. 当前不建议固定“必须 14 天”

旧文档的 14 天节奏是 Alpha 阶段估算。C4 以**证据数量或固定窗口**为准：

- 推荐 5–10 个真实订单；
- 如果订单不足，可在预先设定的时间窗后用询盘/未成交数据复盘；
- 不为凑订单而降价、夸大文案或自动化高风险动作。

## 4. Codex 定时任务当前允许范围

适合：
- 本地 Runtime/product tests；
- docs/claim consistency；
- Gitleaks/Syft；
- package SHA/integrity；
- GitHub PR/CI 状态摘要；
- 生成待审核 KPI/报告。

不适合：
- 自动登录闲鱼；
- 自动读取 Cookie/Profile；
- 自动回复真实买家；
- 自动付款确认；
- 自动发货/改价/退款；
- 自动签 Human Decision。

## 5. 建议的非阻断定时任务

| 任务 | 频率 | 目的 |
|---|---|---|
| Runtime regression | 每日或代码变化后 | 防止 C3 能力漂移 |
| Product artifact SHA | 每次 Pilot 批次开始前 | 确保交付版本正确 |
| Gitleaks | 每日/提交后 | 防秘密泄漏 |
| Docs claim consistency | 每次 listing 变化后 | 防营销超出 evidence |
| Pilot KPI draft | 每日或每 1–2 单 | 只生成复盘草稿 |

所有定时结果只生成内部报告，不触发外部平台动作。

## 6. 当前成功标准

C4 成功不是“无人值守运行 14 天”，而是：

- 0 duplicate Entitlement/Receipt；
- 0 wrong-version delivery；
- 0 unauthorized platform action；
- package/release traceability 100%；
- 真实市场反馈足够判断产品/价格/售后；
- 人工负担可量化；
- Jovi 能基于数据选择下一项 permission expansion。

完成状态：

`C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION`
