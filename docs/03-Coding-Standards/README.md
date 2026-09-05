# 编码规范与工程规则分类视图

**最后校准：2026-09-05**

本目录仍没有单独的一份语言风格规范；当前工程规则由以下 living 文件定义：

- [`../../AGENTS.md`](../../AGENTS.md) — Agent 行为、安全边界、C4 当前规则
- [`../../CODEX_MASTER_TASK.md`](../../CODEX_MASTER_TASK.md) — 当前主任务与停止点
- [`../CURRENT_PROJECT_GUIDE.md`](../CURRENT_PROJECT_GUIDE.md) — 架构/阶段/OSS 总览
- [`../05_验收测试_回滚与运维手册.md`](../05_验收测试_回滚与运维手册.md) — 测试/回滚规范

## 当前工程强制模式

- Runtime/Product/Governance 分仓；
- 实现 Agent 不自审；
- frozen evidence 不覆盖；
- claim evidence-bound；
- deterministic package 使用 byte-level 验收；
- product source zero-write；
- Gitleaks/Syft 保留；
- 六个 real-action flags 未经 Human Decision 不翻转。

## 历史说明

旧 `CODEX_MASTER_TASK.md` 曾描述 Track P/I 和旧 C0-C6；该文件现在已经更新。若在历史报告/Prompt 中仍看到这些术语，按 `docs/HISTORICAL_DOCUMENT_STATUS.md` 处理。
