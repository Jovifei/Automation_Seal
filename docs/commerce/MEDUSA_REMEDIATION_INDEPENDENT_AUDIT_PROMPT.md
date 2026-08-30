# Medusa 修复后独立审核 Prompt

> 仅在 R1–R4 修复和证据冻结完成后使用。

```text
这是同一个项目：E:\project\jovi-automation。

请执行一次全新的、只读、独立 Medusa Adoption Audit。不要继承候选生成者的结论，不要修改任何文件，不要签发 Approval/Decision，不要执行真实支付、闲鱼、邮件、Webhook、外网下载、发布、交付、remote 或 Hook 操作。

必读：
1. E:\project\jovi-automation\AGENTS.md
2. E:\project\jovi-automation\docs\commerce\MEDUSA_ADOPTION_FRAMEWORK.md
3. E:\project\jovi-automation\docs\commerce\oss-reuse\README.md
4. 最新 Medusa remediation review package 及其 source manifest、lockfile/SBOM、test results、oracle comparison、license review 和 SHA sidecar
5. 当前隔离 Medusa 源码；只读复算所有关键 SHA

必须独立检查：
- Entitlement/DeliveryReceipt 是否只能经事务化策略 Workflow 创建，是否仍有 CRUD 绕过路径。
- 付款确认是否重新读取并验证 Medusa Order/PaymentCollection 和已登记 evidence；synthetic mark-paid 是否与人工付款严格区分。
- Asset、Entitlement、Receipt、stdout/report 是否都持久化 synthetic_only、environment、test_run_id、fixture SHA，并保持 real_commerce_pilot_started=false。
- replay、重复同证据、冲突证据、错误 SHA、未付款、非法 rights、路径遍历、未知文件和故障注入是否 fail-closed 且无部分状态。
- Backend/Admin/PostgreSQL 是否只监听 loopback；是否没有 Storefront、真实 Provider、外部动作或真实数据。
- Node/Medusa/PostgreSQL/pnpm 版本、Tag/Commit/integrity/digest、源码 manifest、lockfile、SBOM、命令、退出码与测试结果是否可复核且相互绑定。
- Python oracle 是否仅作验收参考，不是 Medusa 运行依赖；哈希差异是否有明确规范化契约。
- R12 是否仍未执行；没有 Jovi 新 Decision 时不得宣称已 superseded。

输出必须包含：
1. 最终判定：MEDUSA_SPIKE_PASS / MEDUSA_SPIKE_PASS_WITH_GAPS / MEDUSA_SPIKE_FAIL。
2. Critical、High、Medium、Low findings，逐项给出文件、行号、机制、风险和所需修复。
3. 每个 R1–R4 Gate 的 PASS/FAIL 与证据路径。
4. 明确回答 production_integration_allowed 是否为 true；没有完整证据时必须为 false。
5. 明确区分：静态检查、单元测试、数据库集成、runtime、Admin UI、synthetic、真实平台和生产证明。

不要因为命令退出码为 0 就判定通过，也不要把候选报告或 SHA sidecar 当成对源码和运行证据的充分绑定。
```
