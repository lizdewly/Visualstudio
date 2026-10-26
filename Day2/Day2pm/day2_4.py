import random
#ages = random.sample(range(0,100),10) #랜덤하게 샘플 중 10개를 고르겠음, 0-100세 사이

ages = random.sample(range(100), 10)
ages = [71,5,27,91,94,35,85,6,61,66]
results = []
for i in ages:
    if i>=20:
        results.append('성인')
    else:
        results.append('미성년자')

print(results)
