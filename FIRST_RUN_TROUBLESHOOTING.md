# 第一次运行排障

## Python找不到

只读入口要求Python 3.11或更高版本。先检查：

```powershell
py -3.11 --version
python --version
```

不要让Codex未经审阅自动修改系统PATH。安装Python后重新打开Codex会话。

## Hook未信任或报错

在Codex CLI当前工程运行：

```text
/hooks
```

阅读：

```text
.codex/hooks.json
scripts/codex/pre_tool_guard.py
scripts/codex/Invoke-PreToolGuard.ps1
```

只信任当前精确内容。不要使用绕过Hook信任参数。

## Codex不能读取闲鱼目录

在当前会话添加只读根：

```text
/sandbox-add-read-dir E:\project\xianyu-auto-reply
```

不要将该目录设为可写。

## 没有Docker或Docker未运行

Phase A可以记录为Track I阻塞，但Track P产品Alpha仍可进行。不要为了首个Alpha强行安装全部Docker服务。

## GitHub API失败或限流

使用包内冻结研究快照继续；在报告中标记`NOT_VERIFIED_CURRENT`。不要因为版本刷新失败而重新进行全部市场和架构调研。

## 闲鱼工程路径不存在

确认目录是否为：

```text
E:\project\xianyu-auto-reply
```

使用正确路径重新运行只读入口。不要自动克隆或覆盖现有实例。

## 只读审计出现敏感信息

立即停止，不复制报告到外部。删除该运行生成的报告副本，保留现场，检查审计脚本和输出，再从干净副本重新运行。
