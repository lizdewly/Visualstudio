user_score = 85
#조건문
if user_score >=80:
    grade = 'Pass'
else:
    grade = 'Fail'

#삼항연산자로 표현하면
grade = 'Pass' if user_score >=80 else 'Fail'