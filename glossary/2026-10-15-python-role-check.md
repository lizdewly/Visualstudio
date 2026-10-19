# 사용자 정지 여부와 역할에 따른 분기

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 문제의 요구사항 | [질문 보기](#질문) |
| 빈칸 채우기 | [답변 보기](#답변) |
| 전체 분기와 실행 결과 | [예제 보기](#예제) |
| continue와 break의 차이 | [주의점 보기](#헷갈리기-쉬운-점) |
| 직접 작성한 코드 수정 | [후속 질문 보기](#후속-질문과-답변) |

- 최초 기록일: 2026-10-15
- 수정일: 2026-10-15
- 분류: Python, Coding
- 핵심 용어: 딕셔너리, if, elif, else, continue, break

## 질문

백엔드 API의 사용자 정보 딕셔너리에서 역할과 정지 여부를 읽고, 접근 가능 여부와 기능을 판단하는 코드를 어떻게 채우나요?

- `is_suspended`가 `True`이면 즉시 `정지된 계정입니다`를 출력하고 해당 사용자 검사를 종료합니다.
- 역할은 `admin`, `manager`, `user`, `guest` 중 하나입니다.
- 알 수 없는 역할이면 `[오류] 알수 없는 권한입니다.`를 출력합니다.
- 반복문 안의 `role =`과 `suspended =`가 비어 있습니다.

## 답변

딕셔너리의 키를 사용해 값을 읽습니다. 각 사용자 정보에 두 키가 들어 있다는 문제의 전제에 따라 대괄호로 접근합니다.

```python
role = user["user_role"]
suspended = user["is_suspended"]
```

`role`에는 `"admin"` 같은 문자열이, `suspended`에는 `True` 또는 `False`가 들어갑니다. 먼저 정지 여부를 검사하고, 정지된 사용자이면 `continue`로 다음 사용자로 넘어갑니다. 정지되지 않았을 때만 역할을 검사합니다.

## 예제

역할별 구체적인 기능 목록은 문제에 없으므로, 아래 코드는 역할에 맞는 안내 문구를 출력하는 예시입니다.

```python
test_users = [
    {"username": "alpha", "user_role": "admin", "is_suspended": False},
    {"username": "bravo", "user_role": "user", "is_suspended": True},
    {"username": "charlie", "user_role": "manager", "is_suspended": False},
    {"username": "delta", "user_role": "hacker", "is_suspended": False},
]

for user in test_users:
    username = user["username"]
    role = user["user_role"]
    suspended = user["is_suspended"]

    print(f"[{username}]")

    if suspended:
        print("정지된 계정입니다")
        continue  # 이 사용자의 검사를 끝내고 다음 사용자로 이동

    if role == "admin":
        print("관리자 기능 사용 가능")
    elif role == "manager":
        print("매니저 기능 사용 가능")
    elif role == "user":
        print("일반 사용자 기능 사용 가능")
    elif role == "guest":
        print("게스트 기능 사용 가능")
    else:
        print("[오류] 알수 없는 권한입니다.")
```

실제 실행 결과:

```text
[alpha]
관리자 기능 사용 가능
[bravo]
정지된 계정입니다
[charlie]
매니저 기능 사용 가능
[delta]
[오류] 알수 없는 권한입니다.
```

`bravo`는 역할이 `user`여도 정지된 계정이므로 일반 사용자 기능 안내가 출력되지 않습니다. 사용자 이름 출력은 결과를 구분하기 위한 보조 출력입니다.

## 헷갈리기 쉬운 점

- `if suspended:`는 이 문제처럼 값이 불리언(`True` 또는 `False`)일 때 정지 여부를 확인하는 간단한 표현입니다. 문자열 `"False"`와 불리언 `False`는 다르므로 입력값을 혼동하지 않습니다.
- `continue`는 현재 사용자의 나머지 검사를 건너뛰고 다음 사용자를 처리합니다. `break`를 쓰면 반복문 전체가 끝나므로 뒤의 사용자도 검사하지 않습니다. 여기서는 “검사 종료”를 해당 사용자에 대한 종료로 해석합니다.
- `=`는 값을 변수에 대입할 때, `==`는 두 값이 같은지 비교할 때 씁니다.
- `elif`와 `else`는 연결된 `if`와 같은 들여쓰기에 둡니다. 각 분기 내부는 한 단계 더 들여씁니다.
- 이 예제는 조건 분기 연습입니다. 실제 기능별 접근 규칙은 별도로 정해야 합니다.

## 후속 질문과 답변

### 2026년 10월 15일 정지 여부를 반복문 뒤에서 검사해도 되나요

사용자는 역할별 권한 문구를 작성하고, `suspended = user["is suspended"]`로 값을 읽은 뒤 반복문 바깥에 다음 검사를 추가했습니다.

```python
if suspended == user["is suspended"]:
    print("정지된 계정입니다")
```

수정할 부분은 다음과 같습니다.

1. 원래 딕셔너리의 키는 `"is_suspended"`입니다. 공백이 있는 `"is suspended"`는 다른 키라서 원래 입력에서는 `KeyError`가 발생합니다.
2. 키를 고쳐도 `suspended == user["is_suspended"]`는 방금 읽은 값을 같은 값과 비교하므로 `False == False`일 때도 참입니다. 정지 여부를 보려면 `if suspended:`라고 씁니다.
3. 정지 검사는 반복문 안에서 역할 검사보다 먼저 해야 합니다. 반복문 뒤에 두면 모든 사용자를 처리한 뒤 마지막 사용자의 값만 검사하게 됩니다. 정지된 사용자에게 권한 안내를 출력하는 것도 막지 못합니다.
4. 알 수 없는 역할을 처리하는 `else`도 추가합니다.

사용자가 정한 권한 문구를 반영한 수정 코드입니다. 앞서 정의한 `test_users` 아래에 작성합니다.

```python
for user in test_users:
    username = user["username"]
    role = user["user_role"]
    suspended = user["is_suspended"]

    if suspended:
        print("정지된 계정입니다")
        continue

    if role == "admin":
        print("전체 시스템 관리 및 데이터 수정 권한 부여")
    elif role == "manager":
        print("팀 데이터 조회 및 수정 권한 부여")
    elif role == "user":
        print("개인 데이터 조회 권한 부여")
    elif role == "guest":
        print("게스트 권한 (읽기 전용 일부 허용)")
    else:
        print("[오류] 알수 없는 권한입니다.")
```

`continue`는 정지된 사용자의 나머지 코드를 건너뛰고 다음 사용자를 검사하게 합니다. 이 코드는 권한 부여 안내를 출력하는 연습이며, 출력 자체가 실제 API의 권한을 설정하지는 않습니다.

### 2026년 10월 15일 키 이름 때문에 발생한 오류

사용자가 `day_2_modules/day2-7.py`의 `suspended = user["is suspended"]` 줄에서 발생한 오류 위치를 공유했습니다. 입력 딕셔너리에는 `"is_suspended"`만 있으므로, 공백을 밑줄로 바꿔야 합니다. 딕셔너리에서 존재하지 않는 키를 대괄호로 조회하면 `KeyError`가 발생합니다.

실습 파일의 키를 수정하고 정지 검사를 역할 검사 앞으로 옮겼으며, 알 수 없는 역할을 처리하는 `else`를 추가했습니다.
