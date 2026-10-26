# Pydantic Field로 입력 조건 정하기

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 답변 | [답변 보기](#답변) |
| 예제 | [예제 보기](#예제) |
| 헷갈리기 쉬운 점 | [주의점 보기](#헷갈리기-쉬운-점) |
| Literal 후속 질문 | [질문과 답변](#literal-후속-질문) |
| 수량 0 테스트 실패 | [201과 422의 차이](#수량-0-테스트-실패) |
| admin 추가 항목 테스트 | [요청과 예상 오류 필드](#admin-추가-항목-테스트) |

- 최초 기록일: 2026-10-21
- 수정일: 2026-10-23
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

## 수량 0 테스트 실패

2026-10-23 질문: `test_order_invalid[body0-quantity]`에서 수량 0을 보냈는데 `assert 201 == 422`로 실패하는 이유는 무엇인가요?

현재 `Day8/lesson_03_body_validation/main.py`에는 다음 조건이 있습니다.

```python
quantity: int = Field(ge=0, le=5, strict=True)
```

`ge=0`은 0 이상을 허용한다는 뜻입니다. 따라서 정수 0은 검증을 통과합니다. 요청 처리 함수가 실행되고, `@app.post(..., status_code=201)` 설정에 따라 성공 상태 201을 반환합니다. 반면 테스트는 수량 0이 잘못된 입력이라서 422가 나와야 한다고 기대합니다.

`assert response.status_code == 422`는 응답을 422로 바꾸는 명령이 아닙니다. 실제 응답과 기대값을 비교합니다. 사용자가 제공한 로그에서 실제 값은 201이므로 `201 == 422`가 거짓이 되어 AssertionError가 발생했습니다.

수량을 1~5로 제한하려면 `ge=0`을 `ge=1`로 바꿉니다.

```python
quantity: int = Field(ge=1, le=5, strict=True)
```

그러면 수량 0은 입력 검증에서 거부되어 기본적으로 422가 반환됩니다. `strict=True`는 엄격한 타입 검사이며, 0을 금지하는 범위 조건은 아닙니다. `body0-quantity`는 이 매개변수화 테스트의 첫 번째 입력과 예상 오류 필드 quantity를 나타냅니다. 이번 답변에서는 원인과 수정 방법을 설명했으며 코드를 변경하거나 테스트를 재실행하지 않았습니다. 실제 201 응답의 근거는 사용자가 제공한 실행 로그입니다.

참고한 파일: [주문 API](../Day8/lesson_03_body_validation/main.py), [API 테스트](../Day8/lesson_03_body_validation/test_api.py).

## admin 추가 항목 테스트

2026-10-23 질문: `({"name": "tea", "quantity": 1, "admin": True}, "admin"),` 부분을 더 설명해 주세요.

이 줄은 테스트 사례 하나이며, 두 값을 묶은 튜플입니다. `@pytest.mark.parametrize("body, field", [...])`에 의해 첫 번째 값인 딕셔너리는 body로, 두 번째 값인 문자열은 field로 전달됩니다.

```python
body = {"name": "tea", "quantity": 1, "admin": True}
field = "admin"
```

body는 API에 보낼 요청 데이터이고, field는 오류가 발생할 것으로 예상하는 항목 이름입니다. 딕셔너리 안의 `"admin": True`는 일부러 추가한 입력입니다. 바깥의 `"admin"`은 테스트에서 비교할 기대값이며 서버에 별도로 보내지 않습니다. 마지막 쉼표는 테스트 목록에서 항목을 구분합니다.

현재 OrderIn 모델에는 name과 quantity만 정의되어 있고 `ConfigDict(extra="forbid")`가 있습니다. 이는 모델에 정의하지 않은 추가 항목을 금지한다는 뜻이므로 admin이 포함된 요청은 거부되어야 합니다. True라서 거부하는 것이 아니므로 False로 바꾸어도 추가 항목인 점은 같습니다. admin이라는 이름 자체에 특별한 기능은 없으며 관리자 권한을 부여하는 코드도 아닙니다.

```python
response = client.post("/orders", json=body)
assert response.status_code == 422
assert response.json()["detail"][0]["loc"] == ["body", "admin"]
```

첫 검사는 잘못된 입력으로 거부되었는지, 다음 검사는 첫 번째 오류 위치가 요청 본문의 admin인지 확인합니다. `detail`은 오류 목록, `[0]`은 첫 번째 오류, `loc`는 오류 위치입니다. 의도대로 요청이 거부되면 테스트는 성공합니다. 위 응답 조건은 코드에서 읽은 기대값이며 이번 답변에서 실행하지 않았습니다.

### 2026-10-23: 예상대로 거부되어 테스트가 성공한 것인가요?

질문: “그럼 이 요청을 예상대로 거부되어서 테스트가 성공한것인가?”

네. 이번에는 현재 앱에 TestClient로 `{"name": "tea", "quantity": 1, "admin": True}`를 직접 보내 확인했습니다. 실제 상태는 422였고, 첫 번째 오류의 type은 `extra_forbidden`, loc는 `["body", "admin"]`이었습니다. 기존 테스트의 두 assert를 직접 실행했고 모두 통과했습니다. pytest 전체 실행 결과는 아닙니다.

이 테스트의 목표는 주문 성공이 아니라 잘못된 요청을 정확히 거부하는지 확인하는 것입니다. 따라서 요청 거부는 예상한 동작이며 테스트 성공입니다. 앞서 사용자가 보여 준 `quantity=0`의 실패는 별도 사례로, 그 요청은 거부되어야 하는데 201로 허용되어 테스트가 실패했습니다.

### 2026-10-23: quantity=0이 허용된 이유는 ge=0인가요?

질문: “그럼 quantity=0 테스트는 거부해야 하는데 허용이 된 이유는 main.py 파일에 코드가 ge=0으로 되어 있어서요?”

네, 정확합니다. 앞서 확인한 main.py의 `Field(ge=0, le=5, strict=True)`는 정수 0부터 5까지 허용합니다. ge는 경계값을 포함하는 ‘이상’이므로 0도 통과합니다. 테스트는 1~5만 허용하는 요구사항을 기준으로 0을 거부할 것으로 기대하기 때문에 코드와 기대가 달라 실패했습니다. `ge=1`로 바꾸면 0이 최소값보다 작아 검증에서 거부됩니다. 이번 답변에서는 코드를 변경하거나 테스트를 재실행하지 않았습니다.

## 참고 자료

- [현재 학습 파일](../Day_6/ch03_field/demo.py)
- [Pydantic 공식 문서: Fields](https://docs.pydantic.dev/latest/concepts/fields/)
- [Python 공식 문서: Literal](https://docs.python.org/3/library/typing.html#typing.Literal)
