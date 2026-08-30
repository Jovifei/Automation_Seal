# Keygen：当前阶段拒绝

**核验日期：2026-08-30；结论：`REJECT_CURRENT_PHASE`。**

## 官方身份与审查锚点

- 官方仓库：[keygen-sh/keygen-api](https://github.com/keygen-sh/keygen-api)；官方文档：[keygen.sh/docs](https://keygen.sh/docs/)。
- 审查锚点：`v1.7.0`；使用前必须锁定 tag 对应提交、镜像 digest、CE/EE edition 与官方 SDK 版本。
- 许可证：Fair Core License 1.0，未来 Apache-2.0（每个版本发布两周年后按条款生效）；这不是当前版本的 OSI 开源许可。EE 需要单独授权。

## 技术栈、借鉴与不采用

Keygen API 是 Ruby/Rails 风格的许可、激活、entitlement 和发行服务，附有 Python 等 SDK 与可选 self-host/cloud。可借鉴离线许可证、机器绑定、撤销、签名验证和账户隔离设计；不部署 CE/EE、Cloud、Portal、Relay，不复制激活服务或示例，也不创建/管理真实许可证。

## 与本工程的关系

首个 Modbus 数字产品尚不能因本次文档获得许可服务授权。Medusa 不应把 Keygen 当作默认 provider；Python oracle 只核验本地确定性规则，不能铸造许可证；n8n 不保存 API token 或自动发码；闲鱼适配器的卡密、买家消息、Cookie 与 SQLite 均不可读取或迁移。

## 集成成本、许可义务与安全风险

成本包括 SaaS/自托管选择、密钥层级、设备指纹隐私、离线策略、撤销一致性、客户支持、可用性和数据保留。FCL 禁止竞争性使用、禁止绕过许可证功能；分发衍生物须带条款/版权，且须按版本分别判定两年后的 Apache 生效日期。风险包括 token/私钥泄露、license 伪造、设备指纹侵犯隐私、离线时钟欺骗、误撤销和将授权服务变为单点故障。

## 升级触发条件

只有产品许可模型、离线需求、隐私告知、密钥托管和合同/许可审查获得单独批准时才评估。安全公告、FCL/EE 条款或 SDK/协议变化触发重审；POC 必须使用虚构客户与测试密钥，并验证签名、重放、撤销、离线期限和秘密扫描。

## 结论枚举

1. `REJECT_CURRENT_PHASE`；2. `FAIR_CORE_LICENSE_REQUIRES_REVIEW`；3. `NO_LICENSE_ISSUANCE_OR_TOKEN_STORAGE`；4. `NO_XIANYU_CARDKEY_ACCESS`。

## 来源与限制

- [官方仓库](https://github.com/keygen-sh/keygen-api)、[v1.7.0 release](https://github.com/keygen-sh/keygen-api/releases/tag/v1.7.0)、[LICENSE](https://github.com/keygen-sh/keygen-api/blob/master/LICENSE.md)、[官方入门文档](https://keygen.sh/docs/getting-started/)。
- 不构成对 Fair Core/EE 条款的法律解释，且未创建任何账号或密钥。

## 固定栏目核对

- **官方仓库：** `keygen-sh/keygen-api`；**官方文档：** `keygen.sh/docs`；**核验日期：** 2026-08-30。
- **Tag 或 Commit：** `v1.7.0`；**许可证：** Fair Core License 1.0，按版本两年后可转 Apache-2.0，EE 另行授权；**技术栈：** Ruby/Rails、许可/激活/entitlement/发行 API、SDK、self-host/cloud。
- **可直接复用的模块：** 无；当前不创建许可证、账号或 token。
- **只借鉴的设计：** 离线许可证、机器绑定、撤销、签名验证和账户隔离。
- **明确不采用部分及原因：** CE/EE、Cloud、Portal、Relay、激活服务与示例；Fair Core 许可、密钥运营与产品授权范围未获批准。
- **与 jovi-automation/Medusa/Python oracle/n8n/闲鱼适配器关系：** `jovi-automation` 不能因本文获得发码授权；Medusa 不默认接 Keygen；Python oracle 不铸造许可证；n8n 不存 token/自动发码；闲鱼适配器卡密、消息、Cookie、SQLite 不读取。
- **集成成本：** 自托管/SaaS、密钥层级、设备隐私、撤销与支持；**运行依赖：** 许可 API、密钥/加密、数据库或 Keygen Cloud；**许可义务：** FCL 禁止竞争使用/绕过功能并需保留条款；**安全风险：** 私钥/token、伪造、指纹隐私、时钟欺骗和单点故障。
- **升级触发条件：** 许可模型、离线需求、隐私、密钥托管与合同获批，或 FCL/EE/SDK/安全变化。
- **固定结论：** `REJECT_CURRENT_PHASE`；**来源登记：** 官方仓库、release、LICENSE、入门 docs；**推断：** 授权设计有参考价值；**限制：** 未建账号/密钥且无合同/法务批准；**待复核：** tag/commit/digest、FCL/EE 适用性、测试密钥 POC 和秘密扫描。
