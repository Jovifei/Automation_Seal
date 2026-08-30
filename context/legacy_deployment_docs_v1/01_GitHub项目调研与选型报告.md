# GitHub项目调研与选型报告

## 1. 选型原则

评估维度包括：是否解决真实流程问题、官方部署路径是否清晰、许可证能否接受、是否可隔离、是否便于版本锁定、是否存在对外账号或素材风险。

## 2. 选型结论

### 2.1 核心采用

| 项目 | 结论 | 原因 |
|---|---|---|
| OpenClaw | 采用 | 本地常驻、支持Agent工作区、Skill、Cron与沙箱；官方推荐onboard守护进程 |
| Spec Kit | 采用 | 原生支持Codex skills模式，将PRD转成可执行规格和任务 |
| n8n | 采用 | 确定性工作流、人工审批、凭证管理和可视化运维 |
| changedetection.io | 采用 | 适合低频监控公开页面、规则和Release |
| MkDocs | 采用 | 低成本生成产品文档和离线交付 |

### 2.2 可选采用

| 项目 | 阶段 | 限制 |
|---|---|---|
| TrendRadar | 核心稳定后的调研阶段 | GPL-3.0；作为独立服务使用，不打包转售其代码 |
| MoneyPrinterTurbo | 核心稳定后的视频阶段 | 素材权利和API Key风险；只输出草稿 |
| n8n-skills | 构建n8n工作流时 | 先审查并固定Commit，不能盲装所有脚本 |

## 3. 项目逐项分析

### 3.1 OpenClaw

官方README将其定位为运行在自有设备上的个人AI助手，推荐Node 24或22.19+，通过`openclaw onboard --install-daemon`安装常驻Gateway。其工作区可放置`AGENTS.md`、`SOUL.md`、`TOOLS.md`和`skills/<skill>/SKILL.md`。安全上，主会话工具默认可在宿主机运行，非主会话应启用Docker沙箱。

选型决定：OpenClaw不纳入核心Docker Compose，而按官方推荐以主机/WSL守护进程运行。这样更符合其渠道、节点和本地工具设计，也避免容器内再控制宿主机Docker的高权限做法。

### 3.2 Spec Kit

官方流程为constitution、specify、plan、tasks、implement，并支持`specify init . --integration codex --integration-options="--skills"`。适合把既有PRD变成可追踪的工程过程。

选型决定：所有正式产品使用Spec Kit；一次性小脚本可以走简化流程，但仍需验收和版本记录。

### 3.3 n8n

n8n支持Docker自托管、代码节点、人工审批和大量集成。其许可证是Sustainable Use License/Enterprise License，适合内部自用，但不能未经核对将n8n包装为对外商业托管产品。

选型决定：只作为个人内部自动化基础设施，不向客户提供n8n本身。

### 3.4 changedetection.io

项目提供Docker部署、CSS/XPath/JSON过滤和多种通知。Apache-2.0许可证较宽松。

选型决定：只监控公开页面和官方Release，限制频率，不用于登录态高频抓取或平台风控绕过。

### 3.5 TrendRadar

项目支持Docker Compose、关键词配置、AI分析和MCP，许可证GPL-3.0。

选型决定：作为独立服务运行；配置和生成的报告可用于内部研究，但若修改并分发其程序，需要遵守GPL义务。

### 3.6 MoneyPrinterTurbo

项目可从主题生成文案、素材、字幕、音乐和视频，官方提供预构建Docker镜像和API；GPU不是必需，但8GB以上显存适合本地转录和批量处理。项目为MIT许可证。

选型决定：在核心系统稳定后接入；使用4070S做本地转录和批量渲染。外部素材默认不进入商业产品，优先使用用户原创素材。

### 3.7 n8n-skills

该仓库包含14个互补技能、路由和Hooks，明确支持Codex插件安装场景，并以MIT许可发布。

选型决定：借鉴其“路由Skill+专业Skill+验证Hook”架构；实际安装时固定Commit并阅读全部脚本。

## 4. 不建议直接采用的模式

- 号称一键自动赚钱、自动养号或自动私信的项目。
- 需要上传浏览器Cookie到第三方服务器的项目。
- 没有License、Security和活跃维护记录的Skill合集。
- 直接把别人的课程、软件、预设和源码打包售卖的资源仓库。
- 自动追随`latest`且没有回滚机制的生产部署。

## 5. 许可证结论

| 项目 | 许可证 | 本项目用法 |
|---|---|---|
| OpenClaw | MIT | 可内部使用和修改，保留声明 |
| Spec Kit | MIT | 可使用和定制 |
| n8n | Sustainable Use | 内部自托管；商业再分发需单独核对 |
| n8n-skills | MIT | 可借鉴、固定Commit并保留声明 |
| TrendRadar | GPL-3.0 | 独立运行；分发修改版需遵守GPL |
| changedetection.io | Apache-2.0 | 可内部使用，保留Notice要求 |
| MoneyPrinterTurbo | MIT | 可二次开发；素材权利另行审核 |
| MkDocs | BSD-2-Clause | 可用于文档构建，保留许可 |

## 6. 版本策略

首次拉取可以查询最新稳定Release，但部署通过后必须锁定Tag、Commit或镜像Digest。大版本升级必须单独分支、备份、迁移演练和回滚验证。

## 7. 资料来源

完整链接见`sources/web_sources.md`。
