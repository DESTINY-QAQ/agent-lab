# agent-lab：本地笔记 Agent

使用 Python 和 Requests 手写模型与工具循环的学习项目。支持笔记目录发现、关键词检索、正文读取、多轮对话和可复查的固定用例评估。

## 当前阶段

截至 2026-10-26，已跑通本地笔记问答最小版本；最近一轮固定用例综合结果为 **5/5**。

评估范围为两份示例笔记、五条固定用例。工具与文件条件由程序检查，回答内容由人工审核；该结果对应本次记录。

## 启动程序

当前项目路径为 `D:\Dev\projects\agent-lab`，已有 `.venv` 使用现有 Conda base 的 Python 3.12.14 创建。依赖清单见 `requirements.txt`。

在 PowerShell 中执行：

```powershell
Set-Location 'D:\Dev\projects\agent-lab'
.\.venv\Scripts\python.exe .\tool_call_demo.py
```

程序持续接收任务，支持：

- `exit`：退出程序。
- `/clear`：同时清空内存对话和 `conversation_history.json` 存档。
- 空输入：提示重新输入。

示例任务：

```text
请先搜索关键词“字典”，收到搜索结果后读取匹配的笔记正文，再根据正文用一句话解释字典的作用，并标注来源。
```

### 模型配置

本机客户端优先读取环境变量 `DEEPSEEK_API_KEY`；未设置时读取源码目录之外的 `D:\Dev\config\private\agent-lab-deepseek.key`，因此已有配置下无需每天重新设置终端。

其他机器可使用自己的 `DEEPSEEK_API_KEY` 环境变量。密钥值不写入源码、文档或评估记录。

当前代码配置：`deepseek-flash`、关闭 thinking、非流式响应、`max_tokens=512`。Agent 调用时启用 JSON 输出模式；`call_model()` 的普通文本模式仍可由其他练习入口使用。

## 已实现能力

- 手写模型请求、工具执行、结果回填与继续请求的完整循环。
- 每次任务最多发起三次模型请求；这不是整个终端会话的总上限。
- 处理一次模型响应中的多个工具调用，并按调用 ID 回传各自结果。
- 根据注册表分发函数，解析 JSON 参数并使用 `**arguments` 传参。
- 工具成功回传 `ok/data`，失败回传 `ok/error`，供模型继续处理。
- 检查结束原因；截断等非正常结果不作为完整最终回答加入历史。
- 终端多轮对话、JSON 历史保存与加载、清空命令。
- 模型最终返回结构化判断；程序控制资料不足时的文案和实际读取来源。

### 工具列表

| 工具 | 参数 | 返回用途 |
|---|---|---|
| `inspect_text` | `text` | 字符数和行数 |
| `uppercase_text` | `text` | 转为大写的文本 |
| `list_notes` | 无，调用参数为 `{}` | `notes` 顶层的 `.md`、`.txt` 文件名 |
| `read_note` | `filename` | `notes` 顶层 UTF-8 文件的正文和文件名 |
| `search_notes` | `keyword` | 匹配文件名、从 1 开始的行号及该行原文 |

搜索去掉关键词首尾空白，英文字母忽略大小写，每个匹配行返回一条记录。非字符串或空关键词会被拒绝；无匹配正常返回 `count: 0` 和 `matches: []`。

`read_note` 对解析后的路径检查父目录，将读取范围限定在 `notes` 顶层。自动列出和搜索的笔记类型为 `.md` 与 `.txt`。

### 资料与来源约定

- 搜索结果用于定位；解释笔记知识时再通过 `read_note` 获取完整正文。
- `list_notes` 列出了文件名，不等于模型已取得这些文件的正文。
- 搜索无匹配只表示关键词没有命中，不能据此断言不存在相关主题资料。
- 完整正文缺少答案时，模型返回 `insufficient: true`；程序使用固定资料不足文案。
- 用户看到的来源由程序根据本次成功的 `read_note` 记录生成。

## 最终结果与对话历史

模型的最终 JSON 格式示例：

```json
{"insufficient": true, "answer": ""}
```

`run_agent(user_input, messages)` 在成功生成最终答复时返回字典，包含：

| 字段 | 含义 |
|---|---|
| `answer` | 程序最终交付给用户的文本 |
| `raw_final_content` | 模型返回的原始 JSON 字符串 |
| `insufficient` | 模型对资料是否不足的布尔判断 |
| `read_files` | 程序记录的本次实际读取文件名 |

失败或达到请求上限而没有最终答复时，当前函数返回 `None`。

`messages` 保存用户消息、工具调用及结果、程序展示后的 assistant 最终消息。终端启动时从 `conversation_history.json` 加载，每次任务调用结束后保存当前历史。运行途中手工修改该文件不会自动同步到内存，之后的保存可能覆盖文件修改。

评估脚本另外保存 `agent_result`，保留原始 JSON 与最终展示文本，便于检查程序行为。

## 固定用例评估

五条用例定义在 `eval_cases.json`：

| 用例 ID | 验证场景 | 本轮结果 |
|---|---|---|
| `read_agent_note` | 指定文件读取与概括 | 通过 |
| `choose_python_note` | 列出笔记并选择正确文件 | 通过 |
| `missing_information` | 正文不含答案时说明资料不足 | 通过 |
| `search_hit` | 搜索命中后读取正文并回答 | 通过 |
| `search_no_match` | 正常报告零匹配结果 | 通过 |

按顺序逐条运行，每条结束后再执行下一条：

1. 执行任务并保存结果，真实调用模型：

   ```powershell
   .\.venv\Scripts\python.exe .\eval_demo.py
   ```

2. 对照工具返回与最终回答，人工审核并输入 `y/n`：

   ```powershell
   .\.venv\Scripts\python.exe .\eval_review.py
   ```

3. 基于审核快照生成综合报告，本地执行：

   ```powershell
   .\.venv\Scripts\python.exe .\eval_report.py
   ```

每条用例使用独立空历史。综合通过需要同时满足：有非空最终回答、成功读取文件符合预期、必需工具成功执行、人工内容审核通过。

`required_tools` 检查必需工具是否至少成功执行一次，目前不检查调用顺序。人工审核还要核对资料不足判断是否符合正文、最终答案是否有依据、来源是否准确。

### 评估产物

| 文件 | 内容 |
|---|---|
| `eval_cases.json` | 问题及预期条件，仅问题交给 Agent |
| `eval_results.json` | 本轮执行轨迹、最终回答与 `agent_result` |
| `eval_reviews.json` | 当时执行结果的完整快照及人工审核结论 |
| `eval_report.json` | 自动条件、人工内容结论和综合结果 |
| `eval_reviews_before_formatter.json` | 引入展示函数前的五条用例与审核基线 |

### 本轮改进记录：4/5 → 5/5

原基线中，`missing_information` 虽说明资料不足，但继续加入笔记之外的术语，人工内容审核未通过。其他四条通过。

改动后，模型返回 `insufficient/answer` JSON；`answer_formatter.py` 对资料不足使用固定文案，并由程序追加实际读取来源。相同五条问题按相同综合条件重新执行与人工审核，本轮结果为 5/5。

评估对象是程序最终交付的回答；原始模型 JSON 保留用于审计。后续改动需重新执行、审核并生成报告，读取旧报告本身不会重新运行任务。

## 核心文件

| 文件 | 职责 |
|---|---|
| `model_client.py` | DeepSeek HTTP 请求、密钥读取、可选 JSON 输出模式 |
| `tool_definitions.py` | 模型可见的工具名称、说明和参数 schema |
| `tool_executor.py` | 工具注册表与参数解析分发 |
| `text_tools.py` | 文本统计和大写转换 |
| `note_tools.py` | 笔记列表、正文读取和关键词搜索 |
| `answer_formatter.py` | 最终文本与实际读取来源的展示 |
| `history_store.py` | 对话历史 JSON 读写 |
| `tool_call_demo.py` | Agent 循环与终端入口 |
| `eval_demo.py` | 独立历史下批量执行固定任务 |
| `eval_check.py` | 从调用 ID 和成功工具结果提取验证证据 |
| `eval_review.py` | 人工内容审核与快照保存 |
| `eval_report.py` | 综合条件汇总与报告保存 |

早期 Python、HTTP、模型调用练习和旧项目对照说明保存在[学习记录归档](docs/learning-history/README-20261026-before-sync.md)。该归档反映同步前的早期进度；当前功能以本 README 和实际代码为准。

## 下一阶段

- 记录每次任务的请求次数、工具调用次数、耗时与 token 用量。
- 将更多错误路径纳入可重复检查，并扩充真实笔记与评估任务。
- 随资料和会话规模增加，完善上下文长度及历史存储处理。
