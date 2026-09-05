# 当前需要 Jovi 决定的事项

**最后校准：2026-09-05**

旧 Track P/I、X3/X4 决策已经不是当前主线。当前唯一关键 Human Gate 是 **C4 Human Pilot**。

## 1. C4 前必须由 Jovi 决定

### Pilot 产品形态

当前 reported：
- SKU：Modbus RTU Diagnostic Toolkit
- version：`0.2.0-dev`
- installer：`UNSIGNED`

选择：
- `BETA_PILOT`：透明以 dev/unsigned 小规模试卖；
- `STABLE_FIRST`：先返回产品仓做 stable/signing/release notes，再重新资格化。

### Pilot 价格

当前仅有 candidate：`99.00 CNY`。

Jovi 必须确认最终 Pilot price；该数字不是已经验证的市场价格。

### Pilot 规模

建议：
- 5–10 单，或
- 明确固定时间窗。

### 人工交付通道

选择一个真实人工传输方式：
- 受控下载链接；
- 网盘；
- 其他人工方式。

必须保持 package bytes/SHA 可追溯，并明确链接撤销/到期方式。

### C4 Human Pilot Decision

最终 Decision 必须由 Jovi 本人签发：

`issued_from_human=true`

并绑定：
- C3 audit SHA；
- Runtime main；
- product/version；
- final listing SHA；
- package SHA；
- price；
- pilot size/window；
- human-only action matrix；
- privacy rules。

## 2. 当前真实平台动作仍由 Jovi 决定/执行

即使 C4 获批：
- 闲鱼发布；
- 消息/商业承诺；
- 改价；
- 付款确认；
- 最终发货；
- 退款/争议。

系统不能自动继承这些权限。

## 3. Pilot 后再决定

C4 完成后，Jovi 再基于真实数据逐项决定：
- listing 自动化；
- reply suggestion；
- order metadata helper；
- delivery preparation；
- 是否需要有限自动交付或其他平台动作。

每项独立 Decision，不一次性开放。

## 4. 尚需事实核验，不是“拍脑袋决定”

- 当前闲鱼数字/虚拟商品规则；
- 当前退款/争议规则；
- final C4 listing claim evidence；
- Runtime dedicated Git remote / public-private；
- branch protection；
- 当前商品 package 实际客户可见内容。

这些应先核验，再由 Jovi 做决定。
