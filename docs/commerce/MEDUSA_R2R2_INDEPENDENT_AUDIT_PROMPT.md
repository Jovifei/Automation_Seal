# Medusa R2-R2 独立审核 Prompt

> 仅在 R2-R1 冻结 + R2-R2 gap 关闭与证据冻结后使用。

```text
这是同一个项目：E:\project\jovi-automation。
当前 Jovi 已单独授权将本项目受控文档提交到 https://github.com/Jovifei/Automation_Seal.git 的 root Git；这不授权修改根 Commerce 目录、生产部署、Stripe、Storefront 公网暴露、自动交付、闲鱼动作或 R12 supersede。

请执行一次全新的、只读、独立 Medusa R2-R2 Adoption Audit。**不要继承候选生成者（R2-R2 Commerce Landing Executor）的结论，不要修改任何文件，不要签发 Approval/Decision，不要执行真实支付、闲鱼、邮件、Webhook、外网下载、发布、交付、remote、Hook 或生产集成操作。**

必读：
1. E:\project\jovi-automation\AGENTS.md
2. E:\project\jovi-automation\docs\commerce\MEDUSA_ADOPTION_FRAMEWORK.md
3. E:\project\jovi-automation\docs\commerce\oss-reuse\README.md
4. E:\project\jovi-automation\docs\commerce\MEDUSA_R2_INTEGRATION_POINTER.md
5. E:\project\jovi-automation\docs\commerce\MEDUSA_R2_INDEPENDENT_AUDIT_R2_RESULT.md（R2-R1 审核基线）
6. 固定审核对象：`E:\project\jovi-automation\workspace\review-queue\commerce-v1\medusa-v2-spike-remediation-r2-r2\`
   - package manifest SHA `a1e07b28ac3ec3753e55da20b342f911a54b6bd3de1492b13d9b7ae5434009e5`，135 个成员
   - source snapshot tree SHA `e533f0ce0010cc0f75848b9854d8ccd4da364768f31174349d8981827342f8aa`，74 个成员
   - source snapshot manifest SHA `186c836b9996a9e22f0bb86018c20db7854a1d9936180b134ad1638928ec3753`
   - pnpm lockfile SHA `9855eabfc4fc37d916af0ac64585f15594b44a90dc6d8488d594789956237119`
   - backend image ID `sha256:19da68692a32b02d98ada22d8a83633600978c2d19823c7aa104a43c8ac1ad62`、manifest digest `sha256:31a3e509a7cb67c01f31cdb310ff108f659de0d2b83352c80777b94fd0498ff3`、image labels `org.opencontainers.image.source-tree-sha=e533f0ce...` `org.opencontainers.image.lock-sha=9855eabf...` `org.opencontainers.image.medusa-version=2.19.0`
   - Medusa 2.19.0；Node 22.17.1-bookworm-slim；PostgreSQL 16-alpine `sha256:cf78e76683b9ca8c5733cbbdce6c9262b45b6767934dd0a95e671f9a0fc20685`；Redis 7.2.11-alpine `sha256:1cd18c9774579b583415e2a1ce464f183e5ed15203c5d8195dcfc6b9dc710cd1`
7. R2-R1 冻结包（必须保持不可修改）：`workspace/review-queue/commerce-v1/medusa-v2-spike-remediation-r2-r1/`，package manifest SHA `748ec4bcc2eb7061b2280ef367e43fcc0458bb21ff46583aacf882e1cd90a4c6`、source tree SHA `d15eb73e94a1fcf8b19ac2c8e03b317fa5ea94f7d8242548aa3eac4dec334e8d`
8. 上述 R2-R2 审核包及其 source manifest、source snapshot manifest、package manifest、lockfile、SBOM、test results、replay/concurrency/negative/recovery/oracle 证据、jest shutdown 证据、admin browser 证据、license review、admin license scope、gate matrix、adoption decision 与逐文件 SHA sidecar
9. 隔离 Medusa 源码：E:\Claude_allow\Download\jovi-medusa-v2-spike-r2-r2\（不要修改）；只读复算所有关键 SHA

必须独立检查：
- R1 策略/写入口：service.ts 中 capability mint 是否仍为词法私有、是否只通过事务化 workflow 写入 Entitlement/Receipt；R2-R2 新增的 `apps/backend/src/api/admin/jovi-commerce/receipts/route.ts` 是否严格只读（无 create/update/delete）。
- R2 provenance：synthetic provenance（environment/synthetic_only/test_run_id/source_fixture_sha256/real_commerce_pilot_started）是否在所有终态持久化。
- R3 事务/恢复：RECOVERY_PENDING + Backend PID1 SIGKILL + 120 秒重放单一 Entitlement/Receipt 证据是否可复算。
- R4 证据：74 项 source、117→135 项 package、image/lock labels、oracle 7/7、SBOM、license scope 可复算。
- 初始源树 SHA 匹配（任务第 III 条）：`MEDUSA_R2R2_INITIAL_SOURCE_PROOF.json` 记录 reconstructed initial source tree SHA == R2-R1 audited source SHA `d15eb73e...`，delta 仅 3 处文档化变更（M1 package.json、L1 新增 receipts route.ts、隔离改名 docker-compose.r2.yml）、`undocumented_drift_entries=0`；可用 `tools/prove_initial_source.py` 或等效只读方法独立复算。
- M1 Jest natural shutdown：Run A/B/C（unit + integration）全部 exit_code=0、自然退出、open_handles=0、forced_exit=false、--detectOpenHandles 诊断无 handle 报告。
- L1 Admin 浏览器冒烟：Chromium headless 启动、/app 200、login page 渲染（React/i18next）、synthetic admin 鉴权 round-trip（/auth/user/emailpass 200 + /auth/session 200）、匿名 /admin/* 401、external_requests=0、pageerror=0；并独立评估"dashboard React 客户端在 auth API 200 后跳回 /app/login"这一未关闭的 Low 缺口是否需要进入下一轮 R2-R3 修复，还是可由独立审核签署为可接受。
- Backend/Admin 边界：仅 loopback（Admin 通过 127.0.0.1:19003 → backend:9000）；backend 容器无宿主机端口；ENETUNREACH 外部探测。
- 版本与 digest：Node 22.17.1 / pnpm 10.32.0 / Medusa 2.19.0 / Tag `v2.19.0`、Commit `87d77fa1b56ec287aa6655aaa2f54245387aa2f2`、四 Admin 包 tarball/integrity/MIT scope 与 Enterprise 排除路径的逐项对比。
- Python oracle 仅作验收参考；非 Medusa 运行依赖；per-file SHA 7/7 相等；package ZIP 字节差异的规范化契约是否被显式记录。
- R2-R1 frozen 证据未被改写；R12 Git baseline/import 仍未执行；没有 Jovi 新 Decision 时不得宣称已 superseded。
- `production_integration_allowed` 必须为 false 除非有完整独立证据链；本轮不得修改它。

输出必须包含：
1. 最终判定：MEDUSA_R2R2_PASS / MEDUSA_R2R2_FAIL。**不允许** PASS_WITH_GAPS；若 L1 INCOMPLETE 仍存在但已记录清晰 finding + backend auth 链路证明，且其余 gate 全部 PASS，则可判 PASS 并将 L1 finding 记为需在 R2-R3 关闭的 Low 残留；否则判 FAIL。
2. Critical、High、Medium、Low findings，逐项给出文件、行号、机制、风险和所需修复。
3. 每个 Gate（R1–R4、M1、L1）的 PASS/FAIL 与证据路径。
4. 明确回答 `production_integration_allowed` 是否为 true；没有完整证据时必须为 false。
5. 明确区分：静态检查、单元测试、数据库集成、runtime、Admin UI、synthetic、真实平台和生产证明。
6. 独立交叉复算至少 5 个 source SHA、3 个 license tarball SHA、2 个 oracle fixture SHA、image label SHA 是否匹配。

不要因为命令退出码为 0 就判定通过，不要把候选报告或 SHA sidecar 当成对源码和运行证据的充分绑定。
```

## 引用证据速查（仅供审核时 cross-check，不替代独立复算）

| 项 | 路径 / SHA |
|---|---|
| Source tree SHA | `e533f0ce0010cc0f75848b9854d8ccd4da364768f31174349d8981827342f8aa` |
| Source snapshot manifest SHA | `186c836b9996a9e22f0bb86018c20db7854a1d9936180b134ad1638928ec3753` |
| Package manifest SHA（135 项） | `a1e07b28ac3ec3753e55da20b342f911a54b6bd3de1492b13d9b7ae5434009e5` |
| Initial source SHA match proof | `MEDUSA_R2R2_INITIAL_SOURCE_PROOF.json` — verdict `R2R2_INITIAL_SOURCE_SHA_MATCH_PROVEN`（initial == `d15eb73e...`，undocumented drift = 0） |
| pnpm lockfile SHA | `9855eabfc4fc37d916af0ac64585f15594b44a90dc6d8488d594789956237119` |
| Backend image ID | `sha256:19da68692a32b02d98ada22d8a83633600978c2d19823c7aa104a43c8ac1ad62` |
| Backend image manifest digest | `sha256:31a3e509a7cb67c01f31cdb310ff108f659de0d2b83352c80777b94fd0498ff3` |
| R2-R1 frozen package SHA（参考） | `748ec4bcc2eb7061b2280ef367e43fcc0458bb21ff46583aacf882e1cd90a4c6` |
| R2-R1 frozen source SHA（参考） | `d15eb73e94a1fcf8b19ac2c8e03b317fa5ea94f7d8242548aa3eac4dec334e8d` |
| M1 verdict | `JEST_NATURAL_SHUTDOWN_PASS` |
| L1 verdict | `ADMIN_INTERACTIVE_SMOKE_INCOMPLETE`（带 finding；由审核裁定 PASS 或 R2-R3 关闭） |
| candidate_verdict | `READY_FOR_INDEPENDENT_R2R2_AUDIT` |
| production_integration_allowed | `false` |
