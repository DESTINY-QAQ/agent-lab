# Python 工程基础与最小 Agent

本项目按小步练习逐步扩展，当前包含文本功能模块 `text_tools.py`、JSON 练习入口 `main.py`、HTTP 练习入口 `http_demo.py`、HTTP 功能模块 `http_tools.py`、模型调用练习入口 `model_demo.py`，以及正在验收的模型请求模块 `model_client.py`。

## 当前环境

- 项目目录：`D:\Dev\projects\agent-lab`
- 项目解释器：`D:\Dev\projects\agent-lab\.venv\Scripts\python.exe`
- Python 版本：3.12.14
- 环境来源：使用现有 Conda base 的 Python 创建独立 `.venv`。
- 第三方依赖安装位置：项目 `.venv` 内。
- pip 下载缓存：`D:\Dev\cache\pip`，沿用机器已有的 `PIP_CACHE_DIR` 设置，已核实实际生效路径。
- 已安装 HTTP 客户端 Requests 2.34.2，实际导入位置在项目 `.venv` 中；`requirements.txt` 记录本次安装后的依赖版本，`pip check` 已通过。
- 尚未安装模型 SDK 或 Agent 框架。

`.venv` 的 Python 运行时依赖现有 Conda base 的安装位置。若以后迁移或删除 base，需要重建此项目环境。

## 第一次运行

在 PowerShell 中执行：

```powershell
Set-Location 'D:\Dev\projects\agent-lab'
.\.venv\Scripts\python.exe .\main.py
```

当前入口保留了 JSON 格式错误测试输入 `request_json = '{"text":}'`，预期输出：

```json
{
  "ok": false,
  "error": "Expecting value: line 1 column 9 (char 8)"
}
```

命令明确选择了本项目的解释器，因此这一步不要求先激活环境。

## 已完成的亲手练习

- 修改初始脚本的输出文字并成功运行。
- 创建 `text_tools.py`，实现文本字符数和行数统计。
- 在 `main.py` 中导入并调用函数，以 `if __name__ == "__main__"` 控制程序入口。
- 助手已验证：直接运行输出 `{'characters': 11, 'lines': 2}`；执行 `import main` 时没有输出。
- 使用 `splitlines()` 统一行数口径；助手已验证空字符串为 0 行、`Hello\n` 为 1 行、`Hello\nAgent` 为 2 行，字符数也符合预期。
- 在工具函数入口增加 `isinstance(text, str)` 检查；助手已验证正常文本仍返回统计结果，整数和字节串均抛出 `TypeError: text 必须是字符串 str`。
- 在 `main()` 中捕获 `TypeError`，以 `else` 展示成功结果。学习者提供的两次运行输出表明：错误输入显示清楚的失败提示，正常输入返回统计结果，两种情况均继续执行到“本次调用处理完毕”；助手已核对当前代码中的异常处理逻辑。
- 使用标准库 `json.dumps()` 输出统一的 JSON 响应。学习者提供的实际输出表明：正常输入得到 `ok: true` 及统计数据，错误输入得到 `ok: false` 及异常说明；助手已核对当前代码中的序列化逻辑。
- 使用 `json.loads()` 解析工具参数、检查顶层对象类型，再调用工具。助手在不修改源文件的情况下验证了三组输入：`{"text": "Hello Agent"}` 返回 11 个字符、1 行；`{"text": 123}` 返回字符串类型错误；`{"text":}` 返回 JSON 解析错误。
- 创建 `http_demo.py`，通过 Requests 发送带查询参数的 GET 请求，设置超时、检查 HTTP 错误并解析响应。学习者实际输出为 HTTP 200，回显参数是 `page: "1"` 与 `topic: "agent"`；助手已核对当前代码。
- 修正 HTTP 功能模块的自身导入，并在 `http_demo.py` 中调用 `fetch_echo()`。助手已验证导入 `http_tools` 时无输出，运行当前入口得到 `page: "2"` 与 `topic: "agent"`，模块连接与参数传递通过。
- 简化 HTTP 工具函数，去掉捕获后立即重新抛出的冗余处理。学习者提供的实际输出表明：临时请求 `/status/404` 时，`HTTPError` 传播到入口并显示失败提示；恢复 `/get` 后正常返回参数字典。助手已核对代码，确认地址已恢复、入口仍负责捕获请求异常。
- DeepSeek 密钥配置：学习者已在本机当前 PowerShell 会话中交互设置 `DEEPSEEK_API_KEY`，并报告 Python 输出“密钥已读取”。这一步仅检查环境变量存在；后续已通过首次真实模型请求。密钥未提供给助手或写入项目资料。
- 首次模型调用：学习者亲手创建 `model_demo.py`，使用环境变量中的密钥、Bearer 请求头和 JSON 请求体，通过 Requests 调用 `deepseek-flash`。学习者实际返回：“Agent 是一个能感知环境、自主决策并采取行动以达成目标的智能实体。”助手已核对当前代码中的请求与回答提取逻辑，调用通过。
- 模型响应观察：学习者成功打印第一条 choice 的消息、结束原因与用量。本次实际 `role=assistant`、`finish_reason=stop`；输入 11 token，生成 18 token，总计 29；输入缓存命中 0、未命中 11，两者合计为输入 11，缓存字段不额外累加到总数。助手已核对当前摘要输出代码；这些数值属于本次响应，后续调用以实际返回为准。

## 学习进度

- 当前：Python 工程基础、HTTP 练习、首次 DeepSeek 模型请求，以及模型响应观察均已完成；模型请求函数已拆出，离线验收发现返回类型不符合约定，待学习者修正。
- 学习起点：学习者已有 Python 语法基础，跳过基础语法复习。
- 行数约定：空字符串为 0 行，末尾换行不额外增加一行，采用 `len(text.splitlines())`。
- 类型标注：修改前曾实测传入 `bytes` 仍成功返回统计结果，说明类型标注本身不自动执行运行时校验；现在通过显式类型检查拒绝非字符串。
- HTTP 函数拆分进度：已修复自身导入、简化异常处理，通过正常调用、HTTP 404 失败提示和恢复成功路径的练习。
- 模型服务选择：学习者选择 DeepSeek；按 DeepSeek 官方 API 准备，沿用已有 Requests，以便观察 HTTP 请求头、JSON 请求体和模型响应。
- 官方接口核实（2026-10-21）：入口 `https://api.deepseek.com/chat/completions`，认证方式为 Bearer API Key；官方入门示例当前采用模型名 `deepseek-flash`。来源：https://api-docs.deepseek.com/zh-cn/ 。学习者已通过该模型完成一次真实请求。
- 当前模型参数：`deepseek-flash`，关闭 thinking，`stream=False`，`max_tokens=128`；请求用一句话解释 Agent。封装后的入口当前直接 `print(body)`，原先的响应摘要需要恢复。
- 模型函数离线验收：助手未发送真实模型请求，以替代响应和临时测试配置检查了实际代码。模块导入没有输出或网络请求，传入的消息正确进入请求体，缺少密钥时抛出 `RuntimeError`，HTTP 请求异常能向调用方传播。当前 `model_client.py` 第 32 行仅返回回答正文，实测返回类型为 `str`，不符合 `-> dict` 与完整响应的约定；此项尚未验收通过。
- 下一步练习：学习者将客户端返回值改为完整 `body`；移除入口中重复的密钥读取及检查，由客户端负责配置检查；恢复入口的 `message`、`finish_reason`、`usage` JSON 摘要，并打印返回类型确认是 `dict`。
- HTTP 404 验证（2026-10-21）：助手已确认测试地址返回 HTTP 404，`raise_for_status()` 抛出 `HTTPError`，且该异常属于 `RequestException`；学习者已通过自身工具观察失败并恢复成功路径。
- HTTP 准备验证（2026-10-21）：`https://httpbin.org/get?topic=agent&page=1` 实测 HTTP 200，响应中的 `args` 包含 `topic: agent` 和 `page: "1"`。
- 本机笔记服务观察（2026-10-21）：Java 进程监听 8080，但读取笔记列表的两次请求分别在 5 秒和 12 秒超时；当前未确认服务响应问题的原因，尚未修复。HTTP 入门练习使用已验证的公开回显接口，后续接入笔记服务前需重新检查。
- 后续：模型请求函数验收与失败处理、会话消息与上下文、两个工具的 Agent 循环。

Java 笔记阶段按本次交接记录收尾：新增/修改的正常、空白、5000 和 5001 字符，共 8 项专项验证通过。该结果来自学习者交接，本项目没有重新执行 Java 接口测试。
