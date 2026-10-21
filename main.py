from text_tools import inspect_text
import json

def main() -> None:
    request_json = '{"text": "123"}'

    try:
        request = json.loads(request_json)

        if not isinstance(request, dict):
            raise TypeError("请求必须是 JSON 对象")

        result = inspect_text(request.get("text"))
    except (json.JSONDecodeError, TypeError) as exc:
        response = {"ok": False, "error": str(exc)}
    else:
        response = {"ok": True, "data": result}

    print(json.dumps(response, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()