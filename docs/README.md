# 文档导航

本目录按“项目基础 → 架构治理 → 阶段执行 → 验收交付 → Commerce 专题”组织。Markdown 是工程事实来源；DOCX 仅供人类阅读，历史压缩包保留作交接材料。

## 工程主线

1. [项目初衷、需求 PRD 与科研复核](01_项目初衷_需求PRD与科研复核.md)
2. [系统架构与安全边界](02_系统架构与安全边界.md)
3. [闲鱼本地系统接入方案](03_闲鱼本地系统接入方案.md)
4. [Codex 分阶段部署执行书](04_Codex分阶段部署执行书.md)
5. [验收测试、回滚与运维手册](05_验收测试_回滚与运维手册.md)
6. [14 天快速落地与 Codex 定时任务](06_14天快速落地与Codex定时任务.md)
7. [数据治理、商业上线与合规检查](07_数据治理_商业上线与合规检查.md)
8. [交付包内容说明与执行索引](08_交付包内容说明与执行索引.md)

## Commerce 专题

- [Medusa 采用与修复框架](commerce/MEDUSA_ADOPTION_FRAMEWORK.md)
- [修复后独立审核 Prompt](commerce/MEDUSA_REMEDIATION_INDEPENDENT_AUDIT_PROMPT.md)
- [开源复用总览](commerce/oss-reuse/README.md)
- [Medusa v2](commerce/oss-reuse/01-Medusa-v2.md)
- [n8n](commerce/oss-reuse/02-n8n.md)
- [OpenMeter](commerce/oss-reuse/03-OpenMeter.md)
- [Kill Bill](commerce/oss-reuse/04-Kill-Bill.md)
- [Saleor](commerce/oss-reuse/05-Saleor.md)
- [Vendure](commerce/oss-reuse/06-Vendure.md)
- [Lago](commerce/oss-reuse/07-Lago.md)
- [Keygen](commerce/oss-reuse/08-Keygen.md)
- [Lemon Squeezy](commerce/oss-reuse/09-Lemon-Squeezy.md)

## 阅读与维护规则

- 先读根目录 `README_FIRST.md`、`PROJECT_STATE.json`、`context/` 和 `AGENTS.md`。
- 过程计划、运行日志、审计包和临时缓存不作为项目长期主文档。
- 证据路径、哈希和验证边界必须保持可复核；不能把 synthetic 结果写成生产结果。
- 新文档优先使用 Markdown；只有在需要人类排版交付时才生成 DOCX。

