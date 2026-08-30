# Modbus RTU诊断与模板工具包 Alpha

状态：`HOST_SIDE_ALPHA_READY_FOR_CODEX_REVIEW`

这是包内预制的首个产品Alpha。Codex不应重新从零实现，而应先运行测试、审阅边界，再根据用户验证结果扩展。

## 已有功能

- CRC16/Modbus计算、附加和校验；
- 空格、冒号、逗号和`0x`格式十六进制输入；
- 常见请求、响应和异常帧解析；
- FC03、FC04、FC06、FC16；
- 寄存器和异常码解释；
- JSON格式CLI；
- 标准库`unittest`测试；
- 无第三方运行时依赖；
- CycloneDX SBOM；
- Alpha打包脚本。

## 快速测试

```powershell
cd products\modbus-rtu-toolkit
python -m unittest discover -s tests -v
python -m modbus_toolkit.cli "01 03 00 00 00 0A C5 CD"
```

## 构建Alpha包

```powershell
python scripts\build_alpha.py
```

输出到：

```text
dist\modbus-rtu-toolkit-alpha.zip
dist\modbus-rtu-toolkit-alpha.zip.sha256.txt
```

## 当前范围

这是主机侧诊断工具，不包含未经验证的板级工程。STM32/GD32示例必须在用户提供MCU、板卡和工具链后另行适配。

## 不承诺

- 不保证自动识别所有私有协议；
- 不替代示波器、逻辑分析仪和真实硬件联调；
- 不对高压、医疗、汽车安全等高风险系统给出最终安全结论；
- 不包含任何第三方课程、破解软件或权利不明资源。

## 待用户验证

- 最常见功能码；
- 用户希望的GUI/CLI形态；
- 是否需要CSV批量解析；
- 价格和售后范围；
- 第一块目标MCU板卡。
