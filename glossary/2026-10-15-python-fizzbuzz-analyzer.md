# Smart FizzBuzz Analyzer 만들기

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 답변 | [답변 보기](#답변) |
| 예제와 검증 | [예제 보기](#예제) |
| 헷갈리기 쉬운 점 | [주의점 보기](#헷갈리기-쉬운-점) |
| 문제 설명의 문법 오류 | [후속 질문과 답변](#후속-질문과-답변) |
| assert 검증 파이프라인 | [검증 단계와 실행법](#assert-검증-파이프라인) |

- 최초 기록일: 2026-10-15
- 수정일: 2026-10-15
- 분류: Python, Coding
- 핵심 용어: FizzBuzz, for, if, elif, else, 나머지 연산자, 딕셔너리

## 질문

별도 폴더에 `analyze_fizzbuzz(limit: int) -> dict` 함수를 작성하고 오류가 없는지 확인한다. 1부터 limit까지 순회하며 3과 5의 공배수는 FizzBuzz, 그 외 3의 배수는 Fizz, 그 외 5의 배수는 Buzz, 나머지는 Number로 센다. 반환 형식은 `{"FizzBuzz": int, "Fizz": int, "Buzz": int, "Number": int}`이다. limit가 1 미만이면 모든 카운트를 0으로 반환한다.

## 답변

[소스코드](../smart_fizzbuzz_analyzer/analyze_fizzbuzz.py)를 `smart_fizzbuzz_analyzer/` 폴더에 작성했다.

```python
def analyze_fizzbuzz(limit: int) -> dict:
    counts = {"FizzBuzz": 0, "Fizz": 0, "Buzz": 0, "Number": 0}

    if limit < 1:
        return counts

    for i in range(1, limit + 1):
        if i % 3 == 0 and i % 5 == 0:
            counts["FizzBuzz"] += 1
        elif i % 3 == 0:
            counts["Fizz"] += 1
        elif i % 5 == 0:
            counts["Buzz"] += 1
        else:
            counts["Number"] += 1

    return counts
```

## 예제

프로젝트 폴더에서 실행한다. 이 환경에서는 앞서 `py`가 설치된 Python을 찾지 못해 `python`을 사용했다.

```powershell
python smart_fizzbuzz_analyzer/analyze_fizzbuzz.py
```

15를 입력해 실제 확인한 반환값:

```text
{'FizzBuzz': 1, 'Fizz': 4, 'Buzz': 2, 'Number': 8}
```

- FizzBuzz: 15 (1개)
- Fizz: 3, 6, 9, 12 (4개)
- Buzz: 5, 10 (2개)
- Number: 1, 2, 4, 7, 8, 11, 13, 14 (8개)

`python -m py_compile smart_fizzbuzz_analyzer/analyze_fizzbuzz.py` 문법 검사를 통과했다. -5, 0, 1, 3, 5, 15, 30의 7가지 입력에 대해 예상 딕셔너리와 일치함을 확인했다. 각 입력에서 전체 카운트의 합이 `max(limit, 0)`인지도 검증했다. 30의 실제 결과는 `{'FizzBuzz': 2, 'Fizz': 8, 'Buzz': 4, 'Number': 16}`이다.

## 헷갈리기 쉬운 점

- 15는 3과 5 모두의 배수이므로 공배수 조건을 먼저 확인해야 한다.
- `if`, `elif`, `else`를 사용하면 한 숫자는 한 분류에만 포함된다. 독립적인 if 문으로 각각 세면 중복 집계할 수 있다.
- `range(1, limit + 1)`에서 끝값은 포함되지 않으므로 limit까지 확인하려면 1을 더한다.
- `limit: int`와 `-> dict`는 입력과 반환 타입을 알려주는 힌트다. 타입 힌트 자체가 입력값을 정수로 변환하지는 않는다.

## 후속 질문과 답변

### 2026-10-15 문제 설명을 붙여 넣은 뒤 SyntaxError 발생

질문: 파일의 `[Mission 1: Smart FizzBuzz Analyzer]` 줄에서 `SyntaxError: invalid syntax. Perhaps you forgot a comma?`가 발생하는 이유는 무엇인가?

답변: 파일 상단에 문제 설명을 주석 없이 붙여 넣어서 파이썬이 설명을 코드로 해석했기 때문이다. `[Mission 1: Smart FizzBuzz Analyzer]`는 올바른 파이썬 코드가 아니다. 오류 메시지의 쉼표 안내는 추측이며, 여기서는 쉼표를 추가하는 것으로 해결되지 않는다.

설명을 유지하려면 각 줄 앞에 `#`을 붙여 주석으로 만든다.

```python
# [Mission 1: Smart FizzBuzz Analyzer]
# 함수명: analyze_fizzbuzz(limit: int) -> dict
```

원래 설명 위아래의 `...`는 여러 줄 주석을 만드는 문법이 아니다. `...` 자체는 파이썬의 Ellipsis 값이며 그 사이 내용을 주석 처리하지 않는다.

소스코드의 문제 설명 전체를 `#` 주석으로 바꾸고 불필요한 `...`를 제거했다. 수정 후 `python -m py_compile smart_fizzbuzz_analyzer/analyze_fizzbuzz.py` 검사를 통과했고, 직접 실행하여 15를 입력했을 때 `{'FizzBuzz': 1, 'Fizz': 4, 'Buzz': 2, 'Number': 8}`을 확인했다.

### assert 검증 파이프라인

질문(2026-10-15): Mission 1의 기능을 정확히 읽고, 다양하게 검증할 수 있도록 assert 키워드로 검증 파이프라인까지 작성해 달라.

답변: [검증 파일](../smart_fizzbuzz_analyzer/test_analyze_fizzbuzz.py)에 `run_validation()`을 작성했다. 기존 함수는 1부터 limit까지 순회하며 공배수 조건을 먼저 확인하고 `elif`로 분류하므로 요구한 로직에 맞는다. 검증은 다음 순서로 진행한다.

1. 직접 계산한 예상값 13개: 음수, 0, 1, 첫 Fizz/Buzz, 15 직전·당일·직후, 여러 공배수, 100, 1000을 확인한다.
2. -10부터 300까지 311개 입력: 딕셔너리 반환, 정확한 키 4개, 값이 음이 아닌 정수인지, 전체 합이 `max(limit, 0)`인지 확인한다. `type(value) is int`로 bool이 정수처럼 통과하는 것도 방지한다.
3. 1부터 300까지와 999, 1000, 10000의 303개 입력: 배수의 개수 공식으로 결과를 교차 검증한다. 예를 들어 Fizz는 `limit // 3 - limit // 15`이다. 함수와 같은 반복문을 복제하지 않아 예상값까지 같은 실수를 할 가능성을 줄인다.
4. 0과 15의 반복 호출: 결과가 같고 반환 딕셔너리가 서로 독립적인지, 이전 반환값 수정이 다음 호출에 영향을 주지 않는지 확인한다.

`assert 조건, 메시지`는 조건이 거짓일 때 `AssertionError`를 발생시키고 실행을 멈춘다. 이 검증 파일은 실패한 입력과 예상값·실제값 또는 실패 이유를 표시하며, 단계별로 성공 메시지를 출력한다. 문자열·실수 입력의 처리 방식은 Mission 1에서 정하지 않았으므로 정수 입력을 검증 범위로 삼았다.

프로젝트 폴더에서 문법 검사와 검증을 실행한다.

```powershell
python -m py_compile smart_fizzbuzz_analyzer/analyze_fizzbuzz.py smart_fizzbuzz_analyzer/test_analyze_fizzbuzz.py
python smart_fizzbuzz_analyzer/test_analyze_fizzbuzz.py
```

`assert`는 `python -O` 최적화 모드에서는 생략되므로 검증 시에는 `-O` 없이 실행한다. 실제 확인할 때는 한글 출력 인코딩을 명확히 하기 위해 `python -X utf8 smart_fizzbuzz_analyzer/test_analyze_fizzbuzz.py`로 실행했다. 두 파일의 문법 검사와 검증 4단계가 모두 통과했으며 최종 출력은 다음과 같았다.

```text
1단계 통과: 대표 입력 13개
2단계 통과: -10~300의 반환 형식과 전체 카운트
3단계 통과: 공식으로 303개 입력 교차 검증
4단계 통과: 반복 호출과 반환값 독립성
Mission 1: 모든 검증을 통과했습니다.
```
