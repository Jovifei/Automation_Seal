# Documentation Mainline Alignment — 2026-09-05

**状态：COMPLETED DOCUMENTATION CLEANUP RECORD**

## 1. 为什么需要本轮校准

仓库经历了：

`V3.0 initial handoff -> Governance/Gate -> Medusa R2/R6 -> R2-R3 -> C2 -> C3 -> Runtime Promotion -> C4 preparation`

但大量入口 Markdown 仍停在 2026-07/08 的 `Phase 0/A/X0`、`Track P/I`、`X0-X4`、“Medusa 尚未采用”等状态。新 Agent 如果只读 README/docs，可能会重复执行已经完成的路线或误把历史计划当当前 Gate。

## 2. 本轮采用的文档治理策略

### 直接更新 Living docs

更新所有会影响新 Agent 当前执行路径的入口/导航/状态：

- `README.md`
- `README_FIRST.md`
- `00_先读我.txt`
- `AGENTS.md`
- `CODEX_START_PROMPT.txt`
- `CODEX_MASTER_TASK.md`
- `PROJECT_STATE.json`
- `NEXT_STEP_MAP.md`
- `FAST_TRACK.md`
- `DECISIONS_REQUIRED.md`
- `USER_ACTION_CHECKLIST.md`
- `docs/README.md`
- `docs/目录总览.md`
- `docs/00_*.md` ~ `docs/08_*.md`
- 分类目录 README
- 关键 Commerce living docs

### 新增 Current/Historical 索引

- `docs/CURRENT_PROJECT_GUIDE.md`
- `docs/HISTORICAL_DOCUMENT_STATUS.md`
- `docs/commerce/README.md`

### 保留历史证据原字节

不为了“清爽”重写：
- archived OpenSpec；
- Superpowers 历史计划/报告；
- 历史 Medusa independent audit result；
- 带 sidecar 的冻结 task plan；
- stale/failed evidence package。

这些由历史索引降级为 `HISTORICAL / DO NOT USE AS CURRENT INSTRUCTIONS`。

## 3. 当前统一后的主线

```text
Governance                       COMPLETED
Medusa R6                       COMPLETED
R2-R3 Admin/Security            COMPLETED
C2 Synthetic Digital Commerce   COMPLETED / INDEPENDENT PASS
C3 First Real SKU               COMPLETED / INDEPENDENT PASS
Runtime C3 Promotion            COMPLETED / REPORTED POST-PROMOTION PASS
C4 Human Pilot                  CURRENT / HUMAN DECISION PENDING
```

当前停止状态：

`C4_HUMAN_PILOT_DECISION`

## 4. 当前统一后的 OSS 路线

- Medusa v2.19.0 = ADOPTED Commerce Core
- Playwright = ADOPTED browser acceptance
- Gitleaks v8.24.0 = ADOPTED secret scan
- Syft v1.20.0 = ADOPTED SBOM
- Redis/PostgreSQL/Docker = ADOPTED Runtime infra
- MakePay digital-downloads = SELECTIVE ARCHITECTURE REUSE
- PyInstaller/Inno Setup = PRODUCT PACKAGING REFERENCE ONLY
- Saleor/Vendure/OpenMeter/Kill Bill/Lago/Keygen/Lemon Squeezy = historical/future assessment, not current runtime
- n8n production / Trivy / SLSA/cosign = deferred, not C4 blocker

## 5. 本轮直接修复的高风险错误

### C3 mirror encoding

修复 `C3_LOCAL_AUDIT_CLOSURE_MIRROR_20260905.md` 中 Windows escape/control-character 污染，保持其 mirror 身份，不修改本地 Runtime 原始 evidence。

### C4 fake evidence risk

重写 `C4_PILOT_OPERATIONAL_KIT_V1.md`：
- 删除预填的两条“已完成”Pilot 订单；
- 正式 ledger 从 0 条真实记录开始；
- Operational Kit 明确 `DO_NOT_PUBLISH_AS_IS`；
- listing 改为 `[VERIFIED_*]` evidence-bound skeleton；
- CRC 不再写“纠错”；
- SHA256 不再写“数字签名”；
- beta/dev/unsigned 状态必须透明；
- support script 不预写未经验证产品细节。

### C4 Human Decision Gate

更新 `C4_HUMAN_PILOT_DECISION_CANDIDATE_V1.md`：
- 保持 `issued_from_human=false`；
- 增加 Pre-Publish QA 前置；
- candidate price / pilot size 明确为未验证候选；
- 不允许 Agent 把第一人称模板当 Jovi 已签 Decision。

## 6. 仍然存在的外部/本地待核事实

本轮只改 Governance 文档，不伪造本地事实。新 Agent 仍需现场核：
- Runtime dedicated Git remote；
- Runtime C3 audit/promotion 原始 sidecar；
- Product HEAD / artifact bytes；
- 本地 C3 `C3_LISTING_CLAIM_EVIDENCE.json`；
- 当前闲鱼数字商品/退款规则；
- Jovi 对 beta/dev/unsigned vs stable-first 的选择；
- C4 Human Pilot Decision。

## 7. DOCX

旧 00–08 `.docx` 不在本轮同步更新。它们是历史排版导出，当前 Markdown 是权威 Living docs。`docs/HISTORICAL_DOCUMENT_STATUS.md` 已明确这一点。

## 8. 当前下一步

文档校准后，新 Agent 应直接进入：

`C4 Pre-Publish QA -> READY_FOR_JOVI_C4_HUMAN_PILOT_DECISION`

而不是回到 Gate A、Track P/I、Medusa adoption、C2 或 C3。
