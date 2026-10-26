#List comprehension
result = []
list_1 = [1,2,3,4,5]

#for i in list_1: 
#    if i % 2 == 0: 
#       result.append(i)

#result = [i for i in list_1 if i%2 ==0]
#result = [i*2 for i in list_1]

# print(result)

# menu = ['아메리카노', '라떼', '초코']
# ice_menu = ['아이스'+i for i in menu]
# len_menu = [len(i) for i in menu if len(i)%2==0]
# print(ice_menu)
# print(len_menu)

#['참' if 조건 else '거짓' for i in 집합]
ages = [20,15,60,25,30,45,5]
print([ i for i in ages if i>=20])
print(['성인' if i>=20 else '미성년' for i in ages]) # list comprehension 한줄로 축약 

# if "":
    # print("abc") # 출력 불가, 조건에 맞지 않음 - grey 처리됨 "print"

print( set([1,2,3,4,5,6,7,8,1,2,3,4,5])  ) # set : 중복제거
#sorted
#set 

bad_words = ['바보', '뭉탱이', '멍청이', '', '뭉탱이']
words = sorted(set (word for word in bad_words if word), key=len, reverse=True) 
#긴 단어부터 찾아서 (길이기준 = len) 내림차순으로 (reverse), 중복 제거 (set) 
print(words)

import re
print(re.escapte(word) for word in words)
pattern = "|".join(re.escape(word) for word in words)

#print(type("|".join(words))) #합치기, 문자열로 (join)