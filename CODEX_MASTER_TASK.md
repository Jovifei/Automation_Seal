# Jovi Automation V3.0 主任务书

## 主线与边界

当前主线是本地、可审计的 Commerce Engine：产品资产、商品草稿、人工付款确认、授权、待人工交付包、售后记录和合成商业验证。Modbus 仅作为独立 SKU；OpenClaw_VideoFactory 是独立项目。两者不能替代 Commerce 主线验收。

永久安全约束：

- Hook 保持 `DO_NOT_TRUST`，且不是 Commerce 运行依赖。
- 未经人类精确回执，不修改 Decision、Approval、Manifest、Gate 或控制面。
- Gate A.P 验证前不写正式 Commerce 目录、运行代码、SQLite 或 `products/`；只允许在 `workspace/review-queue/commerce-v1/` 准备候选。
- 不读取或修改外部闲鱼工程，不读取 Cookie、消息、订单库、Token、支付数据或客户 PII。
- 不自动发布、聊天、收款、发货、改价、退款或验证；所有真实平台动作由 Jovi 人工完成。
- 不配置 Git remote、不 push、不运行 human-only 入口。

## 治理收口顺序

```text
G0 执行包与精确授权
→ G1 治理整改与测试隔离
→ G2 冻结 V3/Controlled Baseline 候选
→ G3 独立预审
→ G4 Jovi 签发 Decision V3
→ G5 Manifest-only APPLY 与独立 Post-Apply Audit
→ G6 S1 收口、Gate A.P、人类批准和 C/APPLY
```

Luna只能整改、测试和准备候选；独立审核必须由不属于当前任务 lineage 的新 Agent 执行；Jovi本人负责 Decision V3 与 Gate A.P 人工作用。任何门失败即保持 `BLOCKED`。

## Commerce 实施顺序（Gate A.P 与 C/APPLY 之后）

```text
C0 本地 Git 基线（无 remote）
→ C1 契约冻结
→ C2 产品资产与确定性商品草稿
→ C3 SQLite 订单账本与哈希链
→ C4 人工付款、授权和待人工交付包
→ C5 闲鱼草稿适配器（外部仓库零访问）
→ C6 售后、指标与 X2 合成端到端
```

最终出口只允许：

```text
X2_COMMERCE_FLOW_PASS
REAL_COMMERCE_PILOT_NOT_STARTED
REMOTE_REPOSITORY_NOT_CONFIGURED
HUMAN_ONLY_ENTRYPOINTS_CANDIDATE_NOT_INSTALLED
```

不得声称已发布、已自动售卖或无人值守上线。

## 只读入口

`scripts/00-run-readonly-audit.ps1` 仅调用 Commerce readiness validator，将结果写入 review queue；它不读取闲鱼、不生成 Gate 计划、不修改权威状态。readiness 不是授权，必须等待人类 Decision/Gate 回执。

## 每项任务的强制闭环

代码任务采用“失败测试 → 最小实现 → 聚焦测试 → 全量回归 → 文档/台账 → 小提交”。每轮更新 `tasks/todo.md`、`STATUS.md`、`CHANGELOG.md` 与 Obsidian 双账本，并报告：完成、未完成、测试、证据、风险、下一步、提交。
