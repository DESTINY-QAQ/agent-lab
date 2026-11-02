from quiz_demo import main as start_quiz
from quiz_history import main as show_latest_quiz


def main() -> None:
    while True:
        print("\n笔记复习助手")
        print("1. 开始自测")
        print("2. 查看最近一次练习")
        print("0. 退出")

        choice = input("请选择：").strip()

        if choice == "1":
            start_quiz()
        elif choice == "2":
            show_latest_quiz()
        elif choice == "0":
            print("已退出")
            break
        else:
            print("请输入 1、2 或 0")


if __name__ == "__main__":
    main()