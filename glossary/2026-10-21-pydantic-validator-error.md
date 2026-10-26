# field_validator의 필드 이름 오류 해결

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 답변 | [답변 보기](#답변) |
| 실행 확인 | [실행 확인](#실행-확인) |
| 세 데코레이터 사용법 | [후속 질문](#세-데코레이터-사용법) |

- 최초 기록일: 2026-10-21
- 수정일: 2026-10-21
- 분류: Python, Coding
- 핵심 용어: field_validator, PydanticUserError, tags, 들여쓰기

## 질문

`Signup.parse_tags`에서 `PydanticUserError: Decorators defined with incorrect fields`가 발생하는 문제를 어떻게 고치나요?

## 답변

모델에는 `tags`라는 필드가 있지만 검사기는 `@field_validator('tag', mode='before')`로 존재하지 않는 `tag`를 지정했습니다. 검사기의 문자열은 실제 필드 이름과 정확히 일치해야 합니다.

```python
@field_validator('tags', mode='before')
```

`mode='before'`는 필드의 타입 검증 전에 실행한다는 뜻입니다. 여기서는 쉼표로 구분한 문자열을 문자열 리스트로 바꾼 뒤 `list[str]` 검증을 받도록 합니다.

오류 메시지의 `check_fields=False`는 상속받을 모델에서 필드를 정의하는 등의 상황을 위한 옵션입니다. 이번 문제는 오타이므로 이름을 바로잡습니다. 이 오류는 모델 정의 문제인 `PydanticUserError`이며, 잘못된 입력 때문에 발생하는 `ValidationError`와 구분합니다.

함께 수정한 문제:

- `if '' in text:`는 모든 문자열에서 참이므로 정상 아이디도 거부했습니다. `if ' ' in text:`로 바꾸어 일반 공백 문자를 검사합니다. 탭 등 모든 종류의 공백을 검사하는 조건은 아닙니다.
- `main()`과 실행 진입점이 `Reservation` 클래스 내부에 들여쓰기되어 있었습니다. 클래스 정의 중 `main()`이 호출되면 아직 정의가 끝나지 않은 `Reservation`을 참조하게 되므로 둘 다 클래스 밖으로 옮겼습니다.
- `start > end`에 맞게 오류 문구를 '종료일은 시작일보다 빠를 수 없습니다.'로 바로잡았습니다.

## 실행 확인

`py -m py_compile Day_6/ch04_validator/demo.py`가 통과했습니다. `py` 및 사용자의 traceback에 나타난 `simple_calculator/.venv/Scripts/python.exe`로 각각 실행하여 정상 종료를 확인했습니다.

- 아이디 전처리 결과: `student01`
- 태그 전처리 결과: `['python', 'api']`
- 시작일 2026-10-21, 종료일 2026-10-22인 예약 생성 성공
- 비밀번호 불일치 예제에서 `value_error`를 잡아 출력

## 세 데코레이터 사용법

2026-10-21 후속 질문: `field_validator`, `classmethod`, `model_validator`의 사용을 쉽게 알려주세요.

`@...`는 함수에 역할을 붙이는 데코레이터 문법입니다. `Signup(...)`으로 데이터를 만들면 Pydantic이 등록된 검사기를 호출하므로 검사 함수를 일일이 직접 부를 필요가 없습니다.

| 표현 | 역할 | 현재 예제 |
| --- | --- | --- |
| `@field_validator('필드명')` | 지정한 필드의 값을 검사하거나 변환 | 아이디 정리, 태그 문자열을 리스트로 변환 |
| `@classmethod` | 메서드가 첫 인자로 클래스 자체인 `cls`를 받도록 지정 | `cls`는 여기서 `Signup` 클래스 |
| `@model_validator(mode='after')` | 필드 검증을 통과한 모델 전체를 검사 | 비밀번호 일치 여부, 예약 날짜 순서 |

현재 코드에서 발췌한 예:

```python
@field_validator('username')
@classmethod
def normal_username(cls, value: str) -> str:
    text = value.strip().lower()
    if ' ' in text:
        raise ValueError('아이디에는 공백을 사용할 수 없습니다.')
    return text
```

`value`는 검사할 아이디입니다. 양끝 공백을 제거하고 소문자로 만든 뒤, 중간에 일반 공백이 있으면 거부합니다. 반환한 `text`가 필드 값으로 사용됩니다. `classmethod`는 파이썬 기본 기능이며 그 자체로 입력을 검사하지 않습니다. 현재처럼 `field_validator` 바로 아래에 붙입니다. `cls`를 함수 본문에서 사용하지 않아도 이 형태로 작성할 수 있습니다.

`field_validator`의 기본 모드는 `after`입니다. 현재 `username`은 문자열 및 최소 길이 검사를 먼저 통과한 뒤 위 함수가 실행됩니다. 따라서 공백 제거 후 길이까지 보장하려면 별도 설계가 필요합니다. 반면 `tags`의 `mode='before'`는 원래 입력을 먼저 받아 `list[str]` 검사 전에 문자열을 리스트로 바꿉니다.

```python
@model_validator(mode='after')
def verify_password(self) -> 'Signup':
    if self.password != self.password_confirm:
        raise ValueError('비밀번호가 일치하지 않습니다.')
    return self
```

`self`는 검사 중인 개별 가입 객체입니다. 두 필드의 값을 함께 비교할 수 있습니다. 이 `after` 모델 검사기에는 `classmethod`를 붙이지 않으며, 성공하면 `self`를 반환합니다.

현재 tags 흐름: 원본 문자열 → before 검사기로 리스트 변환 → `list[str]` 검사 → 나머지 필드도 성공하면 after 모델 검사 → 생성 완료.

검사기에서 `ValueError`를 발생시키면 Pydantic이 `ValidationError`로 모아 전달합니다. 필드 검사기는 사용할 값을 반환하고, 여기서 사용한 after 모델 검사기는 객체 자신을 반환한다는 차이를 기억합니다. 이 설명을 위해 Python 코드는 변경하지 않았습니다.

## 참고 자료

- [수정한 학습 코드](../Day_6/ch04_validator/demo.py)
- [Pydantic 공식 문서: Decorator on missing field](https://docs.pydantic.dev/latest/errors/usage_errors/#decorator-on-missing-field)
- [Pydantic 공식 문서: Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [Python 공식 문서: classmethod](https://docs.python.org/3/library/functions.html#classmethod)
