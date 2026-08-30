# 已完成工作清单

## 业务与产品

- 平台渠道比较和优先级；
- 嵌入式知识产品机会评估；
- 摄影原创数字产品机会评估；
- 产品价格梯度和商业模型；
- 用户调研方案和访谈问题；
- 嵌入式MVP PRD；
- 摄影MVP PRD；
- 内容运营方案；
- 90天执行计划；
- 版权和风险控制手册；
- Excel执行看板。

## 技术与科研路线

- Codex、Spec Kit、n8n、changedetection、Promptfoo、Gitleaks、Trivy、Docling、PaperQA2、MkDocs、OpenClaw、视频工具等选型；
- OpenSpec、BMAD、Superpowers和12-Factor Agents方法论复核；
- PlatformIO、Ceedling、Unity和Renode嵌入式测试路线；
- Syft SBOM和Cosign签名路线；
- 官方Codex Plugin/Skill方向复核。

## 架构与执行

- Jovi控制平面和闲鱼执行适配器分离；
- X0-X4灰度阶段；
- Track P/Track I独立批准；
- SHA256绑定的阶段门；
- review-queue、approved和quarantine目录；
- 本机端口、密钥、备份、恢复和回滚策略；
- Codex项目规则、Skill和安全Hook；
- 第一轮只读入口和阶段提示模板。

## 已预制产品

`products/modbus-rtu-toolkit/`包含：

- CRC16/Modbus；
- 十六进制帧解析；
- FC03、FC04、FC06、FC16及异常帧解释；
- CLI；
- 标准库单元测试；
- 示例；
- 中文README；
- SBOM和第三方声明；
- Alpha打包脚本。

Codex的任务是先运行测试、审阅和改进，而不是重新从零实现。

## 尚未完成且必须由目标机验证

- 用户电脑实际环境；
- 本地闲鱼实例实际Commit、配置和运行状态；
- 当前官方Release和安全公告；
- Docker镜像拉取和RepoDigest；
- n8n真实启动；
- 备份和隔离恢复；
- 真实平台规则和商业许可证澄清；
- 真实用户访谈和付费验证。
