# 下一步状态地图 — Commerce V1

**最后校准：2026-09-05**

> 旧 `Track P / Track I / X0-X4` 提示词地图已经完成历史使命，不再作为当前执行入口。

## 当前状态

```text
Governance / Medusa / R2-R3 / C2 / C3 / Runtime Promotion = COMPLETED
Current Stop = C4_HUMAN_PILOT_DECISION
```

## 当前状态 → 下一动作

| 当前状态 | 下一动作 | 允许执行者/文件 |
|---|---|---|
| `C4_PREP_REQUIRED` | 远端/本地事实复核、claim QA、ledger/privacy/document cleanup | 普通实现 Agent / C4 prep prompt |
| `READY_FOR_JOVI_C4_HUMAN_PILOT_DECISION` | Jovi 审阅 SKU/version/price/listing/package/privacy/human-only matrix | **Jovi Human Decision** |
| `C4_HUMAN_PILOT_AUTHORIZED` | 启动 5–10 单或固定时间窗人工 Pilot | Jovi + Runtime 内部准备能力 |
| `C4_HUMAN_PILOT_IN_PROGRESS` | 记录最小化 order/payment fact/Entitlement/Receipt/package/support | 系统内部；平台动作仍 Jovi 手工 |
| `C4_HUMAN_PILOT_PASS_PENDING_PERMISSION_DECISION` | 复盘数据，提出下一项逐动作权限候选 | 新计划 + Jovi Human Decision |

## 当前 C4 Pre-Publish QA

1. 检查 `Jovifei/Automation_Seal` main / C3-C4 branch / PR #5 / CI；
2. 检查本地 Runtime C3 audit/promotion 原件；
3. 检查 Product HEAD / package SHA；
4. 清理 C4 ledger 示例；
5. 将 C4 listing 每个 claim 绑定 C3 evidence；
6. 修 CRC/SHA256/compatibility/delivery wording；
7. 核验当前闲鱼数字商品/退款规则；
8. Jovi 选择 beta/dev/unsigned Pilot 或 stable-first；
9. 冻结人工 delivery transport；
10. 生成最终 `issued_from_human=false` Decision Candidate。

推荐本地执行入口：

`prompts/commerce/` 中当前 C4 prep/landing Prompt；若路径发生变化，以 `docs/commerce/README.md` 为准。

## C4 Human Decision 规则

没有 `issued_from_human=true`：
- 不真实发布；
- 不导入真实买家；
- 不确认真实付款到 Runtime 之外的自动流程；
- 不发货；
- 不翻转任何 real-action flag。

## Pilot 平台动作

即使 C4 获批：

- publish = Jovi
- message/commitment = Jovi
- price = Jovi
- payment confirmation = Jovi
- final delivery = Jovi
- refund/dispute = Jovi

系统只准备 candidate/order fact/Entitlement/Receipt/Package/KPI。

## 当前六个边界

```text
production_integration_allowed=false
real_payment=false
real_customer=false
xianyu=false
auto_delivery=false
n8n_production=false
```

## 失败时

- Git/SHA/sidecar 不匹配：停止并报告，不 reset/clean；
- listing claim 无证据：REMOVE/REWRITE，不推断；
- product/package 漂移：停止 Pilot，回产品/Commerce 独立修复流程；
- Human Decision 缺失：保持 `C4_HUMAN_PILOT_DECISION`。

## 历史提示词

根目录/`prompts/` 中仍可能保留 Track P/I、X0-X4、R2/R6/C2/C3 Prompt 作为历史证据。除非在排查对应旧阶段，不要执行它们。
