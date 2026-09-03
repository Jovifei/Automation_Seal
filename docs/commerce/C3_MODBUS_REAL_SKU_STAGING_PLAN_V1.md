# C3：Modbus RTU Diagnostic Toolkit 真实 SKU Staging 计划 V1

## 1. 前置条件

只有以下全部成立才开始：

- `R6_POST_IMPORT_PASS`
- `R2R3_INDEPENDENT_AUDIT_PASS`
- `C2_INDEPENDENT_AUDIT_PASS`
- Commerce 六个真实权限标志仍为 false

任何缺失 → `C3_PRECONDITION_FAIL`。

## 2. 产品源

只读输入：`E:\project\jovi-modbus-diagnostic-toolkit-v1`

不得为了 Commerce 流程修改产品源；如产品本身不满足 release 要求，应返回产品仓单独修复。

## 3. 产品资格冻结

生成 `C3_MODBUS_SOURCE_QUALIFICATION.json`，至少绑定：

- source commit / dirty state
- Windows build artifact
- installer/ZIP SHA256
- version
- supported OS
- test command/results
- license inventory
- README/user guide
- third-party notices
- known limitations

要求工作树可解释且发布字节可复算。

## 4. Product Manifest

从真实证据生成正式候选 manifest：

- `product_id=E01`
- name/version
- rights_status
- deliverables
- supported_platforms
- acceptance_criteria
- third_party_dependencies
- support boundary

不得自动补写无法从产品仓证据支持的兼容性或能力。

## 5. DigitalRelease / Asset / Package

基于 C2 已审核模型创建真实 SKU Release：

- release immutable
- asset private
- artifact bytes 不重编译、不修改
- DeliveryPackage 两次构建字节一致
- package manifest 绑定原产品 artifact SHA

## 6. Listing Candidate

生成：

- verified title
- description
- 功能边界
- 系统要求
- 交付内容
- FAQ
- 售后/支持边界
- rights statement
- version/update statement

禁止未经证据支持的“全兼容”“永久更新”“包教会”等承诺。

## 7. Staging Order Flow

只使用 synthetic customer/order/payment evidence：

`Real SKU → Synthetic Order → Synthetic Payment Evidence → Jovi Entitlement → DeliveryPackage → DeliveryReceipt → DownloadGrant → Draft Bundle`

最终状态仅可 `READY_FOR_HUMAN_DELIVERY`。

## 8. 必测负例

- 产品仓 dirty/unbound
- release artifact SHA drift
- installer mismatch
- license missing
- unsupported OS claim
- wrong product/version order
- stale package
- product asset tamper
- entitlement/order mismatch
- duplicate replay

## 9. 独立审计

实现 Agent 只能停在 `READY_FOR_C3_INDEPENDENT_AUDIT`。

独立 Agent 结论只能：

- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_PASS`
- `C3_REAL_SKU_STAGING_INDEPENDENT_AUDIT_FAIL`

PASS 后才允许进入 C4 Human Pilot。