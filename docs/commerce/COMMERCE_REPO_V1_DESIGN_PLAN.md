# jovi-medusa-commerce-v1 — 正式 Commerce Repo 设计计划

**生成日期：** 2026-09-01
**状态：** `PLAN_ONLY` — 只生成计划，不执行。仅在 Jovi R6 Adoption Decision 明确授权后才可创建该仓库。
**目标仓库：** `jovi-medusa-commerce-v1`（独立的受控 Commerce 仓库，不是本根仓库的扩展）

## 1. 触发条件（全部满足才允许创建）

1. R2-R2 独立审核结论 = `MEDUSA_R2R2_PASS`。
2. Jovi 本人签发 R6 Adoption Decision，`issued_from_human=true`，明确授权创建新 repo 并 supersede R12（如适用）。
3. 授权范围仅限本计划所列导入项；不授权生产部署、真实支付、真实客户、Stripe、Storefront 公网暴露、自动交付或闲鱼动作。

## 2. Exact Import Manifest

只导入 R2-R2 audited source 的受控子集。导入来源 = `workspace/review-queue/commerce-v1/medusa-v2-spike-remediation-r2-r2/source-snapshot/`（与 R2-R2 source tree SHA 绑定）。

| 导入项 | 来源（source-snapshot 内路径） | 目标路径 |
|---|---|---|
| 应用源码（不含 node_modules/.medusa/dist） | `backend/jovi-medusa-backend/apps/backend/src/**` | `apps/backend/src/**` |
| 迁移 | `.../src/modules/jovi-commerce/migrations/**` | `apps/backend/src/modules/jovi-commerce/migrations/**` |
| 配置 | `backend/jovi-medusa-backend/apps/backend/{medusa-config.ts,instrumentation.ts,tsconfig.json,eslint.config.ts,package.json}` | 同构目录 |
| Dockerfile / compose | `backend/jovi-medusa-backend/{Dockerfile,docker-compose.r2.yml}` | 顶层（重命名为 `docker-compose.yml`，仅环境名差异） |
| workspace 配置 | `backend/jovi-medusa-backend/{package.json,pnpm-lock.yaml,pnpm-workspace.yaml,turbo.json,.npmrc,.dockerignore,.gitignore}` | 顶层 |
| 测试 | `backend/jovi-medusa-backend/apps/backend/src/**/__tests__/**` | 同构目录 |
| synthetic fixture | `tests/fixtures/synthetic-digital-checklist/**` | `tests/fixtures/synthetic-digital-checklist/**` |
| 许可证/范围证据 | `license-cache/**`（MIT + ENTERPRISE 排除清单） | `licenses/**` |
| 治理文档（只读参考） | `AGENTS.md`、`CLAUDE.md` | 顶层 |

**明确不导入：**
- `node_modules`、`.medusa`、`dist`、`runtime*`、`.env*`（secrets）
- 运行时 PostgreSQL/Redis 数据、Medusa cache、review-queue、浏览器 Profile、Cookie、Token
- 任何真实客户数据、闲鱼资料、支付 provider 配置、Storefront 公网配置

## 3. 绑定与版本

| 项目 | 绑定方式 |
|---|---|
| Medusa 版本 | `2.19.0`，Tag commit `87d77fa1b56ec287aa6655aaa2f54245387aa2f2` 记录在 README/AGENTS |
| lockfile | `pnpm-lock.yaml` 全量入库，`pnpm install --frozen-lockfile` |
| upstream provenance | `UPSTREAM_PROVENANCE.md`：tag/commit/digest/SBOM/license 来源逐项记录 |
| 镜像 digest | Node `ffb27ca0…`、PostgreSQL `cf78e766…`、Redis `1cd18c97…` 固定在 compose/Dockerfile |
| R2-R2 source tree SHA | 导入仓库的初始树 SHA 必须与 `MEDUSA_R2R2_SOURCE_MANIFEST.json` 的 `source_tree_sha256` 一致；差异即 FAIL |

## 4. 结构设计

```
jovi-medusa-commerce-v1/
├── AGENTS.md / README.md / UPSTREAM_PROVENANCE.md
├── Dockerfile
├── docker-compose.yml          # 环境名替换为 v1，镜像 digest 固定
├── package.json / pnpm-workspace.yaml / pnpm-lock.yaml / turbo.json
├── apps/backend/               # 受控子集
├── tests/fixtures/             # synthetic fixture
├── licenses/                   # MIT + ENTERPRISE 排除清单 + scope 证据
├── .github/workflows/          # CI（见 GitHub 治理计划）
├── CODEOWNERS
├── migrations/                 # medusa 迁移脚本（源码内已有）
├── sbom/                       # CycloneDX 1.5 快照 + 重算脚本
└── releases/                   # release manifest（镜像/源码/lock/SBOM SHA）
```

## 5. 迁移与回滚

- 迁移：`medusa db:migrate` 作为部署前一步，迁移文件入库；每个迁移有独立 revision。
- 回滚：`medusa db:migrate --down <n>`；恢复策略与 R2-R2 `RECOVERY_PENDING` 语义一致（预事务状态 + 120 秒重放窗口）。
- 每次发布生成 `releases/RELEASE_MANIFEST.json`：source SHA、lock SHA、image digest、SBOM SHA、migration head。

## 6. CI（计划，不在本 repo 创建前执行）

required checks：typecheck、unit、integration（loopback PG/Redis）、license、SBOM、secret scan、
manifest/provenance、deterministic build。全部在隔离环境内运行，绝不连接真实支付/闲鱼。

## 7. 验收

1. `pnpm install --frozen-lockfile && pnpm --filter @dtc/backend exec tsc --noEmit` 通过。
2. Jest unit 自然退出（无 `--forceExit`），integration 通过。
3. X2 synthetic replay 幂等；负测全拒；恢复重放单一 Entitlement/Receipt。
4. 导入树 SHA == audited source tree SHA；SBOM/license scope 可复算。
5. 无任何真实平台/支付/客户交互。
