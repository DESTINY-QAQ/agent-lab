import requests




def fetch_echo(topic: str, page: int) -> dict[str, str]:
    try:
        response = requests.get(
            "https://httpbin.org/get",
            params={"topic": topic, "page": page},
            timeout=10,
        )
        response.raise_for_status()
        body = response.json()
    except requests.exceptions.RequestException as exc:
        raise exc
    else:
        return body["args"]

if __name__ == "__main__":
    print(fetch_echo("agent", 1))   