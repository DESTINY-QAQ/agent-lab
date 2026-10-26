import json
from pathlib import Path
from eval_check import (
    actual_read_files,
    successful_tool_names,
    required_tools_pass,
)


def main() -> None:
    reviews_path = Path(__file__).with_name("eval_reviews.json")
    reviews = json.loads(reviews_path.read_text(encoding="utf-8"))

    rows = []
    passed_count = 0

    for review in reviews:
        case = review["case_result"]

        actual = actual_read_files(case["messages"])
        expected = sorted(set(case["expected_read_files"]))

        answer_present = (
            case["has_final_answer"] is True
            and isinstance(case["answer"], str)
            and bool(case["answer"].strip())
        )
        read_files_pass = actual == expected
        tools_pass = required_tools_pass(case)
        content_review_pass = review["content_pass"] is True

        passed = (
            answer_present
            and read_files_pass
            and tools_pass
            and content_review_pass
        )

        if passed:
            passed_count += 1

        rows.append({
            "id": case["id"],
            "answer_present": answer_present,
            "expected_read_files": expected,
            "actual_read_files": actual,
            "read_files_pass": read_files_pass,
            "content_review_pass": content_review_pass,
            "passed": passed,
            "required_tools": case["required_tools"],
            "successful_tools": successful_tool_names(case["messages"]),
            "required_tools_pass": tools_pass,
        })

        print(case["id"], "综合通过：", passed)

    report = {
        "total": len(reviews),
        "passed": passed_count,
        "cases": rows,
    }

    report_path = Path(__file__).with_name("eval_report.json")
    content = json.dumps(report, ensure_ascii=False, indent=2)
    report_path.write_text(content, encoding="utf-8")

    print(f"\n综合检查：{passed_count}/{len(reviews)}")
    print("报告已保存：", report_path)


if __name__ == "__main__":
    main()