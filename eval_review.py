import json
from pathlib import Path


def main() -> None:
    results_path = Path(__file__).with_name("eval_results.json")
    results = json.loads(results_path.read_text(encoding="utf-8"))
    reviews = []

    for case in results:
        print(f"\n用例：{case['id']}")
        print("问题：", case["question"])
        print("预期是否应说明资料不足：", case["expect_insufficient"])
        agent_result = case.get("agent_result")

        if agent_result is not None:
            print("模型的资料不足判断：", agent_result["insufficient"])
            print("程序记录来源：", agent_result["read_files"])
            print("模型原始 JSON：", agent_result["raw_final_content"])

        for message in case["messages"]:
            if message.get("role") != "tool":
                continue

            result = json.loads(message["content"])
            print("\n工具返回结果：")
            print(json.dumps(result, ensure_ascii=False, indent=2))

        print("\n最终回答：", case["answer"])

        verdict = input("\n内容审核是否通过（y/n）：").strip().lower()

        while verdict not in ("y", "n"):
            verdict = input("请输入 y 或 n：").strip().lower()

        reviews.append({
            "case_result": case,
            "content_pass": verdict == "y",
        })

    reviews_path = Path(__file__).with_name("eval_reviews.json")
    content = json.dumps(reviews, ensure_ascii=False, indent=2)
    reviews_path.write_text(content, encoding="utf-8")

    print(f"\n已保存 {len(reviews)} 条审核记录：{reviews_path}")


if __name__ == "__main__":
    main()