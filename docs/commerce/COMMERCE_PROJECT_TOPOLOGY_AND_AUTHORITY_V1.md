# Commerce 工程拓扑与权威边界 V1

**状态：** LANDING_MAINLINE_CANDIDATE  
**目的：** 固定四个本地工程的职责，防止后续 Agent 再次混线或重复造轮子。

## 1. 四仓关系

| 本地路径 | 角色 | 权威内容 | 当前建议 |
|---|---|---|---|
| `E:\project\jovi-automation` | 治理母仓 / Control Plane | Decisions、Gates、Specs、Audit、Product 模板、OSS 选型 | ACTIVE |
| `E:\project\jovi-medusa-commerce-v1` | Commerce Runtime | Product/Order/Payment Evidence/Jovi Policy/Entitlement/DeliveryReceipt/Delivery runtime | ACTIVE |
| `E:\project\jovi-modbus-diagnostic-toolkit-v1` | Track P 第一真实 SKU | Windows GUI、安装包、产品源码、产品文档、发布资产 | ACTIVE / C3 READ-ONLY SOURCE |
| `E:\project\jovi-commerce-engine-v1` | 早期 Python Commerce 试验仓 | 历史 staging / oracle 思路 | LEGACY_ARCHIVE_CANDIDATE |

## 2. 单一权威原则

- **治理/Decision 权威：** `jovi-automation`。
- **Commerce 交易状态权威：** `jovi-medusa-commerce-v1`。
- **第一真实产品字节权威：** `jovi-modbus-diagnostic-toolkit-v1`。
- **Python oracle：** 仅验收参考，不是运行时交易权威。
- **闲鱼真实动作：** 不属于上述任一自动运行时权威；由 Jovi 人工控制。

## 3. 不允许的耦合

- Commerce Runtime 不读写闲鱼 SQLite/Cookie/Token/浏览器资料。
- Modbus SKU 不嵌入 Commerce 数据库或交易逻辑。
- `jovi-automation` 不作为生产 Commerce runtime。
- `jovi-commerce-engine-v1` 不再新增生产能力。
- 同一 Payment、Entitlement、DeliveryReceipt 不允许双写双权威。

## 4. 当前主线

`R2R3_INDEPENDENT_AUDIT_PASS` → `C2 Synthetic Digital Commerce E2E` → `C2 Independent Audit` → `C3 Real SKU Staging (Modbus)` → `C3 Independent Audit` → `C4 Human Pilot`。

## 5. 真实平台边界

在 C2/C3 全阶段保持：

- `production_integration_allowed=false`
- `real_payment=false`
- `real_customer=false`
- `xianyu=false`
- `auto_delivery=false`
- `n8n_production=false`

C4 只允许由 Jovi 人工执行平台动作；任何新增自动化权限都必须有新的 Human Decision。