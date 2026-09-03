# Commerce Runtime 远端化与 CI 治理计划 V1

## 当前事实

`E:\project\jovi-medusa-commerce-v1` 当前 remote=none，因此 Automation_Seal 只能保存 Decision/计划/审计索引，无法远端复核 runtime commit。

## 推荐远端

建议由 Jovi 明确创建/确认：

`Jovifei/jovi-medusa-commerce-v1`

在收到准确 remote URL 前，任何 Agent 不得猜测或 push。

## 首次推送边界

仅允许推送：

- source
- migrations
- Docker/Compose
- tests
- governance manifests
- SBOM/license inventory
- CI definitions
- README/AGENTS

禁止：

- node_modules
- PostgreSQL/Redis runtime data
- secrets/test credentials
- review-queue 临时证据大包
- customer/platform data
- browser profiles/tokens

## 分支策略

R2-R3/C2 期间保留当前 `development` 历史，不改写；远端建立后逐步收敛为：

- `main`：受保护、PR only
- `feature/*`：短期开发
- 不新增第二条长期生产分支

若决定永久保留 `development`，必须另行修改 governance 规则并说明用途。

## Required Checks

最低集合：

1. typecheck
2. unit natural shutdown
3. integration
4. C2/C3 synthetic E2E（阶段相关）
5. manifest/provenance
6. deterministic package/build
7. Gitleaks + existing secret scanner
8. Syft SBOM
9. license inventory
10. negative tests

第二阶段：Trivy filesystem/image；GitHub remote 稳定后再评估 harden-runner / dependency-review。

## Branch Protection

建议：

- require PR
- 1 个 Jovi review
- dismiss stale reviews
- required checks
- branch up-to-date
- prohibit force push/deletion

## 远端首次建立后的验证

本地 Agent 必须回读：

- `git ls-remote`
- remote main SHA
- feature SHA
- workflow checks
- default branch
- branch protection/ruleset（若权限支持）

不得以 `git push` exit 0 单独证明远端成功。