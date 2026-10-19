# ValueError와 KeyError의 차이

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 답변 | [답변 보기](#답변) |
| 예제 | [예제 보기](#예제) |
| 헷갈리기 쉬운 점 | [주의점 보기](#헷갈리기-쉬운-점) |

- 최초 기록일: 2026-10-16
- 수정일: 2026-10-16
- 분류: Python, Coding
- 핵심 용어: ValueError, KeyError, 예외, dict, int, get

## 질문

ValueError와 KeyError의 차이는 무엇인가? 사용자 입력의 `KeyErrror`는 `KeyError`를 뜻한다.

## 답변

`ValueError`는 인자의 타입은 받아들일 수 있지만 값이 해당 연산에 적절하지 않을 때 발생한다. 예를 들어 `int()`는 문자열을 받을 수 있지만 `"abc"`는 정수로 해석할 수 없다.

`KeyError`는 대표적으로 딕셔너리에서 존재하지 않는 키를 대괄호로 조회할 때 발생한다.

| 오류 | 원인 | 대표 예 |
| --- | --- | --- |
| ValueError | 처리할 수 없는 값 | `int("abc")` |
| KeyError | 존재하지 않는 키 | `{"name": "Kim"}["age"]` |

## 예제

아래 코드는 각각 별도로 실행하는 예제다.

```python
int("abc")
```

예외를 잡아 타입과 메시지를 출력해 실제 확인한 결과:

```text
ValueError: invalid literal for int() with base 10: 'abc'
```

```python
user = {"name": "Kim"}
print(user["age"])
```

같은 방법으로 실제 확인한 결과:

```text
KeyError: 'age'
```

숫자 변환 실패는 `try`와 `except ValueError`로 처리할 수 있다. 없는 키가 정상적으로 생길 수 있는 상황에서는 `user.get("age", 0)`처럼 기본값을 지정할 수 있다. 이때 get은 딕셔너리에 키를 추가하지 않는다.

## 헷갈리기 쉬운 점

- 정확한 철자는 `KeyError`이다.
- ValueError가 모든 값 관련 오류를 의미하지는 않는다. 예를 들어 `int(None)`은 타입이 적절하지 않아 TypeError가 발생한다.
- KeyError가 딕셔너리에만 한정되지는 않는다. 예를 들어 집합의 `remove()`도 없는 원소를 삭제하려 하면 KeyError를 발생시킨다.
- 기존 학습의 [딕셔너리 설명](2026-10-15-python-dictionary.md)과 [pop 설명](2026-10-15-python-pop.md)에도 관련 사례가 있다.
