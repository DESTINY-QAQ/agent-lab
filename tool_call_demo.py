import json
import requests
from model_client import call_model
from tool_definitions import TOOLS
from tool_executor import execute_tool
from history_store import load_history, save_history
from answer_formatter import format_final_answer
from time import perf_counter

SYSTEM_PROMPT = (
    "你是本地笔记问答助手。"
    "解释笔记中的具体知识前，必须调用 read_note 取得正文。"
    "知识回答只根据本次工具返回的正文，不补充外部知识。"
    "用户仅要求搜索时，直接报告 search_notes 的结果，无需读取完整正文。"
    "搜索 count 为 0 仅表示关键词无匹配，不能断言不存在相关主题资料。"
    "工具执行失败时如实说明，不编造结果。"
    "需要工具时正常发起工具调用。"
    "最终答复必须是 JSON 对象，包含 insufficient 和 answer 两个字段，不要代码块。"
    "insufficient 必须是布尔值，answer 必须是字符串。"
    '可以回答或报告搜索结果时：{"insufficient": false, "answer": "简洁回答"}。'
    '已读取正文但资料不足时：{"insufficient": true, "answer": ""}。'
    "answer 中不要添加来源标注，来源由程序根据实际读取记录生成。"
)

def make_failure_result(
    error_type: str,
    error: str,
    metrics: dict,
    read_files: list[str],
    started_at: float,
    raw_final_content: str | None = None,
) -> dict:
    metrics["elapsed_seconds"] = round(perf_counter() - started_at, 3)
    print("运行统计：", metrics)

    return {
        "ok": False,
        "answer": None,
        "raw_final_content": raw_final_content,
        "insufficient": None,
        "read_files": sorted(set(read_files)),
        "metrics": metrics,
        "error_type": error_type,
        "error": error,
    }



def run_agent(user_input: str, messages: list[dict]) -> dict:
    started_at = perf_counter()
    read_files = []
    
    metrics = {
        "model_requests": 0,
        "tool_calls": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "token_usage_complete": True,
    }
    
    messages.append({
        "role": "user",
        "content": user_input,
    })

    max_rounds = 3

    for round_number in range(1, max_rounds + 1):
        print(f"第 {round_number} 次模型请求")

        try:
            request_messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                }
            ]
            request_messages.extend(messages)

            metrics["model_requests"] += 1
            body = call_model(
                request_messages,
                tools=TOOLS,
                json_output=True,
            )
        except (RuntimeError, requests.exceptions.RequestException) as exc:
            metrics["token_usage_complete"] = False
            print(f"模型请求失败：{exc}")

            return make_failure_result(
                "model_request_failed", str(exc),
                metrics, read_files, started_at,
            )
        else:
            usage = body.get("usage")

            if usage is None:
                metrics["token_usage_complete"] = False
            else:
                metrics["prompt_tokens"] += usage["prompt_tokens"]
                metrics["completion_tokens"] += usage["completion_tokens"]
                metrics["total_tokens"] += usage["total_tokens"]

            choice = body["choices"][0]
            finish_reason = choice["finish_reason"]
            print("结束原因：", finish_reason)

            if finish_reason not in ("stop", "tool_calls"):
                error = f"模型输出未正常完成，原因：{finish_reason}"
                print(error)

                return make_failure_result(
                    "model_output_incomplete", error,
                    metrics, read_files, started_at,
                    raw_final_content=choice["message"].get("content"),
                )

            message = choice["message"]
            
            tool_calls = message.get("tool_calls") or []
            print("本轮工具调用数：", len(tool_calls))

            if not tool_calls:
                raw_final_content = message.get("content") or ""

                try:
                    final_result = json.loads(raw_final_content)
                    answer = format_final_answer(final_result, read_files)
                except (TypeError, ValueError) as exc:
                    print("最终结果格式错误：", exc)

                    return make_failure_result(
                        "invalid_final_output", str(exc),
                        metrics, read_files, started_at,
                        raw_final_content=raw_final_content,
                    )
                messages.append({
                    "role": "assistant",
                    "content": answer,
                })

                metrics["elapsed_seconds"] = round(
                    perf_counter() - started_at, 3
                )

                print("模型回答：", answer)
                print("运行统计：", metrics)

                return {
                    "answer": answer,
                    "raw_final_content": raw_final_content,
                    "insufficient": final_result["insufficient"],
                    "read_files": sorted(set(read_files)),
                    "metrics": metrics,
                    "ok": True,
                    "error_type": None,
                    "error": None,
                }

            messages.append(message)

            for tool_call in tool_calls:
                metrics["tool_calls"] += 1
                
                try:
                    function = tool_call["function"]
                    print("执行工具：", function["name"])
                    print("工具参数 JSON：", function["arguments"])

                    result = execute_tool(
                        function["name"],
                        function["arguments"],
                    )
                except (KeyError, TypeError, ValueError) as exc:
                    tool_result = {
                        "ok": False,
                        "error": str(exc),
                    }
                else:
                    tool_result = {
                        "ok": True,
                        "data": result,
                    }
                    
                    if function["name"] == "read_note":
                        read_files.append(result["filename"])

                print("工具返回结果：")
                print(json.dumps(tool_result, ensure_ascii=False, indent=2))

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": json.dumps(tool_result, ensure_ascii=False),
                })

    error = f"已达到 {max_rounds} 次模型请求上限，任务尚未完成。"
    print(error)

    return make_failure_result(
        "max_rounds", error,
        metrics, read_files, started_at,
    )


if __name__ == "__main__":
    
    messages = load_history()
    print(f"已加载 {len(messages)} 条历史消息")
    
    while True:
        user_input = input("\n请输入任务（/clear 清空历史，exit 退出）：").strip()

        if user_input.lower() == "exit":
            print("已退出")
            break

        if user_input.lower() == "/clear":
            messages.clear()
            save_history(messages)
            print("对话历史已清空")
            continue

        if not user_input:
            print("任务不能为空")
            continue

        run_agent(user_input,messages)  
        save_history(messages)
