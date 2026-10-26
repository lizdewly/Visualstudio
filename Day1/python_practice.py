# Python 기초 복습: day1-1.py ~ day1-5.py의 예제 모음
# 실행 방법: python python_practice.py
# 메뉴에서 1~5를 선택해 실습하고, 0을 입력하면 종료합니다.
# 숫자 입력이 필요한 곳에는 정수를 입력하세요.

import random

while True:
    print("\n===== Python 기초 실습 =====")
    print("1. 변수와 덧셈")
    print("2. 점수로 합격 / 불합격 판단")
    print("3. 리스트에 숫자 5개 저장하고 짝수 출력")
    print("4. 반복문으로 구구단 출력")
    print("5. 숫자 맞추기 게임")
    print("0. 종료")
    choice = input("실습 번호를 선택하세요: ")

    if choice == "0":
        print("실습을 종료합니다.")
        break
    elif choice == "1":
        # 실습 1: 변수, 정수, 덧셈, print()
        # 복습 과제: number1과 number2를 바꾸고 결과를 예상해 보세요.
        number1 = 100
        number2 = 200
        print("number1 + number2 =", number1 + number2)
    elif choice == "2":
        # 실습 2: input(), int(), 비교 연산자, if / else
        # 사용자로부터 점수를 받아서 60점 이상이면 합격, 미만이면 불합격 출력
        # 복습 과제: 59점과 60점을 각각 입력해 경계값을 확인하세요.
        score = int(input("점수를 입력하세요: "))
        if score >= 60:
            print("합격")
        else:
            print("불합격")
    elif choice == "3":
        # 실습 3: 리스트, append(), for, range(), 나머지 연산자 %
        # 사용자로부터 데이터 5개를 입력받아서 리스트에 저장하고 짝수만 출력
        # 복습 과제: i % 2 == 0을 i % 2 != 0으로 바꾸어 홀수를 출력하세요.
        scores = []
        for i in range(5):
            score = int(input(f"{i + 1}: 숫자를 입력하세요: "))
            scores.append(score)

        print("리스트변수의 값:", scores)
        print("짝수:")
        for i in scores:
            if i % 2 == 0:
                print(i)
    elif choice == "4":
        # 실습 4: for, 중첩 반복문, f-string, 출력의 end 옵션
        # range의 끝값은 포함되지 않습니다. range(1, 10)은 1~9입니다.
        # 복습 과제: 두 반복문의 순서를 바꾸면 출력 모양이 어떻게 달라질까요?
        print("\n[반복문 없이 2단 일부 출력]")
        i = 1
        print(f"2 X {i} = {2 * i}")
        i = 2
        print(f"2 X {i} = {2 * i}")
        i = 3
        print(f"2 X {i} = {2 * i}")
        i = 4
        print(f"2 X {i} = {2 * i}")

        print("\n[반복문으로 2단 출력]")
        for i in range(1, 10):
            print(f"2 X {i} = {2 * i}")

        print("\n[2~9단 세로 출력]")
        for dan in range(2, 10):
            print(f"{dan}단")
            for i in range(1, 10):
                print(f"{dan} X {i} = {dan * i}")
            print("============")

        print("\n[한 줄에 한 단씩 출력]")
        for dan in range(2, 10):
            for i in range(1, 10):
                print(f"{dan} X {i} = {dan * i}", end="\t")
            print()  # 한 단이 끝나면 줄바꿈

        print("\n[한 줄에 같은 곱하는 수를 출력]")
        # 예: 첫 줄에 2 X 1, 3 X 1, ..., 9 X 1 출력
        for i in range(1, 10):
            for dan in range(2, 10):
                print(f"{dan} X {i} = {dan * i}", end="\t")
            print()
    elif choice == "5":
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
    else:
        print("0~5 중에서 선택하세요.")
