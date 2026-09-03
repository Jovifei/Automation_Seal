# Commerce R2-R3 OSS 加速复用评审（2026-09-03）

**状态：** `SOURCE_VALIDATED_READY_FOR_LOCAL_APPLICATION`

**基线：** `Automation_Seal` 候选线 `85401855c24b83e0dea035b0f225fc5a9fbba563`，对应 R6 受控导入已完成、受控仓停在 `READY_FOR_R6_POST_IMPORT_INDEPENDENT_AUDIT`。

本文件不声称远端已经验证 `E:\project\jovi-medusa-commerce-v1` 的本地运行结果。远端只完成开源来源、版本行为和吸收边界核对；实际应用和运行验证必须由本地 Codex 在受控仓执行。

## 1. 当前工程审核结论

按现有 R6 Decision / STATUS 证据，受控导入在证据层满足计划：

- Jovi R6 Human Decision 已绑定 R2-R2 独立审核 `MEDUSA_R2R2_PASS`；
- 授权范围仅限正式受控仓、exact audited import、tests/SBOM/license/provenance/CI、完整 synthetic 重验与独立 Post-Import Audit；
- 真实 production/payment/Stripe/customer/Storefront/auto-delivery/Xianyu/n8n-prod/R12 仍禁止；
- 受控仓记录为 74-file exact byte import，source tree `e533f0ce...`，synthetic regression PASS；
- 当前正确停止点仍是 `READY_FOR_R6_POST_IMPORT_INDEPENDENT_AUDIT`。

因此：**R6 导入不应推倒重做。下一轮只做 Post-Import 独立审核 + R2-R3 Low 残留关闭 + 正式仓 CI 加固。**

## 2. 值得直接吸收的开源项目

### A. `medusajs/medusa` — DIRECT_REUSE_REFERENCE（立即）

用途：关闭 R2-R3 Admin session-cookie Low finding。

固定参考：Medusa `v2.19.0`。

已核对官方源码：

- `packages/medusa/src/api/auth/session/route.ts`：POST 只执行 `req.session.auth_context = req.auth_context`，然后返回 200；
- `packages/core/framework/src/http/express-loader.ts`：production/staging 默认 session cookie `secure=true`、`sameSite="lax"`；`cookieOptions` 在默认项之后 spread，可为受控本地测试覆盖；
- 官方 Admin auth integration test 直接断言 `/auth/session` 响应含 `Set-Cookie` 且 cookie 名含 `connect.sid`；
- 官方 API reference 也明确把 `/auth/session` 定义为获得 cookie session 的入口。

**对 Jovi 的直接结论：** 当前 loopback Admin 用 `127.0.0.1` HTTP，同时后端按 production 运行；此拓扑和 Medusa 默认 `secure=true` cookie 规则冲突，足以解释“200 但不下发 Set-Cookie”。

吸收策略：

- 不 fork Medusa；
- 不改上游 session route；
- 只在 Jovi synthetic-loopback 配置中显式 `cookieOptions.secure=false`，并强制 `sameSite="lax"`、`httpOnly=true`；
- 该覆盖必须由独立环境变量开关控制，只允许 `127.0.0.1` / synthetic；未来真实 HTTPS 环境不得继承该覆盖；
- Playwright 验收必须捕获真实 `Set-Cookie`、浏览器 cookie jar、`/admin/users/me` cookie-session 200、Products/Orders/Receipts 导航。

### B. `microsoft/playwright` — DIRECT_REUSE_TESTING（立即）

用途：把当前 Admin smoke 从“API + 页面加载”升级为真实浏览器会话验收。

吸收：

- 登录表单；
- 网络事件捕获；
- `Set-Cookie` / cookie jar；
- console/pageerror/failed request；
- Product / Order / Receipt UI；
- refresh 后 session 持续性；
- 强制 external request = 0。

不复制 Playwright 源码，仅使用官方 package 与测试模式。

### C. `gitleaks/gitleaks` — DIRECT_REUSE_CI（立即）

用途：替代/补强自研 secret regex 扫描。

吸收：

- Git diff / full history secret scan；
- fail-on-finding；
- 允许项目自己的 `.gitleaks.toml`；
- CI 中固定版本/commit，不使用浮动 latest。

自研扫描保留为辅助；Gitleaks 成为正式仓 required check 候选。

### D. `anchore/syft` — DIRECT_REUSE_SBOM（立即）

用途：从手工/项目脚本 SBOM 升级为通用文件系统与镜像 SBOM 生成。

吸收：

- source tree SBOM；
- backend image SBOM；
- CycloneDX JSON；
- 输出自身 SHA256；
- 与现有 R6 SBOM 做 semantic/component diff。

现有 CycloneDX 证据不删除，Syft 作为第二实现交叉验证。

### E. `aquasecurity/trivy` — DIRECT_REUSE_SECURITY_SCAN（R6 Post-Import 后启用）

用途：镜像、filesystem、misconfiguration、已知漏洞扫描。

边界：

- 先作为非生产 CI；
- HIGH/CRITICAL 设 fail-closed；
- 数据库下载/缓存行为单独记录；
- 不把一次 Trivy PASS 等同于 license/provenance PASS。

### F. `step-security/harden-runner` — ADOPT_AFTER_REMOTE_REPO（条件采用）

用途：GitHub Actions runner egress / supply-chain hardening。

前提：`jovi-medusa-commerce-v1` 正式远端创建后才接入。所有 action 必须 pin 到 commit SHA，不使用 floating tag。

### G. `actions/dependency-review-action` — CONDITIONAL

用途：PR 依赖变更门禁。

是否能用于目标仓取决于仓库 visibility / GitHub 许可能力，接入前由本地 Codex/Owner 实测；不可把不可用的 SaaS 功能写成已启用。

### H. `slsa-framework/slsa-github-generator` — DEFER

价值高但现在不是最短路径。等正式 release artifact / tag 流程出现后再引入 provenance attestation，避免在 synthetic 主线尚未闭合时扩大 CI 复杂度。

## 3. 不建议当前吸收

- 再换 Commerce 核心（Saleor/Vendure/Kill Bill）：无必要；Medusa 已经独立审核 PASS 并正式 Adopt。
- Storefront starter：当前 public Storefront 未授权，先不引入。
- Stripe / payment provider：真实付款未授权。
- n8n：Track I / n8n production 未授权；只保留架构候选。
- OpenMeter：没有 approved metered-product 触发条件，继续 defer。

## 4. 下一阶段最短路径

1. **先运行 R6 Post-Import Independent Audit**；若 FAIL，只修审核 finding。
2. 若 PASS，创建 R2-R3 小变更：synthetic-loopback cookie 配置 + Playwright cookie-session 测试 + 修正硬编码 auth evidence。
3. 运行完整 synthetic regression，确保 source/provenance/entitlement/recovery 均不回归。
4. 独立审核 R2-R3。
5. 再在正式仓接入 Gitleaks + Syft；Trivy、Harden Runner 作为第二批。
6. 进入 full synthetic Commerce E2E：Product Manifest → Listing Candidate → Order → Human-confirmed synthetic payment evidence → Entitlement → Delivery Package → Receipt → Human-approved Xianyu Draft。

## 5. 成功定义

本轮 OSS 吸收成功，不是“装了很多工具”，而是：

- Admin cookie-session 在 loopback synthetic 下真实通过；
- production HTTPS 默认仍保持 secure cookie；
- CI 不再依赖自研 secret/SBOM 单实现；
- 所有新增工具都固定版本、记录许可证和来源；
- 不扩大真实平台授权；
- Post-Import 与 R2-R3 均有独立审核。
