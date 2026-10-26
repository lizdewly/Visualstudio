# 사용자로부터 테이터를 입력받아서 (5개) 리스트에 저장하고
# 저장된 리스트의 값 중에서 짝수만 출력해보기 (i%2 == 0)
# numbers = int(input("숫자를 입력하세요 : "))
scores = []
for i in range(5):
    score = int(input(f"{i+1}: 숫자를 입력하세요 : "))
    scores.append(score)

print('리스트변수의 값 :', scores)

for i in scores:
    if i % 2 == 0:
        print(i)
        
# break to exit the loop (순환문을 종료)


