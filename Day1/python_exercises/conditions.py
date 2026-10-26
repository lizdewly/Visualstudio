def run():
    # 실습 2: input(), int(), 비교 연산자, if / else
    # 사용자로부터 점수를 받아서 60점 이상이면 합격, 미만이면 불합격 출력
    # 복습 과제: 59점과 60점을 각각 입력해 경계값을 확인하세요.
    score = int(input("점수를 입력하세요: "))
    if score >= 60:
        print("합격")
    else:
        print("불합격")


if __name__ == "__main__":
    run()
