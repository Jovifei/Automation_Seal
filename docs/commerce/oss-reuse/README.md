# Commerce V1 OSS 复用与采用边界

**最后校准：2026-09-05**  
**状态：CURRENT / LIVING**

> 本目录最初用于 2026-08 的 Commerce 选型。现在 Medusa 已正式采用、C2/C3 已完成，因此“候选/未部署”的旧描述不再是当前状态。历史单项评估文件仍保留用于追溯。

## 1. 当前确定路线

### A. Medusa v2.19.0 — 已正式采用

Repo：`medusajs/medusa`  
状态：`ADOPTED_COMMERCE_CORE`

当前负责：
- Product / Variant；
- Order；
- payment primitives / workflow；
- Admin；
- Redis-based workflow/locking/recovery；
- Runtime integration foundation。

Jovi 保留以下业务权威：
- payment evidence acceptance；
- rights evidence；
- Entitlement；
- DeliveryReceipt；
- Human Decision / real-action gate。

Medusa adoption/R6/R2-R3 已完成，不再重新做框架选择。

### B. Playwright — 已采用

状态：`ADOPTED_BROWSER_ACCEPTANCE`

用于：
- Admin login / Cookie Session；
- Product / Order / C2/C3 Admin E2E；
- refresh；
- console/page error；
- external-request monitoring。

经验：curl/API 200 不能替代真实浏览器 UI acceptance。

### C. Gitleaks v8.24.0 — 已采用

状态：`ADOPTED_SECRET_SCAN`

验收包括：
- clean scan PASS；
- synthetic private-key fixture 必须 FAIL；
- fixture 删除后再次 PASS。

### D. Syft v1.20.0 — 已采用

状态：`ADOPTED_SBOM`

生成 source/image CycloneDX SBOM，并与现有 license/provenance evidence 双轨使用。

### E. Redis / PostgreSQL / Docker — 已采用 Runtime 基础设施

用途：
- transaction/workflow persistence；
- distributed locking；
- replay/recovery；
- database；
- isolated integration/runtime tests。

## 2. 数字交付模式：MakePay selective reuse

Repo：`makepay-apps/medusa-plugin-digital-downloads`  
固定参考 commit：`a5343ba18cee85b3eed674ed55d0de7e32aaa448`  
License：MIT（项目审查锚点）  
状态：`SELECTIVE_ARCHITECTURE_REUSE`

C2 已吸收/借鉴：
- immutable DigitalRelease；
- protected/private asset；
- local private storage；
- short-lived opaque DownloadGrant；
- Entitlement ownership 与 DownloadGrant capability 分离；
- idempotent digital delivery；
- Admin digital-product observation patterns。

明确不接管：
- payment authority；
- Jovi Entitlement authority；
- DeliveryReceipt authority；
- automatic email；
- S3；
- Storefront；
- license-key authority；
- real customer auto-delivery。

Cloud C2 reference 的 Python Oracle 是本项目自己的验收实现，不以复制整个第三方插件替代本地设计。

## 3. Windows 产品打包参考

### PyInstaller
Repo：`pyinstaller/pyinstaller`  
C3 研究时 observed `develop` head：`5a80d1b93f1fbad3d8c0bdce90ce01f49927a9a1`

### Inno Setup
Repo：`jrsoftware/issrc`  
C3 研究时 observed `main`：`1ae7bf81dc0d2013235dfe4bb0b6f4e4a0b6b25c`

采用原则：
- 只参考已有产品打包 recipe/行为；
- 产品实际使用什么已验证版本就记录/冻结什么；
- C3/C4 不为追 upstream 最新而升级工具链；
- 当前 product installer unsigned 状态必须诚实披露，不能用 OSS 升级绕过产品 release 决策。

## 4. 历史评估 / 当前不采用

本目录中的下列项目属于历史选型研究，当前没有安装为主线 Runtime：

| 组件 | 当前结论 |
|---|---|
| OpenMeter | FUTURE_TRIGGER；只有真正的 metered product 才重新评估 |
| Kill Bill | REFERENCE_ONLY；复杂 billing 参考 |
| Saleor | ALTERNATIVE_NOT_SELECTED；Medusa 已采用，不并行建设 |
| Vendure | NOT_CURRENT_MAINLINE；不在 C4 前重选 Commerce Core |
| Lago | NOT_CURRENT_MAINLINE；计费/AGPL 范围不匹配当前 Pilot |
| Keygen | NOT_CURRENT_MAINLINE；license server 不是首单 Pilot 前置 |
| Lemon Squeezy | EXTERNAL_SAAS_NOT_CURRENTLY_AUTHORIZED |

对应 `03-*` 到 `09-*` 文件保留用于历史 license/architecture 追溯，不代表当前 TODO。

## 5. n8n 当前状态

历史结论曾为 `DIRECT_REUSE_INTERNAL_ORCHESTRATION` 候选。

当前实际边界：

`n8n_production=false`

C4 首轮 Pilot 不需要 n8n production。只有真实 Pilot 数据证明出现大量重复、确定性内部工作后，再独立评估内部编排；n8n 永远不成为 Payment/Entitlement/Receipt 权威。

## 6. 后续安全/供应链增强（非 C4 blocker）

- Trivy：filesystem/image vulnerability scan；
- step-security/harden-runner：Runtime 独立 GitHub remote/Actions 后；
- dependency-review-action：同上，且取决于 GitHub repo/plan；
- SLSA / cosign：稳定 release/attestation 阶段；
- Storefront/S3：只有真实交付规模证明需要时再建。

不要让这些优化阻塞第一真实 Pilot。

## 7. OSS 采用规则

1. 优先解决现成问题，不为“技术先进”引入新组件；
2. pin tag/commit/digest；
3. 读 `LICENSE` / `SECURITY`；
4. 复制/改写源码必须记录 `THIRD_PARTY_NOTICES`；
5. OSS reference 不能自动成为 Runtime authority；
6. 本地 integration/evidence 仍需独立验证；
7. 已审计版本不因上游更新自动升级；
8. 当前 C4 目标优先级高于继续选型。

## 8. 当前系统边界

`jovi-automation` 是 Governance；`jovi-medusa-commerce-v1` 是 Runtime；`jovi-modbus-diagnostic-toolkit-v1` 是第一 SKU；`xianyu-auto-reply` 是独立外部适配器。

不得让 Medusa、n8n、Python oracle 或任何第三方插件直接读写闲鱼 SQLite、Cookie、Token、Browser Profile，或绕过 Jovi 的真实平台 Human Decision。
