def run():
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


if __name__ == "__main__":
    run()
