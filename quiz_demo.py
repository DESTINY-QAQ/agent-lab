from quiz_store import save_quiz_record
from quiz_service import generate_question, review_answer

def main() -> None:
    filename = input("请输入用于出题的笔记文件名：").strip()

    if not filename:
        print("文件名不能为空")
        return

    messages = []
    result = generate_question(filename, messages)
    if not result["ok"]:
        print("本次出题失败：", result["error"])
        return
    if result["insufficient"]:
        return

    user_answer = input("\n请输入你的答案：").strip()

    if not user_answer:
        print("答案不能为空，本次练习结束")
        return

    feedback_result = review_answer(
        filename,
        result["answer"],
        user_answer,
        messages,
    )

    if not feedback_result["ok"]:
        print("本次反馈生成失败：", feedback_result["error"])
        return
        
    if feedback_result["insufficient"]:
        return

    record = {
        "filename": filename,
        "question": result["answer"],
        "user_answer": user_answer,
        "feedback": feedback_result["answer"],
    }

    save_quiz_record(record)
    print("本次练习已保存")

if __name__ == "__main__":
    main()
