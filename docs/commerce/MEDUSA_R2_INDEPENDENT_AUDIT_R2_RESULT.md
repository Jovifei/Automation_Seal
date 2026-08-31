# Medusa R2-R1 独立审阅 R2 结果

**审阅类型：** 新会话、只读、独立复算
**审阅日期：** 2026-09-01
**结论：** `MEDUSA_SPIKE_PASS_WITH_GAPS`
**生产集成：** `production_integration_allowed=false`

## 1. 审阅对象

- 隔离源码：`E:\Claude_allow\Download\jovi-medusa-v2-spike-r2-r1\backend\jovi-medusa-backend`
- 冻结包：`workspace/review-queue/commerce-v1/medusa-v2-spike-remediation-r2-r1/`
- Package manifest：117 项，SHA256 `748ec4bcc2eb7061b2280ef367e43fcc0458bb21ff46583aacf882e1cd90a4c6`
- Source snapshot tree：73 项，SHA256 `d15eb73e94a1fcf8b19ac2c8e03b317fa5ea94f7d8242548aa3eac4dec334e8d`
- Medusa：`2.19.0`，Tag commit `87d77fa1b56ec287aa6655aaa2f54245387aa2f2`
- Backend 镜像：image ID `sha256:53832b2b06a069bbfb10574c56fafa338bc8de46373bd41a50f5755357bfcd66`，manifest `sha256:b52f4f5d8ca5fecc19fe15df705a4fbd1bfe97b5e27d7c7b30e3503b6559d494`。

## 2. Gate 结果

| Gate | 结果 | 复核摘要 |
| --- | --- | --- |
| R1 Policy | PASS | capability mint 为 `service.ts` 词法私有；无独立 capability 文件或导出；直接 service/module import 负测通过。 |
| R2 Provenance | PASS（synthetic） | Order/Payment 重读、`pp_system`、金额/币种/版本、payment snapshot、evidence/asset/entitlement/receipt provenance 均绑定。 |
| R3 Replay/Recovery | PASS（synthetic） | Backend PID1 `docker kill --signal KILL` 后保留 `RECOVERY_PENDING`，重启健康，约 120 秒内重放为单一 Entitlement/Receipt。 |
| R4 Evidence/License | PASS | 117 项 package、73 项 source、image/lock labels、Oracle、SBOM 和四个 Admin 包许可证范围均可复算。 |

## 3. 剩余缺口

- **Medium：** Jest 仍使用 `--forceExit`；当前测试退出码为 0，但没有证明所有异步句柄自然收尾。后续隔离验证应增加 `--detectOpenHandles` 或无强制退出的稳定收尾证据。
- **Low：** Admin 只完成 loopback HTTP `/health` 与 `/app` smoke，没有交互式浏览器/权限操作验收。

这两项不否定当前 synthetic X2 闭环，但在生产采用设计中必须单独关闭；本结论不是生产批准、人工付款批准、R12 Decision 或真实平台证明。

## 4. 保留边界

- 仅 synthetic X2；人工付款入口保持禁用。
- 不启用 Stripe、Webhook、邮件、Storefront、外网下载、闲鱼、自动交付或真实客户数据。
- R12 Git baseline/import、Hook、remote 和正式 Medusa 目录均未执行或修改。
- Python oracle 仅作为验收参考，不是 Medusa 运行依赖。
