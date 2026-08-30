# Saleor：未选定的架构备选

**核验日期：2026-08-30；结论：`ALTERNATIVE_NOT_SELECTED`。**

## 官方身份与审查锚点

- 官方仓库：[saleor/saleor](https://github.com/saleor/saleor)；官方文档：[docs.saleor.io](https://docs.saleor.io/)。
- 审查锚点：`3.23.29`；若重启评估，先固定 tag、提交、容器 digest 及其 dashboard/storefront 相容版本。
- 许可证：BSD-3-Clause。

## 技术栈、可借鉴与不采用

Saleor Core 是 Python/Django/GraphQL 的 composable headless commerce API，常与 PostgreSQL、Redis、Celery 和 React/TypeScript dashboard 组合。可借鉴 GraphQL schema 演进、app/webhook 隔离、频道/多区域建模与权限设计；不复制 Core、Dashboard、Storefront、插件、示例或支付/发货逻辑，也不部署。

## 与本工程的关系

当前选择 Medusa 作为唯一 Commerce 主候选，以防并行维护两套后台。Python oracle/n8n/闲鱼适配器的隔离边界不变：oracle 不写业务状态，n8n 只做内部审核，闲鱼适配器不共享秘密/数据库且平台操作始终人工完成。Saleor 不加入当前运行图。

## 成本、许可与风险

其 Python/GraphQL/Django/Celery 运维与 Medusa 方案并存会扩大栈和培训成本。BSD-3-Clause 要保留版权/许可与不得用作者名背书；第三方依赖另行审计。风险包括 GraphQL 查询复杂度/授权缺陷、app webhook 签名与重放、后台权限错配、异步任务重复执行和支付/PII 扩张。

## 升级触发条件

只有 Medusa 明确不满足已批准的 GraphQL-first、多频道或扩展需求时才独立比较。届时重新审查版本、部署模型、许可证、CVE 与迁移成本，并用合成数据做授权/查询复杂度/webhook 负测。

## 结论枚举

1. `ALTERNATIVE_NOT_SELECTED`；2. `NO_PARALLEL_BACKEND`；3. `REFERENCE_FOR_GRAPHQL_AND_APP_BOUNDARIES`；4. `NOT_DEPLOYED`。

## 来源与限制

- [官方仓库](https://github.com/saleor/saleor)、[release](https://github.com/saleor/saleor/releases/tag/3.23.29)、[LICENSE](https://github.com/saleor/saleor/blob/main/LICENSE)、[官方文档](https://docs.saleor.io/)。
- 当前不证明 Saleor 在本地可运行，也不授权数据迁移或真实渠道接入。

## 固定栏目核对

- **官方仓库：** `saleor/saleor`；**官方文档：** `docs.saleor.io`；**核验日期：** 2026-08-30。
- **Tag 或 Commit：** `3.23.29`；**许可证：** BSD-3-Clause；**技术栈：** Python、Django、GraphQL、PostgreSQL、Redis、Celery、React/TypeScript Dashboard。
- **可直接复用的模块：** 无；当前不部署、复制或迁移。
- **只借鉴的设计：** GraphQL schema 演进、app/webhook 隔离、频道/多区域和权限模型。
- **明确不采用部分及原因：** Core、Dashboard、Storefront、插件、示例和支付/发货逻辑；避免与 Medusa 并行维护第二个后台。
- **与 jovi-automation/Medusa/Python oracle/n8n/闲鱼适配器关系：** `jovi-automation` 控制选择；Medusa 是唯一主候选；Python oracle 不写业务状态；n8n 只审核；闲鱼适配器独立且人工执行。
- **集成成本：** Python/GraphQL/Django/Celery 栈与培训；**运行依赖：** PostgreSQL、Redis、异步 worker 与 Dashboard；**许可义务：** 保留 BSD-3-Clause 版权/许可且不得背书；**安全风险：** GraphQL 授权/复杂度、webhook 重放、任务重复和 PII。
- **升级触发条件：** Medusa 正式不能满足获批的 GraphQL-first、多频道或扩展需求，或上游安全/许可变化。
- **固定结论：** `ALTERNATIVE_NOT_SELECTED`；**来源登记：** 官方仓库、release、LICENSE、docs；**推断：** 可作为 GraphQL 架构参考；**限制：** 未本地运行、未授权迁移/渠道；**待复核：** tag/commit/digest、依赖、迁移成本和独立需求批准。
