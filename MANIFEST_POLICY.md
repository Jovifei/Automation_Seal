# 文件清单与运行期变更策略

本工程使用两类内部SHA256清单，它们承担不同职责。

## 1. `MANIFEST.sha256`：完整交付快照

它覆盖最终ZIP内除自身之外的全部交付文件，用于证明“刚解压的目录”与最终打包时一致。

只应在以下时点验证：

```powershell
python .\scripts\validate-package.py --verify-shipment
```

- ZIP刚解压后；
- 第一次只读审计开始前；
- 目录内尚未生成新的报告、状态或批准回执时。

第一次运行后，`reports/`、`STATUS.md`、`PROJECT_STATE.json`和工作区状态会按设计发生变化，因此完整交付快照自然不再匹配。不得为了“恢复匹配”删除真实运行证据，也不得让Codex重写该清单。

## 2. `FRAMEWORK_MANIFEST.sha256`：不可变安全框架

它只覆盖阶段门、Hook、批准验证、只读审计和包验证等安全关键文件。默认验证命令会在每个阶段检查它：

```powershell
python .\scripts\validate-package.py
```

如果该清单不匹配，应立即停止。不要通过关闭Hook、跳过审批或重建清单继续执行。

## 3. 允许变化的运行期范围

以下内容会在正常执行中变化：

- `PROJECT_STATE.json`；
- `STATUS.md`；
- `reports/`；
- `workspace/review-queue/`；
- `workspace/approved/`；
- `workspace/quarantine/`；
- `workspace/approvals/`，但只能由用户本人运行`human-only`脚本生成；
- `workspace/products/`和`products/`，仅在Track P批准后；
- `deploy/.env`、`deploy/.env.runtime`、`LOCKED_VERSIONS.json`，仅在Track I批准后；
- `data/`、`logs/`和`backups/`。

外部ZIP的SHA256是整个压缩包最外层的完整性证明；内部两类清单则分别负责“初始交付快照”和“运行中不可变安全框架”。

## 一次性 Phase2B Framework 迁移例外

仅在 Jovi Decision V3 与 D2 独立 PASS 精确绑定候选 body/sidecar/apply 工具时允许一次性迁移；不嵌入 Manifest SHA，不允许自动 re-baseline、通用重建或修改 MANIFEST.sha256，迁移后恢复不可变策略。
