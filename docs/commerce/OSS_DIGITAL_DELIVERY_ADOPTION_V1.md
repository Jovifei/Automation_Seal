# OSS Digital Delivery Adoption V1

**状态：** SOURCE_VALIDATED / SELECTIVE_REUSE_ONLY

## 1. 结论

下一阶段不再更换 Commerce Core。Medusa v2.19.0 继续作为 Commerce Core；数字商品交付只吸收成熟开源实现的局部模式。

首选参考：`makepay-apps/medusa-plugin-digital-downloads`。

固定审查锚点：

- commit: `a5343ba18cee85b3eed674ed55d0de7e32aaa448`
- upstream release context: v0.4.0 customer delivery
- license: MIT
- Medusa compatibility: `>=2.18 <3`

## 2. 为什么值得借鉴

该项目已经解决了数字商品常见但容易重复造轮子的领域问题：

- Medusa Product/Variant 与 digital configuration 关联；
- immutable release；
- protected master asset 与 public preview 分离；
- local private storage / private S3 storage；
- durable entitlement；
- ownership 与 short-lived download/stream grant 分离；
- license assignment/audit；
- idempotent fulfillment；
- delivery notification state；
- Admin/read API。

这些结构与 Jovi 自动售卖系统高度相似，可以明显减少领域建模试错。

## 3. Jovi 采用边界

### 直接吸收思想/结构

- immutable DigitalRelease；
- DeliveryAsset 元数据；
- private storage outside static/public；
- opaque short-lived DownloadGrant；
- grant 与 ownership Entitlement 分离；
- retry-safe/idempotent delivery state；
- order/product/release 的强绑定；
- Admin 只读观察模型。

### 只参考，不直接采用

- upstream entitlement issuance；
- license generator/pool；
- refund/chargeback 自动 revoke；
- notification/email；
- Storefront client；
- S3 provider；
- public preview delivery；
- payment-captured subscriber。

原因：Jovi 已有经过独立审核的 payment evidence + rights + Entitlement + DeliveryReceipt 权威边界。引入第二套 entitlement/payment authority 会形成双源真相和新的 capability bypass 风险。

## 4. 首轮实现策略

C2 不 `npm install` 整个插件。

优先采用：

1. 读其 `README.md`、`docs/ARCHITECTURE.md`、`docs/TESTING.md`；
2. 对照 Jovi 当前模型写最小 delta；
3. 如确需复制小段 MIT 工具代码，必须逐文件记录 provenance；
4. 所有 copied code 必须有 `THIRD_PARTY_NOTICES.md`；
5. 复制后仍必须经过 Jovi tests 和独立审核。

未来只有在独立 spike 证明整插件不会接管 Jovi entitlement/payment authority 时，才允许重新评估直接安装。

## 5. License 与供应链

MIT 允许复用/修改/分发，但复制代码时保留许可声明/notice。

任何实际导入前重新确认：

- upstream commit 未漂移；
- LICENSE SHA；
- 复制文件 SHA；
- npm tarball integrity（若未来安装）；
- SBOM；
- secret scan；
- exact Medusa 2.19 compatibility。

## 6. 其他 OSS 状态

### 已采用/验证

- Medusa v2.19.0
- Microsoft Playwright
- Gitleaks v8.24.0
- Syft v1.20.0

### 下一候选

- Aquasecurity Trivy：image/filesystem CVE；C2 核心链 PASS 后再接。

### 延后

- Step Security harden-runner：待 Commerce runtime 有 GitHub remote/Actions；
- dependency-review-action：待 remote 与 GitHub plan 能力确认；
- SLSA generator：正式 release/tag 阶段。

## 7. 不推荐的替代路线

- 不切换 Saleor/Vendure/Kill Bill；
- 不引入新的 payment provider；
- 不引入公网 Storefront；
- 不使用实体物流 fulfillment 插件解决数字交付；
- 不把 n8n 变成订单/付款/Entitlement 权威账本。

当前最快的路线是：保持已审核 Commerce Core，只补数字 release/storage/grant/delivery package，再完成完整 synthetic E2E。
