# Commerce CI / Security OSS Adoption V1

**状态：** `READY_FOR_LOCAL_VALIDATION`

目标：正式仓不再只依赖自研脚本完成 secret / SBOM / vulnerability / runner hardening，而是引入成熟 OSS 做第二实现和 required-check 候选。

## 1. Gitleaks

仓库：`gitleaks/gitleaks`

建议：`ADOPT_NOW_AFTER_POST_IMPORT_PASS`

用途：

- full history secret scan；
- PR diff secret scan；
- fail-on-finding；
- 项目 allowlist 写入 `.gitleaks.toml` 并人工审查。

边界：

- 不因 Gitleaks PASS 删除现有 secret scan；先双轨运行；
- CI pin 精确 release/commit；
- 任何 allowlist 必须有原因和 reviewer。

验收：

- 对干净仓 = exit 0；
- 注入 synthetic fake secret fixture = 必须 exit non-zero；
- 删除 fixture 后恢复 exit 0。

## 2. Syft

仓库：`anchore/syft`

建议：`ADOPT_NOW_AFTER_POST_IMPORT_PASS`

用途：

- source filesystem SBOM；
- backend image SBOM；
- CycloneDX JSON；
- 输出 SHA256 并纳入 provenance。

验收：

- source 与 image 都能稳定生成；
- 相同输入重复生成后做 normalized semantic comparison；
- Medusa / Jovi module / PostgreSQL driver / Redis client 等关键依赖必须出现在结果中；
- 与现有 CycloneDX evidence 组件集合做差异审查。

## 3. Trivy

仓库：`aquasecurity/trivy`

建议：`ADOPT_SECOND_WAVE`

用途：

- filesystem vulnerability；
- backend image vulnerability；
- config / Docker misconfiguration。

建议门：

- HIGH/CRITICAL 可配置 fail-closed；
- 未修复漏洞必须有 exception record，不能静默 ignore；
- DB 下载/更新时间写入 evidence。

本地离线环境若无缓存 DB，不能把“无法下载 DB”误报为 PASS。

## 4. StepSecurity Harden-Runner

仓库：`step-security/harden-runner`

建议：`ADOPT_WHEN_COMMERCE_REMOTE_EXISTS`

用途：GitHub Actions runner 网络与 supply-chain hardening。

要求：

- action pin 到 exact commit SHA；
- 初期 egress policy 用 audit 模式采集，再切 fail-closed；
- 不允许 silently disable。

## 5. GitHub Dependency Review

仓库：`actions/dependency-review-action`

建议：`CONDITIONAL`

只在目标仓 GitHub plan/visibility 支持时启用。必须现场验证可用性；不可只写 workflow 后宣称已经有依赖门禁。

## 6. SLSA GitHub Generator

仓库：`slsa-framework/slsa-github-generator`

建议：`DEFER_TO_RELEASE_PHASE`

当前 synthetic / staging 阶段先不引入。等正式可交付 artifact 和 tag/release 流程稳定后，用于 build provenance attestation。

## 7. Required checks 建议分层

### Wave 1（Post-Import PASS 后立即）

- typecheck
- unit
- integration
- deterministic build
- existing provenance/manifest validator
- existing license/SBOM validator
- Gitleaks
- Syft cross-check

### Wave 2（R2-R3 后）

- Playwright Admin cookie-session
- Trivy filesystem/image/config
- dependency review（若可用）
- harden-runner（远端仓存在后）

### Wave 3（release）

- SLSA provenance
- artifact signing / attestation（另行决策）

## 8. 不要做的事

- 不把多个新工具一次性设为 blocker 后再花时间调 CI；
- 不删除现有自研 validator；
- 不使用 floating `latest`；
- 不复制 OSS 源码进入业务目录；
- 不把 scanner PASS 当作商业/许可证/安全整体 PASS。

成功标准：成熟工具替代重复造轮子，同时每个工具都有负测，且不会让当前 Commerce 主线因为工具接入本身停滞。
