# 下一步提示词地图

Codex每个阶段完成后都必须停止。用户本人根据当前状态选择下一份提示词，不要一次发送多阶段指令。

| 当前状态 | 用户动作 | 发送给Codex的文件 |
|---|---|---|
| 刚解压 | 审阅并信任Hook，添加闲鱼只读目录 | `CODEX_START_PROMPT.txt` |
| 已生成GATE_A计划，决定先做产品 | 本人运行`Approve-Gate.ps1 -Track P` | `prompts/10_track_p_alpha.txt` |
| 已生成GATE_A计划，决定部署基础设施 | 本人运行`Approve-Gate.ps1 -Track I` | `prompts/20_track_i_core.txt` |
| 准备闲鱼加固提案 | 先生成并批准具体X1计划 | `prompts/30_xianyu_x1.txt` |
| 准备合成演练 | 先批准具体X2计划 | `prompts/40_xianyu_x2.txt` |

## 规则

- `Track P`与`Track I`回执互不替代；
- X1/X2必须有单独、哈希绑定的计划；
- 不把多个提示词一次交给Codex；
- 不允许Codex运行`human-only`脚本；
- 当前状态不清楚时先读`PROJECT_STATE.json`和`STATUS.md`，不要猜测。
