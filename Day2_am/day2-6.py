#딕셔너리
#key-value 한쌍이 하나의 값
#리스트 vs 딕셔너리 : list는 위치로, dict는 키로 값을 찾는다. 
list1 = [10,20,30, [1,2,3]] #[값, 값]
dict1 = {'kor': 80, 'eng': 80, 'math': 90} #{키, 값}

#dict1.keys() #key만 가져오기
#dict1.values() #value만 가져오기
#dict1.items() #key-value 쌍 가져오기

#for i in list1:
#    print(i)

for i in dict1: #key값만 가지고온다. 
    print(i)

for i in dict1.values():
    print(i)

for i in dict1.items():  # 집합형태로 바뀜  ('kor', 80), ('eng', 80), ('math', 90)
    print(i)

for i in dict1.items():
    print(i, i[0], i[1]) #key, value

number1,number2 = [10,20]
print(number1,number2)

dict1 = {'kor': 80, 'eng': 80, 'math': 90}
for key, value in dict1.items():
    print(f"key = {key} value ={value}")