import requests
from model_client import call_model


def main() -> None:
    messages = [
        {"role": "user", "content": "请记住：我的项目叫 agent-lab。只回复已记住。"}
    ]

    try:
        first = call_model(messages)
        first_message = first["choices"][0]["message"]

        # TODO：追加第一轮的 assistant 消息
        messages.append(first_message)
        # TODO：追加第二轮的 user 提问
        messages.append({"role": "user", "content": "我的项目叫什么？只回复项目名。"})
        second = call_model(messages)
    except (RuntimeError, requests.exceptions.RequestException) as exc:
        print(f"模型请求失败：{exc}")
    else:
        print("第一轮：", first_message["content"])
        print("第二轮：", second["choices"][0]["message"]["content"])
        print("第二次请求角色：", [m["role"] for m in messages])


if __name__ == "__main__":
    main()