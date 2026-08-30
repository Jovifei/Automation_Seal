# 1. Codex总原则

Codex使用包内上下文，不重新进行广泛调研。每个阶段先读取当前状态、验证回执、执行限定范围、生成证据、更新状态并停止。

# 2. Phase 0/A/X0

第一次只运行：

```powershell
.\scripts\00-run-readonly-audit.ps1 `
  -XianyuRepoPath 'E:\project\xianyu-auto-reply'
```

产物：

- 包验证和离线测试；
- 本机能力报告；
- 易变上游版本报告；
- X0脱敏报告；
- `GATE_A_PLAN.json`和SHA256；
- 更新后的状态。

完成后必须停止。

# 3. GATE_A分轨道

```text
GATE_A.P → 产品快速轨道
GATE_A.I → 基础设施轨道
```

回执分别为：

```text
workspace/approvals/GATE_A.P.approval.json
workspace/approvals/GATE_A.I.approval.json
```

# 4. Track P

前置：验证Track P回执。

使用现有`products/modbus-rtu-toolkit/`，执行：

1. 单元测试和CLI示例；
2. 代码、规格、SBOM和许可证审查；
3. 补充真实报文和错误测试；
4. 构建Alpha ZIP、SHA256和报告；
5. 生成访谈、商品和内容草稿；
6. 写入review-queue；
7. 更新状态并停止。

不启动Docker，不修改闲鱼工程，不做板级猜测。

# 5. Track I

前置：验证Track I回执。

1. 刷新正式Release并锁定镜像Tag/RepoDigest；
2. 用户审阅`.env`并输入秘密；
3. 启动PostgreSQL和n8n；
4. 健康检查和本机端口检查；
5. 备份数据库、n8n数据和加密密钥；
6. 隔离临时恢复；
7. 按需启用changedetection；
8. 生成报告并停止。

# 6. X1/X2

X1只在Jovi报告目录生成并行加固提案，不覆盖闲鱼文件。X2只用合成数据运行候选包和AI回复正负向测试。

# 7. X3/X4

Codex只生成固定回复和单SKU导入候选。用户本人在闲鱼后台启用；Codex不能代替用户点击、调用写API或修改数据库。

# 8. 研究和内容

公开研究任务只输出带来源的证据卡和审核草稿。Docling和PaperQA2仅处理用户有权处理的材料。内容和视频都先进入review-queue，不自动发布。

# 9. 报告格式

每阶段报告包含范围、输入、版本、命令、结果、失败、风险、许可证、变更、测试、回滚、证据、计划SHA256和停止点。
