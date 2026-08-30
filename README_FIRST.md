# Jovi Automation 最终交付包 V3.0

生成日期：2026-07-12  
推荐工程目录：`E:\project\jovi-automation`  
现有闲鱼工程：`E:\project\xianyu-auto-reply`

## 1. 交付目的

这个压缩包就是本次对话的最终工程交接物。解压后，Codex 不需要依赖当前聊天记录，也不需要重新进行大范围市场调研，就能知道：

- 项目为什么立项；
- 已经做过哪些市场、产品、渠道、开源和科研调研；
- 已经确定了哪些架构与风险边界；
- 哪些内容已经完成；
- 哪些事实只能在目标电脑上验证；
- 下一步应该执行什么；
- 每个阶段何时必须停止并等待用户批准。

包内没有复制整段原始聊天，而是将所有与决策和执行有关的内容整理成结构化工程上下文。核心入口是：

```text
PROJECT_STATE.json
context/04_CONVERSATION_CONTEXT.md
context/05_COMPLETED_WORK.md
context/06_RESEARCH_FREEZE_POLICY.md
CODEX_MASTER_TASK.md
NEXT_STEP_MAP.md
```

## 2. 已确定的最终架构

不再开发第二套闲鱼后台。现有工程：

```text
E:\project\xianyu-auto-reply
```

继续作为独立的“闲鱼执行适配器”。Jovi Automation 负责：

- 市场和用户证据；
- PRD和变更规格；
- 产品代码、测试和文档；
- 许可证与密钥检查；
- 商品文案、FAQ和固定回复候选；
- 待审核交付包；
- SHA256绑定的人工批准。

闲鱼工程负责自身的账号、商品、订单和平台会话。两套工程不合并数据库，不共享密钥，Jovi Automation 不直接写闲鱼 SQLite。

## 3. 快速落地策略

工程拆为两条独立轨道：

### Track P：产品快速轨道

优先把可出售的产品做出来，不等待完整基础设施：

```text
现成Modbus主机侧Alpha
→ 本机测试和改进
→ 用户访谈/付费意向
→ 商品草稿与内容草稿
→ 内测
→ 小额付费验证
```

包内已经放入可运行的 `products/modbus-rtu-toolkit/` Alpha，不需要 Codex 从零搜索或重写。

### Track I：基础设施轨道

在确认重复工作和付费需求后，再部署：

```text
PostgreSQL
→ n8n
→ changedetection.io
→ 备份/恢复
→ 研究与审核流水线
```

Docker 和 n8n 不是首个产品 Alpha 的前置条件。

## 4. 用户第一次操作

### 4.1 校验ZIP

使用随ZIP提供的 `.sha256.txt` 校验文件。校验不一致时不要解压。

解压后，第一次入口还会自动执行：

```powershell
python .\scripts\validate-package.py --verify-shipment
```

它验证完整交付快照。第一次运行后，报告和状态文件会正常变化，后续阶段改为验证不可变安全框架。两类清单的区别见`MANIFEST_POLICY.md`。

### 4.2 解压

将ZIP解压到 `E:\project`。最终结构必须是：

```text
E:\project\
├── jovi-automation\
└── xianyu-auto-reply\
```

`jovi-automation`根目录应直接包含：

```text
AGENTS.md
CODEX_MASTER_TASK.md
CODEX_START_PROMPT.txt
PROJECT_STATE.json
FAST_TRACK.md
scripts\
docs\
context\
products\
```

### 4.3 备份现有闲鱼工程

在任何变更前，用你当前可靠的方式备份闲鱼工程的：

- `data/`；
- `browser_data/`；
- `global_config.yml`；
- Compose文件；
- 当前Git Commit、分支和工作区状态。

这些内容不要复制到Jovi工程、聊天或报告中。

### 4.4 打开Codex

在Codex中打开：

```text
E:\project\jovi-automation
```

然后复制根目录 `CODEX_START_PROMPT.txt` 全文发送。

## 5. 第一次Codex只执行一条命令

```powershell
.\scripts\00-run-readonly-audit.ps1 `
  -XianyuRepoPath 'E:\project\xianyu-auto-reply'
```

它会完成：

1. 包结构和清单校验；
2. 离线合成安全测试；
3. Windows、Python、Codex、Git、Docker等本机能力检查；
4. 对少量易变化的开源版本做窄范围刷新；
5. 对本地闲鱼工程做脱敏X0只读审计；
6. 生成Track P和Track I的下一阶段计划；
7. 更新`STATUS.md`并停止。

## 6. 避免重复搜索的规则

Codex不得重新做以下已经完成的广泛调研：

- 平台渠道选择；
- 嵌入式与摄影产品机会；
- 首个MVP选择；
- 是否重做闲鱼后台；
- 开源项目大范围选型；
- 基础安全和版权边界。

这些结论位于`context/`、`docs/`和`sources/`。

Codex只在以下情况下做有限刷新：

- 软件版本、Release、Security和许可证可能发生变化；
- 当前平台规则或法律要求影响真实上线；
- 本机事实与文档冲突；
- 用户明确要求重新研究。

详细策略见`context/06_RESEARCH_FREEZE_POLICY.md`。

## 7. Codex不会自动做的事

- 自动发布或修改闲鱼商品；
- 向真实买家发送生成式AI消息；
- 自动发货、改价、收款或退款；
- 自动处理滑块、验证码、人脸或设备风控；
- 读取Cookie、买家消息、卡密或SQLite表内容；
- 运行`human-only`脚本；
- 伪造批准文件；
- 将任何代码推送到远程仓库；
- 自动升级现有闲鱼系统。

## 8. 何时可以称为完成

交付包准备工作已经完成。真正的“本地部署完成”仍必须由目标电脑上的证据确认，包括：

- 本机环境审计；
- 产品Alpha测试；
- 需要时的核心服务启动；
- 备份与隔离恢复；
- X2合成数据演练；
- 许可证和真实平台规则确认。

因此，当前状态是：

```text
READY_FOR_CODEX_PHASE_0_A_X0
```

不是：

```text
DEPLOYED_AND_LIVE
```
