# Lemon Squeezy：当前阶段拒绝

**核验日期：2026-08-30；结论：`REJECT_CURRENT_PHASE`。**

## 官方身份与审查锚点

- 官方文档：[Lemon Squeezy Developer Guide](https://docs.lemonsqueezy.com/guides/developer-guide) 与 [API Reference](https://docs.lemonsqueezy.com/api)。
- 审查锚点：HTTPS JSON:API `v1`（`https://api.lemonsqueezy.com/v1/`）。这是 SaaS API 版本，不是可本地复用的 OSS 仓库/提交。
- 许可证：不适用 OSS 许可证；服务受其当前服务条款、商户/支付地区资格及 API 条款约束，接入前必须取得业务/法务/平台批准。

## 技术栈、借鉴与不采用

该服务提供托管 checkout、订单、订阅、webhook、软件许可 key 等 HTTP/JSON:API 能力。仅借鉴其 API 版本化、webhook 同步与测试/生产环境区分；当前不注册账户、不保存 API key、不调 API、不创建 checkout、产品、订单、订阅或 license key，更不把它伪装为 OSS 组件。

## 与本工程的关系

Medusa 是被审查的自托管 Commerce 主候选，但不能由此自动接入 Lemon Squeezy。Python oracle 只做本地可复算判定，不处理支付；n8n 不持有 bearer key、不自动消费付款成功事件；闲鱼适配器完全独立，真实发布、客服、交付、退款和平台验证继续由 Jovi 手工控制。

## 集成成本、服务义务与安全风险

成本包括商户资格、地区/税务/退款政策、客户支持、webhook 基础设施、数据处理协议、API 生命周期与对账。需要遵守服务条款、API 限流和数据安全要求，而非 OSS 转载义务。风险包括 API key 泄露、webhook 伪造/重放、test/live 混用、订单状态竞态、付款/退款误操作、客户 PII 外泄和外部服务可用性/政策变化。

## 升级/启用触发条件

只有平台准入、法务/税务/隐私审查、业务负责人批准、明确人工例外流程和签名 webhook 设计齐备后，才可以单独提出接入。API 新 major、官方弃用通知、条款/地区政策变化、安全公告或支付争议触发复核。启用前以官方 test mode 做签名、幂等、重放、失败回调、对账和密钥轮换演练。

## 结论枚举

1. `REJECT_CURRENT_PHASE`；2. `EXTERNAL_SAAS_NOT_OSS_REUSE`；3. `NO_ACCOUNT_KEY_OR_CHECKOUT_CREATED`；4. `NO_AUTOMATED_PAYMENT_OR_XIANYU_ACTION`。

## 来源与限制

- [官方 API 概览/版本化](https://docs.lemonsqueezy.com/api)、[请求与认证](https://docs.lemonsqueezy.com/api/getting-started/requests)、[开发者入门](https://docs.lemonsqueezy.com/guides/developer-guide/getting-started)。
- 本文不是第三方服务准入或法规合规证明，且没有对外发送任何请求或保存任何凭证。

## 固定栏目核对

- **官方仓库：** 无，Lemon Squeezy 是外部 SaaS；**官方文档：** `docs.lemonsqueezy.com`；**核验日期：** 2026-08-30。
- **Tag 或 Commit：** HTTPS JSON:API `v1`；**许可证：** 不适用 OSS 许可证，受服务/API 条款约束；**技术栈：** 托管 checkout、订单、订阅、webhook、license key 的 HTTPS/JSON:API。
- **可直接复用的模块：** 无；当前不注册账户、不调 API、不创建 checkout/订单/订阅/许可证。
- **只借鉴的设计：** API 版本化、webhook 同步、test/live 环境区分。
- **明确不采用部分及原因：** 全部 SaaS 接入、API key、支付与许可操作；尚无商户、法务、税务、隐私和业务批准，且它不是 OSS 复用对象。
- **与 jovi-automation/Medusa/Python oracle/n8n/闲鱼适配器关系：** `jovi-automation` 保持外部准入 Gate；Medusa 不自动接入；Python oracle 不处理支付；n8n 不持 bearer key/消费付款事件；闲鱼适配器独立且 Jovi 手工执行平台动作。
- **集成成本：** 商户资格、税务/退款、客户支持、webhook、数据处理和对账；**运行依赖：** SaaS 账户、HTTPS API、签名 webhook、密钥轮换；**许可义务：** 遵守服务/API 条款而非 OSS 转载义务；**安全风险：** key 泄露、伪造/重放、test/live 混用、PII、外部可用性和政策变化。
- **升级触发条件：** 商户准入、法务/税务/隐私审查、负责人批准、签名 webhook 设计齐备，或 API major/条款/地区政策/安全变化。
- **固定结论：** `REJECT_CURRENT_PHASE`；**来源登记：** 官方 Developer Guide、API、认证文档；**推断：** API 设计仅有借鉴价值；**限制：** 未对外请求、无账号/凭证/平台验证；**待复核：** 当前条款、资格、测试模式、webhook 签名和独立接入批准。
