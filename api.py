from fastapi import FastAPI, HTTPException
from quiz_sessions import create_quiz_session, get_quiz_session
from pydantic import BaseModel
from note_tools import list_notes
from quiz_service import (
    generate_question,
    generate_question_by_topic,
    review_answer,
)

from quiz_store import load_latest_quiz_record, save_quiz_record

app = FastAPI(title="笔记复习助手")


class QuizRequest(BaseModel):
    filename: str


class QuizAnswerRequest(BaseModel):
    quiz_id: str
    user_answer: str


class TopicQuizRequest(BaseModel):
    topic: str


@app.get("/quiz/latest")
def get_latest_quiz() -> dict:
    record = load_latest_quiz_record()
    return {"record": record}


@app.post("/quiz/generate")
def generate_quiz(request: QuizRequest) -> dict:
    messages = []
    result = generate_question(request.filename, messages)
    return register_quiz_result(result, messages)


@app.post("/quiz/answer")
def answer_quiz(request: QuizAnswerRequest) -> dict:
    quiz_id = request.quiz_id.strip()
    session = get_quiz_session(quiz_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="题目不存在或已失效，请重新出题",
        )

    user_answer = request.user_answer.strip()

    if not user_answer:
        raise HTTPException(status_code=400, detail="答案不能为空")

    result = review_answer(
        session["filename"],
        session["question"],
        user_answer,
        session["messages"],
    )
    result["quiz_id"] = quiz_id

    if result["ok"] and not result["insufficient"]:
        record = {
            "quiz_id": quiz_id,
            "filename": session["filename"],
            "question": session["question"],
            "user_answer": user_answer,
            "feedback": result["answer"],
        }
        save_quiz_record(record)

    return result


@app.get("/notes")
def get_notes() -> dict:
    return list_notes()


@app.post("/quiz/generate-by-topic")
def generate_topic_quiz(request: TopicQuizRequest) -> dict:
    topic = request.topic.strip()

    if not topic:
        raise HTTPException(
            status_code=400,
            detail="主题不能为空",
        )

    messages = []
    result = generate_question_by_topic(topic, messages)
    return register_quiz_result(result, messages)


def register_quiz_result(result: dict, messages: list[dict]) -> dict:
    if not result["ok"] or result["insufficient"]:
        return result

    read_files = result["read_files"]

    if len(read_files) != 1:
        raise HTTPException(
            status_code=500,
            detail="出题结果没有唯一的笔记来源",
        )

    quiz_id = create_quiz_session(
        read_files[0],
        result["answer"],
        messages,
    )

    result["quiz_id"] = quiz_id
    return result
