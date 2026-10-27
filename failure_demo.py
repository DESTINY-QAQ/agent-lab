import json
import requests
from unittest.mock import patch
from tool_call_demo import run_agent

with patch(
    "tool_call_demo.call_model",
    side_effect=requests.exceptions.Timeout("模拟请求超时"),
):
    with patch(
        "tool_call_demo.perf_counter",
        side_effect=[100.0, 101.25],
    ):
        result = run_agent("本地失败统计测试", [])

assert result is not None
assert result["ok"] is False
assert result["answer"] is None
assert result["error_type"] == "model_request_failed"
assert result["metrics"]["model_requests"] == 1
assert result["metrics"]["tool_calls"] == 0
assert result["metrics"]["token_usage_complete"] is False
assert result["metrics"]["elapsed_seconds"] == 1.25

print(json.dumps(result, ensure_ascii=False, indent=2))
print("失败路径验证通过")