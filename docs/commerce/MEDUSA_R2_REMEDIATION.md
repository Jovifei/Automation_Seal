# Medusa v2 合成闭环修复 R2

**更新日期：** 2026-09-01
**当前状态：** `MEDUSA_SPIKE_PASS_WITH_GAPS`（R2-R1 独立审阅 R2 已完成；非生产采用）
**最终采用：** `production_integration_allowed=false`

这是一份 R2 实施记录和失败审阅后的接力记录，不是 Approval/Decision。旧 R5 与 R2 审阅 R1 的 `MEDUSA_SPIKE_FAIL` 均保留为历史事实；R2-R1 已完成修复、证据冻结和第二轮独立审阅，结论为 `MEDUSA_SPIKE_PASS_WITH_GAPS`，不等于生产采用。

## 范围与隔离

- 当前源码（R2-R1）：`E:\Claude_allow\Download\jovi-medusa-v2-spike-r2-r1\backend\jovi-medusa-backend`
- 当前证据（R2-R1）：`workspace/review-queue/commerce-v1/medusa-v2-spike-remediation-r2-r1/`；旧 R2 失败包保持原状。
- Medusa `2.19.0`；Node `22.17.1-bookworm-slim`，linux/amd64 digest `sha256:ffb27ca0f26a231a08930c872631cea70cbb318463d1e712922b5c7cfdc3fcca`。
- PostgreSQL `16-alpine` digest `sha256:cf78e76683b9ca8c5733cbbdce6c9262b45b6767934dd0a95e671f9a0fc20685`；Redis `7.2.11-alpine` digest `sha256:1cd18c9774579b583415e2a1ce464f183e5ed15203c5d8195dcfc6b9dc710cd1`，AOF 持久化开启。
- 后端、PostgreSQL、Redis 仅加入 `jovi-medusa-r2-r1-internal` 内部网络；后端没有宿主机端口。由于 Docker `internal` 网络不发布端口，独立固定 Node Admin 转发器才发布 `127.0.0.1:19002`，只转发到内部 `backend:9000`。
- 没有 Storefront、Stripe、Webhook、邮件、云存储、闲鱼、真实客户数据或自动交付。R12 Git baseline/import、root Git、remote、Hook 均未触碰。

## R1–R4 修复

| 门 | R2 实现 | 当前证据 |
|---|---|---|
| R1 策略/写入口 | 删除 `persistVerifiedDelivery`；人工付款接口只返回 `MANUAL_PAYMENT_DISABLED_IN_SYNTHETIC_SPIKE`。生成 CRUD 在服务实例上拒绝；工作流唯一调用 `runSyntheticIssuance`。 | `MEDUSA_R2_NEGATIVE_RESULTS.json`、`MEDUSA_R2_TEST_RESULTS.json` |
| R2 资产/付款证据 | 从 landing-phase1 真实 fixture 读取全量文件并按 `path/sha256/size` 规范化；证据必须带真实内容且内容 SHA 相等，逐项绑定 Order、PaymentCollection、币种、金额、商品、版本和 run。1990 minor 转 `19.90` CNY。 | `MEDUSA_R2_ORACLE_COMPARISON.json`、源 manifest |
| R3 事务/恢复 | `RECOVERY_PENDING` 在预事务中持久化；权益、Receipt、证据、资产和 READY 状态由 `@InjectTransactionManager` 同事务提交。官方 Redis Workflow Engine/locking；同 run/order 使用唯一锁 owner，重复和冲突受唯一约束保护。 | `MEDUSA_R2_RECOVERY_RESULTS.json`、`MEDUSA_R2_CONCURRENCY_RESULTS.json` |
| R4 证据/可复核 | 冻结独立源快照、完整 source manifest、CycloneDX 1.5 SBOM、实际命令/退出码/stdout/stderr、Oracle 对照、ZIP/manifest sidecar、镜像 manifest/build label、四项 Admin tarball/integrity/scope 和 117 项 package manifest。 | `MEDUSA_R2_PACKAGE_MANIFEST.json` SHA `748ec4bcc2eb7061b2280ef367e43fcc0458bb21ff46583aacf882e1cd90a4c6` |

## 实测结果

- X2 首次与独立进程重放返回相同 Product/Variant/Order/Entitlement/Receipt、package SHA 和 manifest SHA；最终状态为 `READY_FOR_HUMAN_DELIVERY`。
- 10 个并发 workflow 请求返回一个逻辑结果；包含首次 X2、并发验证和恢复样本的最终数据库计数为 Order/PaymentCollection/JoviRun/Evidence/Asset/Entitlement/Receipt `2/2/2/4/1/2/2`，Workflow execution 为 `15`。
- 负向用例包括 caller supplied payment fact、fixture source escape、人工付款、金额/Provider/币种错误；全部拒绝，数据库计数保持不变。
- Python oracle 状态 `X2_STAGING_COMMERCE_FLOW_PASS`；全量 fixture manifest `951abc2715fc9be22303c305e82185ff1fae0c79be4db709dcb33eaf8c82f1d6` 与 R2 一致，7/7 文件 SHA 一致；ZIP 字节因 R2 使用固定 metadata 的 fflate STORE 而不同，已显式记录为规范化差异。
- Backend `/health` 与 Admin `/app` 通过本地 HTTP smoke；Backend 实际 Node 为 `/usr/local/bin/node` v22.17.1，内部容器访问外网返回 `ENETUNREACH`。

## 审阅结论与剩余缺口

独立审阅 R2 已复算 117 项 package、73 项 source、镜像/lock 绑定、许可证 scope、X2 replay、并发、负测和 Backend PID1 恢复，结论为 `MEDUSA_SPIKE_PASS_WITH_GAPS`；没有 Critical/High finding。完整记录见 [R2 独立审阅 R2 结果](MEDUSA_R2_INDEPENDENT_AUDIT_R2_RESULT.md)。

1. **Medium：** Jest 仍使用 `--forceExit`；下一轮隔离验证需补无强制退出或 `--detectOpenHandles` 的自然收尾证据。
2. **Low：** Admin 目前只有 loopback HTTP smoke；下一轮隔离验证需补交互式浏览器/权限操作 smoke。
3. 该结论不授权生产 Medusa 仓库、人工付款、真实平台、闲鱼或 R12 superseding Decision；后续仍需单独的人类采用决策。

## 审核入口

独立审阅提示位于 `docs/commerce/MEDUSA_REMEDIATION_INDEPENDENT_AUDIT_PROMPT.md`；本轮结果见 [R2 独立审阅 R2 结果](MEDUSA_R2_INDEPENDENT_AUDIT_R2_RESULT.md)。审阅期间不得修改 R2 源码、证据目录或任何相关 Git 状态。

## 第一轮独立审阅结果

`MEDUSA_R2_INDEPENDENT_AUDIT_R1_RESULT.md` 记录了 `MEDUSA_SPIKE_FAIL` 的五项发现。旧冻结包保持不变；修复只能写入新的隔离 revision，完成后重新生成镜像/构建绑定、四项 Admin 许可证来源、进程恢复证据和独立审阅包。生产集成仍为 `false`。

## R2-R1 候选冻结

新候选源码为 `E:\Claude_allow\Download\jovi-medusa-v2-spike-r2-r1\backend\jovi-medusa-backend`；证据包为 `workspace/review-queue/commerce-v1/medusa-v2-spike-remediation-r2-r1/`。package manifest SHA 为 `748ec4bcc2eb7061b2280ef367e43fcc0458bb21ff46583aacf882e1cd90a4c6`（117 项），source snapshot tree SHA 为 `d15eb73e94a1fcf8b19ac2c8e03b317fa5ea94f7d8242548aa3eac4dec334e8d`（73 项）。候选已补齐词法私有 workflow capability、服务端 Order/Payment 重读、订单级锁与 120 秒恢复等待、SIGKILL 后 Backend PID1 重启重放、image manifest/build label、四项 Admin tarball/integrity/MIT scope 和完整 SBOM；独立审阅 R2 判定 `MEDUSA_SPIKE_PASS_WITH_GAPS`，剩余仅 Jest 自然收尾和交互式 Admin smoke 两项非阻断缺口。
