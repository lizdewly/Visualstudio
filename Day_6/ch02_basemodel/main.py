import Day_6.ch02_basemodel.day6_3 as day6_3



member = day6_3.Member(username='홍길동', age=20, active=True, nickname=None)
if member.age>19:
    print ('성인입니다')

print('main.py',__name__) #__name__이 "main 자신이 실행됨"