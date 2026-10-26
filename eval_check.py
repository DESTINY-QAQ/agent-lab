import json
from pathlib import Path


def required_tools_pass(case: dict) -> bool:
    successful = successful_tool_names(case["messages"])

    for name in case["required_tools"]:
        if name not in successful:
            return False

    return True

def actual_read_files(messages: list[dict]) -> list[str]:
    call_names = {}
    read_files = set()

    for message in messages:
        # 建立调用 ID 与工具名称的对应关系
        for tool_call in message.get("tool_calls") or []:
            call_names[tool_call["id"]] = tool_call["function"]["name"]

        if message.get("role") != "tool":
            continue

        call_id = message["tool_call_id"]

        if call_names.get(call_id) != "read_note":
            continue

        result = json.loads(message["content"])

        if result.get("ok") is True:
            read_files.add(result["data"]["filename"])

    return sorted(read_files)

def successful_tool_names(messages: list[dict]) -> list[str]:
    call_names = {}
    names = []

    for message in messages:
        for tool_call in message.get("tool_calls") or []:
            call_names[tool_call["id"]] = tool_call["function"]["name"]

        if message.get("role") != "tool":
            continue

        result = json.loads(message["content"])
        name = call_names.get(message["tool_call_id"])

        if name is not None and result.get("ok") is True:
            names.append(name)

    return names

def main() -> None:
    results_path = Path(__file__).with_name("eval_results.json")
    results = json.loads(results_path.read_text(encoding="utf-8"))

    passed = 0

    for case in results:
        actual = actual_read_files(case["messages"])
        expected = sorted(set(case["expected_read_files"]))

        if actual == expected:
            passed += 1
            status = "通过"
        else:
            status = "未通过"

        print(f"{case['id']}：{status}")
        print("预期读取：", expected)
        print("实际读取：", actual)

    print(f"\n读取文件检查：{passed}/{len(results)}")


if __name__ == "__main__":
    main()