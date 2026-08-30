# 用户操作清单

## A. 现在立即执行

1. 校验ZIP的SHA256。
2. 解压到`E:\project\jovi-automation`。
3. 确认`E:\project\xianyu-auto-reply`仍然独立存在。
4. 备份闲鱼工程的数据库、配置、浏览器状态和Compose。
5. 在Codex中打开Jovi工程根目录。
6. 审阅并信任项目Hook；必要时为闲鱼目录添加只读根。
7. 复制`CODEX_START_PROMPT.txt`全文给Codex。

## B. 首次审计后

检查：

```text
reports\package-static-tests\
reports\phase-a\
reports\xianyu\x0\
reports\gates\GATE_A_PLAN.json
STATUS.md
```

确认报告没有秘密、Cookie、买家消息、卡密或数据库内容。

## C. 推荐只批准产品轨道

在独立PowerShell中运行Codex输出的准确命令。标准形式为：

```powershell
.\scripts\human-only\Approve-Gate.ps1 `
  -Gate GATE_A `
  -Track P `
  -PlanPath .\reports\gates\GATE_A_PLAN.json `
  -ExpectedSha256 '<64位哈希>' `
  -Approver 'Jovi'
```

该脚本只能由用户本人运行。它会生成：

```text
workspace\approvals\GATE_A.P.approval.json
```

回执生成后，将`prompts/10_track_p_alpha.txt`全文发送给Codex。

## D. 何时批准基础设施轨道

只有在出现稳定重复工作、产品验证或明确需要时，再独立批准Track I：

```powershell
.\scripts\human-only\Approve-Gate.ps1 `
  -Gate GATE_A `
  -Track I `
  -PlanPath .\reports\gates\GATE_A_PLAN.json `
  -ExpectedSha256 '<64位哈希>' `
  -Approver 'Jovi'
```

回执生成后，将`prompts/20_track_i_core.txt`全文发送给Codex。

所有阶段映射见`NEXT_STEP_MAP.md`。

## E. 永远不要交给Codex或聊天

- Cookie和浏览器Profile；
- 买家消息和订单隐私；
- 管理员密码、Token、API Key；
- 卡密库存；
- 支付和退款凭据；
- 公司、客户和雇主源码；
- 未授权课程、软件或摄影素材。
