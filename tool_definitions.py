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
    },
    
    {
        "type": "function",
        "function": {
            "name": "uppercase_text",
            "description": "将文本中的英文字母转换为大写，保留其他字符。",
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
    },
    
    {
        "type": "function",
        "function": {
            "name": "read_note",
            "description": "读取 notes 目录顶层的 UTF-8 文本笔记。",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "包含扩展名的文件名，例如 agent_intro.md。",
                    },
                },
                "required": ["filename"],
                "additionalProperties": False,
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "list_notes",
            "description": "列出 notes 目录顶层的 Markdown 和文本笔记文件名。",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_notes",
            "description": (
                "按关键词搜索笔记正文，忽略英文字母大小写，"
                "返回匹配的文件名、行号和原文。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "需要在笔记正文中查找的非空关键词。",
                    },
                },
                "required": ["keyword"],
                "additionalProperties": False,
            },
        },
    },
]