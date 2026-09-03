# C4 Human Pilot 计划 V1

## 目标

在不开放自动真实平台权限的前提下，用真实用户/订单验证：商品描述、付款确认、版本交付、售后与审计链是否可用。

## 前置 Gate

必须存在 `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`。

## Pilot 范围

建议首轮 5–10 个订单；不足 5 个时可按固定时间窗结束，但必须记录未成交原因。

## 人工控制矩阵

| 动作 | 执行者 |
|---|---|
| 闲鱼发布 | Jovi |
| 改价 | Jovi |
| 关键回复/承诺 | Jovi |
| 付款确认 | Jovi |
| 最终点击/发送交付 | Jovi |
| 退款/争议 | Jovi |
| listing/reply/delivery candidate | 系统 |
| package/hash/entitlement/receipt 准备 | 系统 |

## 每单必须记录

- pilot_order_id
- platform_reference（脱敏）
- product/release/version
- listing candidate SHA
- human publish confirmation
- human payment confirmation + evidence SHA
- Entitlement ID
- DeliveryPackage SHA
- DeliveryReceipt ID
- human delivery confirmation
- support events
- refund/dispute state

## 禁止

- 自动读取/写入闲鱼 Cookie/Token/浏览器 Profile
- 自动发布、自动私信、自动改价
- 自动确认付款
- 自动退款
- 无人审核交付

## Pilot 指标

- inquiry→order conversion（仅观察）
- package preparation success rate
- duplicate entitlement/receipt count
- wrong-version delivery count
- delivery preparation latency
- human correction count
- support issue types
- refund/dispute count

## Exit Criteria

通过至少要求：

1. 0 duplicate Entitlement/Receipt；
2. 0 wrong-version delivery；
3. 0 unauthorized platform action；
4. 每单 package SHA 可回溯到 release；
5. 人工付款证据可回溯到 order；
6. 所有失败都有可重复的 recovery/rollback；
7. Jovi 认为人工负担已足以判断下一项可自动化权限。

通过状态：`C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION`。

Pilot PASS 也不自动开放新权限；下一阶段必须由 Jovi 单独决定每项 permission expansion。