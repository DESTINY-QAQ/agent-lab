import json
from datetime import datetime
from pathlib import Path

QUIZ_FILE = Path(__file__).with_name("quiz_records.json")


def load_latest_quiz_record() -> dict | None:
    if QUIZ_FILE.exists():
        content = QUIZ_FILE.read_text(encoding="utf-8")
        records = json.loads(content)
    else:
        records = []

    if not isinstance(records, list):
        raise ValueError("练习记录文件内容必须是列表")

    if not records:
        return None

    return records[-1]

def save_quiz_record(record: dict) -> None:
    if QUIZ_FILE.exists():
        content = QUIZ_FILE.read_text(encoding="utf-8")
        records = json.loads(content)
    else:
        records = []

    if not isinstance(records, list):
        raise ValueError("练习记录文件内容必须是列表")

    saved_record = record.copy()
    saved_record["created_at"] = (
        datetime.now().astimezone().isoformat(timespec="seconds")
    )
    records.append(saved_record)

    content = json.dumps(records, ensure_ascii=False, indent=2)
    QUIZ_FILE.write_text(content, encoding="utf-8")