# 文档导航 — 当前 Commerce V1 主线

**最后校准：2026-09-05**  
**当前停点：`C4_HUMAN_PILOT_DECISION`**

> 本仓库保留了从早期 Track P/I、X0-X4、Medusa spike、R6、C2 到 C3 的完整历史。新 Agent **不要按文件日期猜当前阶段**，先读 [当前项目指南](CURRENT_PROJECT_GUIDE.md) 与 [历史文档状态](HISTORICAL_DOCUMENT_STATUS.md)。

## 1. 新 Agent 必读

1. [当前项目指南](CURRENT_PROJECT_GUIDE.md)
2. [历史文档状态与使用规则](HISTORICAL_DOCUMENT_STATUS.md)
3. [最终交付与当前操作总说明](00_最终交付与操作总说明.md)
4. [当前系统架构与安全边界](02_系统架构与安全边界.md)
5. [Codex 当前分阶段执行书](04_Codex分阶段部署执行书.md)
6. [Commerce 专题导航](commerce/README.md)
7. 根目录 `STATUS.md`、`PROJECT_STATE.json`、`NEXT_STEP_MAP.md`

## 2. 当前主线文档（00–08）

这些 Markdown 文件继续保留原文件名，以避免破坏旧脚本/引用；内容已经按当前 Commerce V1 阶段重写。

| 文件 | 当前用途 |
|---|---|
| [00_最终交付与操作总说明](00_最终交付与操作总说明.md) | 项目做什么、做到哪、下一步是什么 |
| [01_项目初衷_需求PRD与科研复核](01_项目初衷_需求PRD与科研复核.md) | 当前产品目标、冻结路线、后续 backlog |
| [02_系统架构与安全边界](02_系统架构与安全边界.md) | 四仓架构、Jovi Policy 权威、人类边界 |
| [03_闲鱼本地系统接入方案](03_闲鱼本地系统接入方案.md) | C4 人工平台模式与未来权限扩展原则 |
| [04_Codex分阶段部署执行书](04_Codex分阶段部署执行书.md) | 当前从 C4 Pre-Publish QA 到 Pilot 的执行顺序 |
| [05_验收测试_回滚与运维手册](05_验收测试_回滚与运维手册.md) | C2/C3 已验收能力与 C4 运行/回滚要求 |
| [06_14天快速落地与Codex定时任务](06_14天快速落地与Codex定时任务.md) | 文件名为历史兼容；当前内容是 C4 快速商业验证计划 |
| [07_数据治理_商业上线与合规检查](07_数据治理_商业上线与合规检查.md) | Pilot 隐私、claim、OSS、平台/退款检查 |
| [08_交付包内容说明与执行索引](08_交付包内容说明与执行索引.md) | 当前工程/证据/Prompt 索引 |

同名 `.docx` 是早期人类阅读导出，**不代表当前同步状态**。

## 3. Commerce 当前专题

- [Commerce 专题 README](commerce/README.md)
- [项目拓扑与权威边界](commerce/COMMERCE_PROJECT_TOPOLOGY_AND_AUTHORITY_V1.md)
- [C3 本地审计闭环 mirror](commerce/C3_LOCAL_AUDIT_CLOSURE_MIRROR_20260905.md)
- [Runtime C3 Promotion Decision](commerce/JOVI_RUNTIME_C3_PROMOTION_DECISION_V1.md)
- [C4 Human Pilot 计划](commerce/C4_HUMAN_PILOT_PLAN_V1.md)
- [C4 Privacy Minimization](commerce/C4_PILOT_PRIVACY_MINIMIZATION_V1.md)
- [C4 Decision Candidate](commerce/C4_HUMAN_PILOT_DECISION_CANDIDATE_V1.md) — **`issued_from_human=false`，不是批准**
- [C4 Pilot Operational Kit](commerce/C4_PILOT_OPERATIONAL_KIT_V1.md) — **发布前还需本地 claim evidence QA**
- [OSS 复用总览](commerce/oss-reuse/README.md)

## 4. 已完成阶段参考

C2/C3、R2/R6、Medusa 审计文档继续保留用于追溯。它们的状态是 `COMPLETED STAGE REFERENCE`，不应被新 Agent 当成当前待执行任务。

## 5. 历史证据 / 不作为当前指令

- `docs/openspec/changes/archive/**`
- `docs/superpowers/**`
- 带 sidecar 的历史 task plan
- 历史 `MEDUSA_*AUDIT*` / stale review package

这些尽量保持原字节。

## 6. 当前永久边界

在新的 Jovi Human Decision 之前，至少保持：

`production_integration_allowed=false`  
`real_payment=false`  
`real_customer=false`  
`xianyu=false`  
`auto_delivery=false`  
`n8n_production=false`

当前 C4 允许准备真实 Pilot，但真实发布、消息、付款确认、发货、改价、退款仍由 Jovi 手工执行。
