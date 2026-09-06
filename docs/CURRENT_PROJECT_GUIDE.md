# Jovi Automation 当前项目指南

**状态日期：2026-09-06**  
**文档性质：CURRENT / LIVING / NEW-AGENT ENTRYPOINT**

> 新 Agent 先读本文件，再读 `PROJECT_STATE.json`。仓库中的历史 Gate、Track P/I、X0-X4、Medusa spike、R6/R2-R3/C2/C3 计划与审计材料用于追溯，不代表当前待执行任务。

## 1. 项目最终目标

Jovi Automation 是一套本地优先、可审计、可回滚的数字产品 Commerce 系统。目标不是让 AI 无监管地执行真实交易，而是把产品资格、商品候选、订单事实、人工确认付款事实、Entitlement、DeliveryReceipt、确定性交付准备、测试、支持分类和审计证据自动化，同时把真实平台账号、商业承诺、付款确认、最终发送与退款争议保持在 Jovi 人工控制下，直到未来逐动作授权。

第一真实 SKU：**Modbus RTU Diagnostic Toolkit**。

目标链：

`Product Source -> Qualification -> Immutable Release -> DeliveryPackage -> Listing Candidate -> Order -> Human-confirmed Payment Fact -> Entitlement -> DeliveryReceipt -> Delivery Preparation -> Human Delivery -> Support/KPI -> Permission Decision`

## 2. 当前真实阶段

技术和发布前准备已经闭合到：

`Governance -> Medusa R6 -> R2-R3 -> C2 PASS -> C3 Real SKU PASS -> C3 Runtime Promotion PASS -> C3 Git Reconciliation PASS -> C4 Pre-Publish QA PASS -> Runtime C4 Readiness Remote Promotion + CI PASS`

当前唯一业务硬门：

`READY_FOR_JOVI_C4_HUMAN_PILOT_DECISION`

正式 Decision Candidate 仍必须保持：

`issued_from_human=false`

因此：**现在可以准备最终 Human Decision，但不能开始真实 Pilot。**

## 3. 工程与权威边界

| 路径 | 角色 | 当前状态 |
|---|---|---|
| `E:\project\jovi-automation` | Governance / Decision / Audit mirror / Specs / Control Plane | ACTIVE；C4 Human Decision 前最终治理入口 |
| `E:\project\jovi-medusa-commerce-v1` | 正式 Commerce Runtime（Medusa v2.19.0） | ACTIVE；C4 readiness 已提升到 Runtime main |
| `E:\project\jovi-modbus-diagnostic-toolkit-v1` | 第一真实 SKU 产品源 | ACTIVE；Commerce 必须严格 read-only |
| `E:\project\jovi-commerce-engine-v1` | 早期 Python Commerce 试验 | LEGACY / ARCHIVE ONLY |

`E:\project\xianyu-auto-reply` 仍是独立平台适配器。C4 首轮不启用自动真实动作；Runtime 不读取其 SQLite、Cookie、Token 或浏览器 Profile。

## 4. 当前权威锚点

### Commerce Runtime

GitHub：`Jovifei/jovi-medusa-commerce-v1`

- C3 baseline：`63db06e9628331982893929f39b1037077138480`
- C4-readiness Runtime main：`b7ec762f29092106ad10c88d72bc682b5f9e7ac2`
- Runtime PR #1：MERGED / FAST-FORWARD
- Runtime final CI run：`34016366716` — PASS
- current audited `audit-source` canonical SHA256：`3101604bf10c9c6ed3c9b67a23e5ef77a6704472835ccfd536c2cc0b6b8e568a`
- `audit-source` file count：94
- Jest unit：9/9 suites，41/41 tests PASS
- synthetic terminal：`C4_RUNTIME_SYNTHETIC_REGRESSION_PASS`

Governance 对上述远端锚点使用：

`reference/commerce/c4/C4_RUNTIME_REMOTE_BINDING_20260906.json`

并在 C4 CI 中通过 `git ls-remote` 重新核验 Runtime `main`，不能再靠短 SHA 或 prose 推导完整 object ID。

### Product

- Product HEAD：`25ef15386b21bcc53277c0d5af5973ad8ea272eb`
- Version：`0.2.0-dev`
- Installer：UNSIGNED
- Installer SHA256：`d86ccc3136bc2ed201622c5f961738e9e81762e74e71ac5772ea6d4b5a408e02`
- Portable ZIP SHA256：`7525e4c8d4fd55900d46c51e075b92e47d61c7d8e1393383e2e92206855a9628`
- Delivery package SHA256：`4bd5703ae80fcea9c1dcf7d5d1ea2a02fe282a5cf6ef3f04a2c9703db5188e59`

客户可见 alias 候选：

`JoviModbusDiagnosticToolkit-0.2.0-dev-Windows-x64.zip`

只允许改展示文件名，不允许改变被审计 package bytes；每单仍记录权威 SHA256。

## 5. C4 发布前准备已经完成

本地原始 evidence 已报告并远端固化以下结果：

- `C3_RUNTIME_GIT_RECONCILIATION_PASS`
- `C4_LISTING_CLAIM_REVIEW_PASS`
- `C4_CUSTOMER_PACKAGE_INVENTORY_PASS`
- `C4_MANUAL_DELIVERY_TRANSPORT_FROZEN`
- C4 privacy/minimization ready
- C4 Pilot ledger 从 0 条真实订单开始
- C4 readiness：`C4_PRE_PUBLISH_QA_READY_FOR_HUMAN_DECISION`

本地 Human-check evidence 还记录：

- release posture：`BETA_PILOT`
- Xianyu human rule check：`C4_XIANYU_HUMAN_RULE_CHECK_PASS`

这些记录支持 readiness，但**不等价于最终 C4 Human Pilot Authorization**。

## 6. C4 文案与交付边界

只允许发布 C3/C4 evidence 支持的 claim。

当前明确禁止无证据扩大为：

- 买家必须具备 Python 编程基础；
- 买家普通使用必须预装 Python 3.10+；
- 随包一定交付 Python 源码、QUICKSTART、requirements、com0com；
- “3 分钟跑通”等固定时间承诺；
- CRC-16“纠错”；
- SHA256“数字签名”；
- 100% / 所有设备 / 所有 Windows 通用兼容；
- 永久更新、无限售后；
- 绝对化“不退款”。

正确边界包括：

- 产品为 `0.2.0-dev` Beta Pilot；
- installer 当前 unsigned；
- SHA256 是完整性哈希；
- CRC 是校验/错误检测；
- 当前有 evidence 的系统要求为 Windows 10/11 x64 + 兼容 USB-RS485 适配器及厂商驱动；
- 退款/争议按当前平台规则与实际情况人工处理。

## 7. 当前仅剩 Human Decision

技术侧不应继续扩展功能。下一步只需要 Jovi 对最终 Pilot 作显式商业绑定。

推荐候选参数：

- Release posture：`BETA_PILOT`（本地 human-check 已记录；最终 Decision 再确认）
- Price：`99 CNY`
- Pilot stop：**最多 10 个已付款 Pilot 订单，或自首次发布起 14 个自然日，先到者为准**
- Channel：闲鱼，Jovi 手工发布
- Publish / buyer communication / price change / payment confirmation / final delivery / refund-dispute：全部 Jovi 手工

以上价格与 Pilot 范围在 Jovi 正式签发前仍只是 candidate。

只有 Jovi 明确签发最终 Decision 后，才允许：

`issued_from_human=true`

然后开始统计真实 C4 Pilot。

## 8. 六项强制边界

最终 Human Decision 签发前以及首轮 Pilot 默认期间，除非另有逐项决策：

- `production_integration_allowed=false`
- `real_payment=false`
- `real_customer=false`
- `xianyu=false`
- `auto_delivery=false`
- `n8n_production=false`

`real_customer=false` 并不禁止人工真人 Pilot；含义是 Runtime 不持久化原始买家 Profile/PII。只记录随机内部 `pilot_order_id`、必要时 keyed HMAC 平台引用、产品/版本、人工付款确认事实、Entitlement/Receipt/package SHA、support/refund 分类等最小审计数据。

## 9. 新 Agent / 本地 Codex 唯一推荐入口

先执行：

`prompts/commerce/LOCAL_CODEX_C4_FINAL_RECEIVE_AND_VERIFY_20260906.txt`

它的任务是：

1. fetch Governance / Runtime；
2. 保护 Jovi 的本地未提交修改，尤其已有 `AGENTS.md` 修改；
3. 用本地 Git 和文件重新验证 Runtime/Product/Package 锚点；
4. 运行 C4 verifier；
5. 停在 `READY_FOR_JOVI_C4_HUMAN_PILOT_DECISION`；
6. 不替 Jovi 签字，不执行真实平台动作。

## 10. 不再重复的工作

除非权威 invariant 实际失败，不要：

- 重做 C2；
- 重做 C3；
- 重选 Commerce Core；
- 恢复 legacy Python Commerce 作为主线；
- 重写 Xianyu adapter；
- 扩大开源/市场调研；
- 从 Commerce 修改产品仓；
- 为了匹配旧文档 force-push 或重写 Git 历史。

C4 真人 Pilot 结束后的目标状态：

`C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION`

Pilot PASS 也不自动开启任何新权限；后续仍由 Jovi 逐动作决定 Permission Expansion。
