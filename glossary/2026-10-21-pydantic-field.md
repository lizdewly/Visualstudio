# Pydantic Field로 입력 조건 정하기

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 답변 | [답변 보기](#답변) |
| 예제 | [예제 보기](#예제) |
| 헷갈리기 쉬운 점 | [주의점 보기](#헷갈리기-쉬운-점) |
| Literal 후속 질문 | [질문과 답변](#literal-후속-질문) |

- 최초 기록일: 2026-10-21
- 수정일: 2026-10-21
- 분류: Python, Coding
- 핵심 용어: Pydantic, Field, 입력 검증, ge, le, pattern

## 질문

`Day_6/ch03_field/demo.py`에서 `Field`를 통해 무엇을 배우고 있나요?

## 답변

회원 가입 데이터에 허용할 값의 조건을 정하고, Pydantic으로 입력을 검증하는 방법을 배우고 있습니다. 필드란 `name`, `age` 같은 데이터 항목입니다. `Field()`는 항목에 범위, 길이, 패턴 같은 조건이나 설명을 붙이는 함수입니다.

| 현재 코드 | 의미 |
| --- | --- |
| `name: str = Field(min_length=2, max_length=20, description='실명')` | 이름은 문자열이고 길이는 2~20자. '실명'은 설명일 뿐 실제 실명 여부는 검사하지 않음 |
| `age: int = Field(ge=14, le=100)` | 나이는 정수이며 14 이상, 100 이하 |
| `code: str = Field(pattern=...)` | 코드 문자열이 정규 표현식 조건을 만족하는지 검사 |

`ge`는 greater than or equal(이상), `le`는 less than or equal(이하)의 약자입니다. 모델에 전달한 입력이 조건을 만족하지 않으면 `ValidationError`가 발생합니다.

주변 코드에서는 `EmailStr`로 이메일 형식 검사, `Literal['basic', 'premium']`으로 허용 값 제한, `str_strip_whitespace=True`로 문자열 양끝 공백 제거, `extra='forbid'`로 정의하지 않은 추가 항목 거부도 배우고 있습니다.

## 예제

```python
from pydantic import BaseModel, Field, ValidationError

class Person(BaseModel):
    age: int = Field(ge=14, le=100)

try:
    person = Person(age=13)
except ValidationError as error:
    print(error)
```

예상 동작(실행하지 않은 설명용 예제): 13은 최소 나이 14보다 작으므로 검증 오류를 잡아 출력합니다.

## 헷갈리기 쉬운 점

- 확인 당시 파일의 `Field(pattern=r)`는 미완성입니다. `r`만 쓰면 변수 이름으로 해석되며, 정의되어 있지 않으면 `NameError`가 발생합니다. 예를 들어 `Field(pattern=r'^[A-Z]{3}$')`는 영문 대문자 3글자라는 조건을 표현합니다. 이는 설명용 예시이며 원래 의도한 코드 규칙은 확인되지 않았습니다.
- `Field(ge=14, le=100)`에는 기본값이 없으므로 나이는 여전히 필수입니다.
- 범위 검증과 엄격한 타입 검사는 다릅니다. 기본 설정에서는 Pydantic이 변환 가능한 입력을 변환할 수 있습니다. 엄격한 타입 검사는 `strict=True` 같은 별도 설정을 사용합니다.

## Literal 후속 질문

2026-10-21 질문: `Literal`은 무엇인가요?

`Literal`은 허용할 구체적인 값을 나열하는 타입 힌트입니다. `from typing import Literal`로 가져옵니다.

```python
level: Literal['basic', 'premium'] = 'basic'
```

- `level`: 회원 등급을 저장하는 항목입니다.
- `Literal['basic', 'premium']`: 허용하는 값은 두 문자열 중 하나입니다.
- `= 'basic'`: 입력을 생략했을 때 사용할 기본값입니다.

현재 Pydantic 모델에 다른 필수 항목을 올바르게 입력했다고 가정하면, `level='basic'`과 `level='premium'`은 허용되지만 `level='vip'`나 `level='Basic'`은 `ValidationError`를 발생시킵니다. 대소문자를 구분합니다. 이는 설명용 예시이며 실행 결과를 기록한 것은 아닙니다.

`str`은 문자열이라는 타입을 나타내고, `Literal`은 특정 값들로 선택지를 제한합니다. `Field`는 길이나 범위 같은 조건을 붙이는 데 쓰입니다.

일반 파이썬의 타입 힌트만으로는 실행 중 잘못된 값의 대입을 막지 않습니다. 현재 코드에서는 Pydantic이 모델 생성 시 이 정보를 읽고 실제 입력을 검사합니다.

파일 상태 갱신: 같은 날 다시 확인한 `code` 필드는 `Field(pattern=r'^STU-[0-9]{4}$')`로 완성되어 있습니다. 위의 미완성 설명은 이전 확인 시점의 기록입니다.

## 참고 자료

- [현재 학습 파일](../Day_6/ch03_field/demo.py)
- [Pydantic 공식 문서: Fields](https://docs.pydantic.dev/latest/concepts/fields/)
- [Python 공식 문서: Literal](https://docs.python.org/3/library/typing.html#typing.Literal)
