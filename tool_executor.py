import json
from text_tools import inspect_text, uppercase_text
from note_tools import read_note, list_notes, search_notes

TOOL_FUNCTIONS = {
    "inspect_text": inspect_text,
    "uppercase_text": uppercase_text,
    "read_note": read_note,
    "list_notes": list_notes,
    "search_notes": search_notes,
}


def execute_tool(function_name: str, arguments_json: str) -> dict:
    arguments = json.loads(arguments_json)

    if not isinstance(arguments, dict):
        raise TypeError("工具参数必须是 JSON 对象")

    tool_function = TOOL_FUNCTIONS.get(function_name)

    if tool_function is None:
        raise ValueError("不支持的工具：" + function_name)

    result = tool_function(**arguments)
    return result