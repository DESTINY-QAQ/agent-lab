import json
from pathlib import Path

HISTORY_FILE = Path(__file__).resolve().parent / "conversation_history.json"


def load_history() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []

    content = HISTORY_FILE.read_text(encoding="utf-8")
    messages = json.loads(content)

    if not isinstance(messages, list):
        raise ValueError("历史文件内容必须是列表")

    return messages


def save_history(messages: list[dict]) -> None:
    content = json.dumps(messages, ensure_ascii=False, indent=2)
    HISTORY_FILE.write_text(content, encoding="utf-8")