# Codex 当前分阶段执行书

**最后校准：2026-09-05**  
**当前停点：`C4_HUMAN_PILOT_DECISION`**

> 文件名保留“部署执行书”以兼容旧引用，但当前不再执行历史 Phase 0/A/X0、Track P/I、X1-X4 作为主线。

## 1. Codex 总原则

1. 先读 `docs/CURRENT_PROJECT_GUIDE.md`、`STATUS.md`、`PROJECT_STATE.json`；
2. 现场 Git/SHA/sidecar 优先于聊天摘要；
3. 不重新执行已通过独立审核的 C2/C3，除非锚点不匹配；
4. 实现 Agent 不得自审；
5. Human Decision 不由测试结果自动生成；
6. 当前优先商业落地，不扩新框架。

## 2. 当前执行梯子

```text
C4-P0 远端/本地事实复核
-> C4-P1 Pre-Publish 文档与 claim QA
-> C4-P2 Jovi 商业形态选择（beta/dev/unsigned vs stable-first）
-> C4-P3 人工交付通道冻结
-> C4-P4 Jovi Human Pilot Decision
-> C4-P5 5–10 单或固定时间窗人工 Pilot
-> C4-P6 Pilot 证据与复盘
-> C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION
```

## 3. C4-P0：事实复核

Governance：
- `Jovifei/Automation_Seal`
- 复核 `main`、当前 C3/C4 branch、PR #5、CI；
- 当前 main 与 PR 分支存在 split-brain 时先记录，不直接 reset/rebase。

Runtime：
- `E:\project\jovi-medusa-commerce-v1`
- 复核本地 main 是否等于 audited C3 closure；
- 复核 `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`；
- 复核 `C3_RUNTIME_PROMOTION_AUDIT_PASS`；
- 复核六个 real-action flags；
- 复核 dedicated Git remote。

Product：
- `E:\project\jovi-modbus-diagnostic-toolkit-v1`
- 只读复核 HEAD 与 C3 产品资格化证据；
- 不重新修改/构建产品仓来“配合 Pilot”。

## 4. C4-P1：Pre-Publish QA

必须完成：

1. 清理 C4 ledger 的 synthetic/example completed rows；
2. 从本地 `governance/c3/C3_LISTING_CLAIM_EVIDENCE.json` 生成 C4 claim review；
3. 逐条 KEEP / REWRITE / REMOVE；
4. 修正 CRC、SHA256、compatibility、源码交付、时间承诺；
5. 核验当前闲鱼数字商品/退款规则；
6. 修复治理 mirror 的编码/转义问题；
7. rerun docs/reference CI；
8. 通过 PR 合并当前治理分支到 main。

此阶段**不发布真实商品**。

## 5. C4-P2：Jovi 商业形态选择

当前 reported SKU：`0.2.0-dev`，installer `UNSIGNED`。

Agent 只能准备两个候选：

- `BETA_PILOT`：透明说明 dev/unsigned，小范围试点；
- `STABLE_FIRST`：返回产品仓单独做 stable/signing，然后重新资格化。

选择权属于 Jovi。

## 6. C4-P3：人工交付通道

选择一个人工传输方式并冻结：
- 文件名/alias；
- package SHA；
- 链接到期/撤销；
- 不采集原始客户 PII；
- Jovi 手工发送。

C4 不需要为此建设 S3/Storefront/自动发货服务。

## 7. C4-P4：Human Decision

当前 `C4_HUMAN_PILOT_DECISION_CANDIDATE_V1` 为 `issued_from_human=false`。

最终 Decision 必须由 Jovi 本人签发并至少绑定：
- C3 audit SHA；
- Runtime main；
- SKU/version；
- DeliveryPackage SHA；
- final listing candidate SHA；
- pilot price；
- pilot size/time window；
- human-only action matrix；
- privacy rules。

没有 `issued_from_human=true`，停止。

## 8. C4-P5：真实人工 Pilot

每单：

1. Jovi 手工发布/沟通；
2. 买家下单；
3. Jovi 手工确认付款；
4. Runtime 记录脱敏 order/payment fact；
5. 系统准备 Entitlement / Package / Receipt；
6. Jovi 核 package SHA；
7. Jovi 手工发送交付；
8. Runtime/台账记录最小化 support/refund 分类。

不自动发布、发消息、确认付款、发货、改价或退款。

## 9. C4-P6：退出与复盘

至少要求：
- duplicate Entitlement = 0；
- duplicate Receipt = 0；
- wrong-version delivery = 0；
- unauthorized platform action = 0；
- package/release traceability = 100%；
- 统计人工分钟/单、咨询、support、退款原因。

退出状态：

`C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION`

之后必须停止，等待新的权限扩大 Decision。

## 10. 当前不做

C4 前不重新做：
- Commerce 框架选型；
- Medusa 大版本升级；
- Python Commerce 重启；
- Storefront / S3 / CRM；
- n8n production；
- 多渠道自动化；
- 自动闲鱼行为。

## 11. 报告格式

每阶段仍报告：scope、输入 SHA、变更、测试、失败、风险、隐私/许可证、回滚、证据、停止点和唯一下一动作。
