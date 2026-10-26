def format_final_answer(result: dict, read_files: list[str]) -> str:
    if not isinstance(result, dict):
        raise TypeError("最终结果必须是字典")

    if not isinstance(result.get("insufficient"), bool):
        raise TypeError("insufficient 必须是布尔值")

    if result["insufficient"]:
        answer = "资料不足：目前没有取得足以回答该问题的笔记内容。"
    else:
        answer = result.get("answer")

        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("answer 必须是非空字符串")

        answer = answer.strip()

    if read_files:
        sources = "、".join(sorted(set(read_files)))
        answer += "\n已读取来源：" + sources + "。"

    return answer