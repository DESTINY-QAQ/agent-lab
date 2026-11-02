from quiz_store import load_latest_quiz_record


def main() -> None:
    record = load_latest_quiz_record()

    if record is None:
        print("暂无练习记录，请先完成一次自测")
        return

    print("最近一次练习")
    print("时间：", record["created_at"])
    print("笔记：", record["filename"])

    print("\n题目：")
    print(record["question"])

    print("\n你的答案：")
    print(record["user_answer"])

    print("\n反馈：")
    print(record["feedback"])


if __name__ == "__main__":
    main()