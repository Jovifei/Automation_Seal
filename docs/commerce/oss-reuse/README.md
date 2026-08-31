# Commerce V1 OSS 复用边界

**核验日期：2026-08-30。** 本目录是架构与许可审查材料，不是安装说明、采购批准、支付/交付启用证明或闲鱼平台授权。版本仅为审查锚点；任何实际部署均须重新核对上游 tag、提交、镜像 digest、`LICENSE`、`SECURITY` 和供应链证据。

当前 Medusa spike 的采用与修复框架见 [Medusa 采用与修复框架](../MEDUSA_ADOPTION_FRAMEWORK.md)；修复完成后使用 [独立审核 Prompt](../MEDUSA_REMEDIATION_INDEPENDENT_AUDIT_PROMPT.md)。

## 本轮吸收范围

本目录已经把开源项目的可复用能力、许可义务、依赖风险和采用触发条件吸收到 `jovi-automation` 的架构知识库。吸收的是经过边界审查的设计与集成契约，不是把所有上游源码、`node_modules`、示例素材或运行数据复制进正式工程。

- Medusa R2 的源码仍位于隔离目录，当前只通过 [R2 集成指针](../MEDUSA_R2_INTEGRATION_POINTER.md) 绑定版本、证据和后续采用门。
- n8n、OpenMeter、Kill Bill、Saleor、Vendure、Lago、Keygen、Lemon Squeezy 按下表结论处理；没有把 `REFERENCE_ONLY`、`FUTURE_TRIGGER` 或 `REJECT_CURRENT_PHASE` 项误当成已安装组件。
- 任何正式代码导入都必须在独立审核和 Jovi Decision 之后新建受控 Medusa 仓库；本根仓库继续保存规格、边界、审计提示和可复核证据索引。

## 固定决策矩阵

| 组件 | 固定结论 | 本期边界 |
|---|---|---|
| Medusa v2 | `DIRECT_REUSE_PRIMARY` | Commerce 核心候选；仅在独立批准后进入受控运行环境。 |
| n8n | `DIRECT_REUSE_INTERNAL_ORCHESTRATION` | 仅内部确定性编排、审核队列与可审计重试；不面向客户托管工作流。 |
| OpenMeter | `FUTURE_TRIGGER_METERED_PRODUCTS` | 仅在出现经批准的按量计费产品时重新评估。 |
| Kill Bill | `REFERENCE_ONLY` | 参考订阅计费与审计边界，不部署、不复制。 |
| Saleor | `ALTERNATIVE_NOT_SELECTED` | 备选架构，当前不引入。 |
| Vendure | `REJECT_CURRENT_PHASE` | GPLv3 与工程成本不适合当前阶段。 |
| Lago | `REJECT_CURRENT_PHASE` | AGPLv3、计量/计费范围过宽，当前不引入。 |
| Keygen | `REJECT_CURRENT_PHASE` | Fair Core 许可与许可服务器运营范围不匹配。 |
| Lemon Squeezy | `REJECT_CURRENT_PHASE` | 外部 SaaS/支付服务，未获得平台、法务或业务批准。 |

## 采用触发条件

| 组件 | 允许重新采用或评估的必要触发条件 | 当前动作 |
|---|---|---|
| Medusa v2 | 独立 Gate、固定 tag/commit/digest、SBOM、迁移/回滚与安全验收齐备。 | 主候选，尚未部署。 |
| n8n | Track I 独立 Gate、内部最小权限工作流、凭证恢复演练与重放负测齐备。 | 仅内部编排候选。 |
| OpenMeter | 获批按量产品、计量定义、对账/争议处理与独立安全审查同时成立。 | 未来触发才选型。 |
| Kill Bill | 获批复杂订阅/跨 provider 对账，且 Medusa 无法满足。 | 仅参考。 |
| Saleor | Medusa 被正式否决且已批准 GraphQL-first/多频道需求。 | 备选，不并行建设。 |
| Vendure | 法务或商业许可路径明确、Medusa 被正式否决、许可兼容性审查通过。 | 当前拒绝。 |
| Lago | 按量产品、账单归属、AGPL 方案和合规责任均获批准。 | 当前拒绝。 |
| Keygen | 产品许可模型、隐私告知、密钥托管和合同/许可审查获单独批准。 | 当前拒绝。 |
| Lemon Squeezy | 商户准入、法务/税务/隐私审查、负责人批准和 webhook 设计齐备。 | 当前拒绝。 |

## 系统关系与不可跨越边界

`jovi-automation` 是控制与证据项目；Medusa 是潜在 Commerce 核心；Python oracle 只生成可复算的业务建议/校验结论，不能以模型文本改变确定性信号；n8n 只执行批准后的内部编排；闲鱼适配器保持独立，且真实发布、回复、发货、改价、收款、退款和验证均由 Jovi 人工控制。不得让 Medusa、n8n 或 Python oracle 直接读写闲鱼适配器的 SQLite、Cookie、浏览器资料或 Token。

任何外部输入均需经 schema、来源、权限和幂等性校验；支付 webhook、许可证回调和计量事件必须验证签名、时间窗、重放标识与审计链。候选文案与交付材料先入 `workspace/review-queue/`；权利、秘密或隐私不明的内容入隔离区。

## 阅读方式与共通限制

每篇均记录官方仓库/文档、审查锚点、许可、技术关系、成本、风险、升级触发条件、结论、来源和限制。文中“可直接复用”表示架构许可范围内的候选能力，**不等于当前已安装、已配置、已通过安全验收或获准上线**。不得用本目录替代批准文件、供应链锁定或真实平台验证。

## 文档索引

1. [Medusa v2](01-Medusa-v2.md)
2. [n8n](02-n8n.md)
3. [OpenMeter](03-OpenMeter.md)
4. [Kill Bill](04-Kill-Bill.md)
5. [Saleor](05-Saleor.md)
6. [Vendure](06-Vendure.md)
7. [Lago](07-Lago.md)
8. [Keygen](08-Keygen.md)
9. [Lemon Squeezy](09-Lemon-Squeezy.md)
