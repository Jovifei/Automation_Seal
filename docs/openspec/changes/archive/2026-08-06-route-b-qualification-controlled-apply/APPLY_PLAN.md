# Route B 受控 APPLY 计划（快照）

- 生成时间(UTC): 2026-08-06T00:31:24.733625+00:00
- 来源决策: `workspace/decisions/JOVI_S1_RESTART_DECISION_V1.json`
- 独立审核 PASS: `reports/audit/JOVI_S1_ROUTE_B_FINAL_INDEPENDENT_AUDIT_RESULT_V1.md`

## 门条件（全部 false = fail-closed）
- `real_apply_allowed` = false
- `formal_manifest_real_write_allowed` = false
- `hook_trust_allowed` = false
- `track_p_allowed` = false
- `track_i_allowed` = false
- `xianyu_real_actions_allowed` = false

## 目标清单（10 项）

| # | 路径 | 决策SHA | 实时SHA | 比对 | 动作 |
|---|------|---------|---------|------|------|
| 1 | `.codex/hooks.json` | `8db93c1976ff88b64b4371e6850aff14593d890a3bb71ae0432f6f8635597e5a` | `8db93c1976ff88b64b4371e6850aff14593d890a3bb71ae0432f6f8635597e5a` | OK | ACCEPT_CURRENT_BYTES_AS_QUALIFICATION_CANDIDATE_PENDING_INDEPENDENT_REVIEW |
| 2 | `CODEX_START_PROMPT.txt` | `14f45f1857efa814a03bfc358c8a46c0b56ef0eab28deca41198e54c19a0f689` | `14f45f1857efa814a03bfc358c8a46c0b56ef0eab28deca41198e54c19a0f689` | OK | ACCEPT_CURRENT_BYTES_AS_QUALIFICATION_CANDIDATE_PENDING_INDEPENDENT_REVIEW |
| 3 | `scripts/00-run-readonly-audit.ps1` | `52ba03696d52b10372367ad8ecb559fbe27cca45f03e38bc18fad91120c54dd1` | `52ba03696d52b10372367ad8ecb559fbe27cca45f03e38bc18fad91120c54dd1` | OK | ACCEPT_CURRENT_BYTES_AS_QUALIFICATION_CANDIDATE_PENDING_INDEPENDENT_REVIEW |
| 4 | `scripts/codex/Invoke-PreToolGuard.ps1` | `795386ded6c613cd797716055ee9ddfbd164dc60f7d9e639cf765dd5afe8db81` | `795386ded6c613cd797716055ee9ddfbd164dc60f7d9e639cf765dd5afe8db81` | OK | ACCEPT_CURRENT_BYTES_AS_QUALIFICATION_CANDIDATE_PENDING_INDEPENDENT_REVIEW |
| 5 | `scripts/codex/pre_tool_guard.py` | `7d549aab11d14d7ec19024eaf9d8110b50ba3f7149cda7ba60ff5a38f655ee20` | `7d549aab11d14d7ec19024eaf9d8110b50ba3f7149cda7ba60ff5a38f655ee20` | OK | ACCEPT_CURRENT_BYTES_AS_QUALIFICATION_CANDIDATE_PENDING_INDEPENDENT_REVIEW |
| 6 | `scripts/common.ps1` | `f2798687919718a1199bb912db70fa8118a5f945a57442e235afd39c00b50987` | `f2798687919718a1199bb912db70fa8118a5f945a57442e235afd39c00b50987` | OK | ACCEPT_CURRENT_BYTES_AS_QUALIFICATION_CANDIDATE_PENDING_INDEPENDENT_REVIEW |
| 7 | `scripts/generate_gate_a_plan.py` | `e60b11a499867c8912d89cb511f6b046b0c49cb48cda2036289c352d0a074877` | `e60b11a499867c8912d89cb511f6b046b0c49cb48cda2036289c352d0a074877` | OK | ACCEPT_CURRENT_BYTES_AS_QUALIFICATION_CANDIDATE_PENDING_INDEPENDENT_REVIEW |
| 8 | `scripts/validate-package.py` | `5b8259ade0776cc226d159b3950edab8d22bef5a0a51a97e62c74567577a5b8a` | `5b8259ade0776cc226d159b3950edab8d22bef5a0a51a97e62c74567577a5b8a` | OK | ACCEPT_CURRENT_BYTES_AS_QUALIFICATION_CANDIDATE_PENDING_INDEPENDENT_REVIEW |
| 9 | `scripts/xianyu/validate_xianyu_bundle.py` | `fe3020ce42b287a67d6cad70b5166dcdafa7f3e4d26e543adedbb51b7bf2c844` | `fe3020ce42b287a67d6cad70b5166dcdafa7f3e4d26e543adedbb51b7bf2c844` | OK | ACCEPT_CURRENT_BYTES_AS_QUALIFICATION_CANDIDATE_PENDING_INDEPENDENT_REVIEW |
| 10 | `scripts/xianyu/xianyu_readonly_audit.py` | `70064383a5761b23f27fcdbf85203bbc916b2b0ca4845dd353f2beda5905aa82` | `70064383a5761b23f27fcdbf85203bbc916b2b0ca4845dd353f2beda5905aa82` | OK | ACCEPT_CURRENT_BYTES_AS_QUALIFICATION_CANDIDATE_PENDING_INDEPENDENT_REVIEW |

## 证据链
- 每项目标可追溯到决策 JSON 的对应 item（路径 + current_sha256）。
- 独立审核 PASS 证明决策 SHA 与真实文件及冻结目标映射一致、13 套回归全 PASS、真实树零漂移。
- 本快照为只读生成；真实树未被修改（零漂移）。
