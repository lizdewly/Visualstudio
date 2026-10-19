# 실습 메뉴: 각 모듈의 run() 함수를 호출합니다.
# 숫자 입력이 필요한 곳에는 정수를 입력하세요.
import variables, conditions, lists, multiplication, guessing_game


def main():
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
            variables.run()
        elif choice == "2":
            conditions.run()
        elif choice == "3":
            lists.run()
        elif choice == "4":
            multiplication.run()
        elif choice == "5":
            guessing_game.run()
        else:
            print("0~5 중에서 선택하세요.")


if __name__ == "__main__":
    main()
