# Medusa v2：主复用候选

**核验日期：2026-08-30；结论：`DIRECT_REUSE_PRIMARY`。**

## 官方身份与审查锚点

- 官方仓库：[medusajs/medusa](https://github.com/medusajs/medusa)；官方文档：[docs.medusajs.com](https://docs.medusajs.com/)。
- 固定核心锚点：`v2.19.0` / `87d77fa1b56ec287aa6655aaa2f54245387aa2f2`。实际采用时必须校验 tag 到该提交的指向、签名（如有）、发布说明和容器 digest。
- 示例锚点：`medusajs/medusa` examples commit `aae76657952903750dfcaaaf28b6746f20ab1af5`。若该示例树未给出明确且适用的许可证，**只能阅读和抽象设计，不得复制代码、素材、配置或品牌资产**。
- 核心仓库许可证：MIT；仍必须分别清点 npm/镜像依赖与各示例的许可证/NOTICE。

## 技术栈与直接复用

Medusa v2 是 TypeScript/Node.js 的模块化、headless commerce 平台，核心由 Modules、Workflows、REST/Admin/Store API、事件/订阅与可替换 provider 组成。可直接复用的候选仅限：商品、库存、订单、区域/价格、支付与履约的领域边界，工作流/事件的幂等编排模式，以及官方 API/模块扩展点。选择它是为了避免另造第二个 Commerce 后台，而不是把现有闲鱼工程迁入或替换。

## 借鉴但不采用

借鉴其模块化领域模型、provider 隔离、工作流补偿与 API schema 方法；不采用未经批准的 starter、云服务、分析遥测、第三方支付/履约 provider、前端模板、示例数据或任何自动化平台操作。当前不允许创建真实商品、订单、支付、履约或客户数据。

## 与本工程的关系

- `jovi-automation` 保存规格、批准、清单、测试与证据；Medusa 不得绕过其 Gate、清单或审查队列。
- Python oracle 只能为 Medusa 的候选决策提供带版本和输入摘要的确定性结果；不得由 LLM 文本直接写价格、订单或履约状态。
- n8n 只能消费已签名/验证的内部事件并生成审核任务；不持有 Commerce 超级权限，不作为真实支付或发货的唯一裁决者。
- 闲鱼适配器独立运行；仅可交换人工批准、无秘密的候选文件。不得直连 SQLite、Cookie、浏览器 profile、Token 或人机验证流程。

## 集成成本、许可义务与安全风险

成本为 Node/TypeScript 运维、PostgreSQL/缓存/对象存储/邮件或支付 provider 的明确选择、迁移、RBAC、审计、备份恢复和接口契约测试。MIT 允许复用和修改，但分发时应保留版权/许可文本，并完成依赖 NOTICE/SBOM 审计。主要风险是管理 API 暴露、错误的 CORS/会话/密钥管理、webhook 伪造或重放、provider 权限过大、迁移不兼容、库存/价格竞争和第三方扩展供应链。

## 升级触发条件

仅在安全公告、`v2.19.0` 依赖 CVE、官方迁移/破坏性变更、支付/履约 provider 变更、Node/PostgreSQL 兼容性变化或批准的新能力需求出现时评估升级。升级前须在隔离环境锁定新 tag+commit+digest，生成 SBOM，跑迁移/回滚、API 契约、幂等与 webhook 负测；无这些证据不得升级。

## 结论枚举

1. `DIRECT_REUSE_PRIMARY`：Medusa v2 核心可作为后续获批 Commerce 主候选。
2. `NOT_DEPLOYED`：本文件不表示已经安装、运行或接入支付/履约。
3. `EXAMPLES_REFERENCE_ONLY_UNLESS_LICENSE_CONFIRMED`：固定示例提交不可直接复制。
4. `XIANUYU_ADAPTER_ISOLATED`：不复制其后台、不接管其秘密、不自动执行平台行为。

## 来源与限制

- [官方仓库](https://github.com/medusajs/medusa)、[v2.19.0 release](https://github.com/medusajs/medusa/releases/tag/v2.19.0)、[核心 LICENSE](https://github.com/medusajs/medusa/blob/v2.19.0/LICENSE)、[官方示例索引](https://docs.medusajs.com/resources/examples)。
- 这是 2026-08-30 的文档审查，不是对生产就绪、支付合规、地区税务、个人信息合规或上游示例许可证的法律意见。部署时重新核验全部上游材料。

## 固定栏目核对

- **官方仓库：** `medusajs/medusa`；**官方文档：** `docs.medusajs.com`；**核验日期：** 2026-08-30。
- **Tag 或 Commit：** `v2.19.0` / `87d77fa1b56ec287aa6655aaa2f54245387aa2f2`；examples `aae76657952903750dfcaaaf28b6746f20ab1af5`；**许可证：** 核心 MIT，示例许可证待单独确认；**技术栈：** TypeScript、Node.js、Modules、Workflows、REST API。
- **可直接复用的模块：** 已批准后的商品、库存、订单、价格领域边界、官方 API/模块扩展点与幂等工作流模式。
- **只借鉴的设计：** provider 隔离、补偿工作流和 schema 演进。
- **明确不采用部分及原因：** 未批准 starter、云服务、遥测、第三方支付/履约 provider、模板与示例资产；避免未经授权的外部副作用和许可证/权利风险。
- **与 jovi-automation/Medusa/Python oracle/n8n/闲鱼适配器关系：** `jovi-automation` 管控证据；Medusa 是主候选；Python oracle 只给可复算输入；n8n 只建内部审核项；闲鱼适配器独立且仅人工批准文件交换。
- **集成成本：** Node/TypeScript、迁移、RBAC、审计和契约测试；**运行依赖：** PostgreSQL、缓存/对象存储及按需 provider；**许可义务：** 保留 MIT/NOTICE 并审计依赖；**安全风险：** 管理 API、CORS/会话、webhook 重放、provider 权限和供应链。
- **升级触发条件：** CVE、破坏性迁移、provider 或 Node/PostgreSQL 兼容性变化，或获批新需求。
- **固定结论：** `DIRECT_REUSE_PRIMARY`；**来源登记：** 本文“来源与限制”中的官方仓库、release、LICENSE、示例索引；**推断：** 其模块边界可减少重复后台建设；**限制：** 未部署、未验证支付/履约；**待复核：** tag 指向、digest、SBOM、SECURITY、examples 许可证和 Gate。
