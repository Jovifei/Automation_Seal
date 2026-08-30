# Codex总任务书：部署 Jovi Automation V1.0

请把当前目录作为项目根目录执行。不要跳过预检，不要直接运行所有脚本。

## 最终目标

在本机搭建一套本地优先的数字产品自动化系统：

- 搜集嵌入式与摄影方向的公开市场信号；
- 对主题、竞品和用户痛点进行带来源的评分；
- 将已确认的PRD转成Spec Kit规格与任务；
- 自动完成代码开发、测试、说明文档和交付包制作；
- 将图文和视频草稿放入人工审核队列；
- 永远不自动发布、不自动聊天、不自动交易。

## 已知环境假设

- Windows 11 x64。
- Docker Desktop使用WSL2后端。
- NVIDIA RTX 4070 Super。
- 项目路径为纯英文且无空格，例如 `D:\Jovi-Automation`。
- 用户拥有Codex可用账号；OpenClaw模型授权在人工检查点完成。

如果实际环境不一致，请在只读预检报告中说明，不要擅自改系统。

## 阶段A：只读审计

1. 阅读全部根目录说明与`docs/*.md`。
2. 先运行 `python scripts/validate-package.py`，再运行 `scripts/preflight.ps1`；不得自动安装缺失软件。
3. 运行 `scripts/resolve-versions.ps1`，生成 `deploy/repositories.lock.json`。
4. 检查：磁盘、端口、WSL版本、Docker状态、Node/Python/uv/Git、GPU、网络和目录权限。
5. 对每个第三方仓库读取当前官方README、Release、License和Security。
6. 输出 `logs/phase-a-audit.md`。
7. 如有严重风险，停止；否则提交执行计划。

## 阶段B：核心Docker服务

1. 检查 `deploy/docker-compose.core.yml` 与当前n8n、PostgreSQL、changedetection.io兼容性。
2. 将已验证的镜像Tag或Digest写入`.env`和锁文件。
3. 执行 `scripts/bootstrap.ps1` 生成密钥和本地目录。
4. 运行 `scripts/start-core.ps1`。
5. 运行 `scripts/healthcheck.ps1`。
6. 验证所有端口仅绑定127.0.0.1。
7. 导出容器配置和日志摘要到`logs/phase-b-core.md`。

## 阶段C：OpenClaw、Spec Kit与Skill

1. 按官方稳定版本安装OpenClaw；优先使用官方推荐的Node版本和onboard守护进程方式。
2. 到模型登录或消息渠道绑定时暂停，提示用户完成。
3. 配置工作区为本项目`workspace`；非主会话启用Docker沙箱。
4. 安装Spec Kit，并在`workspace/products/embedded/modbus-toolkit`初始化Codex skills模式。
5. 确认Codex从`.agents/skills/`发现9个Skill；确认同一组Skill位于`workspace/skills/`供OpenClaw使用，并逐个安全审查。
6. 运行 `openclaw doctor` 并记录结果。
7. 输出 `logs/phase-c-agents.md`。

## 阶段D：自动化工作流

使用`n8n-skills`或等价的严格工作流开发方式，将`automation_specs/*.yaml`实现为n8n工作流。

最低工作流：

- 每日趋势简报；
- 竞品/规则页面变更；
- 产品开发任务入队；
- 人工审核闸门；
- 交付包生成与隔离；
- 健康检查与备份提醒。

要求：

- 每个工作流先在测试数据上验证。
- 工作流默认禁用，验证后逐个启用。
- 外部动作只能生成草稿或写入review-queue。
- n8n凭证必须使用Credential Store，不得出现在JSON导出中。
- 输出工作流JSON到`deploy/n8n-workflows/`并写测试报告。

## 阶段E：第一个产品MVP

以`Modbus RTU诊断与模板工具包`为第一个完整演示。

1. 阅读`context/source_docs/04_PRD_嵌入式知识产品_MVP.docx`和`context/PRODUCT_CONTEXT.md`。
2. 使用Spec Kit生成constitution、spec、plan和tasks。
3. 用户未提供目标板卡前，先实现与MCU无关的主机侧部分：
   - Modbus帧解析；
   - CRC16/Modbus；
   - 异常码解释；
   - Python测试向量；
   - 文档网站；
   - License清单。
4. MCU工程必须等用户明确GD32/STM32型号、IDE和编译器后再进入硬件相关实现。
5. 生成Alpha包到`workspace/review-queue`，不得自动发布。

## 阶段F：可选视频模块

1. 只有核心系统稳定后，才安装MoneyPrinterTurbo。
2. 优先使用官方Release或锁定镜像，不直接追随latest。
3. GPU启用前验证Docker可见NVIDIA GPU。
4. 仅使用原创/授权素材；输出必须进入review-queue。
5. 不配置自动上传或平台账号。

## 验收

执行`tests/smoke_tests.md`与`tests/acceptance_matrix.csv`，输出：

- `FINAL_DEPLOYMENT_REPORT.md`
- `SECURITY_REVIEW.md`
- `ROLLBACK_RUNBOOK.md`
- `LOCKED_VERSIONS.md`
- `STATUS.md`

只有P0验收全部通过，才报告“第一版完成”。


# 详细验收标准

## P0必须通过

1. 端口只绑定本机。
2. Git和日志没有密钥。
3. n8n和changedetection健康。
4. 数据库重启后数据保留。
5. 无批准文件时，产物无法进入approved。
6. 产物修改后，旧批准失效。
7. OpenClaw doctor无严重问题。
8. 非主Agent无法越过工作区。
9. 备份和隔离恢复演练成功。
10. 自动发布和消息功能均未配置。

## Codex交付物

- 最终部署报告。
- 版本锁文件。
- Compose实际渲染结果。
- 安全审查报告。
- 工作流JSON与测试记录。
- 备份恢复报告。
- 回滚手册。
- 未完成事项和需要用户决定的清单。

## 失败处理

P0失败时，不得通过“暂时忽略”结束任务。应将失败项标记为阻塞，停止后续阶段，提供最小修复步骤和可验证的重测方法。
