from uuid import uuid4

QUIZ_SESSIONS: dict[str, dict] = {}


def create_quiz_session(
    filename: str,
    question: str,
    messages: list[dict],
) -> str:
    quiz_id = uuid4().hex

    QUIZ_SESSIONS[quiz_id] = {
        "filename": filename,
        "question": question,
        "messages": messages,
    }

    return quiz_id


def get_quiz_session(quiz_id: str) -> dict | None:
    return QUIZ_SESSIONS.get(quiz_id)