import json
from tool_executor import execute_tool

cases = [
    ("uppercase_text", {"text": "Hello\nAgent"}),
    ("inspect_text", {"text": "HELLO\nAGENT"}),
    ("inspect_text", {"text": 123}),
    ("unknown_tool", {"text": "Hello"}),
    ("inspect_text", {}),
    ("uppercase_text", {"text": "Hello", "extra": 1}),
]

for name, arguments in cases:
    arguments_json = json.dumps(arguments)

    try:
        result = execute_tool(name, arguments_json)
    except (KeyError, TypeError, ValueError) as exc:
        print(name, "失败：", type(exc).__name__, str(exc))
    else:
        print(name, "成功：", result)