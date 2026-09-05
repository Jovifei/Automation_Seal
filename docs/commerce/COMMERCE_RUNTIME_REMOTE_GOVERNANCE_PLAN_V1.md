# Commerce Runtime 远端化与 CI 治理计划 V1

**状态：CURRENT / REQUIRES LIVE CHECK**  
**最后校准：2026-09-05**

## 1. 当前事实

C3 已 reported 完成：
- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`
- Jovi `JOVI_RUNTIME_C3_PROMOTION_DECISION_V1`
- Runtime local `main` reported 已 fast-forward 到 audited closure `63db06e9fd2e1cbdf6e7926b48ba72d3fbe06cb1`
- `C3_RUNTIME_PROMOTION_AUDIT_PASS`

**本治理仓无法证明 Runtime 现在是否已经配置 dedicated remote。**

因此任何 Agent 进入 C4 前必须在：

`E:\project\jovi-medusa-commerce-v1`

现场执行：

`git remote -v`

不要继续引用早期“remote=none”作为当前事实，也不要假定已经建远端。

## 2. 推荐 dedicated remote

若仍没有 remote，建议由 Jovi 明确创建/确认：

`Jovifei/jovi-medusa-commerce-v1`

public/private 由 Jovi决定。

在收到准确 remote URL 前，Agent 不得猜 URL，也不得把 Runtime 源码推入 `Jovifei/Automation_Seal`。

## 3. 首次推送前 Gate

只有以下都成立才推：
- local `main` == audited C3 promoted closure；
- post-promotion audit PASS；
- working tree 可解释；
- secret scan PASS；
- runtime data / credentials / customer data 未纳入 Git；
- Jovi 明确提供/确认 remote URL；
- push 范围经过 review。

## 4. 允许进入 Runtime remote 的内容

- source；
- migrations；
- Docker/Compose；
- tests；
- Runtime governance manifests；
- SBOM/license inventory；
- CI definitions；
- README/AGENTS；
- deterministic package/test reference（不含真实客户数据）。

禁止：
- `node_modules`；
- PostgreSQL/Redis runtime data；
- `.env` / secrets / test credentials；
- Browser Profile / Cookie / Token；
- customer/platform PII；
- raw payment evidence；
- 临时 review/evidence 大包，除非经过专门脱敏与大小审查。

## 5. 分支策略

目标：
- `main`：唯一正式主线，PR only；
- `feature/*`：短生命周期；
- 历史 `development` 如仍存在可保留为历史 ref，但不作为第二生产主线。

C3 audited closure 已 promoted 到 local `main` 后，C4 不应从旧 feature branch 直接运行“正式” Pilot。

## 6. Required Checks

最低建议：
1. TypeScript typecheck；
2. Jest unit natural shutdown；
3. integration；
4. current C2/C3 regression；
5. replay/recovery/concurrency；
6. negative tests；
7. deterministic package；
8. Gitleaks + existing scanner；
9. Syft SBOM；
10. license/provenance/source manifest；
11. Admin Playwright cookie-session。

C4 前不需要为了 CI 引入新的 Commerce framework 或 n8n production。

## 7. Branch Protection

Runtime remote 建立后建议：
- require PR；
- Jovi review；
- dismiss stale reviews；
- required checks；
- prohibit force push；
- prohibit branch deletion；
- secret/provenance checks fail-closed。

## 8. Automation_Seal 与 Runtime 的关系

Automation_Seal 保存：
- Human Decision；
- audit mirror；
- plan/spec；
- cloud reference；
- handoff。

Runtime remote 保存正式业务源代码。

不要在 Governance 仓“顺便备份” Runtime 业务源码，避免双权威和证据混乱。

## 9. 远端建立后的验证

必须回读：
- `git ls-remote`；
- exact remote main SHA；
- default branch；
- workflow status；
- branch protection/ruleset；
- local/remote clean sync。

`git push` exit 0 单独不能证明最终状态。
