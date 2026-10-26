# Enum과 Literal의 차이

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 답변 | [답변 보기](#답변) |
| 예제 | [예제 보기](#예제) |
| 헷갈리기 쉬운 점 | [주의점 보기](#헷갈리기-쉬운-점) |

- 최초 기록일: 2026-10-21
- 수정일: 2026-10-21
- 분류: Python, Coding
- 핵심 용어: Enum, 열거형, Literal, name, value

## 질문

`Enum`은 무엇인가요?

## 답변

`Enum`은 enumeration의 줄임말로, 한국어로 열거형이라고 합니다. 정해진 선택지에 이름을 붙여 하나의 타입으로 묶습니다. 회원 등급, 주문 상태, 요일 등을 표현할 때 사용합니다.

`Literal['basic', 'premium']`은 허용할 값을 타입 힌트에 나열합니다. `Enum`은 `Level.BASIC`처럼 이름이 있는 멤버를 정의하여 여러 곳에서 재사용할 수 있습니다. Literal도 타입 별칭으로 재사용할 수 있으므로 재사용 가능 여부만으로 둘을 구분하지는 않습니다.

## 예제

```python
from enum import Enum

class Level(Enum):
    BASIC = 'basic'
    PREMIUM = 'premium'

level = Level.BASIC
print(level.name)
print(level.value)

if level == Level.BASIC:
    print('기본 회원입니다.')
```

예상 출력(실행하지 않은 설명용 예제):

```text
BASIC
basic
기본 회원입니다.
```

`Level`은 타입 이름, `Level.BASIC`은 멤버, `BASIC`은 멤버 이름, `'basic'`은 멤버의 값입니다. `Level('basic')`으로 값에 해당하는 멤버를 찾을 수 있습니다. 정의되지 않은 값으로 `Level('vip')`를 호출하면 `ValueError`가 발생합니다.

## 헷갈리기 쉬운 점

- 위처럼 일반 `Enum`을 사용하면 `Level.BASIC`과 문자열 `'basic'`은 같지 않습니다. 문자열 값이 필요하면 `.value`를 사용합니다.
- `level: Level` 같은 일반 파이썬 타입 힌트만으로 모든 대입을 실행 중 검사하는 것은 아닙니다.
- `Enum`은 파이썬 표준 라이브러리 기능으로 별도 설치가 필요 없습니다.

## 참고 자료

- [Python 공식 문서: enum](https://docs.python.org/3/library/enum.html)
