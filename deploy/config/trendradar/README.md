# TrendRadar接入说明

采用上游官方Docker Compose，不将其硬编码进核心Compose。

Codex执行：

1. 锁定稳定Tag/Commit。
2. 克隆到`vendor/TrendRadar`。
3. 将本目录`frequency_words.txt`合并到上游关键词配置。
4. API Key/Webhook只写入上游`docker/.env`，并加入Git忽略。
5. 第一阶段只启动`trendradar`，MCP服务在需要对话分析时再启用。
6. 输出只写入本地研究目录或review-queue。
