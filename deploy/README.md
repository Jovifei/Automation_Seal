# 部署配置说明

- 初始启动只包含PostgreSQL和n8n。
- changedetection使用`research` profile：`docker compose --profile research up -d`。
- Redis使用`scale` profile，首期不需要。
- `.env.example`中的版本是候选值，目标机Codex必须重新验证Tag/Digest。
- 最终不得使用`latest`。
- 所有端口必须保持`127.0.0.1`绑定。
