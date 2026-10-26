# 숫자 맞추기 게임
# 규칙
# 컴퓨터가 1부터 100까지의 숫자를 임의로 생성한 후 사용자가 숫자를 맞추는 게임
# 사용자가 입력한 숫자가 컴퓨터가 생성한 숫자보다 크면 "크다" 작으면 "작다"를 출력하고, 같으면 "정답"을 출력하고 게임 종료

# -- 필요한 기능
# 입력 : int(input())
# 컴퓨터가 1부터 100까지의 숫자를 임의로 생성 : random.randint(1, 100)
# 비교연산자를 통해 크다 작다 정답 판변
# 순환문, 조건문, break를 통해 게임 종료

#import random
#for i in range(3): #3번 반복
    #number = random.randint(1, 100)
    #print(number) # 정답 확인용

import random 
com_number = random.randint(1, 100) # 컴퓨터가 1~100까지의 숫자를 임의로 생성
count = 0 # 사용자가 입력한 횟수 초기화
user_number = 0 # 사용자가 입력한 숫자 초기화
while com_number != user_number: # 컴퓨터가 생성한 숫자와 사용자가 입력한 숫자가 같지 않으면 반복
    user_number = int(input("1~100  : ")) # 사용자가 입력한 숫자를 정수로 변환하여 저장
    count += 1 # 사용자가 입력한 횟수 증가 (복합대입연산자 +=1)
    # count = count + 1 , #count += 1
    if com_number > user_number: # 컴퓨터가 생성한 숫자가 사용자가 입력한 숫자보다 크면
        print("작다") # 작다 출력
    elif com_number < user_number: # 컴퓨터가 생성한 숫자가 사용자가 입력한 숫자보다 작으면
        print("크다") # 크다 출력
    else: # 컴퓨터가 생성한 숫자와 사용자가 입력한 숫자가 같으면
        print(f"정답! 총 시도회수는 : {count}") # 정답 출력
        break # 반복문 종료
#print(f"사용자가 {count}번 만에 정답을 맞췄습니다.") # 입력 횟수 출력

