# Medusa R5 独立审核接收与复核

更新日期：2026-08-31。当前结论：`MEDUSA_SPIKE_FAIL`，`production_integration_allowed=false`。

本记录接收 Jovi 提供的独立审核，并纠正此前 `READY_FOR_INDEPENDENT_AUDIT` 和 R1–R4 已完成的表述。它不是 Approval、Decision，也不是新修复验收报告。旧候选包保留原状。

## 已直接复核的问题

1. **策略入口绕过（C-01）**：`service.ts` 的公开 `persistVerifiedDelivery` 接受调用者付款状态；只阻断两个 create；通过 `BaseService.prototype` 执行底层写入；没有跨整个流程的事务证明。顺序调用和 try/catch 补偿不能证明崩溃或并发安全。
2. **付款与证据未绑定（C-02）**：`policy-command.ts` 只读 PaymentCollection 状态和 metadata 中的 order_id，没有在策略入口校验真实 Order、金额、商品以及已登记证据对象。
3. **fixture 不真实（H-01）**：`jovi-x2.ts` 的资产和 fixture SHA 仍为重复字符常量；路径前缀校验不等于文件存在性、内容 SHA 或权利凭证验证。
4. **重放证明不足（H-02）**：现有顺序双跑与进程内补偿测试不能证明跨进程、崩溃、并发和全部中间失败状态。
5. **清单不闭合（H-03）**：目录 19 个文件，清单列 16 项，加两个清单自文件仍遗漏 `GIT_DELIVERY_BLOCKER.md`。源码清单仅 13 项，未涵盖配置、迁移、入口和 seed。
6. **运行时不符（H-04）**：现场查询 19000 监听进程路径为系统 `C:\Program Files\nodejs\node.exe`，版本 v24.18.0。直接执行隔离 Node v22.17.1 时，解析 `@medusajs/utils` 得到 `MODULE_NOT_FOUND`。用 Node 22 启动 pnpm 并不证明子进程仍使用 Node 22。
7. **输出与回读校验不足（M-03）**：输出接收 any 并展开输入；已有记录返回路径未完整重验 provenance、商品和 receipt 属性。

## 需要保留区别的结论

- **Git 漂移（H-05）可归因**：初始化与两次 push 是本会话按 Jovi 后续授权执行；当前本地 main 为 `73768c20c55d0c29d69597bbf975844ff3c6287f`。审核 Agent 未执行这些操作。虽然有授权，同时改变审核对象仍使审核基线失效。没有理由因此回滚、清理 Git 或再次推送。
- **上游 Tag 与 npm gitHead**：两个不同值本身还不能证明包不可信；需核对发布流程及归档、包 integrity、lock 与安装树的映射，当前记 `NOT_VERIFIED`。
- **许可证 inventory**：不得继续把 `pnpm licenses list` 输出称为标准 SBOM。报告中的 Unknown 数量与组件许可需要逐项复核。
- **Provider**：依赖树包含 Provider 与配置启用 Provider 是不同事实；没有配置启用不能自动证明运行期间无外连。

## 后续整改验收顺序

1. 先建立能复现 C-01/C-02/H-01/M-03 的拒绝用例：绕过入口、无效或未登记 SHA、未知文件、伪造订单金额、污染后的已有记录。
2. 使用 Medusa 提供的 Workflow、事务与持久化恢复机制修复策略边界；以并发、跨进程和崩溃恢复实证验收，不能仅把函数改名或增加外层 wrapper。
3. 读取实际 allowlisted fixture 与文件内容计算 SHA；证据与权利对象可查询、可校验；synthetic 与人工付款路径分开验收。
4. 固定实际执行程序及子进程运行时，修复直接依赖声明，重新建立可复现的测试环境。
5. 从完整运行输入清单生成 source inventory 和标准 SBOM，绑定真实命令、退出码、stdout、测试及运行结果。明示排除项，不覆盖旧失败包。
6. 在整个审核期间冻结被审源码与证据，修复完成后再开启一次新的独立审核。

本轮只完成审核接收和状态纠正。上述实现缺陷尚未修复；原 12/12、4/4 和顺序重放是历史候选报告，不构成当前 R1–R4 通过证据。
