# GitHub 治理计划 — Governance 与 Commerce Runtime

**最后校准：2026-09-05**  
**状态：CURRENT / PARTIALLY IMPLEMENTED**

## 1. 当前远端现实

### Automation_Seal
Repo：`Jovifei/Automation_Seal`

本轮文档校准前核验：
- default branch：`main`
- `main` 未启用 branch protection / required checks；
- 当前 C3/C4 工作在 `commerce-c3-real-sku-readiness-20260905` / PR #5；
- C3 Reference QA 已在 PR 分支实际运行并 PASS。

因此本文件不再是“R6 前 plan-only”；Governance repo 已真实存在并持续使用，但 branch protection 仍是未完成项。

### Commerce Runtime
本地：`E:\project\jovi-medusa-commerce-v1`

reported C3 promoted main：`63db06e9fd2e1cbdf6e7926b48ba72d3fbe06cb1`。

是否已有 dedicated GitHub repo/remote：**必须现场检查，治理仓无法证明。**

推荐准确目标仍为：
`Jovifei/jovi-medusa-commerce-v1`

但任何 Agent 在没有 Jovi 明确 remote URL 前不得猜测或 push。

## 2. Automation_Seal 当前目标保护

`main` 应配置：
- Require pull request before merging；
- 至少 1 个 Jovi review（如果个人仓/计划能力允许）；
- Dismiss stale reviews；
- Require current docs/reference QA checks；
- Prohibit force push；
- Prohibit deletion。

当前 C3/C4 文档应通过 PR #5 收口，不应继续直接 push `main`。

## 3. Governance Required Checks

建议当前至少要求：
- C3 Reference QA / 后续阶段对应 reference QA；
- Markdown/JSON parse；
- verifier self-tests；
- secret scan；
- 文档 current/historical link sanity（后续可新增）。

Governance CI 不需要运行全部 Medusa Runtime integration；Runtime 应在独立 repo 执行自己的完整 checks。

## 4. Runtime 分支模型

Runtime dedicated remote 建立后：
- `main`：唯一正式主线；
- `feature/*`：短生命周期；
- 不建立第二条长期生产分支；
- 历史 `development` 若保留，只作历史 ref。

C3 后 local `main` 已 reported promoted 到 audited closure，所以首个 remote main 应与该 audited main 精确一致，不应从旧 baseline `8290392...` 建仓。

## 5. Runtime Required Checks

最低：

| Check | 内容 |
|---|---|
| typecheck | `tsc --noEmit` |
| unit | Jest natural exit |
| integration | PostgreSQL/Redis loopback integration |
| regression | C2/C3 current regression |
| replay/recovery | exactly-once / restart recovery |
| negative | fail-closed suites |
| deterministic package | same input -> same bytes/SHA |
| secret scan | Gitleaks + existing scanner |
| SBOM | Syft source/image |
| license/provenance | source/lock/SBOM/license manifest |
| admin e2e | Playwright cookie-session |

Trivy / harden-runner / dependency-review 可在 remote 稳定后逐步加入，不阻塞 C4 首单 Pilot。

## 6. CODEOWNERS / Review

Runtime 高风险路径建议要求 Jovi review：
- `apps/backend/src/modules/jovi-commerce/**`
- migrations；
- auth/session/config；
- delivery/download grant；
- license/provenance；
- CI/security workflows。

Governance 高风险路径：
- Human Decision；
- Approval/Gate；
- current state；
- C4 Pilot Decision / permission expansion。

## 7. Release / Pilot 分离

C4 Pilot 不等于自动 release pipeline。

当前第一 SKU 是 reported `0.2.0-dev` + unsigned installer。是否先创建 stable/tag/signing 由 Jovi 商业决定。

Pilot 如果以 beta/dev 方式执行：
- 商品文案透明；
- package SHA 固定；
- 不通过 CI 自动发布闲鱼；
- 不自动上传客户可见 artifact。

## 8. 禁止

- 把 Runtime 源码推入 Automation_Seal；
- 因 GitHub Actions PASS 自动签发 Human Decision；
- 因 C4 Pilot 开始自动开放 Xianyu/Payment/Delivery；
- 把 secrets/runtime DB/customer data 上传 GitHub；
- 通过 force push 重写 audited history。

## 9. 当前下一步

1. 清理 PR #5 中 C4 Draft Kit/历史 mirror；
2. 确认 CI；
3. 通过 PR merge 当前 Governance docs 到 main；
4. 为 Automation_Seal main 配 branch protection；
5. 现场核 Runtime remote；如无，由 Jovi 创建/确认 dedicated repo；
6. 将 audited Runtime main 推到 dedicated repo 后验证 remote SHA/checks；
7. 再进入 C4 Human Pilot Decision。
