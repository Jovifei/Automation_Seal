# GitHub 治理建议 — Commerce Repo（R6 后）

**生成日期：** 2026-09-01
**状态：** `PLAN_ONLY` — 只生成计划。本轮不修改任何 GitHub 仓库或保护设置。
**适用：** R6 Decision 授权后创建的 `jovi-medusa-commerce-v1` 仓库。

## 1. 分支模型

- `main`：唯一受保护的主线分支；**PR only**，不允许直接 push。
- 功能分支：`feature/<area>/<change>`，短生命周期，合并前必须通过全部 required checks。
- 不设长生命周期 develop；发布从 `main` 打 tag。

## 2. main 分支保护（PR only）

| 设置 | 值 |
|---|---|
| Require pull request reviews | 1（Jovi 本人 review） |
| Dismiss stale reviews | true |
| Require status checks | true（见下表） |
| Require branches up to date | true |
| Restrict push | 仅 PR 合并 |
| Force push / deletion | 禁止 |

## 3. Required Checks（CI 门禁）

| Check | 内容 | 失败行为 |
|---|---|---|
| typecheck | `tsc --noEmit` | BLOCK |
| unit | Jest unit 自然退出（无 --forceExit） | BLOCK |
| integration | 模块集成测试（loopback PG/Redis） | BLOCK |
| license | license scope / 引入新依赖扫描 | BLOCK |
| SBOM | CycloneDX 生成 + 变更 diff | BLOCK |
| secret scan | 禁止 secrets/token 入库 | BLOCK |
| manifest/provenance | source/lock/image SHA 清单可复算 | BLOCK |
| deterministic build | 相同输入 → 相同镜像/包 | BLOCK |

所有 CI 在隔离容器内运行：仅 127.0.0.1 / internal 网络，`production_integration_allowed=false` 写入 CI 环境。

## 4. CODEOWNERS

- `*` → 仓库 Owner（Jovi），商业/许可证相关路径（licenses/、docs/commerce/）强制 Owner review。
- `apps/backend/src/modules/jovi-commerce/` → 保留 Owner review（策略边界代码）。

## 5. 发布流程（R6 批准后按步骤执行）

1. 从 `main` 打 `release/<version>` tag（SemVer）。
2. 生成 `releases/RELEASE_MANIFEST.json`（source/lock/image/SBOM/migration head SHA）。
3. 由 Jovi 人工确认 release manifest 后再合并/推送；禁止自动发布。

## 6. 禁止

- 本轮及 R6 之前：不创建仓库、不修改保护设置、不 push 任何 Commerce 代码。
- 任何自动部署到真实环境、真实支付/闲鱼动作均未授权。
