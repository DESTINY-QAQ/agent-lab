TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "inspect_text",
            "description": "统计文本的字符数（包含换行符）和行数。",
            "parameters": {
                "type": "object",
                "properties": {
                    # TODO：描述 text 参数及其类型
                    "text":{
                        "type": "string",
                    },
                },
                "required": ["text"],  # TODO：填写必填参数名
                "additionalProperties": False,
            },
        },
    }
]