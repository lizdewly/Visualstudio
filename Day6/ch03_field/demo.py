#Field 범위, 길이, 패턴에 대해서 엄격하게 검사
from pydantic import BaseModel,Field,ValidationError,EmailStr,ConfigDict
from typing import Literal

class Registration(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    name : str = Field(min_length=2, max_length=20, description='실명')
    age : int = Field(ge=14, le=100) #strict = True 의 경우 자동변환X 
    email : EmailStr
    level : Literal['basic','premium']='basic' #Literal ->  Basic,Premuim 등 미리 지정된 값만 사용가능, #Union은 변수의 타입 (ex. 문자vs. 정수 중 하나)
    code : str = Field(pattern=r'^STU-[0-9]{4}$') #r = 정규표현, #STU-0001 문자열의 시작, 0에서 9까지의 숫자가 4자리가 존재
    #code : str = Field(pattern=r'^[A-Z]{3}$') :영문 대문자 정확히 3글자”**예요. "ABC"는 통과하고 "ab12"는 실패.
    agreed : bool=Field(strict=True)

def main() -> None:
    user1 = Registration(name='kim', age=50, email='lee@abc.com', code='STU-0001', agreed=True)
    print('검증성공', user1.model_dump())
    print('오류확인')
    try:
        user2 = Registration(name='lee', age=70, email='lee@abc.com', code='STU-0001', agreed=True)
        print(user2.age)
    except ValidationError as e:
        for error in e.errors():
            print(error['loc'], error['type'])
if __name__=='__main__':
    main()