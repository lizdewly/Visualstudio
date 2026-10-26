# Day_6 코드·문법 종합 정리표

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문과 정리 범위 | [질문](#질문) |
| 전체 흐름과 원본 | [답변](#답변) |
| 기초 문법 연결 | [1. 기초 문법](#1-기초-문법) |
| 클래스와 타입 | [2. 클래스와 타입](#2-클래스와-타입) |
| 입력 조건 | [3. field와-입력-조건](#3-field와-입력-조건) |
| 검사 함수 | [4. validator와-문자열-처리](#4-validator와-문자열-처리) |
| 중첩 데이터 | [5. 중첩-모델](#5-중첩-모델) |
| 데이터 변환과 수정 | [6. 변환과-부분-수정](#6-변환과-부분-수정) |
| 웹 요청과 응답 | [7. fastapi](#7-fastapi) |
| 저장과 검색 | [8. 저장소와-검색](#8-저장소와-검색) |
| 코드를 이어 읽기 | [9. 연결해서-읽는-예제](#9-연결해서-읽는-예제) |
| 혼동 방지와 원본 상태 | [헷갈리기 쉬운 점](#헷갈리기-쉬운-점) |
| 출처 | [참고 자료](#참고-자료) |

- 최초 기록일: 2026-10-21
- 수정일: 2026-10-21
- 분류: Python, Coding
- 핵심 용어: 타입 힌트, BaseModel, Field, validator, 중첩 모델, 직렬화, PATCH, FastAPI, dict

## 질문

Day_6에 명시된 코드와 문법을 종합해, 어떤 코드가 어떤 의미로 어떻게 쓰이는지 일목요연한 표로 정리하고 연관 코드도 함께 표시해 주세요. 아직 배우지 않은 내용은 제외하고 지난 6일 동안 나온 코드와 문법 위주로 쉽게 설명해 주세요.

## 답변

**Day_6의 핵심은 ‘데이터의 모양과 조건 정하기 → 입력 검사하기 → 저장·수정하기 → API로 주고받기’입니다.** 예전에 배운 변수·조건문·함수·클래스·딕셔너리를 이 과정에 함께 사용합니다.

Day_6의 ch02~ch08 Python 파일과 요청 예제를 기준으로 정리했습니다. 앞선 내용은 Day_1~Day_4 파일과 10월 20일 FastAPI 학습 기록에서 확인한 것만 연결했습니다. `Day_5` 폴더는 없어서 특정 파일을 ‘5일차 코드’라고 추정하지 않았습니다. 예제·정답 파일에 있는 내용도 포함하되, 실제로 수업을 어디까지 진행했는지는 파일만으로 단정하지 않습니다. 아래 짧은 코드는 문법을 읽기 위한 발췌이며 각각 독립 실행 파일은 아닙니다.

| 단계 | 하는 일 | 원본 위치 |
| --- | --- | --- |
| ch02 | 모델, 타입, 필수 항목과 기본값 | [day6_1.py](../Day_6/ch02_basemodel/day6_1.py), [day6_2.py](../Day_6/ch02_basemodel/day6_2.py), [day6_3.py](../Day_6/ch02_basemodel/day6_3.py), [책 실습](../Day_6/ch02_basemodel/day6_3ex.py) |
| ch03 | 숫자 범위·길이·형식 제한 | [demo.py](../Day_6/ch03_field/demo.py) |
| ch04 | 값 정리, 여러 필드 사이의 관계 검사 | [demo.py](../Day_6/ch04_validator/demo.py), [solution.py](../Day_6/ch04_validator/solution.py) |
| ch05 | 모델 안에 모델 넣기, 합계 계산 | [demo.py](../Day_6/ch05_nested/demo.py), [solution.py](../Day_6/ch05_nested/solution.py) |
| ch06 | 모델과 dict/JSON 변환, 부분 수정 | [demo.py](../Day_6/ch06_serialization/demo.py), [solution.py](../Day_6/ch06_serialization/solution.py) |
| ch07 | 작업 생성·조회·수정·삭제 API | [app.py](../Day_6/ch07_fastapi/app.py), [requests.http](../Day_6/ch07_fastapi/requests.http) |
| ch08 | 회원·작업 관리 종합 | [models.py](../Day_6/ch08_project/models.py), [store.py](../Day_6/ch08_project/store.py), [app.py](../Day_6/ch08_project/app.py) |

## 1. 기초 문법

| 코드·문법 | 쉬운 뜻과 사용법 | 연결되는 Day_6 코드 |
| --- | --- | --- |
| `name = '하늘'` | 변수에 값을 연결. `=`는 대입 | `_next_id = 2`로 다음 번호 준비 |
| `==`, `!=`, `>`, `<`, `>=`, `<=` | 같은지·다른지·큰지 등을 비교 | 비밀번호 `!=`, 시작일 `>`, `Field(ge=...)`의 범위 조건 |
| `if / elif / else` | 조건에 따라 다른 코드 실행 | `if task_id not in _db:`로 없는 작업 처리 |
| 들여쓰기와 `:` | `if`, `def`, `class`, `for` 아래 실행 범위를 구분 | 검사 함수는 클래스 안, 실행용 `main()`은 클래스 밖 |
| `and / or / not` | 둘 다 만족 / 하나라도 만족 / 참·거짓 뒤집기 | `value is not None and not value.strip()` |
| `is None / is not None` | 값이 없음을 나타내는 `None`인지 확인 | 선택 항목 검사, `done=False`도 검색 조건으로 인정 |
| `in / not in` | 포함 여부. dict에서는 기본적으로 **키**를 검사 | `'title' in changes`, `task_id not in _db` |
| `for error in e.errors():` | 오류들을 하나씩 꺼내 반복 | ch03에서 오류 위치와 종류 출력 |
| `[값 for 항목 in 목록 if 조건]` | 조건을 통과한 항목으로 새 리스트 생성 | 태그 정리, 회원별 작업 검색 |
| `A if 조건 else B` | 조건에 따라 사용할 값 하나 선택 | `value.strip() if value is not None else None` |
| `def main() -> None:` | 함수 정의. 여기서 `-> None`은 반환값을 사용하지 않는다는 타입 안내 | 각 실습의 실행 함수 |
| `return 값` | 함수를 끝내고 호출한 곳에 값 전달 | 검사기는 정리한 값, API 함수는 응답 데이터 반환 |
| `print(값)` | 콘솔에 표시 | `print(student.model_dump())`; `return`과 역할이 다름 |
| `type(student.age)` | 실제 값의 타입 확인 | 입력 문자열이 정수로 바뀌었는지 확인 |
| `type(parsed.age).__name__` | 타입의 이름만 읽기 | ch02에서 `int` 같은 이름 확인 |
| `isinstance(value, str)` | 해당 값이 문자열 타입인지 검사 | 문자열 태그에만 `split(',')` 적용 |
| `try / except ValidationError as e` | 시도하다 검증 오류가 발생하면 `e`로 받아 처리 | 입력 실패를 잡아서 설명 출력 |
| `raise ValueError('설명')` | 잘못된 값이라는 예외를 직접 발생 | 비밀번호 불일치, 날짜 순서 오류 |
| `e.errors()[0]['loc']` | 오류 목록 → 첫 오류 → 위치 정보 순서로 접근 | `['type']`은 종류, `['msg']`는 설명 |
| `import ...`, `from ... import ...` | 다른 파일·라이브러리의 기능 가져오기 | `from pydantic import BaseModel` |
| `import ... as day6_3` | 가져온 모듈에 짧은 이름 부여 | `day6_3.Member(...)` |
| `from .models import TaskCreate` | 같은 패키지의 models 모듈에서 가져오기 | ch08의 app/store가 모델 공유 |
| `if __name__ == '__main__':` | 파일을 직접 실행했을 때만 아래 코드 실행 | 다른 파일에서 import할 때 `main()` 자동 실행 방지 |

기초 연결 원본: [조건과 논리](../Day_2_am/day2-2.py), [딕셔너리](../Day_2_am/day2-6.py), [컴프리헨션](../Day_2_pm/day2_3.py), [예외 처리](../Day_3/day3_6).

## 2. 클래스와 타입

| 코드·문법 | 쉬운 뜻과 사용법 | 연관 코드·차이 |
| --- | --- | --- |
| `class NormalClass:` | 객체를 만들기 위한 설계도 정의 | Day_3의 `BaristaBot`과 같은 기본 문법 |
| `def __init__(self, name: str, age: int):` | 객체를 만든 뒤 초기 값 설정 | `self.name = name`으로 개별 객체에 이름 저장 |
| `self` | 현재 다루는 개별 객체 | `self.password`, `self.start` |
| `class Student(BaseModel):` | BaseModel을 상속해 데이터 검사 기능 사용 | 일반 클래스의 타입 힌트만으로는 자동 검사가 생기지 않음 |
| `name: str`, `age: int` | 문자열·정수 항목 정의 | Pydantic 모델에서는 기본값이 없으므로 필수 입력 |
| `active: bool = True` | 참·거짓 항목, 생략하면 `True` | `False`는 거짓, `None`은 값 없음 |
| `interests: list[str]` | 문자열을 담는 리스트 | `['AI', 'python']`; `list[OrderItem]`으로 확장 |
| `nickname: str \| None = None` | 문자열 또는 None 허용, 생략 시 None | 타입의 `\| None`과 기본값 `= None`은 서로 다른 역할 |
| `Optional[str]` | `str \| None`과 같은 타입 의미 | 생략 가능 여부는 기본값을 따로 봐야 함 |
| `Union[int, str]` | 정수 또는 문자열 허용 | `int \| str`과 같은 타입 의미; Literal은 구체적인 값 제한 |
| `Student(name='하늘', age=23, ...)` | 항목 이름을 지정해 모델 객체 생성 | `name=...` 같은 전달 방식은 키워드 인자 |
| `Book(price='19000', title='파이썬기초')` | 기본 설정에서 변환 가능한 문자열을 정수로 검사·변환 | `'스무살'`처럼 변환 불가능한 입력은 실패 |
| `Member.model_validate(raw)` | dict 등 입력을 모델 기준으로 검사하여 객체 생성 | `raw`는 원본 데이터라는 뜻으로 지은 변수 이름 |
| `member.age` | 모델 객체의 속성 읽기 | dict는 `raw['age']`로 읽음 |
| `NormalClass(**params)` | dict의 키·값을 이름 있는 인자로 풀어서 전달 | `params={'name':'홍길동','age':20}`이면 `name=..., age=...` |
| `class TaskOut(TaskIn):` | TaskIn의 필드를 물려받고 출력용 필드 추가 | 본문에 `id: int`를 추가 |
| `-> str`, `-> 'Signup'` | 함수의 반환 타입 안내 | 따옴표로 감싼 클래스 이름도 타입 안내이며 문자열 반환 지시가 아님 |

`payload`, `raw`, `record`, `stored`, `changes`는 특별한 문법이 아니라 작성자가 지은 이름입니다. 각각 요청 데이터, 원본 데이터, 저장 항목, 기존 값, 변경분으로 읽으면 이해하기 쉽습니다.

## 3. Field와 입력 조건

원본: [ch03 demo](../Day_6/ch03_field/demo.py), [ch08 models](../Day_6/ch08_project/models.py).

| 코드·옵션 | 의미와 쓰는 상황 | 연관 코드·주의점 |
| --- | --- | --- |
| `Field(...)` | 필드에 조건·기본값·설명을 붙임 | `BaseModel` 안의 타입 선언과 함께 사용 |
| `Field(ge=14, le=100)` | 14 **이상**, 100 **이하** | `ge`/`le`는 경계 포함 |
| `Field(gt=0)` | 0 **초과** | `ge=0`은 0도 허용하므로 다름 |
| `Field(min_length=2, max_length=20)` | 문자열 길이 2~20 | 리스트에서는 항목 개수 조건 |
| `Field(default=False, strict=True)` | 기본값 False, 느슨한 타입 변환 거부 | bool 필드에서 문자열 `'yes'` 대신 실제 `True`/`False` 사용 |
| `Field(description='실명')` | 필드 설명 제공 | 실제로 실명인지를 검사하는 조건은 아님 |
| `EmailStr` | 이메일 형식으로 검사하는 타입 | 이메일이 실제 소유자의 것인지 확인하는 기능은 아님 |
| `Literal['basic', 'premium']` | 나열한 두 값 중 하나만 허용 | `= 'basic'`은 생략 시 기본값; 대소문자 구분 |
| `Field(pattern=r'^STU-[0-9]{4}$')` | 지정한 문자열 패턴 검사 | 아래의 각 기호를 조합 |
| `r'...'` | 역슬래시를 그대로 다루기 편한 문자열 표기 | **r 자체가 정규식이라는 뜻은 아님**; `pattern`이 패턴으로 해석 |
| `^`, `$` | 이 예제에서 문자열 시작·끝을 지정 | 앞뒤에 다른 문자를 붙이지 않는 코드 형식 표현 |
| `[0-9]{4}` | 숫자 0~9가 4번 | `STU-0001` 같은 코드 |
| `[A-Z]{3}` | 영문 대문자가 3번 | 원본 주석의 `^[A-Z]{3}$` 예시 |
| `model_config = ConfigDict(...)` | 모델에 공통 설정 적용 | 이름에 Strict가 들어가는 것만으로 엄격해지지는 않음 |
| `str_strip_whitespace=True` | 문자열 양끝 공백 제거 | 중간 공백까지 전부 삭제하는 기능은 아님 |
| `extra='forbid'` | 선언하지 않은 추가 필드를 받으면 오류 | `Task(..., unexpected=10)` |
| `extra='ignore'` | 선언하지 않은 추가 필드를 무시 | ch08 TaskOut에서 내부 메모를 출력 모델에 포함하지 않음 |

## 4. Validator와 문자열 처리

원본: [ch04 demo](../Day_6/ch04_validator/demo.py), [쿠폰 정답](../Day_6/ch04_validator/solution.py).

| 코드·문법 | 의미와 사용법 | 연결해서 읽기 |
| --- | --- | --- |
| `@...` | 바로 아래 함수에 역할을 부여하는 데코레이터 문법 | 검사기 등록과 API 경로 등록에 모두 사용 |
| `@field_validator('username')` | username 한 필드의 값을 검사·변환 | 괄호 안 이름이 실제 필드와 일치해야 함 |
| `@classmethod`와 `cls` | 첫 인자로 클래스 자체를 받는 메서드 | 현재 field_validator 아래에 사용; 이것 자체는 검사 기능이 아님 |
| `value` | 검사 함수가 받은 값의 매개변수 이름 | `return text`로 정리한 값을 돌려줌 |
| `mode='before'` | Pydantic 타입 검사 전에 원래 입력을 처리 | 문자열 `'python, api'`를 리스트로 바꾼 뒤 `list[str]` 검사 |
| 모드 생략 또는 `mode='after'` | 해당 필드의 기본 검증을 통과한 값 처리 | username의 길이 검사 뒤 공백 제거·소문자화 |
| `@model_validator(mode='after')` | 필드 검증 후 객체 전체의 관계 검사 | 비밀번호와 확인 값 비교, 시작일과 종료일 비교 |
| `return self` | 검사한 모델 객체를 반환 | 현재 after 모델 검사기의 성공 경로 |
| `value.strip()` | 문자열 양끝 공백 제거 | `'  abc  '`를 `'abc'`로 정리하는 용도 |
| `.lower() / .upper()` | 영문 소문자 / 대문자로 변환 | 아이디 통일 / 쿠폰 통일 |
| `value.split(',')` | 쉼표 기준으로 문자열 나누기 | 나눈 결과는 리스트 |
| `if not cleaned:` | 빈 문자열이면 조건 만족 | 공백 제거 뒤 내용이 남았는지 확인 |
| `if ' ' in text:` | 일반 공백 문자가 포함되었는지 검사 | 탭 등 모든 공백 문자를 통틀어 검사하는 것은 아님 |
| `[item.strip() for item in value.split(',') if item.strip()]` | 쉼표로 나누고, 공백을 지운 결과가 비지 않은 것만 모음 | `split` → `for` → 조건 확인 → 정리된 값으로 리스트 |
| `start: date`, `end: date` | 날짜 항목 정의 | Pydantic에서 예제의 날짜 문자열을 날짜 값으로 변환 |
| `if self.start > self.end:` | 시작일이 종료일보다 늦은지 비교 | 참이면 `raise ValueError(...)` |

필드 검사기는 사용할 **값**을, 현재 after 모델 검사기는 **self**를 반환합니다. 검사기에서 발생시킨 ValueError는 Pydantic 검증 오류에 포함됩니다. before/after와 반환 방식은 [Pydantic Validators 문서](https://docs.pydantic.dev/latest/concepts/validators/)로도 확인했습니다.

## 5. 중첩 모델

원본: [ch05 demo](../Day_6/ch05_nested/demo.py), [강좌 정답](../Day_6/ch05_nested/solution.py).

| 코드·문법 | 의미와 사용법 | 연관 코드 |
| --- | --- | --- |
| `address: Address` | 주문 안에 주소 모델 하나 포함 | `Order.model_validate(raw)`가 안쪽 주소도 검사 |
| `items: list[OrderItem]` | 주문 안에 주문 항목 모델 여러 개 포함 | dict들의 리스트를 항목 모델들의 리스트로 검사 |
| `Field(min_length=1)` | 항목이 최소 하나 필요 | 주문 항목·수강생이 빈 리스트이면 안 됨 |
| `order.address.city` | 주문 → 주소 → 도시 순서로 접근 | dict 원본이라면 `raw['address']['city']` |
| `order.items[0].quantity` | 첫 번째 주문 항목의 수량 | `[0]`은 첫 항목; 인덱스는 0부터 |
| `class DeliveryMethod(str, Enum):` | 문자열 값을 가진 이름 있는 선택지 정의 | `STANDARD = 'standard'`, `EXPRESS = 'express'` |
| `DeliveryMethod.STANDARD` | 정의한 배송 방식 중 기본 배송 선택 | Literal은 값을 나열하고 Enum은 선택지에 이름도 붙임 |
| `@property` | 메서드를 값처럼 읽도록 지정 | `order.total`로 사용하며 `order.total()`이 아님 |
| `sum(item.quantity * item.unit_price for item in self.items)` | 각 항목의 수량×단가를 모두 더함 | `for`로 값을 하나씩 만들어 `sum`에 전달 |
| `course.learners[0].name` | 강좌 → 첫 수강생 → 이름 | 주소·주문과 같은 중첩 접근 방식 |
| `error.errors()[0]['loc']` | 중첩 데이터의 어느 위치에서 실패했는지 확인 | 잘못된 항목의 인덱스와 필드명까지 위치에 포함될 수 있음 |

이전에 배운 연결점: [Day_3 클래스](../Day_3/day3_1), [property](../Day_3/day3_2), [상속](../Day_3/day3_3). 이 표에서는 중첩을 이해하는 데 필요한 범위만 다시 사용합니다.

## 6. 변환과 부분 수정

원본: [ch06 demo](../Day_6/ch06_serialization/demo.py), [ch06 solution](../Day_6/ch06_serialization/solution.py).

| 코드·옵션 | 의미와 쓰는 상황 | 연관 코드·주의점 |
| --- | --- | --- |
| `task.model_dump()` | 모델을 Python dict로 변환 | 날짜 값은 Python의 date로 남을 수 있음 |
| `task.model_dump(mode='json')` | JSON에 넣을 수 있는 값으로 구성된 dict 생성 | date를 문자열로 변환; **반환값은 여전히 dict** |
| `task.model_dump_json()` | 모델을 JSON 문자열로 변환 | 위의 dict 반환과 구분 |
| `Task.model_validate(raw)` | 입력을 검사하여 Task 모델 생성 | dump와 방향이 반대 |
| `patch.model_dump(exclude_unset=True)` | 입력할 때 지정하지 않은 필드 제외 | 실제 보낸 변경분만 추출 |
| `exclude_none=True` | 값이 None인 필드 제외 | ch06의 비교 주제; 명시적으로 보낸 None도 제외한다는 차이 |
| `{**기존dict, **변경dict}` | 두 dict를 풀어 새 dict로 합침 | 같은 키가 있으면 뒤의 변경값이 적용 |
| `Task.model_validate(merged)` | 합친 전체 데이터를 다시 검사 | 부분 수정 모델이 허용한 값도 최종 모델 조건에는 실패할 수 있음 |
| `ProfilePatch(bio=None)` | bio를 None으로 바꾸겠다고 명시 | exclude_unset에서도 bio를 남김 |
| `ProfilePatch()` | bio를 비롯한 변경 항목을 보내지 않음 | exclude_unset 결과에는 변경 항목이 없음 |

변환 옵션과 생략/None의 구분은 [Pydantic Serialization 문서](https://docs.pydantic.dev/latest/concepts/serialization/)로도 확인했습니다.

| 보내는 의도 | 변경분 표현 | 처리 의미 |
| --- | --- | --- |
| 완료 여부만 수정 | `TaskPatch(done=True)` | 제목·날짜 등 보내지 않은 값은 유지 |
| 날짜 지우기 | `TaskPatch(due=None)` | ch06에서는 due가 None을 허용하므로 삭제 의도 반영 |
| 제목을 None으로 바꾸기 | `TaskPatch(title=None)` | ch06에서는 모델 검사기가 거부; ch07/08은 병합 후 전체 모델 검사에서 거부 |

## 7. FastAPI

원본: [ch07 app](../Day_6/ch07_fastapi/app.py), [ch08 app](../Day_6/ch08_project/app.py).

| 코드·문법 | 의미와 사용법 | 연관 코드·주의점 |
| --- | --- | --- |
| `app = FastAPI(title=..., version=...)` | API 앱 생성, 문서에 표시할 정보 지정 | 이것만으로 서버가 실행되지는 않음 |
| `@app.get('/tasks')` | 이 주소의 GET 요청을 아래 함수에 연결 | 조회 기능 |
| `@app.post('/tasks')` | POST 요청 연결 | 생성 기능 |
| `@app.put('/tasks/{task_id}')` | PUT 요청 연결 | ch07에서는 전달받은 TaskIn으로 교체; 생략한 done은 기본값 False 사용 |
| `@app.patch('/tasks/{task_id}')` | PATCH 요청 연결 | 보낸 항목만 수정; exclude_unset과 함께 사용 |
| `@app.delete('/tasks/{task_id}')` | DELETE 요청 연결 | `del _db[task_id]`로 실제 삭제 |
| `'/tasks/{task_id}'`, `task_id: int` | 경로에서 작업 번호 받기 | `/tasks/1`에서 1 |
| `payload: TaskIn` | 요청 본문을 TaskIn 모델로 검사하여 받기 | payload는 요청 데이터라는 용도로 지은 이름 |
| `owner_id: int \| None = Query(default=None, gt=0)` | 선택적인 쿼리 값, 전달하면 0보다 큰 정수 | `/tasks?owner_id=1` |
| `done: bool \| None = None` | 완료 여부 필터를 선택적으로 받기 | `/tasks?done=false`; `if done is not None`으로 처리 |
| `response_model=TaskOut` | 응답에 사용할 데이터 모양 지정 | 응답을 검사·변환하고 모델에 맞게 필드 제한 |
| `response_model=list[TaskOut]` | TaskOut 여러 개를 담은 목록 응답 | `list(_db.values())`와 연결 |
| `status_code=status.HTTP_201_CREATED` | 생성 성공 상태 201 지정 | status는 숫자 코드를 이름으로 읽기 쉽게 제공 |
| `raise HTTPException(status_code=404, detail='...')` | HTTP 오류 응답으로 현재 처리 중단 | `detail`은 요청자에게 전달할 설명 |
| `raise HTTPException(...) from error` | 새 HTTP 오류가 기존 검증 오류에서 비롯됐음을 연결 | ch07/08의 병합 후 오류 처리 |
| `Response(status_code=status.HTTP_204_NO_CONTENT)` | 본문 없는 성공 응답 | 삭제 성공 시 사용 |

ch08에서는 저장 데이터에 `internal_note`가 있어도 TaskOut에 그 필드가 없고 추가 필드를 무시하므로 응답에서 빠집니다. 저장소의 내용을 지우는 것은 아닙니다. [FastAPI 응답 모델 문서](https://fastapi.tiangolo.com/tutorial/response-model/)에서도 응답 필드 제한 역할을 확인했습니다.

| 상태 코드 | 예제에서의 뜻 | 관련 상황 |
| --- | --- | --- |
| 200 | 일반 성공 | 목록·개별 조회, 수정의 기본 성공 응답 |
| 201 | 생성 성공 | 회원·작업 등록 |
| 204 | 성공, 응답 본문 없음 | 작업 삭제 |
| 404 | 찾는 대상 없음 | 저장소에 없는 회원·작업 |
| 409 | 기존 데이터와 충돌 | 같은 이메일로 회원 등록 |
| 422 | 요청 데이터 검증 실패 | 범위 위반, 잘못된 bool, 잘못된 수정 결과 |
| 501 | 예제의 미구현 표시 | exercise/starter에 남아 있는 TODO |

| 요청 파일의 표현 | 의미 | 연결 |
| --- | --- | --- |
| `GET {{baseUrl}}/tasks` | 지정한 기본 주소에 목록 요청 | `@app.get('/tasks')` |
| `Content-Type: application/json` | 보내는 본문이 JSON임을 표시 | `payload: TaskIn` |
| `{"done":true}` | JSON 형식의 변경 데이터 | Python에서는 `{'done': True}` |
| JSON `null` | JSON에서 값 없음 | Python `None` |
| `?owner_id=1&done=false` | URL의 검색 조건 두 개 | `Query`, 리스트 컴프리헨션 |
| `###`, `@baseUrl`, `{{baseUrl}}` | 현재 요청 파일 형식의 구분·변수·치환 표기 | Python 문법이 아님 |

앞선 FastAPI 기록의 `Annotated[int, Path(ge=1)]`은 경로 값의 타입에 범위 조건을 붙인 표현입니다. `Query`는 쿼리 값, `Path`는 경로 값, `Field`는 모델 필드에 조건을 붙인다는 위치 차이로 연결해 기억하세요.

## 8. 저장소와 검색

원본: [ch08 store](../Day_6/ch08_project/store.py), [ch08 app](../Day_6/ch08_project/app.py).

| 코드·문법 | 의미와 사용법 | 연관 코드 |
| --- | --- | --- |
| `members: dict[int, dict] = {}` | 정수 번호를 키로, 회원 dict를 값으로 저장 | 빈 dict로 시작 |
| `_db: dict[int, TaskOut]` | 정수 키에 TaskOut 모델을 저장 | ch07은 모델, ch08은 dict를 저장한다는 차이 |
| `members[member.id] = ...` | 해당 번호의 값 저장·교체 | 같은 키이면 기존 값 덮어씀 |
| `store.members.get(member_id)` | 해당 키의 값 조회, 없으면 기본적으로 None | `if member is None:`에서 404 처리 |
| `list(store.tasks.values())` | 작업 값들을 리스트로 모음 | 앞서 배운 dict의 `values()` |
| `record.items()` | 키와 값의 쌍들을 가져옴 | `for key, value in ...`로 각각 받음 |
| `[record for record in results if record['done'] == done]` | 완료 여부가 같은 작업만 모음 | Day_2의 리스트 컴프리헨션 재사용 |
| `any(m['email'] == str(payload.email) for m in store.members.values())` | 하나라도 같은 이메일이 있으면 참 | 중복 등록 409 처리 |
| `{key: value for key, value in record.items() if key != 'id'}` | id를 제외한 새 dict 만들기 | TaskCreate에 정의되지 않은 id를 빼고 재검증 |
| `global _next_id` | 함수 안에서 바깥의 번호 변수에 새 값을 대입하겠다는 선언 | `_next_id += 1`과 연결 |
| `_next_id += 1` | 다음 번호를 1 증가 | Day_1의 시도 횟수 누적과 같은 문법 |
| `del tasks[task_id]` | 해당 키와 값을 삭제 | 조회 성공 확인 후 삭제 |
| `members.clear()` | dict의 모든 항목 제거 | 예제 상태 초기화 함수 |
| `_next_id`, `_db` | 밑줄로 시작하는 작성자 지정 이름 | 밑줄 자체가 접근을 막지는 않음 |

| 파일 | 맡은 역할 | 연결 흐름 |
| --- | --- | --- |
| `models.py` | 데이터 항목과 검사 조건 정의 | app과 store가 가져다 사용 |
| `store.py` | 메모리 dict 저장·번호 부여 | 서버가 재시작되면 데이터가 사라짐 |
| `app.py` | 요청을 받아 검사·저장·응답 연결 | 모델 검사 → 존재 여부 확인 → 저장소 호출 → 응답 |

## 9. 연결해서 읽는 예제

아래는 원본의 핵심 흐름을 발췌한 설명입니다. 실행 결과를 새로 측정한 것은 아닙니다.

```python
class Book(BaseModel):
    title: str
    price: int
    in_stock: bool = True
    note: str | None = None

book = Book(title='파이썬기초', price='19000')
print(book.model_dump())
```

| 읽는 순서 | 해석 |
| --- | --- |
| `class Book(BaseModel)` | 책 데이터를 검사할 모델 정의 |
| `title: str`, `price: int` | 제목과 가격은 필수 |
| `= True`, `= None` | 재고 여부·메모를 생략하면 기본값 사용 |
| `Book(...)` | 주어진 값으로 책 모델 생성·검증; 가격 문자열은 기본 설정에서 정수로 변환 가능 |
| `book.model_dump()` | 검사된 모델을 dict로 꺼내 보기 |

```python
changes = patch.model_dump(exclude_unset=True)
updated = Profile.model_validate({**stored.model_dump(), **changes})
```

| 읽는 순서 | 해석 |
| --- | --- |
| `patch` | 바꾸겠다고 받은 데이터 |
| `exclude_unset=True` | 보내지 않은 항목은 변경 목록에서 제외 |
| `stored.model_dump()` | 기존 데이터를 dict로 꺼냄 |
| `{**기존, **변경}` | 기존 값 위에 변경값을 덮어 새 dict 생성 |
| `Profile.model_validate(...)` | 최종 Profile 조건에 맞는지 재검사 |
| `updated = ...` | 검사된 새 모델을 변수에 연결; 실제 저장소 반영은 별도 대입 필요 |

## 헷갈리기 쉬운 점

| 혼동하기 쉬운 것 | 정확한 구분 |
| --- | --- |
| `age: int`와 `age = 20` | 앞은 타입 안내, 뒤는 값 대입. Pydantic은 타입 안내를 읽어 검사 기능을 제공 |
| `str \| None`과 `= None` | None 허용과 입력 생략 시 기본값은 서로 다른 의미 |
| `Field(...)`가 있으면 선택 입력인가? | 기본값 없이 조건만 지정하면 여전히 필수 |
| `False`와 `None` | 미완료라는 값과 조건을 지정하지 않음은 다름. 검색은 `if done is not None` 사용 |
| `dict`와 JSON | dict는 Python 객체, JSON은 데이터를 주고받는 텍스트 형식 |
| `model_dump(mode='json')`와 `model_dump_json()` | 앞은 JSON에 맞는 값의 dict, 뒤는 JSON 문자열 |
| `Field`와 validator | 길이·범위 등 선언적 조건과 직접 작성한 검사·정리 함수 |
| 검사 함수 이름과 필드 이름 | 함수 이름은 지을 수 있지만 `@field_validator('tags')`의 tags는 실제 필드와 일치해야 함 |
| username 공백 제거 후 최소 길이 | 현재 ch04는 길이 검사 뒤 공백 제거. 정리된 값의 길이가 자동으로 다시 검사된다고 보면 안 됨 |
| `@property total` | 읽을 때 계산하는 속성. 현재 코드에서는 일반 모델 필드로 선언한 것이 아니므로 model_dump에 자동 포함된다고 보면 안 됨 |
| `**params`와 `{**a, **b}` | 앞은 함수 호출에 키워드 인자로 풀기, 뒤는 dict 구성에 풀기 |
| `__main__` 보호 범위 | 그 if 블록 안만 보호. 파일 맨 위 수준의 다른 코드는 import할 때도 실행 |

원본을 읽으면서 확인한 현재 상태도 구분합니다. 아래는 설명상 정정이며 Python 파일을 수정한 것은 아닙니다.

| 원본 위치 | 현재 상태·읽을 때 주의할 점 |
| --- | --- |
| ch02 `day6_1.py` | user2도 `NormalClass(...)`로 생성. Pydantic 예제로 오해하지 않기. ‘매개변수가 없는 생성자’라는 주석도 실제 name/age 인자 전달과 맞지 않음 |
| ch02 `day6_2.py` | 주석의 `Union[str.None]`은 올바른 표기가 아님. `Optional[str]`, `str \| None`, `Union[str, None]`으로 이해 |
| ch02 `day6_3.py` | `MemberOut(id=1)`의 MemberOut이 이 파일에 정의·import되어 있지 않아 실행 시 NameError 원인이 됨. 이를 import하는 main.py에도 영향 |
| ch03 `demo.py` | r은 정규식 전용 표시가 아니라 raw 문자열 표기. 현재 ‘오류확인’ 부분의 입력은 조건을 만족하므로 반드시 오류가 발생하는 예제는 아님 |
| ch03 `exercise.py` | 현재 빈 파일 |
| ch04·ch05·ch06 exercise, ch07 exercise_app, ch08 students_starter | TODO가 남은 시작용 코드. 정답·완성 app과 구분 |
| ch06 `TaskPatch` | 주석보다 실제 조건이 구체적임: title/done의 명시적 None은 거부하지만 due=None은 허용 |
| ch08 `StrictModel` | 설정은 추가 필드 거부·문자열 공백 제거. 모든 필드의 타입 변환을 막는 설정은 아님 |

## 후속 질문과 답변

2026-10-21 질문: “I want to see this in excel file.”

답변: 같은 정리 내용을 [Excel 파일](../outputs/01a15d8f-44a8-7bd0-995e-82d6bedbcc48/Day_6_코드_문법_정리.xlsx)로 변환했습니다. 181개 표 항목을 학습 안내, 주제별 정리, 연결 예제, 주의점 등 11개 시트에 나누고 코드 예제와 설명을 함께 담았습니다.

## 참고 자료

- 본문 각 표에 연결한 Day_6 원본 파일과 Day_1~Day_4 학습 파일.
- [기존 Field 기록](2026-10-21-pydantic-field.md), [검사기 기록](2026-10-21-pydantic-validator-error.md), [Enum 기록](2026-10-21-python-enum.md).
- [이전 경로 매개변수 기록](2026-10-20-fastapi-path-validation.md), [이전 검색·쿼리 기록](2026-10-20-fastapi-query-filter.md).
- [기존 Day_6 웹툰](2026-10-21-day6-webtoon.md): 같은 내용을 이야기 형식으로 복습할 때 사용.
- [Pydantic Validators](https://docs.pydantic.dev/latest/concepts/validators/).
- [Pydantic Serialization](https://docs.pydantic.dev/latest/concepts/serialization/).
- [FastAPI Response Model](https://fastapi.tiangolo.com/tutorial/response-model/).

이 문서는 코드 독해와 문서 확인에 기반한 정리입니다. 원본 Python 실행이나 API 요청 테스트를 수행한 결과 보고서는 아닙니다.
