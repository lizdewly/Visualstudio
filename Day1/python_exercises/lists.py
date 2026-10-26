def run():
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


if __name__ == "__main__":
    run()
