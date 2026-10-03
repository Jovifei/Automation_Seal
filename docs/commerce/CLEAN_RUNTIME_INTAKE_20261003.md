# 替代Runtime独立干净基线

日期：2026-10-03

Jovi再次明确继续完全替换Medusa并采用GitHub双向执行接力。
实际目标GitHub仓库是 `Jovifei/Automation_Jovi`，替代此前建议仓库名。

## 接收事实

- 原本地候选：`c091ac3f63ba96b37aba59d3f4184caf4659bff5`，原历史保持隔离，**禁止上传**。
- 新接收目录（本地事实）：`E:\\project\\jovi-xianyu-commerce-intake`。
- 新独立根提交：`734949ba047d33c76fc9fee013b1373404c14a6f`。
- 从旧候选Git对象只导出14个允许文件；raw blob逐文件一致。
- `INTAKE_MANIFEST.json`记录来源blob、SHA256和大小；新README/AGENTS/来源约定/git属性等接收元数据单独新增，不宣称完整复制旧历史。
- 本轮Python 3.14离线21测试PASS。
- Gitleaks v8.24.0对工作树与完整新历史扫描均为零发现。
- 旧上游2提交扫描仍有10项未资格化 finding，因此旧历史不得进入新Runtime GitHub。
- 原产品包和原运行环境未修改；Runtime源码不得混入Governance。

## GitHub可见性事实

远端已核验 `Jovifei/Automation_Jovi` 存在，当前为 **Public / empty**。
源码尚未上传。

本地GitHub安全设置检查报告：当前Public仓的secret scanning与push protection已启用；
切换Private的确认页面提示Advanced Security将关闭。因此私有化不是“无安全副作用”的普通设置，
需要Jovi对该具体安全效果作出确认后再执行。Gitleaks CI不能被描述为GitHub这些保护能力的完整等价替代。

## 双向接力

在准确的新根SHA上传后：

1. Remote ChatGPT在 `Automation_Jovi` 基于可验证Git证据实施下一受限阶段（源码接收验证、CI、构建/容器、合成测试、幂等/恢复验证），实际提交并返回SHA/branch/PR/CI。
2. Local Codex拉取该提交，执行本机构建/测试，修复本地暴露的问题并push回同一受审分支。
3. Remote ChatGPT重新审查Git diff、CI与本地执行凭据，再决定下一阶段。

在源码上传前不得宣称Runtime源码已审核。真实闲鱼、支付、客户、自动交付与生产编排门禁继续关闭。
