import os
import requests


def call_model(messages: list[dict],tools: list[dict] | None = None,) -> dict:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("未读取到 DEEPSEEK_API_KEY")
    # 由你搬入原来的 POST 请求、状态检查和返回逻辑
    #请求体中的 "messages" 使用传入的 messages。
    #保留原来的模型、超时等参数。
    #检查 HTTP 状态后，返回 response.json()。
    #函数内不打印，由入口处理异常、展示结果。
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": "deepseek-flash",
                "messages": messages,
                "tools": tools,
                "thinking": {"type": "disabled"},
                "max_tokens": 128,
                "stream": False,
            },
            timeout=60,
        )
        response.raise_for_status()
        body = response.json()
    except requests.exceptions.RequestException as exc:
        raise exc
    else:
        return body