# 技术路线复核快照 - 2026-07-12

本文件保存已经完成的技术路线结论，防止Codex在首次执行中重复做广泛选型。版本、Security和许可证仍应在Phase A窄范围刷新。

## 核心采用

| 项目/方法 | 决策 | 用途 |
|---|---|---|
| OpenAI Codex | 核心 | 本地审计、开发、测试和文档 |
| AGENTS + 项目Skill + Hook | 核心 | 规则、任务能力和防越权 |
| Spec Kit | 产品级可选 | 大型产品规格和任务分解 |
| 轻量变更记录 | 核心 | 日常proposal/spec/design/tasks |
| n8n | Track I | 确定性、可重试流程 |
| PostgreSQL | Track I | n8n持久化和可恢复数据 |
| changedetection.io | Track I可选 | 公开页面、规则和竞品变化 |
| Promptfoo | X3前 | AI回复合成测试和红队 |
| Gitleaks/Trivy | 安全 | 密钥、依赖和容器扫描 |
| MkDocs | 产品 | 文档网站和离线交付 |

## 嵌入式路线

| 项目 | 决策 | 说明 |
|---|---|---|
| Python unittest/pytest | Alpha核心 | 主机侧协议与工具测试 |
| Unity/Ceedling/CMock | 后续核心 | C模块测试、Mock、覆盖率 |
| PlatformIO | 条件采用 | 跨平台构建、测试和静态分析 |
| Renode | 条件采用 | 支持SoC时做虚拟板级测试 |
| STM32Cube/GD32 SDK | 板卡确认后 | 官方基线和硬件示例 |

## 研究与知识处理

| 项目 | 决策 | 说明 |
|---|---|---|
| Docling | 可选推荐 | 有权处理的PDF/DOCX/PPTX/XLSX结构化 |
| PaperQA2 | 文献密集时 | 科研论文带引用检索 |
| Syft | 发布增强 | CycloneDX/SPDX SBOM |
| Cosign | 稳定发布后 | 容器和产物签名 |
| Langfuse | 延后 | LLM调用规模化后再部署 |

## 方法论参考，不整体安装

- OpenSpec：借鉴适合已有工程的轻量proposal/spec/design/tasks；
- BMAD：借鉴产品Brief、PRD、市场研究和测试检查表；
- Superpowers：借鉴TDD、系统调试、Worktree、计划执行和双阶段审查；
- 12-Factor Agents：借鉴确定性控制流、小Agent、状态管理和人工介入。

## 后续可选

- OpenClaw：常驻调度，权限面大，核心稳定后再评估；
- MoneyPrinterTurbo：快速视频草稿，素材和版权需审核；
- Remotion：品牌化程序视频，商用许可证按场景核验；
- TrendRadar/RSSHub：出现稳定内容运营需求后再启用。

## 当前Plugin方向

旧`openai/skills`示例仓库已不再作为最新分发基线。跨项目复用时应参考OpenAI Plugins结构；当前阶段保留项目级`.agents/skills/`以降低首次部署复杂度。

## 决策原则

- 产品优先于基础设施；
- 一个问题只保留一个主框架；
- 不因为热门而安装；
- 每个新增组件必须有明确重复工作、验收和回滚；
- 正式部署必须锁定Tag/Commit/Digest。
