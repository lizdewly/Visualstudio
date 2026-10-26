## Vibe Coding
# What 
# Constraints : 제약
# How : 구현
# Vibe Check : 검증 
# 3대 핵심 룰 P (Prompt) -> G (Generate) -> V (Validate)
# P (Prompt) : 입력 (Input), 출력(Output), 알고리즘, 제약 조건, 함수 명시 
# V : 결과 검증  (평가기준이 중요) -> Test Case 검증

# 1부터 N까지의 짝수 합과 개수 구하기

#[Problem] 1 부터 n까지의 정수 중 짝수들의 합과 짝수의 총 개수를 계산한다. 
#[Function] calculate_even_sum_and_count(n)
#[Rules]
#    - n이 1 미만인 경우 합 0, 개수 0을 반환할것
#    - for 문과 if 문을 활용하여 짝수(i % 2 ==0)를 판단할 것
#[Output]    {"Sum": int, "Count":int  }

#zip
list_1 = ['a','b','c']
list_2 = [100,200,300]
# zip 을 생성한 객체를 dict로 변환 
result = list(zip(list_1, list_2))
#print(range(5))
#for i in result:
#    print(i)

results2= dict(result)
print(results2)
 