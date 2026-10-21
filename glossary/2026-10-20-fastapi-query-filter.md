# FastAPI 쿼리 매개변수로 검색과 페이지 나누기

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 답변 | [답변 보기](#답변) |
| 예제 | [예제 보기](#예제) |
| 헷갈리기 쉬운 점 | [주의점 보기](#헷갈리기-쉬운-점) |
| 참고 자료 | [출처 보기](#참고-자료) |

- 최초 기록일: 2026-10-20
- 수정일: 2026-10-20
- 분류: Python, Coding
- 핵심 용어: FastAPI, Query, Annotated, None, casefold, 리스트 컴프리헨션, 슬라이싱, 페이지 나누기

## 질문

사용자가 Lesson 04 FastAPI 코드를 제공했다. 별도의 질문 문장은 없으며, 앞선 학습 흐름에 따라 동작과 예상 응답을 설명하는 것으로 해석했다.

```python
from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI(title="Lesson 04")
tasks = [
    {"id": 1, "title": "FastAPI basics", "done": False},
    {"id": 2, "title": "HTTP methods", "done": True},
    {"id": 3, "title": "Python review", "done": False},
]

@app.get("/tasks")
def list_tasks(
    q: str | None = None,
    done: bool | None = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=20)] = 10,
):
    rows = tasks
    if q is not None:
        rows = [t for t in rows if q.casefold() in t["title"].casefold()]
    if done is not None:
        rows = [t for t in rows if t["done"] == done]
    total = len(rows)
    return {"items": rows[skip:skip + limit], "total": total}
```

## 답변

이 API는 할 일 목록에 검색 조건과 완료 여부 조건을 적용하고, 결과 중 일부를 반환한다. 이번 `tasks`는 딕셔너리들을 담은 리스트다.

쿼리 매개변수는 URL의 `?` 뒤에 적으며 여러 조건은 `&`로 연결한다. 예: `/tasks?q=python&done=false&skip=0&limit=1`.

| 매개변수 | 역할 | 생략 시 값 | 조건 |
| --- | --- | --- | --- |
| `q` | 제목에 포함된 문자열 검색 | `None` | 문자열 |
| `done` | 완료 여부 필터 | `None` | 불리언으로 변환 가능한 값 |
| `skip` | 필터 결과에서 앞의 몇 개를 건너뛸지 지정 | `0` | 정수, 0 이상 |
| `limit` | 최대 몇 개를 반환할지 지정 | `10` | 정수, 1 이상 20 이하 |

`str | None`은 문자열 또는 `None`을 허용하는 타입 표현이다. 뒤의 `= None`은 매개변수를 생략했을 때의 기본값이다. `Annotated[int, Query(...)]`는 정수 타입에 쿼리 검증 정보를 붙인다. `ge`는 이상, `le`는 이하라는 뜻이다.

처리 흐름:

1. `rows = tasks`로 전체 목록을 가리킨다. 리스트를 복사하는 문장은 아니다.
2. `q`가 있으면 제목에 검색어가 포함된 항목만 새 리스트로 만든다. `t`는 반복 중인 할 일 딕셔너리다. `casefold()`는 대소문자를 구분하지 않는 비교에 사용한다. 예를 들어 `PYTHON`으로도 `Python review`를 찾는다.
3. `done`이 지정되었으면 완료 상태가 같은 항목만 남긴다. 두 조건을 모두 주면 둘 다 만족해야 한다.
4. `total = len(rows)`로 필터를 통과한 전체 개수를 구한다.
5. `rows[skip:skip + limit]`로 일부를 잘라 `items`에 넣는다. 시작 인덱스는 포함하고 끝 인덱스는 제외한다.

## 예제

아래 내용은 코드와 공식 문서를 바탕으로 한 예상 응답이며 실제 서버 실행 결과는 아니다. 서버가 실행 중이라면 주소 앞에 `http://127.0.0.1:8000`을 붙여 브라우저에서 확인할 수 있다.

| 요청 경로 | 반환되는 할 일 ID | `total` |
| --- | --- | --- |
| `/tasks` | 1, 2, 3 | 3 |
| `/tasks?q=python` | 3 | 1 |
| `/tasks?done=true` | 2 | 1 |
| `/tasks?done=false` | 1, 3 | 2 |
| `/tasks?skip=1&limit=1` | 2 | 3 |
| `/tasks?done=false&skip=1&limit=1` | 3 | 2 |
| `/tasks?q=missing` | 없음 | 0 |

`/tasks?done=false&skip=1&limit=1`의 예상 JSON 응답:

```json
{
  "items": [
    {"id": 3, "title": "Python review", "done": false}
  ],
  "total": 2
}
```

미완료 항목은 ID 1과 3인 두 개다. 그중 첫 항목을 건너뛰고 하나를 반환하므로 `items`에는 ID 3만 있지만 `total`은 2다.

## 헷갈리기 쉬운 점

- `if done is not None`은 `False`도 유효한 필터 값으로 처리한다. `if done`으로 바꾸면 미완료 항목 검색이 제대로 적용되지 않는다.
- `skip`은 ID가 아니라 필터링된 리스트에서 건너뛸 항목 수다.
- `limit=10`이어도 데이터가 3개라면 3개만 반환한다.
- 검색 결과가 없으면 기본적으로 200 응답에 `{"items": [], "total": 0}`을 반환한다. 이 코드에는 404를 발생시키는 부분이 없다.
- `skip=-1`, `limit=0`, `limit=21`처럼 조건을 벗어나면 FastAPI가 기본적으로 422 검증 오류를 응답한다.
- `skip`이 결과 수보다 커도 슬라이싱 오류 없이 `items`는 빈 리스트가 된다. `total`은 필터 결과 수를 유지한다.
- 이 코드는 원본 리스트를 직접 수정하지 않는다. 필터링은 새 리스트를 만들고 슬라이싱도 새 리스트를 만든다.

## 참고 자료

- [FastAPI: Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
- [FastAPI: Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/)
