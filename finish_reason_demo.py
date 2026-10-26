from unittest.mock import patch
from tool_call_demo import run_agent

fake_response = {
    "choices": [{
        "finish_reason": "length",
        "message": {
            "role": "assistant",
            "content": "这是一段被截断的",
        },
    }]
}

messages = []

with patch("tool_call_demo.call_model", return_value=fake_response):
    run_agent("测试截断处理", messages)

print("历史消息角色：", [item["role"] for item in messages])