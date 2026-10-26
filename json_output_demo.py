import json
from model_client import call_model
from answer_formatter import format_final_answer


def main() -> None:
    messages = [{
        "role": "user",
        "content": (
            '这是格式测试，请只返回这个 JSON 对象：'
            '{"insufficient": true, "answer": ""}'
        ),
    }]

    body = call_model(messages, json_output=True)
    choice = body["choices"][0]
    print("结束原因：", choice["finish_reason"])

    if choice["finish_reason"] != "stop":
        print("模型输出未正常完成")
        return

    try:
        result = json.loads(choice["message"]["content"])
        display = format_final_answer(result, [])
    except (TypeError, ValueError) as exc:
        print("最终结果格式错误：", exc)
        return

    print("解析后类型：", type(result).__name__)
    print("解析后的结果：", result)
    print("程序展示：", display)


if __name__ == "__main__":
    main()