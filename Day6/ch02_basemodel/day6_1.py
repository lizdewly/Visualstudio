# pydantic
# 데이터의 유효성 및 타입을 체크
# BaseModel이 구현된 클래스를 상속받아서 pydantic 클래스 또는 모델을 만들 수 있음.
from pydantic import BaseModel, ValidationError

# 일반 파이썬 클래스
class NormalClass:
    def __init__(self, name: str, age: int):  # NormalClass('홍길동', 20) -> 매개변수가 없는 생성자를 호출
        self.name = name
        self.age = age

user1 = NormalClass(name='홍길동', age=20)
print('일반클래스', user1.age)
print('데이터 타입', type(user1.age))

params = {'age':20, 'name':'홍길동'}
# user1 = NormalClass('홍길동', 20) --> NormalClass(params) - name = params 이고 두번째 age 는 data 없음 - error
# --> user1 = NormalClass(**params) ** 는 풀어서

# pydantic 모델
class pydanticUser(BaseModel):
    name: str
    age: int

user2 = NormalClass(name='홍길동', age=20)
print('일반클래스', user2.age)
print('데이터 타입', type(user2.age))

try:
    user3 = pydanticUser(name='홍길동', age='스무살')
    print('일반클래스', user3.age)
    print('데이터 타입', type(user3.age))
except ValidationError as e: 
    print('에러', e)