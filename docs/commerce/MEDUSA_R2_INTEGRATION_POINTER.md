# Medusa R2 集成指针

**日期：** 2026-09-01
**状态：** `MEDUSA_SPIKE_PASS_WITH_GAPS`（R2-R1 独立审阅 R2；尚未生产采用）
**生产集成：** `production_integration_allowed=false`

本文件说明“开源复用已吸收”与“正式代码导入”之间的边界，供后续 agent 接力使用。它不是 Approval、Decision、部署许可或独立审核结论。

## 已吸收的能力

- Medusa `v2.19.0`：Product/Variant、Order、PaymentCollection、Workflow、官方 Redis Workflow Engine/locking 和 Admin 领域边界。
- Python oracle：只作为 synthetic X2 的确定性对照，不成为 Medusa 运行依赖。
- R2 薄适配层：真实 fixture allowlist、资产/权利/付款证据绑定、精确 CNY 金额、事务化 Entitlement/Receipt、确定性本地包和 `READY_FOR_HUMAN_DELIVERY` 语义。
- n8n：只保留未来 Track I 的内部审核、通知、备份和售后任务设计；不作为订单、付款或 Entitlement 账本。

## 当前绑定

| 项目 | 位置/锚点 |
|---|---|
| 隔离源码 | `E:\Claude_allow\Download\jovi-medusa-v2-spike-r2-r1\backend\jovi-medusa-backend` |
| 冻结证据包 | `workspace/review-queue/commerce-v1/medusa-v2-spike-remediation-r2-r1/` |
| package manifest | SHA256 `748ec4bcc2eb7061b2280ef367e43fcc0458bb21ff46583aacf882e1cd90a4c6`，117 个成员 |
| source snapshot tree | SHA256 `d15eb73e94a1fcf8b19ac2c8e03b317fa5ea94f7d8242548aa3eac4dec334e8d`，73 个成员 |
| 版本 | Medusa `2.19.0`；Node `22.17.1-bookworm-slim`；PostgreSQL `16-alpine`；Redis `7.2.11-alpine` |

## 明确不复制

不复制 `node_modules`、缓存、构建产物、运行时 PostgreSQL/Redis 数据、secrets、Storefront、示例素材、第三方支付/通知 provider 或任何闲鱼资料。R2 证据包保持 review-queue 隔离，旧失败包保持原状。

## 正式导入触发条件

当前 `PASS_WITH_GAPS` 只关闭 synthetic spike，不足以导入生产仓库。只有以下条件全部满足，才允许另行申请 `E:\project\jovi-medusa-commerce-v1`，并将受控适配层导入该新仓库：

1. 独立审阅 R2 已复算 R2-R1 冻结包，结论为 `MEDUSA_SPIKE_PASS_WITH_GAPS`。
2. `admin-bundler`、`admin-sdk`、`admin-shared`、`admin-vite-plugin` 四个 SBOM 条目、tarball/integrity、官方 LICENSE/ENTERPRISE-LICENSE 和 MIT scope 已逐项复核通过。
3. Jest 自然收尾（无 `--forceExit` 或等价句柄证据）和交互式 Admin smoke 均已在新的隔离运行中通过；两项不改变 synthetic-only 边界，生产集成仍需单独授权。
4. 进程级杀停/恢复窗口和所有运行输入仍有独立证据。
5. Jovi 单次汇总 Decision 明确允许创建新仓库；该 Decision 不授权闲鱼、真实付款、自动交付或 R12 Git baseline。

在触发前，本根仓库的正确动作是维护 OSS 知识、集成指针、审核 Prompt 和证据索引，而不是把候选源码伪装成已采用的生产代码。
