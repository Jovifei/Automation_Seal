# Lago：当前阶段拒绝

**核验日期：2026-08-30；结论：`REJECT_CURRENT_PHASE`。**

## 官方身份与审查锚点

- 官方仓库：[getlago/lago](https://github.com/getlago/lago)；官方文档：[doc.getlago.com](https://doc.getlago.com/)。
- 审查锚点：`v1.52.1`；未来试点前必须锁定 tag/commit、镜像 digest 与全套部署依赖。
- 许可证：AGPL-3.0-only（以仓库 LICENSE 为准）。

## 技术栈、借鉴与不采用

Lago 面向 usage-based billing，项目跨 Ruby/Rails、Go、React、PostgreSQL、ClickHouse、消息/后台任务与 OpenAPI/SDK。可借鉴事件账本、价格版本、计费预览和可观测性思路；不采用源码、Docker Compose、分析/跟踪默认设置、发票/支付模块、客户门户或 SDK。

## 与本工程的关系

当前没有获批的按量产品，所以它既不替代 Medusa，也不与 OpenMeter 并行部署。Python oracle 不能直接生成可收费用量；n8n 不得把计量/发票失败当成可自动重试的外部副作用；闲鱼适配器不与 Lago 交换数据或凭证。

## 成本、许可与风险

AGPLv3 对网络交互软件的源码提供义务及组合边界有重大影响，需独立法务确认。技术成本包括多服务基础设施、事件一致性、价格/税务/发票治理、PII 留存和运营告警。风险含误账、事件重放、租户泄露、服务链复杂度、默认遥测及许可不合规。

## 升级触发条件

只有按量产品、账单归属、争议处理、合规责任和 AGPL 方案均获批准时才重审；安全公告、许可证变化、计量架构变化也需触发复核。须先在合成数据环境验证乱序/重复事件、账单可复算、权限、备份恢复与停用回滚。

## 结论枚举

1. `REJECT_CURRENT_PHASE`；2. `AGPLV3_SEPARATE_LEGAL_GATE`；3. `NO_METERING_OR_BILLING_RUNTIME`；4. `NO_XIANYU_INTEGRATION`。

## 来源与限制

- [官方仓库](https://github.com/getlago/lago)、[release](https://github.com/getlago/lago/releases/tag/v1.52.1)、[LICENSE](https://github.com/getlago/lago/blob/main/LICENSE)、[官方文档](https://doc.getlago.com/)。
- 未核验本地部署、真实计费或任何外部支付服务。

## 固定栏目核对

- **官方仓库：** `getlago/lago`；**官方文档：** `doc.getlago.com`；**核验日期：** 2026-08-30。
- **Tag 或 Commit：** `v1.52.1`；**许可证：** AGPL-3.0-only；**技术栈：** Ruby/Rails、Go、React、PostgreSQL、ClickHouse、消息/后台任务、OpenAPI/SDK。
- **可直接复用的模块：** 无；不部署计量/计费 runtime。
- **只借鉴的设计：** 事件账本、价格版本、计费预览和可观测性。
- **明确不采用部分及原因：** 源码、Compose、默认跟踪、发票/支付、客户门户和 SDK；没有获批按量产品且 AGPL/多服务负担过宽。
- **与 jovi-automation/Medusa/Python oracle/n8n/闲鱼适配器关系：** `jovi-automation` 管控未来审查；Medusa 不被替换；Python oracle 不生成收费真相；n8n 不自动重试外部计费副作用；闲鱼适配器不交换数据/凭证。
- **集成成本：** 多服务、事件一致性、价格/税务/发票和数据治理；**运行依赖：** PostgreSQL、ClickHouse、后台/消息服务；**许可义务：** AGPL 网络交互源码义务及依赖审查；**安全风险：** 误账、重放、租户泄露、遥测和许可不合规。
- **升级触发条件：** 按量产品、账单归属、AGPL 方案和合规责任均获批，或安全/许可证/架构变化。
- **固定结论：** `REJECT_CURRENT_PHASE`；**来源登记：** 官方仓库、release、LICENSE、docs；**推断：** 可作计费设计参考；**限制：** 未部署、未核验真实计费；**待复核：** commit/digest、AGPL 方案、事件负测和合规/业务批准。
