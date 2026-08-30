# Vendure：当前阶段拒绝

**核验日期：2026-08-30；结论：`REJECT_CURRENT_PHASE`。**

## 官方身份与审查锚点

- 官方仓库：[vendurehq/vendure](https://github.com/vendurehq/vendure)；官方文档：[docs.vendure.io](https://docs.vendure.io/)。
- 审查锚点：`v3.7.2`；未来若重新评估，必须锁定 tag、提交与镜像 digest。
- 许可证：社区版 GPLv3；另有 Vendure Commercial License。插件有特定例外，但不改变核心 GPLv3 审查需求。

## 技术栈、借鉴与不采用

Vendure 是 TypeScript/Node.js、GraphQL、NestJS/TypeORM 风格的 headless commerce 平台，具插件和 channel 能力。仅借鉴插件接口、channel 权限隔离和 schema 变更治理；当前不复制、不链接、不部署核心或官方插件，也不使用商业许可。

## 与本工程的关系

Medusa 已是唯一主候选；引入 Vendure 会形成第二套 Commerce 后台。Python oracle、n8n 和闲鱼适配器的最小权限与人工平台控制边界完全不因 Vendure 而改变；Vendure 不得接触订单、支付、客户、Cookie、Token 或闲鱼数据。

## 成本、许可与风险

除 GraphQL/Node/PostgreSQL/插件运维外，GPLv3 对分发、修改、组合和交付边界需要法务审查；商业许可证则增加采购/合同成本。风险为错误理解 GPL/插件例外、GraphQL/RBAC 缺陷、插件供应链、升级破坏性变更和重复建设。

## 升级触发条件

仅当获得明确法务许可、商业许可预算或开源发布策略，并且 Medusa 被正式否决时，才重开评估。需完成 license compatibility、SBOM、源码/镜像来源、权限/多 channel 负测和回滚验证。

## 结论枚举

1. `REJECT_CURRENT_PHASE`；2. `GPLV3_REQUIRES_SEPARATE_LEGAL_REVIEW`；3. `NO_RUNTIME_OR_CODE_REUSE`；4. `NO_SECOND_BACKEND`。

## 来源与限制

- [官方仓库](https://github.com/vendurehq/vendure)、[v3.7.2 release](https://github.com/vendurehq/vendure/releases/tag/v3.7.2)、[LICENSE](https://github.com/vendurehq/vendure/blob/master/LICENSE.md)、[插件许可说明](https://docs.vendure.io/current/core/how-to/publish-plugin)。
- 本结论是当前工程决策，不是对 GPLv3/商业许可证的法律意见。

## 固定栏目核对

- **官方仓库：** `vendurehq/vendure`；**官方文档：** `docs.vendure.io`；**核验日期：** 2026-08-30。
- **Tag 或 Commit：** `v3.7.2`；**许可证：** 社区版 GPLv3，或另行商业许可；**技术栈：** TypeScript、Node.js、GraphQL、NestJS/TypeORM、插件与 channel。
- **可直接复用的模块：** 无；当前禁止 runtime 或代码复用。
- **只借鉴的设计：** 插件接口、channel 权限隔离和 schema 变更治理。
- **明确不采用部分及原因：** 核心、官方插件和商业许可；GPLv3/合同边界与第二后台成本不适合当前阶段。
- **与 jovi-automation/Medusa/Python oracle/n8n/闲鱼适配器关系：** `jovi-automation` 保持 Gate；Medusa 是主候选；Python oracle 和 n8n 不取得 Commerce/平台权限；闲鱼适配器独立、秘密不共享；Vendure 不在运行图。
- **集成成本：** Node/GraphQL/PostgreSQL/插件与法务/采购；**运行依赖：** Node 服务、数据库、插件治理；**许可义务：** GPLv3/商业条款须独立确认；**安全风险：** 许可误用、GraphQL/RBAC、插件供应链和升级破坏。
- **升级触发条件：** 法务/商业许可路径明确、Medusa 被否决、兼容性/SBOM/权限负测通过，或上游安全/许可变化。
- **固定结论：** `REJECT_CURRENT_PHASE`；**来源登记：** 官方仓库、release、LICENSE、插件许可 docs；**推断：** 设计可参考但复用风险高；**限制：** 未部署、无商业/法务批准；**待复核：** 许可兼容性、commit/digest、插件例外和正式替代决定。
