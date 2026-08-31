# Medusa R2 独立审阅 R1 结果

**日期：** 2026-08-31
**审核对象：** `workspace/review-queue/commerce-v1/medusa-v2-spike-remediation-r2/`
**package manifest SHA：** `da31915c0fa11935ff262593ad06c926af927a6d4c23f73ecb65c95dd64145e3`
**结论：** `MEDUSA_SPIKE_FAIL`
**生产集成：** `production_integration_allowed=false`

本文件是新会话的只读独立审阅记录，不是 Approval、Decision，也不覆盖或删除旧失败包。审阅复算确认冻结包 103/103 成员、源码快照 70/70 成员和 source snapshot tree SHA `a232a05f8d1c28f861c3a850fea3f5a6c8fbe061f259244c8727378d98944cab` 一致；失败来自行为和证据门，而不是清单漂移。

## 阻断发现

1. **R1 策略边界 FAIL（Critical）**：`runSyntheticIssuance` 接受普通 `transactionId/runId`，自身没有重新读取并验证 Medusa Order/PaymentCollection；付款校验只在 workflow step。进程内调用者可伪造 context 后直接触发持久化。
2. **R3 进程恢复 FAIL（High）**：现有故障测试替换应用内方法抛错，没有 backend/worker 进程中止、数据库中断和重启后的持久恢复证据；中间写入窗口仍可能留下 `RECOVERY_PENDING` 与半成品。
3. **R4 运行闭合 FAIL（High）**：测试结果记录了 `jovi-medusa-r2-backend:local`，但环境证据没有可复核的 backend image ID/digest、build receipt 和源码/lock 到运行镜像的绑定。
4. **R4 许可证 FAIL（High）**：`admin-bundler`、`admin-sdk`、`admin-shared`、`admin-vite-plugin` 仍是待核验 Unknown；SBOM 还没有完整覆盖这四项。
5. **网络/管理端为非阻断缺口（Medium）**：宿主机 edge 确实为 `127.0.0.1:19001`，backend/db/Redis 无宿主端口且内部外网探测为 `ENETUNREACH`；但容器内监听与交互式 Admin 浏览器 smoke 尚未独立证明。

## 修复要求

- 将签发写入封闭为 workflow capability，并在策略入口自身重读、交叉校验 Order、PaymentCollection、资产、权利和付款证据；普通 context 必须拒绝。
- 在冻结镜像中记录 build 命令、实际 image ID/digest、源码树、lock/integrity 与测试进程证据；证据包必须能从清单闭合复核。
- 为四项 Admin 依赖补齐一手许可证、purl、integrity 和 SBOM 条目，无法核实则保持失败。
- 使用受控进程 kill/restart 或等价持久故障注入，证明 `RECOVERY_PENDING` 只可恢复为同一单一终态或明确失败/补偿，不能重复付款或生成半成品。
- 交互式 Admin smoke 单独记录；在所有阻断项关闭前不得发出 adoption PASS、生产 Decision 或创建正式 Medusa 仓库。

## 当前处置

旧 R2 冻结包保持不可变。本轮修复必须在新的隔离 revision 中进行，重新生成 source/package manifest、SBOM、测试和审阅包；新的审阅仍需独立执行。R12、Hook、闲鱼、真实付款、remote 和生产目录不在范围内。
