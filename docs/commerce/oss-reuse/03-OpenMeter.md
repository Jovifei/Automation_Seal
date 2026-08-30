# OpenMeter：未来按量计费触发项

**核验日期：2026-08-30；结论：`FUTURE_TRIGGER_METERED_PRODUCTS`。**

## 官方身份与审查锚点

- 官方仓库：[openmeterio/openmeter](https://github.com/openmeterio/openmeter)；官方文档：[openmeter.io/docs](https://openmeter.io/docs)。
- 审查锚点：`v1.0.0-beta.232`；实际试点前须锁定 tag 解析提交、容器 digest 与依赖 SBOM。
- 许可证：Apache-2.0。

## 技术栈、候选复用与不采用范围

OpenMeter 以 Go 构建，官方架构使用 PostgreSQL/Ent 保存计费与产品数据、ClickHouse 作实时聚合、Kafka 作事件流，API-first（TypeSpec/OpenAPI）并接收 CloudEvents。可借鉴不可篡改的计量事件、聚合器和配额/entitlement 分层。当前不安装、不接入；只有获批产品确实按 API/AI/服务用量收费时，才可重新立项。不得将其 beta 状态当作生产资格。

不采用其完整计费、发票、订阅、客户门户、支付连接器或高容量基础设施；更不能以伪造事件、估算 token 或 LLM 文本生成应收金额。

## 与本工程的关系

Medusa 仍是 Commerce 主候选，OpenMeter 只能在未来提供独立的用量事件层；Python oracle 可以产出算法结果但必须有稳定 schema、输入摘要、时间与来源，不能直接作为计费真相；n8n 可投递经签名并去重的内部审核事件；闲鱼适配器不产生或消费 OpenMeter 计量事件。

## 集成成本、许可义务与安全风险

成本很高：Kafka/ClickHouse/PostgreSQL 运维、事件 schema 演进、时钟/去重、对账、数据保留、GDPR/PII 分级与支付/税务边界。Apache-2.0 要保留许可/NOTICE，并对依赖履行各自义务。风险包括事件伪造/重放、重复收费、迟到事件、租户隔离错误、usage 泄露、指标高基数和 Kafka/ClickHouse 运营复杂度。

## 升级/启用触发条件

只有“获批的按量产品 + 明确计量定义 + 数据留存/争议处理 + 账单对账方案 + 独立安全评审”同时存在时才触发选型；安全公告、beta 转 GA 或架构/许可证变化触发版本重审。任何启用前需模拟事件、重复/乱序/重放负测、账单可复算验证和回滚演练。

## 结论枚举

1. `FUTURE_TRIGGER_METERED_PRODUCTS`；2. `NOT_DEPLOYED`；3. `BETA_REQUIRES_REQUALIFICATION`；4. `NO_BILLING_SOURCE_OF_TRUTH_YET`。

## 来源与限制

- [官方仓库/架构/许可证](https://github.com/openmeterio/openmeter)、[releases](https://github.com/openmeterio/openmeter/releases/tag/v1.0.0-beta.232)、[官方文档](https://openmeter.io/docs)。
- 未做真实吞吐、支付、合规或生产环境验证；不得把未来选项解释为当前收费能力。

## 固定栏目核对

- **官方仓库：** `openmeterio/openmeter`；**官方文档：** `openmeter.io/docs`；**核验日期：** 2026-08-30。
- **Tag 或 Commit：** `v1.0.0-beta.232`；**许可证：** Apache-2.0；**技术栈：** Go、PostgreSQL/Ent、ClickHouse、Kafka、TypeSpec/OpenAPI、CloudEvents。
- **可直接复用的模块：** 当前无运行时直接复用；未来仅评估计量事件、聚合和配额边界。
- **只借鉴的设计：** 不可篡改事件、聚合器与 entitlement 分层。
- **明确不采用部分及原因：** 完整计费、发票、订阅、客户门户、支付连接器和高容量基建；当前没有按量产品且 beta/运维风险过高。
- **与 jovi-automation/Medusa/Python oracle/n8n/闲鱼适配器关系：** `jovi-automation` 控制未来选型；Medusa 仍为主候选；Python oracle 不是计费真相；n8n 仅投递已验证内部审核事件；闲鱼适配器不产生/消费计量事件。
- **集成成本：** Kafka/ClickHouse/PostgreSQL、对账与数据治理；**运行依赖：** 三类数据服务、事件 schema 和监控；**许可义务：** 保留 Apache-2.0/NOTICE 并审计依赖；**安全风险：** 事件伪造/重放、重复收费、租户泄露与高基数。
- **升级触发条件：** 获批按量产品、明确计量/争议/对账方案和独立安全审查，或 beta/许可证/架构变化。
- **固定结论：** `FUTURE_TRIGGER_METERED_PRODUCTS`；**来源登记：** 官方仓库、release 和 docs；**推断：** 适合未来独立用量层；**限制：** 未部署、未进行真实吞吐/支付验证；**待复核：** GA 状态、commit/digest、事件负测和合规方案。
