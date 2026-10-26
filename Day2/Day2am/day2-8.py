list_a = [1,2,3,4,5,6,7,8,9,10]

for i in list_a:
    if i % 2 ==0: #짝수가 아니면 출력 (짝수면 continue 를 만나서 순환문의 다음 것을 실행)
        continue 
    print(i)

    #if i == 5: 
        #continue 5 빼고 출력 