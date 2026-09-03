# Commerce C2 — Synthetic Commerce E2E + Digital Delivery V1

**状态：** PLAN_ONLY / SOURCE_VALIDATED
**目标执行仓：** `E:\project\jovi-medusa-commerce-v1`
**治理母仓：** `E:\project\jovi-automation` / GitHub `Jovifei/Automation_Seal`
**前置本地状态（须由本地 Executor 重新核验）：** `R2R3_INDEPENDENT_AUDIT_PASS`

## 1. 本阶段目的

R2-R3 已解决 Medusa Admin cookie-session 与基础 OSS 安全工具问题。C2 不再继续研究 Cookie、Medusa 选型或 Commerce Core，而是第一次把正式 Commerce Runtime 串成完整、可重复、可审计的数字产品 synthetic 售卖链：

`Product Manifest -> Digital Release -> Private Asset -> Listing Candidate -> Synthetic Order -> Synthetic Payment Evidence -> Jovi Entitlement -> Delivery Package -> Download Grant -> DeliveryReceipt -> Xianyu Draft Bundle`

本阶段仍严格禁止真实付款、真实客户、自动交付、真实闲鱼动作和公网 Storefront。

## 2. 前置 Gate

本地执行前必须重新验证：

- `development` R6 Post-Import 基线已 PASS；
- R2-R3 audited feature HEAD 与独立审核报告 SHA/sidecar 一致；
- `main` 未修改；
- 6 项真实商业边界仍全部 false；
- `remote=none` 时不得猜远端；
- R2-R3 审计失败或证据 SHA 不匹配时直接停止。

## 3. 开源选择性吸收

参考 `makepay-apps/medusa-plugin-digital-downloads`，固定审查锚点：

- Repo: `makepay-apps/medusa-plugin-digital-downloads`
- Commit: `a5343ba18cee85b3eed674ed55d0de7e32aaa448`
- License: MIT
- Compatibility: Medusa `>=2.18 <3`

只吸收以下模式：

1. Product/Variant 关联数字配置；
2. immutable Digital Release；
3. protected asset 与 public preview 分离；
4. local private storage 位于 public/static 目录之外；
5. short-lived opaque DownloadGrant 与 ownership Entitlement 分离；
6. idempotent delivery state / retry-safe 设计；
7. Admin 只读观察面。

明确不吸收/不接管：

- 第三方插件自己的 Entitlement authority；
- 自动付款触发；
- 自动邮件；
- S3；
- Storefront；
- DRM；
- License key 自动签发；
- 真实客户下载；
- 真实平台发布。

Jovi Policy 仍是唯一可以根据 payment evidence + rights evidence 签发 Entitlement/DeliveryReceipt 的权威边界。

若复制任何 MIT 源码片段，必须新增 `THIRD_PARTY_NOTICES.md`，记录 upstream repo、commit、原文件、license、复制/修改范围；不得无来源复制。

## 4. C2 数据模型

### DigitalRelease

至少包含：

- release_id
- product_id
- variant_id
- version
- state (`DRAFT|READY|FROZEN`)
- release_manifest_sha256
- source_product_manifest_sha256
- rights_evidence_sha256
- created_at

FROZEN 后不得原地修改；新版本创建新 release。

### DeliveryAsset

至少包含：

- asset_id
- release_id
- relative_path
- sha256
- size
- media_type
- rights_status
- private_storage_key

要求：path traversal fail-closed；磁盘读取前后都校验 SHA。

### DownloadGrant

不是 Entitlement，只是访问能力。至少包含：

- grant_id
- entitlement_id
- delivery_asset/package_id
- opaque_token_hash
- expires_at
- revoked_at
- synthetic_only=true

Grant 不能自行创造 ownership；只有已存在、有效且未 revoked 的 Jovi Entitlement 才能签发。

### DeliveryPackage

至少包含：

- package_id
- release_id
- artifact_sha256
- manifest_sha256
- deterministic_build_id
- file_count
- total_bytes

相同 release + 相同输入必须产生相同字节和 SHA。

## 5. Product Manifest -> Release

只读使用治理母仓现有模板/规范：

- `templates/product_manifest.yaml`
- `templates/xianyu_listing_draft.md`
- `automation_specs/product_build_pipeline.yaml`
- `automation_specs/xianyu_draft_pipeline.yaml`

C2 使用 synthetic fixture，不触碰真实 Modbus SKU 仓。

要求：

- rights_status 未确认 -> FAIL；
- prohibited_content_confirmed_absent != true -> FAIL；
- deliverables 为空 -> FAIL；
- asset SHA 与 manifest 不符 -> FAIL；
- release 不能进入 FROZEN。

## 6. Listing Candidate

从冻结 Product/Release 生成纯候选：

- title
- description
- verified feature bullets
- version
- system requirements
- delivery contents
- support boundary
- FAQ
- rights/copyright statement
- delivery instructions

输出必须标记：

`candidate_only=true`
`platform_action_allowed=false`

不得生成夸大未验证能力，不得访问 `xianyu-auto-reply`，不得发布或发送消息。

## 7. Synthetic Commerce E2E

最少完整流程：

1. ingest approved synthetic product manifest；
2. build/freeze digital release；
3. build deterministic delivery package；
4. generate listing candidate；
5. create synthetic Medusa Product/Variant；
6. create synthetic Order；
7. bind existing synthetic payment evidence；
8. run Jovi policy workflow；
9. issue exactly one Entitlement；
10. generate exactly one DeliveryReceipt；
11. issue short-lived DownloadGrant；
12. retrieve package through grant in loopback-only synthetic test；
13. recompute package SHA after retrieval；
14. generate Xianyu Draft Bundle；
15. replay same run/order and prove no duplicate Entitlement/Receipt/DeliveryPackage；
16. restart/recovery replay and prove same logical result。

## 8. 必须负测

至少：

- tampered product manifest；
- rights missing；
- asset hash mismatch；
- path traversal (`../`)；
- order/product mismatch；
- payment evidence mismatch；
- expired grant；
- revoked grant；
- entitlement revoked；
- grant for different order/customer；
- package tamper after build；
- duplicate/replay；
- platform_action_allowed=true injection；
- real-payment flag + synthetic mode conflict。

所有负测必须 fail-closed 且 DB/asset state 不产生不完整副作用。

## 9. Admin 验收

使用已修复的 cookie-session Playwright：

- login；
- Product；
- Order；
- Entitlement；
- DeliveryReceipt；
- Digital Release；
- Delivery Package metadata；
- refresh session；
- external request=0。

不要求 Storefront。

## 10. OSS 安全工具

保留 R2-R3 的 Gitleaks + Syft 双轨。

C2 核心功能 PASS 后可加 Trivy 作为非核心 Wave 2：

- filesystem scan；
- image scan；
- HIGH/CRITICAL policy；
- 固定版本/digest；
- 无法获取 vulnerability DB 时诚实标 `NOT_VERIFIED`，不得伪 PASS。

SLSA、harden-runner、dependency-review 继续等正式 GitHub runtime repo。

## 11. 证据输出

至少生成：

- `C2_CHANGE_MANIFEST.json`
- `C2_PRODUCT_MANIFEST.json`
- `C2_DIGITAL_RELEASE.json`
- `C2_ASSET_MANIFEST.json`
- `C2_DELIVERY_PACKAGE_MANIFEST.json`
- `C2_LISTING_CANDIDATE.json`
- `C2_XIANYU_DRAFT_BUNDLE.json`
- `C2_SYNTHETIC_E2E_RESULT.json`
- `C2_NEGATIVE_TEST_RESULTS.json`
- `C2_REPLAY_RECOVERY_RESULT.json`
- `C2_ADMIN_E2E_RESULT.json`
- `C2_OSS_PROVENANCE.json`
- `C2_SOURCE_MANIFEST.json`
- `C2_ROLLBACK_PLAN.json`
- `C2_INDEPENDENT_AUDIT_PROMPT.md`

每个关键 JSON/MD 均生成 SHA256 sidecar。

## 12. Git 与停止点

建议从已审计 R2-R3 HEAD 创建短期分支：

`feature/c2-synthetic-commerce-e2e`

本阶段不修改 `main`。

`remote=none` 时只做本地 commit，不猜 URL，不把 Commerce runtime 推到 `Automation_Seal`。

实现 Agent 不得自审。成功停止状态：

`READY_FOR_C2_INDEPENDENT_AUDIT`

只有全新独立审计 `C2_INDEPENDENT_AUDIT_PASS` 后，才允许申请把受控 Commerce repo 创建/绑定 GitHub remote，并进入真实 SKU staging（优先 Modbus）。
