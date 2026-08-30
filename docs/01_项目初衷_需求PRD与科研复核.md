# 1. 项目初衷

用户希望家中电脑在无人持续控制时，由Codex完成调研、产品开发、测试、文档和内容草稿，减少重复工作并形成收入。工程不追求未经监管的自动交易，而是把可验证的生产环节自动化，把账号、承诺、支付和争议保留给用户。

# 2. 用户优势与产品方向

用户是嵌入式工程师，优势包括STM32/GD32、FreeRTOS、Modbus、4G、MQTT、OTA、Bootloader、HardFault和状态机。摄影是第二产品线，必须使用用户原创且权利清晰的素材。

# 3. 首个嵌入式MVP

首个产品为“Modbus RTU诊断与模板工具包”。V3.0已经预制主机侧Alpha：

- 十六进制帧解析；
- CRC16/Modbus；
- FC03、FC04、FC06、FC16；
- 异常码；
- JSON CLI；
- 12项标准库单元测试；
- SBOM、第三方声明和Alpha打包。

板级工程等待用户明确MCU、开发板和工具链。

# 4. 摄影MVP

“金鸡湖城市风光调色与机位工具包”包括原创XMP、练习RAW、原片与成片、调色视频和机位指南。没有原创素材时不阻塞嵌入式主线。

# 5. 渠道结论

| 方向 | 主渠道 | 成交渠道 | 说明 |
|---|---|---|---|
| 嵌入式 | B站、抖音、小红书 | 闲鱼 | 技术信任、故障演示、搜索图文 |
| 摄影 | 小红书、抖音 | 闲鱼 | 视觉结果和原创工具包 |
| 微博 | 同步 | 非主成交 | 低投入维护 |

# 6. 知识和资源销售边界

不卖资料数量，卖经过验证的结果。禁止未经授权的课程、破解软件、共享账号、他人预设、公司代码和权利不明源码。允许原创产品、明确商业授权资源、合规开源组件和官方免费软件的配置服务。

# 7. 技术与科研路线

## 核心

- Codex、项目AGENTS、Skill和Hook；
- 轻量变更记录，较大产品可使用Spec Kit；
- Promptfoo、Gitleaks、Trivy和MkDocs；
- Track I按需部署n8n、PostgreSQL和changedetection。

## 嵌入式增强

- 主机侧Python测试；
- Ceedling、Unity和CMock；
- PlatformIO跨平台构建；
- Renode在目标SoC支持时做虚拟板级测试。

## 研究和供应链

- Docling处理有权使用的本地文档；
- PaperQA2用于文献密集研究；
- Syft生成SBOM；
- Cosign在稳定发布后签名；
- OpenClaw、Langfuse和视频工具延后。

## 方法论参考

OpenSpec、BMAD、Superpowers和12-Factor Agents只借鉴规格、TDD、调试、状态和人工介入原则，不在首期同时安装多套总控框架。

# 8. 调研冻结

渠道、MVP、架构和大范围选型已冻结。Codex只刷新易变化的Release、Security、License、平台规则和本机事实。详细策略见：

```text
context/06_RESEARCH_FREEZE_POLICY.md
sources/technology_route_review_2026-07-12.md
```
