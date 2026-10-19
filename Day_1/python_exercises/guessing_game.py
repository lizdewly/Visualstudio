import random


def run():
    # 실습 5: random.randint(), while, if / elif / else, +=, break
    # 컴퓨터가 1~100 중 임의의 숫자를 정하고 사용자가 맞추는 게임
    # 복습 과제: 숫자 범위를 1~50으로 바꾸고 입력 안내도 수정하세요.
    com_number = random.randint(1, 100)
    count = 0  # 사용자가 입력한 횟수 초기화
    user_number = 0

    while com_number != user_number:
        user_number = int(input("1~100 사이의 숫자를 입력하세요: "))
        count += 1  # count = count + 1과 같은 의미
        if com_number > user_number:
            print("입력한 숫자가 정답보다 작다")
        elif com_number < user_number:
            print("입력한 숫자가 정답보다 크다")
        else:
            print(f"정답! 총 시도 횟수는: {count}")
            break  # 게임 반복문 종료 후 실습 메뉴로 돌아갑니다.


if __name__ == "__main__":
    run()
