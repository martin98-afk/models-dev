#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 models.dev/api.json 提取精简版：剔除与模型选择/使用无关的字段。

剔除：
- 模型: description（纯文本描述，占体积最大）
- 服务商: env/npm/doc（SDK 集成信息，DriFox 配置模型用不到）
保留：模型能力/价格/限制/状态等全部字段 + 服务商 id/name/api。
"""
import json
import sys

DROP_MODEL = {"description"}
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
