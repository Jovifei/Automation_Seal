# 测试、审计与回滚分类视图

**最后校准：2026-09-05**

当前测试/验收入口：

- [`../05_验收测试_回滚与运维手册.md`](../05_验收测试_回滚与运维手册.md)
- [`../commerce/README.md`](../commerce/README.md)
- `reference/commerce/c2/**`
- `reference/commerce/c3/**`

## 已完成测试层

- R6 Post-Import independent audit；
- R2-R3 Cookie/Admin/Gitleaks/Syft；
- C2 Synthetic Digital Commerce E2E + independent audit；
- C3 Real SKU + zero-write + 25 negative cases + independent audit；
- Runtime C3 promotion audit。

当前不要把“再跑一遍全部历史 Governance test”当作 C4 前置。只有代码/锚点发生变化时重跑对应范围。

## 当前 C4 验收

Pre-Publish：claim evidence、ledger/privacy、平台规则、package SHA、Human Decision。  
Pilot：0 duplicate、0 wrong-version、0 unauthorized platform action、traceability、真实 support/refund/人工耗时。

## Historical

`docs/superpowers/reports/**`、旧 Route B Verify、历史 Medusa audit result 继续保留作为历史证据，但不是当前测试 TODO。

同名 Word 是旧人类导出；当前以 Markdown、Runtime 原始 evidence 和 Independent Audit 为准。
