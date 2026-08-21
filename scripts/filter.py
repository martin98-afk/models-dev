#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 models.dev/api.json 提取精简版：剔除与模型选择/使用无关的字段。

剔除原则（以 DriFox 实际消费为准，见 app/core/models_dev_sync.py）：
- 模型 id：与 models 字典 key 重复（冗余）
- 模型 provider：与所属服务商重复（冗余）
- 模型 attachment/experimental/interleaved/temperature/knowledge/open_weights：
  DriFox 未消费、且与"选模型/用模型"无关
- 服务商 env/npm/doc：SDK 集成信息，DriFox 未消费

保留（DriFox 消费 + 通用能力标识）：
- 模型: name/description/family/status/reasoning/reasoning_options/limit/modalities/
  cost/release_date/last_updated/tool_call/structured_output
- 服务商: id/name/api/models
"""
import json
import sys

DROP_MODEL = {"id", "provider", "attachment", "experimental", "interleaved",
              "temperature", "knowledge", "open_weights"}
DROP_PROVIDER = {"env", "npm", "doc"}


def main(src: str, dst: str) -> None:
    with open(src, encoding="utf-8") as f:
        data = json.load(f)
    out = {}
    for pid, p in data.items():
        op = {k: v for k, v in p.items() if k not in DROP_PROVIDER}
        op["models"] = {
            mid: {k: v for k, v in m.items() if k not in DROP_MODEL}
            for mid, m in p.get("models", {}).items()
        }
        out[pid] = op
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"filtered: {src} -> {dst}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
