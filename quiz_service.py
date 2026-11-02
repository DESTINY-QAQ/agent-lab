from tool_call_demo import run_agent

def generate_question_by_topic(
    topic: str,
    messages: list[dict],
) -> dict:
    topic = topic.strip()

    if not topic:
        raise ValueError("主题不能为空")

    task = (
        f"我想围绕这个主题进行自测：{topic}。"
        "请先从主题中选一个简短关键词，调用 search_notes 进行一次搜索。"
        "收到搜索结果后，选择一份相关笔记，调用 read_note 读取完整正文。"
        "仅根据实际读取的正文，生成一道能够凭正文回答的简答题。"
        "本次只展示题目，不展示答案、提示或解析。"
        "若搜索无匹配或正文不足以出题，请按资料不足返回，不编造题目。"
        "搜索无匹配不能据此断言不存在相关主题的笔记。"
    )

    return run_agent(task, messages)


def generate_question(filename: str, messages: list[dict]) -> dict:
    task = (
        f"请调用 read_note 工具读取笔记 {filename}。"
        "仅根据实际读取的正文，生成一道简答题。"
        "题目必须能够仅凭该正文回答。"
        "本次只展示一道题目，不展示答案、提示或解析。"
        "如果正文不足以出题，请明确说明资料不足。"
    )

    return run_agent(task, messages)


def review_answer(
    filename: str,
    question: str,
    user_answer: str,
    messages: list[dict],
) -> dict:
    task = (
        f"请调用 read_note 工具读取笔记 {filename}。"
        "仅根据实际读取的正文，评阅下面的题目和作答。\n"
        f"题目：{question}\n"
        f"我的作答：{user_answer}\n"
        "请对照题目逐项核对，先判断：正确、部分正确或不正确。"
        "然后简要说明已答对的内容和遗漏或错误，最后给出参考答案。"
        "不要补充笔记正文之外的知识。"
    )

    return run_agent(task, messages)
