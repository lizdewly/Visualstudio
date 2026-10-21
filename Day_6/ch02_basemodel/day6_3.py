#필수/기본값, 모델 생성/검증
from pydantic import BaseModel, ValidationError

class Member(BaseModel):
    username : str
    age : int
    active : bool = True
    nickname : str | None = None

def main() ->None:
    member = Member(username = 'lee', age=20)
    print(member)
    raw = {'username' :'kim', 'age':'34', 'active':False}
    parsed = Member.model_validate(raw)
    print(parsed, 'age 타입', type(parsed.age).__name__)
    print('nickname 기본값', parsed.nickname)

#필수 필드 누락 
try:
    Member(username='kim') #맞는 것 : Member.model_validate({'username':'kim'})
except ValidationError as e:
    print(e.errors()[0]['loc'], e.errors()[0]['type'])

#memberout 객체생성
memberout = MemberOut(id=1)
print(memberout)


if __name__ =='__main__': #__XX__ 미리 만들어놓은 변수, main 에서 쓸때는 day6_3의 아래 코드가 사용되지 않도록
    # m = Member(username='홍길동', age=20, active=True, nickname=None)
    # print (m.username)
    # print('day6_3.py', __name__)
    main()