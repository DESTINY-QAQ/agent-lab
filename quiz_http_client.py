import requests

BASE_URL = "http://127.0.0.1:8000"


def post_json(path: str, payload: dict) -> dict:
    response = requests.post(
        BASE_URL + path,
        json=payload,
        timeout=120,
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        try:
            detail = response.json().get("detail", str(exc))
        except (ValueError, AttributeError):
            detail = str(exc)
        raise RuntimeError(f"HTTP {response.status_code}: {detail}") from exc

    result = response.json()

    if not result["ok"]:
        raise RuntimeError(result["error"])

    return result


def main() -> None:
    print("1. 按笔记文件出题")
    print("2. 按主题自动选笔记出题")
    mode = input("请选择：").strip()

    if mode == "1":
        response = requests.get(BASE_URL + "/notes", timeout=10)
        response.raise_for_status()
        filenames = response.json()["filenames"]

        if not filenames:
            print("暂无可用笔记")
            return

        print("\n可用笔记：")
        for name in filenames:
            print("-", name)

        value = input("请输入笔记文件名：").strip()
        path = "/quiz/generate"
        payload = {"filename": value}

    elif mode == "2":
        value = input("请输入自测主题：").strip()
        path = "/quiz/generate-by-topic"
        payload = {"topic": value}

    else:
        print("请输入 1 或 2")
        return

    if not value:
        print("输入不能为空")
        return

    question_result = post_json(path, payload)

    print("\n题目：")
    print(question_result["answer"])

    if question_result["insufficient"]:
        return

    quiz_id = question_result.get("quiz_id")

    if not quiz_id:
        print("服务端未返回题目编号，本次练习结束")
        return

    user_answer = input("\n请输入你的答案：").strip()

    if not user_answer:
        print("答案不能为空")
        return

    feedback_result = post_json(
        "/quiz/answer",
        {
            "quiz_id": quiz_id,
            "user_answer": user_answer,
        },
    )

    print("\n反馈：")
    print(feedback_result["answer"])

    if not feedback_result["insufficient"]:
        print("\n本次练习已由服务端保存")


if __name__ == "__main__":
    try:
        main()
    except (requests.exceptions.RequestException, RuntimeError) as exc:
        print("本次练习未完成：", exc)
