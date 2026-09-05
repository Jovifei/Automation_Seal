# Commerce Post-R6 Mainline Plan — 已完成阶段回顾

**原生成日期：2026-09-01**  
**当前状态：COMPLETED / HISTORICAL REFERENCE**  
**最后校准：2026-09-05**

> 本文件原本定义 R6 之后的实施路线。该路线已经实际执行到 C3 并完成 Runtime Promotion。不要把本文当成“现在还要从 R6 开始”的执行计划。

## 1. 原计划执行结果

| 原计划步骤 | 当前结果 |
|---|---|
| R6 Human Adoption Decision | COMPLETED |
| Controlled Commerce Repo Import | COMPLETED |
| Post-Import Independent Audit | `R6_POST_IMPORT_PASS` |
| Admin Cookie / OSS hardening | `R2R3_INDEPENDENT_AUDIT_PASS` |
| Synthetic Full Commerce E2E | `C2_INDEPENDENT_AUDIT_PASS` |
| Product Manifest / DigitalRelease / DeliveryPackage | COMPLETED in C2/C3 |
| Listing Candidate | COMPLETED in C2/C3 candidate path |
| Order / human-confirmed payment evidence | Synthetic path validated; real confirmation remains Jovi-controlled |
| Entitlement / DeliveryReceipt | COMPLETED and exactly-once validated |
| DownloadGrant / loopback delivery | COMPLETED |
| First Real SKU Staging | `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS` |
| Runtime main Promotion | Human Decision completed; reported `C3_RUNTIME_PROMOTION_AUDIT_PASS` |

## 2. 当前真实下一步

现在不再是 Post-R6 implementation。

当前停点：

`C4_HUMAN_PILOT_DECISION`

请改读：
- `docs/CURRENT_PROJECT_GUIDE.md`
- `docs/commerce/README.md`
- `docs/commerce/COMMERCE_LANDING_MAINLINE_C2_C4_V1.md`
- `docs/commerce/C4_HUMAN_PILOT_PLAN_V1.md`
- `docs/commerce/C4_PILOT_PRIVACY_MINIMIZATION_V1.md`
- `docs/commerce/C4_HUMAN_PILOT_DECISION_CANDIDATE_V1.md`

## 3. 当前 C4 前置 Gate

Candidate 仍：

`issued_from_human=false`

当前只允许：
- listing claim evidence QA；
- ledger/privacy cleanup；
- current Xianyu rule refresh；
- product beta/stable decision candidate；
- delivery transport candidate；
- Governance PR/CI/main 收口；
- Runtime remote 核验。

没有 Jovi Human Decision，不真实发布。

## 4. 本历史计划仍然有效的核心原则

- 真实付款确认由 Jovi 人工；
- Entitlement / Receipt 由 Jovi Policy 管理；
- package 绑定 SHA/provenance；
- 闲鱼平台动作 Human-controlled；
- frozen evidence 不覆盖；
- independent audit 不由实施 Agent 自审；
- `production_integration_allowed` 等 real-action flags 不因测试自动翻转。

## 5. 当前强制边界

```text
production_integration_allowed=false
real_payment=false
real_customer=false
xianyu=false
auto_delivery=false
n8n_production=false
```

C4 结束后仍需新的 Permission Expansion Decision。
