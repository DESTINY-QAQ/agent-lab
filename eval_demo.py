import json
from pathlib import Path
from tool_call_demo import run_agent

PROJECT_DIR = Path(__file__).resolve().parent


def main() -> None:
    cases_path = PROJECT_DIR / "eval_cases.json"
    cases = json.loads(cases_path.read_text(encoding="utf-8"))

    results = []

    for case in cases:
        print(f"\n开始用例：{case['id']}")

        # 每条用例使用独立历史
        messages = []
        agent_result = run_agent(case["question"], messages)

        answer = None
        if agent_result is not None:
            answer = agent_result["answer"]
        results.append({
            "id": case["id"],
            "required_tools": case["required_tools"],
            "required_tool_order": case.get("required_tool_order", []),
            "required_round_order": case.get("required_round_order", []),
            "question": case["question"],
            "expected_read_files": case["expected_read_files"],
            "expect_insufficient": case["expect_insufficient"],
            "has_final_answer": answer is not None,
            "answer": answer,
            "messages": messages,
            "agent_result": agent_result,
        })

    results_path = PROJECT_DIR / "eval_results.json"
    content = json.dumps(results, ensure_ascii=False, indent=2)
    results_path.write_text(content, encoding="utf-8")

    print(f"\n已保存 {len(results)} 条结果：{results_path}")


if __name__ == "__main__":
    main()