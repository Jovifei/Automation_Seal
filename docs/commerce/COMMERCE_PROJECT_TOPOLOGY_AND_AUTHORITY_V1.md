# Commerce 工程拓扑与权威边界 V1

**状态：CURRENT / LIVING**  
**最后校准：2026-09-05**  
**当前停点：`C4_HUMAN_PILOT_DECISION`**

## 1. 四仓关系

| 本地路径 | 当前角色 | 权威内容 | 当前状态 |
|---|---|---|---|
| `E:\project\jovi-automation` | Governance / Control Plane | Human Decisions、Audit mirrors、Specs、Docs、Cloud reference | ACTIVE |
| `E:\project\jovi-medusa-commerce-v1` | Formal Commerce Runtime | Medusa Product/Order、payment evidence、Jovi Policy、Entitlement、DeliveryReceipt、DigitalRelease、DeliveryPackage、DownloadGrant | ACTIVE；reported C3 promoted main |
| `E:\project\jovi-modbus-diagnostic-toolkit-v1` | First Real SKU Product Source | Windows product source、installer/ZIP、product docs/tests | ACTIVE；C3 authoritative read-only product bytes |
| `E:\project\jovi-commerce-engine-v1` | Legacy Python Commerce | 历史 staging/oracle 思路 | LEGACY / ARCHIVE ONLY |

另有：

`E:\project\xianyu-auto-reply` — 独立外部适配器/历史平台能力。当前不是 Commerce 状态权威，也不与 Runtime 共享 SQLite、Cookie、Token、Browser Profile。

## 2. 单一权威原则

- **Governance/Human Decision/Audit index：** `jovi-automation`
- **Commerce Runtime state：** `jovi-medusa-commerce-v1`
- **Payment fact acceptance：** Jovi Human confirmation + Jovi Policy
- **Entitlement / DeliveryReceipt：** Jovi Policy
- **第一商品原始字节：** `jovi-modbus-diagnostic-toolkit-v1`
- **真实平台行为：** Jovi 人工
- **Python/cloud oracle：** 只做可复算验收参考，不是交易权威

不得让两个组件都拥有独立创建同一 Payment fact、Entitlement、Receipt 的 authority。

## 3. 当前真实执行链

已经完成：

`R6 -> R2-R3 -> C2 Synthetic E2E -> C2 Audit PASS -> C3 Real SKU -> C3 Audit PASS -> Runtime Promotion PASS`

当前：

`C4 Pre-Publish QA -> Jovi Human Pilot Decision -> Human-controlled Pilot`

旧文档中“R2R3 PASS -> C2 -> C3 -> C4”的路线已经执行到 C4，不再从 C2 开始。

## 4. C3 当前 reported anchors

本地 Runtime/Product 必须现场重算；Governance mirror 只作索引。

- Runtime C3 implementation：`5b190edce6a530264560a6822b347255fba014ba`
- C3 audited closure / reported Runtime main：`63db06e9fd2e1cbdf6e7926b48ba72d3fbe06cb1`
- C3 audit SHA256：`7123e18295895b84b7ed24c75628822db76dba2f7ba6a04f3ad004348e7b79b4`
- Product HEAD：`25ef15386b21bcc53277c0d5af5973ad8ea272eb`
- Delivery package SHA256：`4bd5703ae80fcea9c1dcf7d5d1ea2a02fe282a5cf6ef3f04a2c9703db5188e59`

## 5. 当前真实平台边界

在 C4 Decision 签发前以及首轮 C4 Pilot 中，至少保持：

- `production_integration_allowed=false`
- `real_payment=false`
- `real_customer=false`
- `xianyu=false`
- `auto_delivery=false`
- `n8n_production=false`

`real_customer=false` 表示 Runtime 不持久化原始买家 Profile/PII；并不禁止 Jovi 与真人买家做人工 Pilot。

## 6. C4 人工控制矩阵

| 动作 | 当前权威 |
|---|---|
| Listing candidate | Runtime/Governance 生成，Jovi 审核 |
| Xianyu publish | Jovi |
| Buyer message/commitment | Jovi |
| Price | Jovi |
| Payment confirmation | Jovi |
| Entitlement/Receipt/Package prep | Runtime |
| Final delivery/link send | Jovi |
| Refund/dispute | Jovi |

## 7. 不允许的耦合

- Runtime 不读写闲鱼 SQLite/Cookie/Token/Profile；
- Governance 不成为生产交易 Runtime；
- Product repo 不嵌入 Commerce DB/交易状态；
- Commerce 不为 Pilot 修改/重建真实产品字节；
- Legacy Python Commerce 不新增主线能力；
- MakePay/第三方插件不得接管 Jovi payment/Entitlement/Receipt authority。

## 8. 当前 Git/远端策略

Automation_Seal 保存治理材料。Runtime 应使用独立 Git repo/remote；如果本地 `jovi-medusa-commerce-v1` 仍没有 dedicated remote，先由 Jovi 决定 public/private 与准确 URL，不能把 Runtime 业务源码推到 Automation_Seal。

Governance `main` 与当前 C3/C4 PR 分支可能暂时分叉；新 Agent 必须现场检查 PR #5 并优先通过 PR 收口，而不是直接重写 main。

## 9. 当前下一步

1. C4 listing claim evidence QA；
2. 清理 Pilot 示例台账；
3. 修正 C3 mirror/营销措辞；
4. 刷新闲鱼当前规则；
5. 选择 beta/dev/unsigned Pilot 或 stable-first；
6. 冻结人工 delivery transport；
7. Jovi Human Pilot Decision；
8. 5–10 单/固定窗口人工 Pilot；
9. `C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION`；
10. 再逐动作决定 permission expansion。
