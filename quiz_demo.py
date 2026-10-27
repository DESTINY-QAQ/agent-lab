from tool_call_demo import run_agent


def main() -> None:
    filename = input("请输入用于出题的笔记文件名：").strip()

    if not filename:
        print("文件名不能为空")
        return

    task = (
        f"请调用 read_note 工具读取笔记 {filename}。"
        "仅根据实际读取的正文，生成一道简答题。"
        "题目必须能够仅凭该正文回答。"
        "本次只展示一道题目，不展示答案、提示或解析。"
        "如果正文不足以出题，请明确说明资料不足。"
    )

    messages = []
    result = run_agent(task, messages)

    if result["insufficient"]:
        return

    user_answer = input("\n请输入你的答案：").strip()

    if not user_answer:
        print("答案不能为空，本次练习结束")
        return

    feedback_task = (
        f"请调用 read_note 工具重新读取笔记 {filename}。"
        "仅根据实际读取的正文，评阅我对上一道自测题的作答。\n"
        f"我的作答：{user_answer}\n"
        "请对照题目逐项核对，先判断：正确、部分正确或不正确。"
        "然后简要说明已答对的内容和遗漏或错误，最后给出参考答案。"
        "不要补充笔记正文之外的知识。"
    )

    feedback_result = run_agent(feedback_task, messages)

    if not feedback_result["ok"]:
        print("本次反馈生成失败：", feedback_result["error"])
        return


if __name__ == "__main__":
    main()