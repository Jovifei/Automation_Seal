# JOVI-MEDUSA-R6-CONTROLLED-ADOPTION-DECISION-V1

**Decision 类型：** Human Decision（Jovi 人工签发，非自动生成）
**issued_from_human：** `true`
**签发人：** Jovi
**签发日期：** 2026-09-02
**记录性质：** 本文件是 Jovi 于 2026-09-02 会话中逐字签发的 Decision 的正式落盘记录；执行 Agent 仅做记录与绑定验证，未改写任何决定内容。

---

## 签发原文（逐字记录）

我作为 Jovi，本人现在签发：
`JOVI-MEDUSA-R6-CONTROLLED-ADOPTION-DECISION-V1`
依据：
* Candidate branch: `r2r2-gap-closure-and-r6-adoption-prep-20260901`
* Independent Audit commit: `6e59863787dfa73348971c694b774e5712950879`
* Independent Audit result: `MEDUSA_R2R2_PASS`
* R2-R2 package manifest SHA256: `a1e07b28ac3ec3753e55da20b342f911a54b6bd3de1492b13d9b7ae5434009e5`
* R2-R2 final source tree SHA256: `e533f0ce0010cc0f75848b9854d8ccd4da364768f31174349d8981827342f8aa`
* R2-R1 audited source baseline SHA256: `d15eb73e94a1fcf8b19ac2c8e03b317fa5ea94f7d8242548aa3eac4dec334e8d`

我接受 Medusa v2.19.0 作为 Jovi Automation Commerce Core 的正式技术基础。

本 Decision 仅授权：
1. 创建新的正式受控 Commerce 仓库：`jovi-medusa-commerce-v1`
2. 从 R2-R2 已审计源码中按 exact import manifest 导入明确批准的源码子集。
3. 导入并冻结：pnpm lockfile、migrations、Docker/Compose、tests、SBOM、LICENSE inventory、provenance、source manifest、rollback manifest。
4. 建立：CI、PR-only main 计划、required checks、secret scan、license/SBOM checks、provenance/manifest validation、deterministic build checks。
5. 在正式仓内重新执行完整 synthetic Commerce 验证。
6. 完成后提交新的独立 Post-Import Audit。

本 Decision 明确不授权：
* production deployment
* real payment
* Stripe
* real customer data
* public Storefront
* automatic delivery
* Xianyu publish
* Xianyu message
* Xianyu payment
* Xianyu refund
* n8n production
* R12 superseding Decision

当前：`production_integration_allowed=false` 仍保持。
R2-R2 独立审核记录的 Admin cookie-session Low residual 必须在后续 R2-R3 / staging 阶段关闭，不得遗忘。

执行顺序：
R6 Decision freeze → create controlled Commerce repo → exact audited import → full synthetic regression → independent Post-Import Audit → Admin session closure → full synthetic commerce E2E。
不得直接进入真实平台动作。

执行：`JOVI-COMMERCE-R6-CONTROLLED-REPO-ADOPTION-AND-IMPORT-V1`

---

## 绑定验证（Executor 记录，2026-09-02）

| 绑定项 | Decision 值 | 磁盘/远端实测 | 结果 |
|---|---|---|---|
| Candidate branch HEAD | `6e59863...` | 本地与 `git ls-remote` 均为 `6e59863787dfa73348971c694b774e5712950879` | ✓ |
| R2-R2 package manifest SHA | `a1e07b28...` | sidecar + 全量重算一致（135 项） | ✓ |
| R2-R2 final source tree SHA | `e533f0ce...` | canonical 算法重算一致（74 项） | ✓ |
| R2-R1 baseline SHA | `d15eb73e...` | 冻结包重算一致（73 项） | ✓ |
| Medusa tag/commit | v2.19.0 / `87d77fa1...` | `MEDUSA_R2R2_ADMIN_LICENSE_SCOPE.json` 绑定一致 | ✓ |
| lockfile SHA | `9855eabf...` | 快照与隔离源现场一致 | ✓ |

授权边界确认：仅限本 Decision 列出的 6 项授权；12 项不授权事项全部维持禁止；`production_integration_allowed=false` 不变。
