# 架构设计文档 — 当前分类视图

**最后校准：2026-09-05**

当前架构先读：

- [`../02_系统架构与安全边界.md`](../02_系统架构与安全边界.md)
- [`../03_闲鱼本地系统接入方案.md`](../03_闲鱼本地系统接入方案.md)
- [`../commerce/COMMERCE_PROJECT_TOPOLOGY_AND_AUTHORITY_V1.md`](../commerce/COMMERCE_PROJECT_TOPOLOGY_AND_AUTHORITY_V1.md)

## 当前四仓模型

- `jovi-automation` — Governance
- `jovi-medusa-commerce-v1` — Formal Commerce Runtime
- `jovi-modbus-diagnostic-toolkit-v1` — First real SKU
- `jovi-commerce-engine-v1` — Legacy archive

`xianyu-auto-reply` 是独立外部适配器，当前真实平台动作 Human-controlled。

## 当前主线

C2/C3 架构已经实际完成并独立审计，当前停点是 `C4_HUMAN_PILOT_DECISION`。

旧 Route B / OpenSpec / Superpowers 架构资料仍保留为历史 Governance 证据，不是当前 Commerce 架构入口。

## DOCX

`../02_系统架构与安全边界.docx` 与 `../03_闲鱼本地系统接入方案.docx` 是旧排版导出，当前以 Markdown 为准。
