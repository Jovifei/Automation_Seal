# 当前接手与运行排障 — Commerce V1 / C4

**最后校准：2026-09-05**

> 本文件不再描述早期 Phase A / Track P-I 首次运行。当前技术链已完成到 C3 + Runtime Promotion，当前停点是 `C4_HUMAN_PILOT_DECISION`。

## 1. Agent 读到旧 Track P/I、X0-X4 或 READY_FOR_CODEX_PHASE_0_A_X0

不要执行旧路线。

先读：

```text
docs/CURRENT_PROJECT_GUIDE.md
docs/HISTORICAL_DOCUMENT_STATUS.md
PROJECT_STATE.json
NEXT_STEP_MAP.md
```

历史 OpenSpec、Superpowers、旧 Prompt 和 audit 保留用于追溯，不代表当前 TODO。

## 2. Governance Git 与文档状态不一致

先核：

```powershell
git status --short --branch
git rev-parse HEAD
git remote -v
git ls-remote --heads origin
```

再核 GitHub 当前 `main`、`commerce-c3-real-sku-readiness-20260905`、PR #5 与 CI。

不要通过 `reset --hard`、`clean`、rebase 历史审计提交来制造一致。

## 3. Runtime 状态与 Governance mirror 不一致

Governance mirror 不是 Runtime 原件。

进入：

`E:\project\jovi-medusa-commerce-v1`

重新核：
- local main HEAD；
- C3 independent audit result + sidecar；
- post-promotion result；
- source tree / lockfile；
- six real-action flags；
- `git remote -v`。

若冲突，停止 C4 越级动作并报告真实本地值。

## 4. Product HEAD / artifact SHA 不一致

进入：

`E:\project\jovi-modbus-diagnostic-toolkit-v1`

只读核对 HEAD、installer/portable/package binding。

不要让 Commerce Agent 为了匹配旧 SHA：
- 修改产品源码；
- 重建产品；
- 删除 untracked artifact；
- reset/clean 产品仓。

产品发生真实变化时，进入新的产品 release qualification / Commerce delta audit。

## 5. C4 商品文案与产品事实冲突

当前 Operational Kit 是 `PRE_PUBLISH_QA_REQUIRED / DO_NOT_PUBLISH_AS_IS`。

必须读取本地：

`governance/c3/C3_LISTING_CLAIM_EVIDENCE.json`

无 evidence 的 claim：REMOVE/REWRITE。

特别注意：
- CRC 是错误检测，不默认写“纠错”；
- SHA256 是哈希/完整性校验值，不是数字签名；
- 无 evidence 不写“3分钟”“全兼容”“永久更新”；
- `0.2.0-dev` / unsigned 不隐藏。

## 6. C4 Pilot ledger 已经有“完成订单”但 Pilot 还没授权

这是错误/示例数据风险。

正式 C4 ledger 必须从 0 条真实订单开始。任何示例必须单独标记：

`EXAMPLE_ONLY / SYNTHETIC / DO_NOT_COUNT_AS_PILOT_EVIDENCE`

当前主文档已经清理，但本地旧副本/派生文件也要检查。

## 7. C4 Decision Candidate 看起来像已经批准

检查：

`issued_from_human`

当前必须是：

`false`

只有 Jovi 本人最终审阅并明确签发 `true` 才能开始真实 Pilot。Agent 不得执行 human-only 签发。

## 8. 闲鱼工程/平台访问失败

C4 Pre-Publish 阶段不需要给 Agent 可写闲鱼目录，也不需要读取 Cookie/Profile/SQLite。

当前只刷新公开平台规则；真实 publish/message/payment confirmation/delivery/refund 都由 Jovi 手工。

不要为排障自动克隆、升级、重启或改写 `E:\project\xianyu-auto-reply`。

## 9. Docker / PostgreSQL / Redis 未运行

仅在需要复核 Runtime C3/C4 内部能力时启动对应受控 Runtime 流程。

不要回到旧“Track I 部署 n8n/changedetection”路线。`n8n_production=false` 仍不是 C4 blocker。

## 10. Runtime 没有 GitHub remote

不要猜 URL，不要把 Runtime push 到 Automation_Seal。

报告：

`RUNTIME_DEDICATED_REMOTE_NOT_CONFIGURED`

建议目标是 `Jovifei/jovi-medusa-commerce-v1`，但 public/private 与准确 remote 必须由 Jovi确认。

## 11. GitHub CI 失败

先区分：
- docs/reference QA；
- Runtime test failure；
- external/service/transient failure。

不能删除/放宽测试来让状态变绿。修复后保留失败 run 作为历史。

## 12. 敏感信息出现在日志/报告

立即停止外发/提交：
- 不继续复制敏感值；
- 隔离新生成的报告；
- 检查输出路径和 redaction；
- 轮换真正泄露的 credential（由 Jovi/秘密管理流程处理）；
- 不通过删除历史 evidence 隐瞒问题。

## 13. 当前正确恢复入口

遇到任何“我现在到底该做哪一步”的问题：

1. `docs/CURRENT_PROJECT_GUIDE.md`
2. `PROJECT_STATE.json`
3. `NEXT_STEP_MAP.md`
4. `docs/commerce/README.md`
5. 现场 Git/evidence

当前正常目标应落在：

`C4 Pre-Publish QA -> READY_FOR_JOVI_C4_HUMAN_PILOT_DECISION`
