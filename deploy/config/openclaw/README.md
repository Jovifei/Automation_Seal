# OpenClaw可选接入说明（默认不部署）

OpenClaw不是Phase 0/A、Track P或Track I首轮的依赖。只有出现明确的多渠道常驻调度需求，并且用户单独批准后，才评估启用。

本目录只保留最小兼容示例。Codex必须先核对当时的官方配置Schema，不得直接覆盖现有`~/.openclaw/openclaw.json`。

启用时必须满足：

- 工作区指向`E:/project/jovi-automation/workspace`；
- 非主会话使用当前官方沙箱等价配置；
- 对外DM保持配对或白名单，不得公开；
- 不授予闲鱼Cookie、消息、订单、支付或验证权限；
- 修改后运行当前官方诊断命令；
- 生成单独计划、回滚方案和人工批准回执。
