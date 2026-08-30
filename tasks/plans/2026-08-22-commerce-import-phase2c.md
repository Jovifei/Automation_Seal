# COMMERCE-IMPORT-PHASE2C：Git baseline → Git-object import → main-root synthetic X2

## 1. 目标与当前边界

本阶段承接已完成的 V16 `CONTROL_PLANE_C_APPLY`，把外置 Commerce Engine 的已完成 staging X2 变成主工程内可审计的导入候选，并最终冻结：

```text
MAIN_GIT_BASELINE_ESTABLISHED
→ COMMERCE_IMPORT_IMPLEMENTED
→ MAIN_PROJECT_X2_SYNTHETIC_PASS
→ IMPORT_AUDIT_PASS
→ COMMERCE_IMPORT_CANDIDATE_PASS
```

当前已确认：

- Formal V16：`workspace/decisions/JOVI_S1_RESTART_DECISION_V16.json`，SHA `363654c5cc8552190e0f7f5c044695984efe1c553eafced0bc117ef298680ee7`。
- Gate A/P strict report：`reports/gates/GATE_A_P_VERIFICATION_V16.json`，SHA `c53639fca3fb90804b0b8a8d5330b5172591dddc5d665235c85f2a5c1a9808d6`。
- C/APPLY receipt：`workspace/review-queue/commerce-v1/governance-closeout-v16-execution-receipts/transition/run-20260822-v16-apply-001/CONTROL_PLANE_TRANSITION_RECEIPT_V16.json`，SHA `10cba4e6315debc891d7bd787c79e6f779238d10b8581d5c92a828aa42a3b485`。
- 当前控制面：`commerce-c-apply-v16 / C / APPLY / revision 3 / blockers=[]`；Hook `DO_NOT_TRUST`；Track I、Hook trust、真实平台动作均为 false。
- 外置对象仓：`E:\project\jovi-commerce-engine-v1`；observed HEAD `3b31f0f2f240038aa261db5c57c43e5e14992dc5`；implementation `fd2321d5a3f12aa923014cadbc397849903fd97c`；evidence `7dbe080c907c1da2eef1c16b79e677e6a1d49470`；implementation 是 evidence 的祖先，工作树 clean、remote 为空。

## 2. 永久禁止

- 不修改 `MANIFEST.sha256`、`FRAMEWORK_MANIFEST.sha256`、`.codex/hooks.json`、Hook 脚本、`AGENTS.md` 或 V16 目标历史。
- 不写入 `scripts/human-only/**`、`scripts/xianyu/human-only/**`、`workspace/approvals/**`（人类 Approval 除外）。
- 不访问或修改外部闲鱼仓，不读取 Cookie、订单、买家消息、Token、支付或客户数据。
- 不创建产品发布、真实付款/交付、真实平台动作；不配置 remote、不 push、不 merge、不 tag、不 release。
- 不从 Windows checkout 复制 Commerce 源码；所有源字节必须来自固定 Git object。
- 不在 exact Git baseline Approval 前执行 `git init`、root-file apply、commit 或 worktree 创建。

## 3. 阶段 D9：Exact Git baseline 候选

### D9.1 候选生成（机器可执行、只写 review-queue）

建立新的 V16-bound Phase2C candidate 工具，不复用旧 generic wrappers。工具启动先验证：formal V16 SHA、C/APPLY receipt SHA、transition contract、当前控制面 `C/APPLY`、root `.git` 无有效 HEAD、`.gitignore` before SHA `6879e1723cf111c34377003f5f0d1c3da0167768b174b9efeaee8a3475216bf4`、`.gitattributes` absent、policy body/sidecar。

输出固定为：

```text
workspace/review-queue/commerce-v1/import-phase2c/git-baseline/
├── GIT_BASELINE_FILES_V1.txt
├── GIT_BASELINE_PATHS_V1.nul
├── GIT_BASELINE_MANIFEST_V1.json (+ sidecar)
├── SECRET_SCAN_REPORT_V1.json (+ sidecar)
├── GIT_BASELINE_REVIEW.md (+ sidecar)
└── PROTECTED_TREE_BEFORE_GIT.json (+ sidecar)
```

Manifest 必须逐项记录 repo-relative path、current bytes/SHA/size、desired bytes/SHA/size、source、disposition；明确排除 `reports/`、`workspace/review-queue/`、`workspace/approvals/`、runtime/data/cache/build/logs/backups、`.git`、`.worktrees` 和临时输出。`.gitignore` 记录 `REPLACE_WITH_APPROVED_BYTES`，`.gitattributes` 记录 `CREATE_FROM_APPROVED_BYTES`，但不写正式树。

Secret scan 只输出脱敏路径、行号和类别，不复制秘密值。所有输出使用临时目录原子发布；任一失败时目标目录保持不存在。

### D9.2 TDD 与冻结

- 先写 RED 测试：C/APPLY 缺失、formal V16/receipt 漂移、有效 HEAD 已存在、`.gitignore` before 漂移、绝对/遍历/大小写碰撞路径、NUL 编码错误、秘密值泄露、Manifest 自引用、排除目录误入。
- GREEN 后运行候选全套测试、PowerShell 5.1 parser、Python compile、Manifest/sidecar 全量重算。
- 生成 package manifest，排除自身、执行回执、`__pycache__` 和 audit 输出；冻结后只读。
- 成功标签：`GIT_BASELINE_CANDIDATE_FROZEN`。

### D9.3 Jovi exact baseline confirmation

候选冻结后生成机器读取命令，要求 Jovi 运行新的 `Approve-GitBaselineV16.ps1` 并输入 Manifest SHA 前 16 位。脚本只写 `workspace/approvals/GIT_BASELINE.V1.approval.json`，不运行 Git、不写 root 文件。Approval body/sidecar 由机器验证；任一漂移都生成新候选，不修改冻结包。

## 4. 阶段 D10：Git baseline 与 Git-object import

仅在 exact baseline Approval 机器验证 PASS 后：

1. 使用已批准 `.gitignore`/`.gitattributes` bytes 写入 root；再次验证 protected snapshot 和 `.git` 无 HEAD。
2. `git init -b main`、`core.autocrlf=false`、确认 remote 为空；只按 NUL pathspec 精确 stage baseline，禁止 `git add .`。
3. 生成 `GIT_BASELINE_ESTABLISHMENT.json` + sidecar，绑定 manifest/Approval SHA、root commit/tree OID、parent_count=0、index match、remote empty。
4. 创建 `.worktrees/commerce-import-phase2` feature worktree；证明 feature HEAD 等于 baseline root，且 root/feature clean。
5. 从外置仓 Git objects 读取 V15 scope 的 59 `IMPORT` rows；34 `RECORD_ONLY_EXCLUDE` 只记录，不落入产品目标。所有 target 写入先 staging，禁止读取 checkout bytes。
6. 对 `jovi_commerce/**`、`docs/commerce/**`、`schemas/commerce/**`、`tests/commerce/**` 和合成 fixtures 做 namespace/line-ending/forbidden-path验证；禁止 Hook、Manifest、Decision、Approval、human-only、products、外部闲鱼、runtime DB/receipts。
7. 生成 `IMPORT_IMPLEMENTATION_RECEIPT_V16.json`、`IMPORT_TESTS_RECEIPT_V16.json`、`IMPORT_EVIDENCE_RECEIPT_V16.json` 及 sidecars，绑定 source commit/blob/mode/size/SHA、target SHA、baseline、Decision、Gate、C/APPLY。

任一 source/target/sidecar/权限失败：staging 零写、删除临时 staging、保留 fail report，不触碰正式 feature tree。

## 5. 阶段 D11：主工程 synthetic X2

- 仅在三组 import receipt PASS 后，在 feature worktree 运行固定合成 fixtures；不访问真实平台、不创建真实客户/支付数据。
- 分离 unit、acceptance、X2 三份机器报告；报告绑定 feature HEAD/tree、baseline root、import receipts 和工具 SHA。
- X2 至少覆盖订单、付款确认、Entitlement、交付准备、售后脱敏和聚合指标各一条合成链；最终状态 `READY_FOR_HUMAN_DELIVERY`，不得宣称真实交付。
- 输出 `MAIN_PROJECT_X2_SYNTHETIC_REPORT.json` + sidecar；失败只修 feature worktree，重新生成候选和报告，不改 control root。

## 6. 阶段 D12：独立 Import Audit

使用未参与实现的全新 Luna `gpt-5.6-terra/xhigh` 只读审计；不运行 human-only、Git init、真实平台或外部闲鱼动作。审计必须验证：

- baseline root/feature HEAD/tree/ancestry/clean/remote empty；
- 59 IMPORT 与 34 RECORD_ONLY_EXCLUDE 完整分类；固定 Git blob bytes 100% 匹配；
- 目标路径无 Hook/Manifest/Decision/Approval/products/runtime/秘密/外部路径；
- 三组 import receipt、unit/acceptance/X2 报告和所有 sidecars 绑定一致；
- root control plane、V16/C/APPLY、Framework 40/40、Hook DNT、human-only 树零漂移；
- 主工程 X2 是合成证据，不是真实商业试点。

唯一 PASS：`COMMERCE_IMPORT_AUDIT_PASS`。FAIL 时只生成新 candidate revision；不得手工修补已冻结 feature tree。

## 7. 阶段 D13：冻结可合并候选

生成 `COMMERCE_IMPORT_CANDIDATE_PASS_V16.json` + sidecar，绑定：formal V16、C/APPLY、baseline/Approval、source selection、三组 import receipt、unit/acceptance/X2、Import Audit、feature HEAD/tree、exact diff 和工具 SHA。状态只能为：

```text
COMMERCE_IMPORT_CANDIDATE_PASS
MAIN_PROJECT_X2_SYNTHETIC_PASS
MERGE_NOT_AUTHORIZED
REAL_COMMERCE_PILOT_NOT_STARTED
REMOTE_REPOSITORY_NOT_CONFIGURED
```

同步 `tasks/todo.md`、`CHANGELOG.md` 和 Obsidian current notes；不手工修改 `STATUS.md`，由下一次受绑定状态转换工具更新。

## 8. 失败与回滚

- D9 候选失败：删除未发布临时目录，保留失败报告，不改正式树。
- Git baseline root-file apply 失败：使用同一 Approval 绑定的 rollback/backup；若已 `git init` 但验证失败，停止所有 import，保留本地 Git 证据并生成 superseding recovery plan，不使用 reset/clean。
- Import/X2/Audit 失败：只删除隔离 staging/worktree 中的候选字节；control root、Hook、Manifest、Approval、Decision 不变。
- 任何未知字段、额外 target、SHA 漂移或 sidecar mismatch 都 fail-closed。

## 9. 当前执行状态

- [x] V16 C/APPLY、strict Gate、回执和 Obsidian 同步。
- [x] D9 baseline candidate implementation/freeze。r3 candidate Manifest `d0df2009fb859b280dc55b0291829519830078e0239951d9a689b3e5769a71d5`，package r2 `79f3ec04022cdf083be8816a7a88a4ee546e200911bcf0298e885feaec222169`，556/556 paths、secret scan PASS、候选测试9/9。
- [ ] Jovi exact Git baseline confirmation。
- [ ] D10 Git baseline establishment and Git-object import。
- [ ] D11 main-root synthetic X2。
- [ ] D12 independent Import Audit。
- [ ] D13 frozen merge candidate。
