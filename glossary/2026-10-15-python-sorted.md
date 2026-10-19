# sorted 함수 사용법

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 기본 문법 | [답변 보기](#답변) |
| 정렬 방향과 기준 | [예제 보기](#예제) |
| sort 메서드와 비교 | [주의점 보기](#헷갈리기-쉬운-점) |
| 내림차순과 순서 뒤집기 | [후속 질문 보기](#후속-질문과-답변) |

- 최초 기록일: 2026-10-15
- 수정일: 2026-10-15
- 분류: Python, Coding
- 핵심 용어: sorted, 정렬, reverse, key, sort

## 질문

add "set" and "sorted"

## 답변

**`sorted()`는 반복 가능한 대상의 원소를 정렬한 새 리스트를 반환하는 내장 함수입니다.** 기본값은 오름차순이며 원본 컨테이너의 원소 순서를 직접 바꾸지 않습니다.

```python
sorted(대상)
sorted(대상, reverse=True)  # 내림차순
sorted(대상, key=기준함수)  # 각 원소에 기준함수를 적용한 값으로 정렬
```

## 예제

아래 결과 주석은 실제 실행해 확인했습니다.

### 오름차순과 내림차순

```python
numbers = [3, 1, 3, 2]

print(sorted(numbers))                # [1, 2, 3, 3]
print(numbers)                        # [3, 1, 3, 2]: 원본 유지
print(sorted(numbers, reverse=True))  # [3, 3, 2, 1]
```

`sorted()` 자체는 중복을 제거하지 않습니다.

### 문자열 길이로 정렬

```python
words = ['pear', 'fig', 'banana']
print(sorted(words, key=len))  # ['fig', 'pear', 'banana']
```

`key=len`은 각 단어의 길이를 정렬 기준으로 사용합니다. `len()`이 아니라 함수 자체인 `len`을 전달합니다.

### 중복 제거와 정렬을 함께 하기

```python
numbers = [3, 1, 3, 2]
print(sorted(set(numbers)))  # [1, 2, 3]
```

먼저 `set()`으로 중복을 제거하고, `sorted()`로 정렬한 리스트를 만듭니다.

## 헷갈리기 쉬운 점

| 비교 | `sorted(numbers)` | `numbers.sort()` |
| --- | --- | --- |
| 원본 리스트 | 원본 순서를 유지 | 원본을 직접 정렬 |
| 반환값 | 정렬된 새 리스트 | `None` |
| 대상 | 리스트, 튜플, 집합 등 반복 가능한 대상 | 리스트의 메서드 |

- 정렬하려는 원소나 기준 값은 서로 비교 가능해야 합니다. 예를 들어 정수와 문자열을 섞은 `[1, "2"]`는 기본 정렬에서 `TypeError`가 발생합니다.
- 같은 정렬 기준을 가진 원소끼리는 기존 상대 순서를 유지합니다.
- 딕셔너리를 그대로 `sorted()`에 넣으면 키들을 정렬한 리스트를 반환합니다.

관련 학습: [set 집합 사용법](2026-10-15-python-set.md)

## 후속 질문과 답변

### 2026년 10월 15일 기본 정렬 방향과 역순

질문: sorted 는 오름차순기준이야? what about if I want to reverse the order?

네. `sorted()`는 기본적으로 오름차순으로 정렬합니다. 내림차순은 `reverse=True`를 지정합니다.

```python
numbers = [3, 1, 4, 2]
print(sorted(numbers))                # [1, 2, 3, 4]
print(sorted(numbers, reverse=True))  # [4, 3, 2, 1]
```

정렬 없이 현재 순서만 뒤집으려면 `list(reversed(numbers))`를 사용합니다.

```python
print(list(reversed(numbers)))  # [2, 4, 1, 3]
```

위 주석은 예상 결과입니다. `reverse=True`는 정렬 방향을 바꾸고, `reversed()`는 현재 원소 순서만 뒤집습니다. 두 예제 모두 원본 `numbers`는 바꾸지 않습니다.
