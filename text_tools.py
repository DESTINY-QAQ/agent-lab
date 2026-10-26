def inspect_text(text: str) -> dict[str, int]:
    # 返回两个字段：
    # characters：字符总数，包含换行符
    # lines：行数
    if not isinstance(text, str):
        raise TypeError("text 必须是字符串 str")
    characters = len(text)
    #lines = text.count("\n") + 1
    lines=len(text.splitlines())
    return {
        "characters": characters,
        "lines": lines
    }

def uppercase_text(text: str) -> dict[str, str]:
    if not isinstance(text, str):
        raise TypeError("text 必须是字符串 str")

    uppercase = text.upper()
    return {"text": uppercase}
    
