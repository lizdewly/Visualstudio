# 리스트 컴프리헨션 사용법

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 기본 문법 | [답변 보기](#답변) |
| 반복문 비교와 조건 사용 | [예제 보기](#예제) |
| 조건 위치와 주의점 | [주의점 보기](#헷갈리기-쉬운-점) |
| 메뉴 예제 오류 수정 | [후속 질문 보기](#후속-질문과-답변) |
| 불량 제거와 remove 비교 | [불량 제거 보기](#불량을-모두-제거할-때-remove와의-차이) |

- 최초 기록일: 2026-10-15
- 수정일: 2026-10-15
- 분류: Python, Coding
- 핵심 용어: list comprehension, 리스트, for, 조건 필터, 조건부 표현식

## 질문

list comprehension 추가

## 답변

**리스트 컴프리헨션(list comprehension)은 반복하면서 얻은 결과를 새 리스트로 만드는 간결한 문법입니다.** 보통 `for`문에서 값을 계산해 `append()`로 모으는 작업을 짧게 표현할 때 사용합니다.

```python
[표현식 for 변수 in 반복할_대상]
```

`for`로 값을 하나씩 가져온 뒤, 앞에 있는 표현식을 계산해 새 리스트에 넣습니다. 아래 예제의 결과는 실제 실행해 확인했습니다.

## 예제

### 일반 반복문과 비교

```python
numbers = [1, 2, 3, 4, 5]

# 일반 for문
doubled = []
for number in numbers:
    doubled.append(number * 2)

# 같은 작업을 리스트 컴프리헨션으로 표현
doubled = [number * 2 for number in numbers]
print(doubled)
```

실행 결과:

```text
[2, 4, 6, 8, 10]
```

이 코드는 새 리스트를 만들며 원래 `numbers` 리스트는 바꾸지 않습니다.

### 조건에 맞는 값만 골라내기

필터 조건은 `for` 뒤에 씁니다.

```python
numbers = [1, 2, 3, 4, 5]
evens = [number for number in numbers if number % 2 == 0]
print(evens)
```

실행 결과:

```text
[2, 4]
```

조건이 거짓인 원소는 결과에 포함하지 않습니다.

### 조건에 따라 결과 값을 바꾸기

각 원소를 짝수 또는 홀수 표시로 바꾸려면 앞에서 배운 조건부 표현식을 `for` 앞에 넣습니다.

```python
numbers = [1, 2, 3, 4, 5]
labels = ["even" if number % 2 == 0 else "odd" for number in numbers]
print(labels)
```

실행 결과:

```text
['odd', 'even', 'odd', 'even', 'odd']
```

`even`은 짝수, `odd`는 홀수라는 뜻입니다. 이 예제에서는 각 입력 원소마다 표시 하나가 만들어집니다.

### 사용자 목록에서 정지되지 않은 사용자 이름 추출

```python
test_users = [
    {"username": "alpha", "is_suspended": False},
    {"username": "bravo", "is_suspended": True},
]

active_names = [
    user["username"]
    for user in test_users
    if not user["is_suspended"]
]
print(active_names)
```

실행 결과:

```text
['alpha']
```

`not`은 참과 거짓을 뒤집습니다. 이 입력에서 정지 여부가 `False`인 사용자를 고르고 이름만 새 리스트에 담습니다. 긴 표현식은 대괄호 안에서 여러 줄로 써도 됩니다.

## 헷갈리기 쉬운 점

| 목적 | 문법 | 결과 |
| --- | --- | --- |
| 원소 골라내기 | `[값 for 값 in 대상 if 조건]` | 조건에 맞는 원소만 포함 |
| 원소별 값 선택 | `[A if 조건 else B for 값 in 대상]` | 원소마다 A 또는 B를 포함 |

- 뒤의 필터 `if`에는 `else`를 붙이지 않습니다. 앞의 조건부 표현식에는 `else`가 필요합니다.
- `append()`는 리스트를 바꾸고 `None`을 반환합니다. `[result.append(x) for x in numbers]`처럼 쓰지 말고, 새 리스트가 필요하면 `[x for x in numbers]`처럼 결과 값 자체를 앞에 둡니다.
- 출력이나 여러 동작을 수행하려는 목적이라면 일반 `for`문이 더 자연스럽습니다. 조건과 중첩이 복잡해 읽기 어려워져도 일반 반복문으로 풀어 씁니다.
- 결과 리스트를 한꺼번에 만들므로 입력이 매우 크면 메모리 사용량을 고려해야 합니다.

관련 학습: [조건부 표현식](2026-10-15-python-conditional-expression.md), [딕셔너리와 리스트 비교](2026-10-15-python-dictionary.md#후속-질문과-답변)

## 후속 질문과 답변

### 2026년 10월 15일 메뉴 리스트 컴프리헨션 오류

질문: What's the issue? 다음 코드에서 무엇이 잘못됐나요?

```python
result = []
list_1 = [1, 2, 3, 4, 5]
# result를 채우는 반복문과 컴프리헨션은 모두 주석 처리됨
print(result)

menu = ['아메리카노', '라떼', '초코']
ice_menu = int ['아이스'+1 for i in menu]
len_menu = [len(i) for 1 in menu if len(i)%2==0]
print(ice_menu)
print(len_menu)
```

수정할 부분:

1. `int [...]`의 `int`는 필요 없습니다. 문자열 목록을 만들려는 것이므로 `[...]`만 사용합니다. `int`는 정수 변환 등에 사용하는 타입이며 리스트 컴프리헨션 앞에 붙이는 표시가 아닙니다.
2. `'아이스' + 1`은 문자열에 정수를 더하려 해서 `TypeError`가 발생합니다. 숫자 `1` 대신 각 메뉴 이름을 담는 변수 `i`를 사용해 `'아이스' + i`로 바꿉니다.
3. `for 1 in menu`의 숫자 `1`에는 값을 대입할 수 없어 `SyntaxError`가 발생합니다. `for i in menu`처럼 변수 이름을 써야 합니다. 소문자 `i`와 숫자 `1`을 구분합니다.
4. 문법 오류를 고친 뒤에도 `result`를 채우는 코드가 모두 주석 처리되어 있으면 `print(result)`는 `[]`를 출력합니다. 원본 파일은 문법 오류 때문에 실행 자체가 시작되지 않으므로 먼저 문법을 고쳐야 합니다.

수정 코드:

```python
menu = ['아메리카노', '라떼', '초코']
ice_menu = ['아이스' + i for i in menu]
len_menu = [len(i) for i in menu if len(i) % 2 == 0]

print(ice_menu)
print(len_menu)
```

실제 실행 결과:

```text
['아이스아메리카노', '아이스라떼', '아이스초코']
[2, 2]
```

`아메리카노`는 길이가 5여서 제외되고, `라떼`와 `초코`의 길이는 각각 2입니다. `len_menu`는 이름이 아니라 길이를 담습니다. 길이가 짝수인 메뉴 이름을 원하면 `[i for i in menu if len(i) % 2 == 0]`으로 작성합니다.

### 불량을 모두 제거할 때 remove와의 차이

기록일: 2026-10-15

질문: `items = [item for item in items if item != '불량']`에서 왜 `items.remove()`를 사용하지 않나요?

**`remove('불량')`는 첫 번째로 발견한 불량 하나만 삭제합니다.** 반면 리스트 컴프리헨션은 모든 원소를 확인하고 조건에 맞는 원소만 새 리스트에 담습니다. 아래 네 가지 경우의 결과는 실제 실행해 확인했습니다.

```python
items = ['정상', '불량', '불량', '정상']
items.remove('불량')
print(items)  # ['정상', '불량', '정상']
```

다음처럼 순회 중인 리스트에서 직접 삭제하면 항목을 건너뛸 수 있습니다.

```python
items = ['정상', '불량', '불량', '정상']
for item in items:
    if item == '불량':
        items.remove(item)
print(items)  # ['정상', '불량', '정상']
```

첫 불량을 지우면 뒤의 불량이 앞자리로 당겨집니다. 반복은 다음 위치로 진행하므로 당겨진 불량을 검사하지 못합니다.

```python
items = ['정상', '불량', '불량', '정상']
items = [item for item in items if item != '불량']
print(items)  # ['정상', '정상']
```

이 코드는 원래 리스트에서 직접 삭제하지 않고 새 리스트를 만든 다음 `items`가 새 리스트를 가리키도록 합니다. 다른 변수가 원래 리스트를 가리키고 있다면 그 변수로 보는 리스트는 그대로입니다.

`remove()`로 모두 삭제하는 방법도 있습니다.

```python
items = ['정상', '불량', '불량', '정상']
while '불량' in items:
    items.remove('불량')
print(items)  # ['정상', '정상']
```

다만 매번 값을 찾고 삭제하므로 목록이 클 때 비효율적일 수 있습니다. 조건으로 원소를 걸러 새 목록을 만들 목적에는 리스트 컴프리헨션이 간결합니다. `remove()`는 원본 리스트를 바꾸고 `None`을 반환하며, 값이 없으면 `ValueError`가 발생합니다.

현재 입력에는 정상과 불량만 있으므로 `item != '불량'`이면 정상만 남습니다. 다른 상태도 들어올 수 있고 정확히 정상만 남기려면 `item == '정상'`을 사용합니다.
