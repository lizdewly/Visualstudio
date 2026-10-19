# 1부터 n까지 짝수의 합과 개수 구하기

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 답변 | [답변 보기](#답변) |
| 예제 | [예제 보기](#예제) |
| 소스코드 작성과 검증 | [후속 질문과 답변](#후속-질문과-답변) |
| JSON 출력과의 차이 | [json.dumps 설명](#json-dumps-출력과의-차이) |
| assert 실패 원인 | [검증값 정정](#assert-실패와-검증값-정정) |
| 문제 설명의 문법 오류 | [주석 처리](#문제-설명의-syntaxerror) |

- 최초 기록일: 2026-10-15
- 수정일: 2026-10-15
- 분류: Python, Coding
- 핵심 용어: for, if, range, 나머지 연산자, 누적 합, 개수, 딕셔너리

## 질문

1부터 정수 n까지 짝수들의 합과 총 개수를 계산하는 `calculate_even_sum_and_count(n)` 함수를 작성한다. n이 1 미만이면 합과 개수 모두 0을 반환한다. for 문과 if 문을 사용하고 `i % 2 == 0`으로 짝수를 판단한다. 반환 형식은 `{"Sum": int, "Count": int}`이다.

## 답변

```python
def calculate_even_sum_and_count(n):
    total = 0
    count = 0

    if n < 1:
        return {"Sum": 0, "Count": 0}

    for i in range(1, n + 1):
        if i % 2 == 0:
            total += i
            count += 1

    return {"Sum": total, "Count": count}
```

- `range(1, n + 1)`은 1부터 n까지 순서대로 반복한다. 끝값은 포함하지 않으므로 `n + 1`을 쓴다.
- `i % 2 == 0`은 i를 2로 나눈 나머지가 0인지 검사한다.
- 짝수일 때 `total`에는 i를 더하고 `count`에는 1을 더한다.
- 마지막 `return`은 반복문 밖에 두어 모든 수를 확인한 뒤 딕셔너리를 반환한다.

## 예제

```python
print(calculate_even_sum_and_count(10))
```

Python으로 실제 실행해 확인한 결과:

```text
{'Sum': 30, 'Count': 5}
```

짝수 2, 4, 6, 8, 10의 합은 30이고 개수는 5이다. 추가로 -3, 0, 1은 모두 합 0과 개수 0, 2는 합 2와 개수 1, 9는 합 20과 개수 4를 반환함을 실행해 확인했다.

## 후속 질문과 답변

### 2026-10-15 별도 폴더에 소스코드를 작성하고 오류 확인하기

질문: 같은 문제를 별도의 폴더에 소스코드로 작성한 뒤 오류가 없는지 확인할 것.

답변: `even_sum_and_count/` 폴더에 [소스코드](../even_sum_and_count/calculate_even_sum_and_count.py)를 작성했다. 직접 실행하면 정수 n을 입력받아 결과 딕셔너리를 출력한다. 다른 파일에서 함수를 가져오면 입력문은 실행되지 않는다.

Windows 실행 명령:

```powershell
python even_sum_and_count/calculate_even_sum_and_count.py
```

이 환경에서는 앞서 `py`로 설치된 Python을 찾지 못했으므로 `python`을 사용했다. `python -m py_compile even_sum_and_count/calculate_even_sum_and_count.py` 문법 검사를 통과했다. 직접 실행해 10을 입력했을 때 `{'Sum': 30, 'Count': 5}`를 확인했다. -3, 0, 1, 2, 9, 10에 대해서도 반환값을 예상 딕셔너리와 비교했으며 모두 일치했다. 문제에서 지정한 정수 입력을 기준으로 확인했다.

### JSON dumps 출력과의 차이

질문(2026-10-15): 마지막의 print를 `print(jason.dumps(calculate_even_sum_and_count(n))`로 쓰면 어떤 차이가 있는가?

답변: 파이썬 딕셔너리를 그대로 표시하는 것과, JSON 형식의 문자열로 변환한 뒤 표시하는 것의 차이다. 모듈 이름은 `jason`이 아니라 `json`이며 맨 끝 닫는 괄호도 하나 더 필요하다. `json`은 파이썬 기본 제공 모듈이므로 별도 설치 없이 `import json`으로 사용한다.

```python
import json

n = 10
print(calculate_even_sum_and_count(n))
print(json.dumps(calculate_even_sum_and_count(n)))
```

실제 실행 결과:

```text
{'Sum': 30, 'Count': 5}
{"Sum": 30, "Count": 5}
```

함수는 두 경우 모두 `dict`를 반환한다. `json.dumps()`가 이 반환값을 JSON 문자열(`str`)로 변환하며, 합과 개수를 계산하는 방식은 바뀌지 않는다. 이 예제에서는 키의 따옴표가 눈에 띄는 차이지만, JSON 변환은 단순히 따옴표를 바꾸는 기능이 아니다. 예를 들어 파이썬의 `True`, `None`도 JSON에서는 `true`, `null`로 표현한다. 함수의 반환값만 요구하면 딕셔너리를 반환하면 되고, 출력 텍스트를 JSON 형식으로 요구하면 `json.dumps()`를 사용한다. 기존 소스코드는 이 설명 질문으로 변경하지 않았다.

### assert 실패와 검증값 정정

질문(2026-10-15): `assert calculate_even_sum_and_count(100) == {"Sum": 2250, "Count": 50}, 'Test 1 Failed'`에서 Traceback이 발생하는 이유는 무엇인가?

답변: 함수의 실제 반환값과 테스트에 적은 예상값이 달라서 발생한다. `assert 조건, 메시지`는 조건이 거짓이면 `AssertionError`를 발생시키고 메시지를 표시한다.

1부터 100까지의 짝수는 2, 4, ..., 100으로 총 50개이다. 합은 `(2 + 100) * 50 // 2 = 2550`이다. 따라서 함수의 합 계산은 맞고, 테스트의 예상 합 2250이 잘못되었다.

정정: 소스코드의 첫 번째 테스트에서 예상 합을 2250에서 2550으로 수정했다.

```python
assert calculate_even_sum_and_count(100) == {"Sum": 2550, "Count": 50}, 'Test 1 Failed'
```

수정 후 `python -m py_compile even_sum_and_count/calculate_even_sum_and_count.py` 문법 검사와 파일 실행이 모두 성공했다. 파일에 있던 세 assert(100, 1, -5)가 모두 통과했고, 함수를 별도로 호출해 실제 반환값 `{'Sum': 2550, 'Count': 50}`도 확인했다.

### 문제 설명의 SyntaxError

질문(2026-10-15): `Day_2_pm/day2_1.py`의 `[Problem] 1부터 n까지의 정수 중 짝수들의 합과 짝수의 총 개수를 계산한다.` 줄에서 `SyntaxError: invalid syntax`가 발생했다.

답변: 문제 설명이 주석 없이 들어 있어 파이썬이 실행할 코드로 해석했기 때문이다. 설명은 각 줄 앞에 `#`을 붙여 주석으로 작성한다. `...`는 여러 줄 주석을 만드는 문법이 아니므로 설명 위아래에 넣어도 설명이 주석 처리되지 않는다.

```python
# [Problem] 1부터 n까지의 정수 중 짝수들의 합과 짝수의 총 개수를 계산한다.
# [Function] calculate_even_sum_and_count(n)
```

[해당 파일](../Day_2_pm/day2_1.py)의 문제 설명 전체를 주석으로 바꾸고 설명 위아래의 불필요한 `...`를 제거했다. `python -m py_compile Day_2_pm/day2_1.py` 문법 검사를 통과했고, 직접 실행한 결과는 `range(0, 5)`였다. 이는 파일에 있는 `print(range(5))`의 출력이며, 이 파일에는 짝수 합 계산 함수 구현은 없다. 짝수 합 함수는 별도의 `even_sum_and_count/calculate_even_sum_and_count.py`에 있다.
