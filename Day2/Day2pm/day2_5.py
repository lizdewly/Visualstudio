#리스트에서 불량을 모두 지우고 정상만 남게
#방법 1
items = ['정상', '불량', '불량', '정상']
items = [item for item in items if item != '불량'] # result = [item for item in items if item != '불량']

print(f'검수결과 :{items}')

#방법2
items =  ['정상', '불량', '불량', '정상']
while '불량' in items:
    items.remove('불량')
print(items)

#방법3
items =  ['정상', '불량', '불량', '정상']
target = items [:] #복사
for item in target:
    if item == '불량':
        items.remove('불량')
print(f'검수결과 :{items}')