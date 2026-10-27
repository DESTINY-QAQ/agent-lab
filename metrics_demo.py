from unittest.mock import patch
from tool_call_demo import run_agent

tool_calls = [
    {
        "id": "local_upper",
        "type": "function",
        "function": {
            "name": "uppercase_text",
            "arguments": '{"text": "hello"}',
        },
    },
    {
        "id": "local_inspect",
        "type": "function",
        "function": {
            "name": "inspect_text",
            "arguments": '{"text": "hello"}',
        },
    },
    {
        "id": "local_unknown",
        "type": "function",
        "function": {
            "name": "unknown_tool",
            "arguments": '{"text": "hello"}',
        },
    },
]

responses = [
    {"choices": [{
        "finish_reason": "tool_calls",
        "message": {
            "role": "assistant",
            "content": "",
            "tool_calls": tool_calls,
        },
    }]},
    {"choices": [{
        "finish_reason": "stop",
        "message": {
            "role": "assistant",
            "content": '{"insufficient": false, "answer": "本地验证结束。"}',
        },
    }]},
]

responses[0]["usage"] = {
    "prompt_tokens": 100,
    "completion_tokens": 20,
    "total_tokens": 120,
}

responses[1]["usage"] = {
    "prompt_tokens": 160,
    "completion_tokens": 30,
    "total_tokens": 190,
}

with patch("tool_call_demo.call_model", side_effect=responses):
    with patch(
        "tool_call_demo.perf_counter",
        side_effect=[100.0, 101.25],
    ):
        result = run_agent("本地计数测试", [])

assert result is not None
assert result["metrics"] == {
    "model_requests": 2,
    "tool_calls": 3,
    "prompt_tokens": 260,
    "completion_tokens": 50,
    "total_tokens": 310,
    "token_usage_complete": True,
    "elapsed_seconds": 1.25,
}

print("统计验证通过：", result["metrics"])