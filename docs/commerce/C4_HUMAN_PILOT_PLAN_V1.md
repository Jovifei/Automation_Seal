# C4 Human Pilot 计划 V1

## 目标

在不开放自动真实平台权限的前提下，用真实用户/订单验证：商品描述、付款确认、版本交付、售后与审计链是否可用。

## 前置 Gate

必须全部存在并重新核验：

- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`
- `C3_RUNTIME_PROMOTION_AUDIT_PASS`
- Jovi 单独签发的 `C4_HUMAN_PILOT_DECISION`
- C4 privacy/data-minimization 规则已确认
- Commerce Runtime 正式 pilot candidate 版本可回滚
- 六个自动真实动作权限仍未被自动放开

不得直接从未提升的临时 C3 feature branch 开始 Pilot。

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
- platform_reference（仅脱敏/哈希化引用，不默认保存原始客户账号）
- product/release/version
- listing candidate SHA
- human publish confirmation
- human payment confirmation + sanitized evidence SHA
- Entitlement ID
- DeliveryPackage SHA
- DeliveryReceipt ID
- human delivery confirmation
- support events（优先结构化分类，避免整段私聊复制）
- refund/dispute state

数据最小化遵守：

`docs/commerce/C4_PILOT_PRIVACY_MINIMIZATION_V1.md`

初始 Pilot 默认保持 `real_customer=false`：Runtime 不创建原始客户资料档案，仅使用伪名化 pilot order / platform reference；如未来要持久化真实客户身份/PII，必须单独 Jovi Decision。

## 禁止

- 自动读取/写入闲鱼 Cookie/Token/浏览器 Profile
- 自动发布、自动私信、自动改价
- 自动确认付款
- 自动退款
- 无人审核交付
- 将未脱敏客户截图/聊天记录默认导入 Runtime
- 因 Pilot 通过而自动翻转任何真实权限

## Pilot 指标

- inquiry→order conversion（仅观察）
- package preparation success rate
- duplicate entitlement/receipt count
- wrong-version delivery count
- delivery preparation latency
- human correction count
- support issue types
- refund/dispute count
- privacy/redaction correction count
- unauthorized platform action count

## Exit Criteria

通过至少要求：

1. 0 duplicate Entitlement/Receipt；
2. 0 wrong-version delivery；
3. 0 unauthorized platform action；
4. 每单 package SHA 可回溯到 release；
5. 人工付款证据可回溯到 order；
6. 所有失败都有可重复的 recovery/rollback；
7. 无未经授权的原始客户 PII / 平台凭据进入 Runtime；
8. Jovi 认为人工负担已足以判断下一项可自动化权限。

通过状态：`C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION`。

Pilot PASS 也不自动开放新权限；下一阶段必须由 Jovi 单独决定每项 permission expansion。
