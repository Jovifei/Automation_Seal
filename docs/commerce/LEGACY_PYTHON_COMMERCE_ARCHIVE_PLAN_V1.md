# Legacy Python Commerce 仓归档计划 V1

目标仓：`E:\project\jovi-commerce-engine-v1`

## 定位

该仓是 2026-08-09 早期纯 Python Commerce staging 试验田。正式 Commerce Runtime 已转向 `jovi-medusa-commerce-v1`，因此不再新增业务能力。

## 为什么不直接删除

历史 Decision、Oracle、审计或交接材料可能引用它；删除会破坏 provenance。

## 归档动作

本轮只生成计划。由本地 Agent 现场确认后：

1. `git status` / HEAD / remote / dirty state；
2. 生成 `LEGACY_ARCHIVE_SNAPSHOT.json`：commit、tree SHA、文件清单、引用路径；
3. 在仓内增加 `ARCHIVED.md`，说明 superseded by Medusa；
4. 禁止新增 production code；
5. 如有远端则 archive repository；无远端则保留只读本地目录；
6. 不移动/删除文件，除非后续 Jovi 单独批准。

## 允许继续使用的内容

只有明确作为 oracle/reference 的纯函数、测试思想或历史 evidence 可以被引用；任何代码复用到 Medusa Runtime 都必须重新做 provenance 和测试，不能把 legacy 结果当生产证明。

## 归档完成状态

`LEGACY_COMMERCE_ENGINE_ARCHIVED_READ_ONLY`

此状态不表示删除，也不影响 `jovi-automation` 与 `jovi-medusa-commerce-v1`。