import json
from pathlib import Path
from eval_check import (
    actual_read_files,
    successful_tool_names,
    required_tools_pass,
    tools_in_order,
)

def summarize_metrics(rows: list[dict]) -> dict | None:
    if not rows:
        return None

    for row in rows:
        metrics = row.get("metrics")
        if not isinstance(metrics, dict):
            return None
        if metrics.get("token_usage_complete") is not True:
            return None

    model_requests = 0  
    tool_calls = 0
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    elapsed_seconds = 0.0

    for row in rows:
        metrics = row["metrics"]
        model_requests += metrics["model_requests"]
        tool_calls += metrics["tool_calls"]
        prompt_tokens += metrics["prompt_tokens"]
        completion_tokens += metrics["completion_tokens"]
        total_tokens += metrics["total_tokens"]
        elapsed_seconds += metrics["elapsed_seconds"]

    case_count = len(rows)

    return {
        "case_count": case_count,
        "model_requests": model_requests,
        "tool_calls": tool_calls,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "elapsed_seconds": round(elapsed_seconds, 3),
        "avg_elapsed_seconds": round(elapsed_seconds / case_count, 3),
    }
    
def extract_run_status(case: dict) -> dict:
    agent_result = case.get("agent_result")

    status = {
        "run_ok": None,
        "error_type": None,
        "error": None,
    }

    if isinstance(agent_result, dict):
        status["run_ok"] = agent_result.get("ok")
        status["error_type"] = agent_result.get("error_type")
        status["error"] = agent_result.get("error")

    return status

def summarize_run_status(rows: list[dict]) -> dict:
    success_count = 0
    failure_count = 0
    unknown_count = 0
    failure_types = {}

    for row in rows:
        run_ok = row.get("run_ok")

        if run_ok is True:
            success_count += 1

        elif run_ok is False:
            failure_count += 1

            error_type = row.get("error_type") or "unspecified"
            previous_count = failure_types.get(error_type, 0)
            failure_types[error_type] = previous_count + 1

        else:
            unknown_count += 1

    return {
        "case_count": len(rows),
        "success_count": success_count,
        "failure_count": failure_count,
        "unknown_count": unknown_count,
        "failure_types": failure_types,
    }
    
def summarize_activity(rows: list[dict]) -> dict | None:
    if not rows:
        return None

    model_requests = 0
    tool_calls = 0
    elapsed_seconds = 0.0

    for row in rows:
        metrics = row.get("metrics")

        if not isinstance(metrics, dict):
            return None

        model_requests += metrics["model_requests"]
        tool_calls += metrics["tool_calls"]
        elapsed_seconds += metrics["elapsed_seconds"]

    case_count = len(rows)

    return {
        "case_count": case_count,
        "model_requests": model_requests,
        "tool_calls": tool_calls,
        "elapsed_seconds": round(elapsed_seconds, 3),
        "avg_elapsed_seconds": round(elapsed_seconds / case_count, 3),
    }

def main() -> None:
    reviews_path = Path(__file__).with_name("eval_reviews.json")
    reviews = json.loads(reviews_path.read_text(encoding="utf-8"))

    rows = []
    passed_count = 0

    for review in reviews:
        case = review["case_result"]
        status = extract_run_status(case)
        agent_result = case.get("agent_result")
        metrics = None

        if agent_result is not None:
            metrics = agent_result.get("metrics")

        actual = actual_read_files(case["messages"])
        expected = sorted(set(case["expected_read_files"]))

        answer_present = (
            case["has_final_answer"] is True
            and isinstance(case["answer"], str)
            and bool(case["answer"].strip())
        )
        read_files_pass = actual == expected
        tools_pass = required_tools_pass(case)
        successful = successful_tool_names(case["messages"])
        required_order = case.get("required_tool_order")

        order_pass = None
        if required_order is not None:
            order_pass = tools_in_order(successful, required_order)
        content_review_pass = review["content_pass"] is True

        passed = (
            status["run_ok"] is not False
            and answer_present
            and read_files_pass
            and tools_pass
            and order_pass is not False
            and content_review_pass
        )

        if passed:
            passed_count += 1

        rows.append({
            "id": case["id"],
            "run_ok": status["run_ok"],
            "error_type": status["error_type"],
            "error": status["error"],
            "answer_present": answer_present,
            "expected_read_files": expected,
            "actual_read_files": actual,
            "read_files_pass": read_files_pass,
            "content_review_pass": content_review_pass,
            "passed": passed,
            "required_tools": case["required_tools"],
            "successful_tools": successful_tool_names(case["messages"]),
            "required_tools_pass": tools_pass,
            "metrics": metrics,
            "required_tool_order": required_order,
            "tool_order_pass": order_pass,
        })

        print(case["id"], "综合通过：", passed)
        print("运行状态：", status["run_ok"])

        if status["run_ok"] is False:
            print("失败类型：", status["error_type"])
            print("失败原因：", status["error"])
        print("运行统计：", metrics)

    metrics_summary = summarize_metrics(rows)
    run_summary = summarize_run_status(rows)
    activity_summary = summarize_activity(rows)

    report = {
        "total": len(reviews),
        "passed": passed_count,
        "cases": rows,
        "metrics_summary": metrics_summary,
        "run_summary": run_summary,
        "activity_summary": activity_summary,
    }

    report_path = Path(__file__).with_name("eval_report.json")
    content = json.dumps(report, ensure_ascii=False, indent=2)
    report_path.write_text(content, encoding="utf-8")

    print(f"\n综合检查：{passed_count}/{len(reviews)}")
    print("指标汇总：")
    print(json.dumps(metrics_summary, ensure_ascii=False, indent=2))
    print("运行状态汇总：")
    print(json.dumps(run_summary, ensure_ascii=False, indent=2))
    print("运行活动汇总：")
    print(json.dumps(activity_summary, ensure_ascii=False, indent=2))
    print("报告已保存：", report_path)


if __name__ == "__main__":
    main()