# Jovi Commerce：Medusa 采用与修复框架

**状态：** `REMEDIATION_CANDIDATE_READY_FOR_INDEPENDENT_AUDIT`  
**更新日期：** 2026-08-30  
**适用范围：** Medusa v2 隔离验证、Python oracle、review-queue、未来 n8n 与闲鱼适配器边界。

## 1. 当前结论

Medusa v2.19.0 已证明 Backend、Admin、Product、Order、`pp_system` 和 Jovi 数字商品模型可以在 loopback PostgreSQL 环境运行。但当前 spike 只能证明技术可行性，不能进入正式采用：持久化写入口、synthetic provenance、付款证据语义、事务幂等和证据绑定仍不满足安全门。

当前正式判定为：

- `MEDUSA_SPIKE_FAIL`
- `TECHNICAL_FEASIBILITY_PROVEN_WITH_GAPS`
- `PRODUCTION_INTEGRATION_ALLOWED=false`
- R12：`R12_NOT_EXECUTED_PENDING_JOVI_DECISION`

## 1.1 2026-08-30 修复候选

R1–R4 修复候选已冻结在 `workspace/review-queue/commerce-v1/medusa-v2-spike-remediation/`。候选使用 Node v22.17.1，从空 PostgreSQL 数据目录重建；单元测试 12/12、数据库集成测试 4/4、TypeScript 检查通过；两次 X2 返回同一 Order、Entitlement 和 Receipt，最终数据库计数为 1/1/1/1。以上仅使候选达到 `READY_FOR_INDEPENDENT_AUDIT`，R5/R6 仍未开始，不能改写为 adoption PASS。

## 2. 目标架构

```mermaid
flowchart TB
  M[Medusa Core<br/>Product Order Payment Workflow]
  P[Jovi Policy Boundary<br/>rights payment evidence entitlement provenance]
  E[Evidence Boundary<br/>manifest receipt audit package]
  O[Python oracle<br/>acceptance reference only]
  N[n8n<br/>future internal orchestration]
  X[Xianyu adapter<br/>human-approved candidates only]

  M --> P
  P --> E
  O -. semantic comparison .-> E
  E -. approved internal task .-> N
  E -. human-approved candidate .-> X
```

### Medusa Core

直接复用 Product、ProductVariant、Order、Payment Module、Fulfillment 和 Workflow。不得在该层加入闲鱼逻辑、交付密钥、客户私密数据或自动发布行为。

### Jovi Policy Boundary

这是唯一允许签发 Entitlement 和 DeliveryReceipt 的边界。它必须在同一个事务化 Workflow 内完成：读取订单与付款状态、校验证据 SHA、校验资产权利、写入 provenance、签发 Entitlement、生成 receipt。通用 CRUD 不得成为业务写入口。

### Evidence/Adapter Boundary

只输出脱敏、哈希绑定的 JSON/receipt。Python oracle 只比较语义；n8n 未来只生成内部任务；闲鱼适配器只接收人工批准候选。三者都不得共享 Medusa 数据库或成为付款/授权权威账本。

## 3. 下一阶段：R1 采用边界修复

### R1.1 收敛持久化入口

- 新建唯一业务命令，例如 `confirmPaymentAndPrepareDelivery`。
- 在事务中重新读取 Medusa Order、PaymentCollection 和 JoviAsset。
- 未满足付款、权利或 provenance 要求时不产生任何持久化副作用。
- 禁止或封装 Entitlement/Receipt 的公共 create/update/delete。

### R1.2 synthetic provenance

Asset、Entitlement、Receipt 与最终输出必须包含：

- `environment=SYNTHETIC_X2`
- `synthetic_only=true`
- `test_run_id`
- `source_fixture_sha256`
- `real_commerce_pilot_started=false`

任何字段缺失时，状态不得升级为可供人工商业交付的候选。

### R1.3 付款证据语义

- synthetic 路径固定命名为 `synthetic_programmatic_mark_paid`。
- 真正的 `confirmManualPayment` 必须绑定 approver、evidence SHA、时间和订单。
- evidence SHA 不只做格式检查；必须绑定一个已登记、可复核的本地证据对象。
- 重复同证据调用幂等；不同证据、不同订单或已冲突状态 fail-closed。

### R1.4 原子性与幂等

- 使用稳定的 `test_run_id`/idempotency key。
- Product、Order、Payment、Entitlement 与 Receipt 的重复执行必须返回同一逻辑结果。
- 中间失败不得留下“已付款但无 Entitlement”或“有 Entitlement 但无 Receipt”的半成品。
- 增加 replay、冲突和故障注入测试。

### R1.5 可复核证据

- 在官方支持的 Node 22 LTS 上重建。
- 锁定 Medusa Tag、npm integrity、PostgreSQL digest 和 pnpm lockfile。
- 生成源码 SHA manifest、依赖清单/SBOM、测试命令、退出码和脱敏日志摘要。
- 删除 PostgreSQL 数据目录后完整重建并重跑 X2。

## 4. 阶段门

| Gate | 必须满足 | 失败结果 |
|---|---|---|
| R1 Policy Gate | 所有 Entitlement/Receipt 只能通过事务化策略入口创建 | `BLOCKED_POLICY_BYPASS` |
| R2 Provenance Gate | synthetic provenance 持久化并出现在所有终态输出 | `BLOCKED_PROVENANCE` |
| R3 Replay Gate | 重放、冲突和故障注入无部分状态 | `BLOCKED_IDEMPOTENCY` |
| R4 Evidence Gate | source/lock/SBOM/commands/results 全部哈希绑定 | `BLOCKED_EVIDENCE_BINDING` |
| R5 Independent Audit | 新会话只读复核上述四门 | `INDEPENDENT_AUDIT_FAIL` |
| R6 Human Decision | Jovi 决定是否 supersede R12 和创建正式仓库 | `NO_PRODUCTION_ADOPTION` |

## 5. 独立审核时机

当前不再重复审核。完成 R1–R4、冻结新的审阅包后，再开启全新会话执行 R5。审核 Agent 不得修改文件、运行真实平台动作或把 synthetic 证据解释为生产证明。

## 6. 当前阻塞与未授权事项

当前阻塞不是 PowerShell 确认，而是代码边界尚不安全。尚未授权：正式 Medusa 仓库、生产部署、真实支付、真实客户、Storefront、n8n Track I、闲鱼动作、远程仓库、R12 superseding Decision。

## 7.1 Git 交付阻塞（2026-08-30）

Jovi 已明确要求后续提交远端并合并主分支，但当前 `E:\project\jovi-automation\.git` 为空目录，`git rev-parse` 失败，且未配置任何 remote URL。不能猜测远端、不能将隔离目录直接当作主工程 Git 历史、不能在目标不明时初始化并推送。执行 Git 交付前必须由 Jovi 提供准确 remote URL，并确认目标仓库的 `main` 分支策略；随后才可在受控范围内初始化/建立提交、推送候选分支、执行 merge 和回读远端结果。

## 8. 后续执行顺序

1. 本轮更新框架、长期知识与审核提示。
2. 新实施会话提交精确代码修改范围，取得 Jovi 授权。
3. 完成 R1–R4 修复及新证据冻结。
4. 使用独立审核提示开启新会话执行 R5。
5. 审核 PASS 后，由 Jovi 作一次汇总 R6 Decision。
6. Git 交付：获得 remote URL 与 main 策略后，单独建立 Git 交付计划；知识库和证据提交不得替代 R6 adoption Decision。
