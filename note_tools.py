from pathlib import Path


NOTES_DIR = Path(__file__).resolve().parent / "notes"


def read_note(filename: str) -> dict[str, str]:
    if not isinstance(filename, str):
        raise TypeError("filename 必须是字符串 str")

    note_path = (NOTES_DIR / filename).resolve()

    if note_path.parent != NOTES_DIR.resolve():
        raise ValueError("只能读取 notes 目录顶层的文件")

    try:
        content = note_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValueError(
            "读取笔记失败，请检查文件是否存在且使用 UTF-8 编码"
        ) from exc

    return {
        "filename": note_path.name,
        "content": content,
    }
    
def list_notes() -> dict[str, list[str]]:
    filenames = []

    try:
        for note_path in NOTES_DIR.iterdir():
            if not note_path.is_file():
                continue

            if note_path.suffix.lower() not in (".md", ".txt"):
                continue

            filenames.append(note_path.name)
    except OSError as exc:
        raise ValueError("无法列出笔记，请检查 notes 目录") from exc

    filenames.sort()
    return {"filenames": filenames}
    
def search_notes(keyword: str) -> dict:
    if not isinstance(keyword, str):
        raise TypeError("keyword 必须是字符串 str")

    keyword = keyword.strip()
    if not keyword:
        raise ValueError("keyword 不能为空")

    matches = []
    for filename in list_notes()["filenames"]:
        note = read_note(filename)
        for line_number, line in enumerate(note["content"].splitlines(), start=1):
            if keyword.lower() in line.lower():
                matches.append({
                    "filename": note["filename"],
                    "line_number": line_number,
                    "content": line,
                })

    return {
        "keyword": keyword,
        "count": len(matches),
        "matches": matches,
    }