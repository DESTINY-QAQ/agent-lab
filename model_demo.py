
import requests
import json
from model_client import call_model


def main() -> None:

    try:
        messages = [
        {"role": "user", "content": "请用一句话解释什么是 Agent。"}
        ]
        body = call_model(messages)
    except (RuntimeError, requests.exceptions.RequestException) as exc:
        print(f"模型请求失败：{exc}")
        return
    else:
        print("返回类型：", type(body).__name__)
        choice = body["choices"][0]
        summary = {
            "message": choice["message"],
            "finish_reason": choice["finish_reason"],
            "usage": body["usage"],
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
if __name__ == "__main__":
    main()