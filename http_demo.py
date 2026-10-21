import json
import requests
from http_tools import fetch_echo

def main() -> None:
    try:
        result = fetch_echo("agent", 2)
    except requests.exceptions.RequestException as exc:
        print(f"HTTP 请求失败：{exc}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()