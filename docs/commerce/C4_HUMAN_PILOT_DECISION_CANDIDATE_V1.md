# C4_HUMAN_PILOT_DECISION_CANDIDATE_V1

**Decision 类型：** Human Pilot Authorization Decision Candidate  
**issued_from_human：** false (等待 Jovi 签发生效)  
**候选日期：** 2026-09-05  
**前置通过依据：**
- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`
- `C3_RUNTIME_PROMOTION_AUDIT_PASS`
- `C3_PRODUCT_SOURCE_ZERO_WRITE_PASS`

---

## 决策草案正文

我作为 Jovi，批准启动 **C4 Human Pilot（首个真实数字产品小规模人工试跑）**。

### 1. 试点基本参数
- **第一 SKU：** Modbus RTU Diagnostic Toolkit（V0.2.0-dev）
- **交付包：** `SYNTH-C3-MODBUS-RTU-0.2.0-dev.zip`（SHA256: `4bd5703ae80fcea9c1dcf7d5d1ea2a02fe282a5cf6ef3f04a2c9703db5188e59`）
- **发布渠道：** 闲鱼（手动发布草稿，候选标识 `candidate_only: true`）
- **试点规模：** 首轮 5–10 单，达到 10 单或固定时间窗后结束复盘
- **参考建议售价：** 99.00 CNY

### 2. 严格人工控制边界
在试点运行期间，所有真实外部平台操作必须由 Jovi 本人手动完成：
- 闲鱼商品发布：Jovi 手动发布
- 买家意向沟通与前置条件确认：Jovi 手动沟通
- 收款与凭证确认：Jovi 手动核实
- 最终交付物发送：Jovi 手动发送
- 售后排查与退款争议：Jovi 手动处理

### 3. 数据最小化与隐私保护
- 保持 `real_customer=false`：Runtime 仅记录系统订单 ID 与买家平台账号脱敏哈希（`platform_reference_hash`），不持久化明文个人隐私信息。
- 严禁抓取或导入买家全量私聊文本、身份证件或支付凭据明文；售后事件按类别归档记录。

### 4. 退出标准
- 0 重复权益/收据；
- 0 错版本交付；
- 0 自动化越权发货；
- 每单交付物 SHA256 100% 可追溯至 C3 Release Candidate。
- 试点完成状态：`C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION`。
