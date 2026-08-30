# 开源与科研项目复核记录（2026-07-12）

## 1. 复核目的

本记录回答三个问题：

1. 是否已有项目可以减少重复开发；
2. 哪些项目适合进入首期运行环境，哪些只适合作为参考；
3. 它们如何与现有 `E:\project\xianyu-auto-reply` 和 Jovi Automation 组合，而不是形成重复系统。

本记录是交付前快照，不替代目标电脑上的 Phase A。Codex必须在安装前重新读取当前 README、Release、License、Security 和安装脚本，并将实际Tag、Commit或镜像Digest先写入`reports/phase-a/upstream-versions.json`，正式部署后再生成`LOCKED_VERSIONS.json`。

## 2. 证据方法

优先使用项目官方GitHub仓库中的：

- README；
- 最新非预发布Release或默认分支Commit；
- LICENSE；
- SECURITY；
- Dockerfile、Compose及安装脚本；
- 与本工程直接相关的配置、测试和接口文件。

没有公开证据的结论标记为“待目标机复核”，不将Star数、营销文案或社区转载当成生产可用性证明。

## 3. 首期核心组件

| 项目 | 交付前观察 | 决策 | 在本工程中的职责 | 安装前必须复核 |
|---|---|---|---|---|
| `openai/codex` | 官方本地编码Agent；当前源码包含 `doctor`、sandbox、approval、project `AGENTS.md`、project hooks和MCP配置 | CORE | 阅读规格、执行脚本、开发和测试、生成证据 | 当前CLI版本、Windows sandbox、Hook信任状态和配置Schema |
| `github/spec-kit` | 规格驱动流程可生成constitution/spec/plan/tasks | CORE | 将已批准PRD转成可追溯开发任务 | 当前Codex集成方式、模板和许可证 |
| `n8n-io/n8n` | 2026-07-10观察到最新非预发布Release `n8n@2.29.10` | CORE | 确定性工作流、定时触发、审核队列编排 | Release、breaking changes、镜像Digest、fair-code边界和加密密钥恢复 |
| PostgreSQL | 稳定关系数据库 | CORE | n8n工作流、执行和凭证元数据 | 选定主版本和镜像Digest；恢复演练 |
| `mkdocs/mkdocs` | 文档生成工具 | CORE | 生成产品快速开始、兼容矩阵和故障排查站点 | 主题与插件许可证 |
| `ThrowTheSwitch/Unity` | 嵌入式C单元测试框架 | CORE_EMBEDDED | CRC、解析器、状态机等主机侧测试 | 当前Release和工具链兼容性 |

## 4. 现有闲鱼系统复核

### 4.1 上游快照

- 仓库：`GuDong2003/xianyu-auto-reply-fix`
- 参考Commit：`837497d576b1b864a7294b8565348531a6ce7039`
- 参考版本：`v2.0.5`
- 参考发布日期：2026-07-10
- 技术栈：FastAPI、SQLite、Playwright、DrissionPage、Docker Compose
- 能力：多账号、关键词回复、AI回复、自动发货、商品/订单管理、日志和健康检查
- LICENSE：AGPL-3.0
- README附加提示：仅供学习研究使用，商业边界需要维护者或专业意见澄清

### 4.2 结论

决策为 `REUSE_STAGED`：

- 复用为独立执行适配器；
- 不重写第二套后台；
- 不合并数据库；
- 不让Jovi Automation直接写SQLite；
- 初期只交换人工批准的候选文件；
- 真实回复和交付由用户在Web界面手动启用。

### 4.3 上游公开Compose需要本地核验的风险

交付前观察到的公开基线包括：

- 管理端口、VNC和noVNC端口未限定到loopback；
- 容器以root运行；
- 整个源码目录读写挂载；
- 默认管理员/JWT示例值；
- 自动回复和自动发货默认开启；
- `latest`镜像；
- 远程滑块和后备验证能力。

这些不是对用户本地实例的断言。X0脚本只输出安全版本号、非敏感Git元数据、布尔风险标志和端口结构；不输出变更路径，不读取或哈希SQLite及其他秘密内容。

## 5. 调研与证据组件

| 项目 | 快照 | 决策 | 用途 | 主要限制 |
|---|---|---|---|---|
| `dgtlmoon/changedetection.io` | 默认分支版本字段为 `0.55.7` | RECOMMENDED | 平台规则、公开竞品页和官方文档变化 | 不监控登录后页面；设置低频率；固定镜像 |
| `sansan0/TrendRadar` | 待目标机刷新 | OPTIONAL_RESEARCH | 热点/RSS关键词聚合 | 热点不等于付费需求，需证据去重 |
| `DIYgod/RSSHub` | 待目标机刷新 | OPTIONAL_RESEARCH | 将公开内容规范化为RSS | 路由条款、请求频率和站点规则 |
| `docling-project/docling` | 官方README声明MIT，支持PDF/DOCX/PPTX/XLSX等、本地执行和MCP | OPTIONAL_RECOMMENDED | 将用户有权处理的文档转成结构化Markdown | 单独核对模型许可证；资源占用 |
| `Future-House/paper-qa` | PaperQA2，Apache-2.0，面向科学文献RAG | OPTIONAL | 对技术论文做带引用检索和综述 | Python/模型/API依赖较重；不是普通市场监控工具 |

首期不需要同时启用全部组件。默认仅部署changedetection；Docling在有本地文档转换需求时安装，PaperQA2仅在文献密集任务中安装。

## 6. AI回复和安全评测

| 项目 | 决策 | 作用 | 接入方式 |
|---|---|---|---|
| `promptfoo/promptfoo` | HIGH_PRIORITY | 合成对话评测、模型比较和红队 | X3前运行；不得使用真实买家消息 |
| `gitleaks/gitleaks` | CORE_SECURITY | 检测Token、密码和密钥 | 每次发布候选和代码提交前执行 |
| `aquasecurity/trivy` | CORE_SECURITY | 容器、依赖、秘密和错误配置扫描 | Phase B和每次镜像升级后执行 |
| `GeniusHTX/SWE-Skills-Bench` | REFERENCE_ONLY | 研究Skill是否真正提升任务表现 | 只借鉴评测方法，不作为运行时组件 |

AI回复验收关注：价格/工期承诺、站外导流、盗版请求、退款争议、提示注入、客户数据泄露、买卖双方身份混淆和高风险技术问题。

## 7. Skill与工作流参考

`czlonkowski/n8n-skills`可借鉴其技能拆分、路由和验证结构，但任何第三方Skill都必须：

1. 固定Commit；
2. 阅读全部文件而非只读`SKILL.md`；
3. 检查下载、网络、秘密、持久化和破坏性命令；
4. 不直接复制到生产Skill目录；
5. 通过本工程的 `skill-security-auditor` 后再改写为本地Skill。

本包已经提供14个本地专用Skill，优先使用这些受控Skill，而不是批量安装Skill合集。

## 8. 视频与常驻调度

| 项目 | 决策 | 原因 |
|---|---|---|
| `harry0703/MoneyPrinterTurbo` | OPTIONAL_LATER | 适合视频草稿，但素材授权和质量必须人工审核 |
| `remotion-dev/remotion` | OPTIONAL_LATER | 适合模板化技术视频，但商业许可按场景核验 |
| `openclaw/openclaw` | OPTIONAL_LATER | 可做常驻调度和消息入口，但权限面大、变化快；Codex+n8n足以完成首期 |

这些项目不进入GATE_A后的第一批部署，避免把“能安装”误当成“有业务价值”。

## 9. 采用顺序

```text
第一层：Codex + Spec Kit + 本地文档/测试
第二层：PostgreSQL + n8n + changedetection
第三层：Gitleaks + Trivy + Promptfoo
第四层：Docling / PaperQA2（按需）
第五层：TrendRadar / RSSHub（证据流程稳定后）
第六层：视频工具 / OpenClaw（核心稳定后单独评审）
```

## 10. 主要来源

- https://github.com/openai/codex
- https://github.com/github/spec-kit
- https://github.com/n8n-io/n8n/releases/tag/n8n%402.29.10
- https://github.com/dgtlmoon/changedetection.io/blob/master/changedetectionio/__init__.py
- https://github.com/GuDong2003/xianyu-auto-reply-fix
- https://github.com/GuDong2003/xianyu-auto-reply-fix/commit/837497d576b1b864a7294b8565348531a6ce7039
- https://github.com/promptfoo/promptfoo
- https://github.com/gitleaks/gitleaks
- https://github.com/aquasecurity/trivy
- https://github.com/docling-project/docling
- https://github.com/Future-House/paper-qa
- https://github.com/mkdocs/mkdocs
- https://github.com/ThrowTheSwitch/Unity
- https://github.com/sansan0/TrendRadar
- https://github.com/DIYgod/RSSHub
- https://github.com/czlonkowski/n8n-skills
- https://github.com/harry0703/MoneyPrinterTurbo
- https://github.com/remotion-dev/remotion
- https://github.com/openclaw/openclaw
- https://github.com/GeniusHTX/SWE-Skills-Bench
