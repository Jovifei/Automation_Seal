# Jovi Automation

Jovi Automation 是一个本地优先、可审计、可回滚的数字产品工程与治理仓库。它负责产品规格、Python 验收基准、测试、许可证审查、证据包和人工批准候选；真实平台行为始终由 Jovi 控制。

## 当前状态

- 首个产品方向：Modbus RTU 诊断工具包。
- Commerce 生产核心候选：Medusa v2；当前仅完成隔离 spike 和修复候选，尚未生产采用。
- Python `jovi_commerce`：状态机、边界规则和 synthetic X2 oracle。
- 闲鱼：独立人工执行适配器，不共享数据库、Cookie、Token 或浏览器资料。
- n8n：未来 Track I 内部编排候选，不作为订单、付款或 Entitlement 权威账本。
- 当前 Medusa 采用门：`READY_FOR_INDEPENDENT_AUDIT`；`production_integration_allowed=false`。

## 文档入口

- [项目状态与首次阅读](README_FIRST.md)
- [Medusa 采用与修复框架](docs/commerce/MEDUSA_ADOPTION_FRAMEWORK.md)
- [开源复用决策矩阵](docs/commerce/oss-reuse/README.md)
- [文档目录](docs/README.md)
- [当前阶段图](NEXT_STEP_MAP.md)

## 证据边界

合成测试、候选包、loopback 服务和本地 PostgreSQL 只能证明相应范围内的技术行为，不能证明真实付款、真实客户、闲鱼平台、生产部署或商业发布。正式批准文件、阶段门和人工决定不会由测试脚本自动生成。

## 本地运行原则

默认使用 Windows PowerShell；临时下载、依赖缓存和 Medusa spike 运行数据放在 `E:\Claude_allow\Download`。运行前先阅读 [AGENTS.md](AGENTS.md)，不要读取或提交秘密、客户记录、浏览器 Profile、Cookie、Token 或真实平台数据。

## 验证说明

Modbus 产品测试在设置模块路径后为 `12 passed`：

```powershell
$env:PYTHONPATH='products/modbus-rtu-toolkit'
python -m pytest products/modbus-rtu-toolkit/tests -q
```

Medusa 隔离验证证据保留在本地 review queue，不随本精简提交上传。当前 Python 全量测试仍有一项历史基线导入错误：Commerce pre-decision 测试依赖旧 validator facade 的缺失导出；该问题已记录，不能把本仓库初始提交描述为全量测试通过。

## 远端仓库

本精简快照已提交到 [Jovifei/Automation_Seal](https://github.com/Jovifei/Automation_Seal)，当前 `main` 提交为 `f370e8dec3cc1abfa093eb52a3bdba7661c69a15`。
