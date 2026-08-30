# Kill Bill：订阅计费参考

**核验日期：2026-08-30；结论：`REFERENCE_ONLY`。**

## 官方身份与审查锚点

- 官方仓库：[killbill/killbill](https://github.com/killbill/killbill)；官方文档：[docs.killbill.io](https://docs.killbill.io/)。
- 审查锚点：`killbill-0.24.21`；未来任何试验须将 tag 解析为提交并锁定镜像 digest。
- 许可证：Apache-2.0。

## 技术栈与参考范围

Kill Bill 是 Java/JVM 的订阅计费与支付平台，配套多仓库组件、插件和较重的账务/支付域。仅参考其订阅状态、账期、支付 provider 隔离、审计、重试与失败处理思想；不复制源码、SQL、插件、支付配置或管理界面，不部署也不接入任何支付渠道。

## 与本工程的关系

它不是 Medusa 的替代落地项：Medusa 保持主候选，Python oracle 只给出可复算建议，n8n 只编排内部审核，闲鱼适配器依旧独立且人工控制。Kill Bill 不得获得任何真实订单、客户、支付、闲鱼或凭证数据。

## 成本、许可与风险

Java 服务、数据库、插件升级、支付合规、对账和运营告警的成本远超首期 Modbus 数字产品需要。Apache-2.0 要保留 LICENSE/NOTICE 并审计依赖。风险是支付误扣、重试重复扣款、账务不可逆错误、PCI/个人信息范围扩大、插件供应链与管理 API 暴露。

## 升级触发条件

仅当未来有已批准的复杂订阅、跨 provider 对账或账期需求，且 Medusa 模块无法满足时，才进行独立 POC；安全公告、支付插件变化或许可证变化要求重审。POC 必须用合成数据、禁用真实扣款并验证冲正/对账/回滚。

## 结论枚举

1. `REFERENCE_ONLY`；2. `NO_CODE_OR_RUNTIME_REUSE`；3. `NO_PAYMENT_AUTHORITY`；4. `REASSESS_ONLY_AFTER_APPROVED_COMPLEX_SUBSCRIPTIONS`。

## 来源与限制

- [官方仓库](https://github.com/killbill/killbill)、[release](https://github.com/killbill/killbill/releases/tag/killbill-0.24.21)、[LICENSE](https://github.com/killbill/killbill/blob/master/LICENSE)、[官方文档](https://docs.killbill.io/)。
- 不构成支付、税务或 PCI 合规意见，也无真实支付验证。

## 固定栏目核对

- **官方仓库：** `killbill/killbill`；**官方文档：** `docs.killbill.io`；**核验日期：** 2026-08-30。
- **Tag 或 Commit：** `killbill-0.24.21`；**许可证：** Apache-2.0；**技术栈：** Java/JVM、多仓库组件、插件、账务与支付域。
- **可直接复用的模块：** 无；当前不复制代码或运行时。
- **只借鉴的设计：** 订阅状态、账期、provider 隔离、审计、重试和失败处理。
- **明确不采用部分及原因：** 源码、SQL、插件、支付配置与管理界面；首期需求不需要其重型账务/支付范围。
- **与 jovi-automation/Medusa/Python oracle/n8n/闲鱼适配器关系：** `jovi-automation` 保持控制；Medusa 是主候选；Python oracle 仅给建议；n8n 仅内部审核；闲鱼适配器独立且人工控制，Kill Bill 不接触其任何数据。
- **集成成本：** Java、数据库、插件、支付合规和对账；**运行依赖：** JVM、数据库、受审计 payment provider；**许可义务：** 保留 Apache-2.0/NOTICE、审计依赖；**安全风险：** 误扣、重复扣款、不可逆账务、PCI/PII 和管理 API。
- **升级触发条件：** 获批复杂订阅/跨 provider 对账且 Medusa 无法满足，或安全/支付插件/许可变化。
- **固定结论：** `REFERENCE_ONLY`；**来源登记：** 官方仓库、release、LICENSE、docs；**推断：** 其审计/订阅方法有参考价值；**限制：** 未部署、无支付验证；**待复核：** 提交/digest、插件许可、支付/PCI 方案和独立 POC 批准。
