import json
import requests
from model_client import call_model
from tool_definitions import TOOLS


def main() -> None:
    messages = [
        {
            "role": "user",
            "content": "请使用 inspect_text 工具统计以下文本的字符数和行数：Hello\nAgent",
        }
    ]

    try:
        body = call_model(messages, tools=TOOLS)
    except (RuntimeError, requests.exceptions.RequestException) as exc:
        print(f"模型请求失败：{exc}")
    else:
        choice = body["choices"][0]
        print("结束原因：", choice["finish_reason"])
        print(json.dumps(choice["message"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()