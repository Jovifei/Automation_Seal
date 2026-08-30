# 需求可追溯矩阵

| 原始需求 | 设计响应 | 主要文件 | 验收证据 |
|---|---|---|---|
| 家中电脑无人值守完成工作 | 定时工作流只生成内部产物 | `automation_specs/` | n8n测试执行记录 |
| 找嵌入式和摄影机会 | 市场雷达、页面变化和证据卡 | `market-opportunity-research` Skill | 带来源日报 |
| 生成正规PRD和执行文档 | Spec Kit流程与原始PRD | `context/source_markdown/` | spec/plan/tasks |
| Codex本地直接部署 | 固定启动Prompt和分阶段脚本 | `CODEX_START_PROMPT.txt` | Phase报告 |
| 复用现有闲鱼系统 | 独立执行适配器，不合并数据库 | `docs/03_闲鱼本地系统接入方案.md`、`deploy/xianyu/` | X0-X4报告 |
| 自动回复/发货提效 | 初期草稿和固定规则，逐SKU开放 | `tests/promptfoo/`、Bundle契约 | 合成测试与人工回执 |
| 防止误操作 | 阶段门、Hook、human-only目录 | `.codex/hooks.json`、`scripts/human-only/` | 阻断测试 |
| 合法售卖资源 | 权利登记、许可证扫描、隔离队列 | `embedded-license-auditor` Skill | THIRD_PARTY_NOTICES |
| 可回滚 | 备份、不可变批准包、回滚手册 | `scripts/backup.ps1`、`scripts/test-backup-restore.ps1`、`docs/05_验收测试_回滚与运维手册.md` | 恢复演练 |
