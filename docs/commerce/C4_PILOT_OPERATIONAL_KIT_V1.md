# C4 Pilot Operational Kit V1 — PRE-PUBLISH DRAFT

**状态：`PRE_PUBLISH_QA_REQUIRED / DO_NOT_PUBLISH_AS_IS`**  
**当前 Gate：`C4_HUMAN_PILOT_DECISION`**  
**Human Decision：尚未签发**

> 本工具包用于准备 C4 Human Pilot。它不是已经发生的 Pilot 证据，也不是可以直接复制发布的最终商品文案。真实发布前必须从本地 C3 原始 `C3_LISTING_CLAIM_EVIDENCE.json` 对每条技术 claim 做证据绑定，并由 Jovi 审阅。
>
> 推荐在本地生成独立 `C4_LISTING_CLAIM_REVIEW.json`，对每条最终文案标记 `KEEP / REWRITE / REMOVE` + `source_c3_claim_id` + `evidence_path` + `evidence_sha256`。没有完成这份 review，本工具包保持 `DO_NOT_PUBLISH_AS_IS`。

## 0. 当前已知且可用于准备的 reported anchors

以下来自 Governance C3 mirror，实际使用前仍应从本地 Runtime/Product 原始 evidence 复算：

- SKU：`Modbus RTU Diagnostic Toolkit`
- Reported version：`0.2.0-dev`
- Installer：`JoviModbusDiagnosticToolkit-0.2.0-dev-unsigned.exe`
- Installer Authenticode：`UNSIGNED`
- Installer SHA256：`d86ccc3136bc2ed201622c5f961738e9e81762e74e71ac5772ea6d4b5a408e02`
- Portable ZIP SHA256：`7525e4c8d4fd55900d46c51e075b92e47d61c7d8e1393383e2e92206855a9628`
- C3 deterministic delivery package SHA256：`4bd5703ae80fcea9c1dcf7d5d1ea2a02fe282a5cf6ef3f04a2c9703db5188e59`
- C3 independent audit：reported PASS
- Reference price candidate：`99.00 CNY`（**未经过真实市场验证**）

## 1. 发布前 Claim Evidence Gate

真实发布前必须从本地：

`E:\project\jovi-medusa-commerce-v1\governance\c3\C3_LISTING_CLAIM_EVIDENCE.json`

生成 C4 review：

```text
claim_text
source_c3_claim_id
evidence_path
evidence_sha256
decision = KEEP | REWRITE | REMOVE
reason
```

必须重点检查：
- 支持的 Modbus 功能码；
- CRC 能力；
- Windows 版本；
- Python 版本；
- 是否真的交付源码；
- 是否真的包含 PDF / QUICKSTART / requirements；
- 是否包含 virtual slave / virtual serial 相关工具；
- 任何“几分钟跑通”之类时间承诺；
- 售后范围。

**无证据的 claim 直接 REMOVE。**

禁止把：
- CRC 写成“纠错”；
- SHA256 写成“数字签名”；
- unsigned 写成“已安全签名”；
- dev 版本写成“正式稳定版”；
- “支持所有设备/所有 Windows/永久更新/包教会”等无限承诺写入商品页。

---

## 2. Listing Copy Card — 仅安全骨架

> 以下只是结构模板。`[VERIFIED_*]` 字段必须由 C4 Claim Review 填入，不能让模型自由发挥。

### 基础参数

- 商品名称候选：`Modbus RTU Diagnostic Toolkit` + `[VERIFIED_POSITIONING]`
- 版本：`0.2.0-dev`
- 当前签名状态：installer `UNSIGNED`
- 参考价：`99.00 CNY`（candidate only）
- 交付方式：Jovi 在人工确认付款后手工发送受控数字交付包/链接
- Pilot 数量：5–10 单或 Human Decision 指定时间窗

### 商品描述骨架

```markdown
【Modbus RTU Diagnostic Toolkit — C4 Beta Pilot】

版本：0.2.0-dev
状态：小规模 Beta Pilot；installer 当前为 unsigned。

适合人群：
[VERIFIED_TARGET_USER]

已验证功能：
- [VERIFIED_CLAIM_1]
- [VERIFIED_CLAIM_2]
- [VERIFIED_CLAIM_3]

已验证运行环境：
[VERIFIED_ENVIRONMENT]

交付内容：
[VERIFIED_DELIVERABLE_LIST]

当前已知限制：
[VERIFIED_KNOWN_LIMITATIONS]

购买前请先确认您的使用场景、系统环境与需要连接的设备/接口。首轮为人工试点，Jovi 会在拍下/交付前人工确认需求与交付版本。

交付时同时提供 SHA256 完整性校验值，便于确认收到的文件与本次受控交付包一致。

售后与退款：由 Jovi 人工按实际兼容性、交付情况和当前平台规则处理；本商品页不作超出已验证范围的保证。
```

### 客户可见文件名

内部 C3 package 目前 reported 使用工程验证命名。若 Pilot 使用客户友好 alias：
- 只改变文件名/传输展示；
- 不改变 package bytes；
- 每单仍记录权威 package SHA256；
- alias 与内部 release/package 形成明确映射。

---

## 3. 售前人工筛选话术 — 不包含未经验证技术 claim

### 开场

> 您好，感谢关注 Modbus RTU Diagnostic Toolkit。当前是 0.2.0-dev 小规模试用版。为了避免买错，麻烦先告诉我您主要是用于协议学习/代码调试，还是需要连接真实设备？另外请告诉我您实际使用的电脑环境和设备接口，我会先核对当前版本的已验证范围。

### 兼容性

> 我会按当前版本已经测试并记录的兼容范围给您确认；如果您的设备/系统不在已验证列表里，我不会直接承诺兼容，可以先说明具体型号/场景再判断。

### 交付

> 付款后我会手工核对订单和版本，再发送本次受控交付包，同时提供 SHA256 完整性校验值。首轮 Pilot 不使用自动发货。

### 退款/争议

> 如果出现实际交付或兼容问题，我会人工核实，并按当时平台规则和具体情况处理，不做自动退款或绝对化承诺。

---

## 4. 人工交付 SOP

### Step 1 — Human payment confirmation

Jovi 在平台侧手工确认付款事实。Runtime 不自动访问支付平台，也不自动将真实订单标记为 paid。

### Step 2 — Package binding

从本地 Runtime 原始 evidence 复核本单目标 package：

Reported C3 package SHA256：

`4bd5703ae80fcea9c1dcf7d5d1ea2a02fe282a5cf6ef3f04a2c9703db5188e59`

必须现场使用 `Get-FileHash` / `certutil` 或 Runtime 验证工具复算。SHA 不一致立即停止。

### Step 3 — Runtime preparation

记录最小化 order/payment fact，生成/确认：
- exactly one Entitlement；
- exactly one DeliveryReceipt；
- 正确 Product/Release/Version；
- DeliveryPackage SHA；
- 必要的 DownloadGrant/交付准备。

### Step 4 — Human delivery

Jovi 使用 Human Decision 已冻结的人工传输通道发送。系统不得直接调用闲鱼写接口、自动发消息或自动点击发货。

### Step 5 — Minimal record

只记录 Pilot 所需的脱敏字段，不把完整聊天、姓名、手机号、地址、Cookie/Token、支付凭证明文写入 Runtime/Git。

---

## 5. Pilot Ledger — 正式模板从 0 条真实记录开始

> **重要：下表没有任何预填“已完成”订单。真实 Pilot 尚未发生时，不得创建看似真实的成交记录。**

| # | pilot_order_id | platform_ref_hmac | order_time | actual_price | human_payment_confirmed | entitlement_id | package_sha256 | receipt_id | human_delivery_confirmed | support_category | refund_dispute | final_state |
|---:|---|---|---|---:|---|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |  |  |  |  |  |
| 6 |  |  |  |  |  |  |  |  |  |  |  |  |
| 7 |  |  |  |  |  |  |  |  |  |  |  |  |
| 8 |  |  |  |  |  |  |  |  |  |  |  |  |
| 9 |  |  |  |  |  |  |  |  |  |  |  |  |
| 10 |  |  |  |  |  |  |  |  |  |  |  |  |

如需示例，请单独使用 `EXAMPLE_ONLY` 文件，不得把示例行计入 C4 evidence/KPI。

### Privacy

优先使用随机内部 `pilot_order_id`。如确实需要稳定映射平台引用，优先用本地 secret key 的 HMAC；key 不入 Git。不要把公开昵称直接裸 SHA256 后误认为不可逆匿名。

---

## 6. Support Taxonomy — 只记录分类，不保存完整聊天

推荐分类：

| Code | Category | 说明 |
|---|---|---|
| `SUPP-ENV` | Environment | 运行环境/依赖/安装问题 |
| `SUPP-SERIAL` | Serial/Interface | 串口、USB-RS485、接口占用/识别 |
| `SUPP-PROTOCOL` | Protocol/Configuration | 地址、波特率、校验、功能码/报文配置 |
| `SUPP-COMPAT` | Compatibility | 当前未覆盖的设备/OS/版本兼容问题 |
| `SUPP-DOC` | Documentation | 文档理解、上手步骤 |
| `SUPP-DELIVERY` | Delivery | 文件/链接/哈希/版本交付问题 |
| `SUPP-REFUND` | Refund/Dispute | 退款或争议，由 Jovi 人工处理 |
| `SUPP-OTHER` | Other | 需要人工分类 |

技术解决建议必须来自实际产品文档/evidence，不能在本 Governance 模板里预写未经验证的工具/命令。

---

## 7. C4 Human Decision 前 Checklist

- [ ] Runtime C3 audit/promotion 原件复核；
- [ ] Product HEAD / package SHA 复核；
- [ ] C4 Claim Review 完成；
- [ ] final listing 仅含 VERIFIED claims；
- [ ] 0.2.0-dev / unsigned 已透明说明或 Jovi 选择 stable-first；
- [ ] 当前闲鱼数字/虚拟商品与退款规则已刷新；
- [ ] 人工 delivery transport 已冻结；
- [ ] ledger 为空；
- [ ] privacy/HMAC 方案明确；
- [ ] six real-action flags 仍 false；
- [ ] final Decision Candidate `issued_from_human=false` 已交 Jovi。

## 8. Pilot Exit Checklist

当且仅当 Jovi 正式授权后开始统计：

- [ ] 0 duplicate Entitlement；
- [ ] 0 duplicate Receipt；
- [ ] 0 wrong-version delivery；
- [ ] 0 unauthorized platform action；
- [ ] 每单 package SHA 可回溯到 Release；
- [ ] payment confirmation 可回溯到 order；
- [ ] 无原始 buyer PII/Cookie/Token 进入 Runtime；
- [ ] 人工分钟/单、support、refund/未成交原因可量化；
- [ ] 结束状态 `C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION`。

Pilot PASS 也不自动开放任何新权限。
