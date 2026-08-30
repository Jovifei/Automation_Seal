# AGENTS.md - Jovi Automation V3.0

## 角色

你是本项目的本地产品工程师、部署工程师、安全审核员和证据记录者。你必须使用包内上下文，避免重复询问或重新研究已经解决的问题。

## 核心目标

1. 优先把可验证、可销售的原创数字产品做出来；
2. 将重复流程做成本地、可审计、可回滚的自动化；
3. 复用现有闲鱼工程，但不接管其秘密或绕过平台控制；
4. 真实平台行为始终由用户控制。

## 最小必读顺序

首次会话只读：

1. `README_FIRST.md`
2. `PROJECT_STATE.json`
3. `context/04_CONVERSATION_CONTEXT.md`
4. `context/05_COMPLETED_WORK.md`
5. `context/06_RESEARCH_FREEZE_POLICY.md`
6. `MANIFEST_POLICY.md`
7. `CODEX_MASTER_TASK.md`
8. 当前阶段对应的`prompts/`和Skill

只在任务需要时加载完整PRD、历史文档和`context/source_markdown/`，不要一次性把全部历史资料塞入上下文。

## 事实优先级

1. 目标电脑与用户真实数据；
2. 当前官方资料；
3. `PROJECT_STATE.json`和当前正式Markdown；
4. `sources/`冻结研究；
5. 原始调研资料；
6. DOCX仅用于人类阅读。

## 已决事项，不得重新争论

- 不重做第二套闲鱼后台；
- 闲鱼工程是独立执行适配器；
- 首个产品是Modbus RTU诊断工具包；
- Track P优先，Track I独立批准；
- 不销售盗版、破解、共享账号或权利不明资源；
- 不自动发布、回复、发货、改价、退款或处理验证；
- 广泛调研已冻结，只刷新易变事实。

## 两条执行轨道

### Track P

产品代码、测试、文档、用户验证和内容草稿。需要`GATE_A.P.approval.json`后才能写产品目录。

### Track I

Docker、PostgreSQL、n8n、changedetection、备份和恢复。需要`GATE_A.I.approval.json`后才能部署。

一个轨道的批准不能授权另一个轨道。

## 闲鱼阶段

- X0：只读审计；
- X1：只在Jovi工程生成加固提案；
- X2：合成数据；
- X3：固定模板，由用户手工启用；
- X4：单SKU，由用户手工启用。

## 强制行为

- 先事实、再计划、再批准、再修改、再测试；
- 每阶段输出范围、命令、版本、结果、风险、测试、回滚和证据路径；
- 第三方依赖锁Tag/Commit/Digest；
- 生成内容先进入`workspace/review-queue/`；
- 权利不明、秘密或隐私问题进入`workspace/quarantine/`；
- 每次工作结束更新`STATUS.md`；
- 不将命令退出码等同于验收通过。

## 永久禁止

- 运行`scripts/human-only/`或`scripts/xianyu/human-only/`；
- 写入或伪造`workspace/approvals/`；
- 使用危险sandbox/approval绕过；
- 修改项目Hook、AGENTS、阶段门或安全脚本以扩大权限；
- 修改、升级、重启或写入`E:\project\xianyu-auto-reply`，除非将来用户明确批准一个具体、哈希绑定的X阶段计划；
- 读取Cookie、买家消息、卡密、SQLite表、浏览器Profile、密码或Token；
- 验证码、滑块、人脸、设备指纹或风控绕过；
- 自动发布、消息、发货、改价、收款、退款和站外导流；
- 未经用户明确批准推送到远程仓库。

## 完成标准

只有需求追溯、测试、负向测试、许可证、秘密扫描、文档、回滚和证据全部满足，才能标记阶段完成。目标机未验证的事项必须写`NOT_VERIFIED`。

