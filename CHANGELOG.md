# CHANGELOG

## 2026-08-09 - G1 audit remediation V2 authorized

- Started a new bounded G1 remediation cycle after the independent `BLOCKED / NO-GO` review.
- Added strict candidate Hook Policy requirements, including explicit `hook_restore_allowed=false`; missing or unknown fields fail closed.
- Preserved the historical `116/116` initial and `118/118` final governance counts while making the machine V2 report authoritative.
- Established a new human-only before/after evidence cycle; old G1 history remains `NOT_VERIFIED`.
- Split pre-Decision readiness from post-apply Gate readiness; no formal Decision, Gate, Approval, Manifest APPLY or Commerce implementation was started.
- Frozen a fresh V3/Controlled Baseline candidate package with a new preflight run ID; it remains non-authoritative until independent G3 review and Jovi Decision V3.
- G3 returned `FAIL` for stale SHA/byte records in `FINAL_CONTROL_TARGET_SET_V2.json`; the failed package was retained and a new RERUN1 human-only cycle plus candidate freeze was started.

## 2026-08-09 - Commerce V1 G1 governance remediation

- Re-centered the control entry and master task on the local Commerce Engine; Modbus remains a separate SKU and VideoFactory remains a separate project.
- Added fail-closed Commerce path protection, known Commerce action labels, the only permitted `S1/CLOSED` to `C/APPLY` transition, and guarded mirror synchronization for state, status and prompt.
- Added Commerce readiness validation for human Decision V3, controlled-baseline candidates, review-package SHA coverage, Framework Manifest state, independent Post-Apply evidence and platform-action flags.
- Replaced the legacy Modbus/Phase-A Gate generator with a Commerce-only readiness-bound generator; it creates no plan while readiness is `NOT_READY` and keeps Track I `NOT_AUTHORIZED`.
- Kept the authoritative state at `S1/CLOSED/1`; no Approval, Decision, Manifest, Hook trust, external-repository access or platform action was performed.

## V3.0 - 2026-07-12

- 形成最终单ZIP交接结构；
- 新增结构化对话上下文、已完成工作和调研冻结策略；
- 新增机器可读PROJECT_STATE.json；
- 执行拆分为Track P和Track I独立批准；
- 新增14天快速落地路线和首次排障；
- 新增分阶段Codex提示；
- 新增可运行的Modbus RTU主机侧Alpha；
- 加强闲鱼X0隐私：不输出Git路径、不读取或哈希SQLite、不输出配置值；
- 第一轮统一为单一入口，避免重复测试；
- 将广泛调研冻结，只刷新易变事实；
- 增加SBOM、供应链和数据治理路线。
- 增加完整交付快照与不可变安全框架双清单；
- 最终离线合成与负向测试扩展为103项。

## V2.0

## 2026-08-09 - Commerce V1 pre-gate candidate

- Re-centered the mainline on the local, auditable Commerce Engine; OpenClaw VideoFactory, the external Xianyu adapter, and Modbus remain separate boundaries.
- Added review-queue-only Commerce V1 architecture, Decision V2 review summary, strict JSON Schema candidates, synthetic fixtures, validation report and candidate manifest.
- Confirmed `COMMERCE_SPEC_CANDIDATE` / `BLOCKED_BEFORE_GATE_A_P`; no product code, formal Commerce paths, approvals, Hook trust or platform actions were changed.

- 引入现有闲鱼系统作为独立执行适配器；
- 增加X0-X4阶段、候选包契约、人工批准和14个专用Skill。
