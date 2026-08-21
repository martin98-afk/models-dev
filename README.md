# models-dev

定时同步并精简 [models.dev](https://models.dev) API 数据镜像仓库。

## 内容

| 文件 | 说明 |
|---|---|
| `models-dev.json` | 精简版镜像（约 3.5MB）：全部 193 个服务商 + 全部 7230 个模型，剔除 `description`（纯文本描述）与服务商 `env/npm/doc`（SDK 集成信息） |
| `.github/workflows/sync.yml` | Actions 工作流：每小时拉取 → 过滤 → 有变化才提交 |
| `scripts/filter.py` | 过滤脚本（本地可复用：`python3 scripts/filter.py api.json models-dev.json`） |

## 触发机制

- **定时触发**：每小时整点（cron `0 * * * *`）
- **手动触发**：仓库 → Actions → `sync-models-dev` → Run workflow
- **推送凭证**：`GITHUB_TOKEN` 自动注入，无明文密钥

## 使用

```bash
curl -fsSL https://raw.githubusercontent.com/martin98-afk/models-dev/master/models-dev.json -o models-dev.json
```
