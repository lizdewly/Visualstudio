# FastAPI 경로 매개변수와 입력 검증

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 답변 | [답변 보기](#답변) |
| 예제 | [예제 보기](#예제) |
| 헷갈리기 쉬운 점 | [주의점 보기](#헷갈리기-쉬운-점) |
| 후속 질문: 출력 확인 | [출력 설명](#후속-질문과-답변) |
| 후속 질문: HTTPException | [HTTPException 설명](#2026-10-20-httpexception은-무엇인가) |
| 참고 자료 | [출처 보기](#참고-자료) |

- 최초 기록일: 2026-10-20
- 수정일: 2026-10-20
- 분류: Python, Coding
- 핵심 용어: FastAPI, Annotated, Path, ge, HTTPException, 경로, 404, 422

## 질문

사용자가 아래 FastAPI 코드를 제공했다. 별도의 질문 문장은 없으며, 코드의 동작을 설명하는 것으로 해석했다.

```python
from typing import Annotated
from fastapi import FastAPI, HTTPException, Path

app = FastAPI(title="Lesson 03")
tasks = {1: {"id": 1, "title": "FastAPI basics", "done": False}}

# Fixed paths must be declared before the variable route.
@app.get("/tasks/stats")
def task_stats():
    return {"total": len(tasks)}

@app.get("/tasks/{task_id}")
def read_task(task_id: Annotated[int, Path(ge=1)]):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]
```

## 답변

이 코드는 할 일의 전체 개수와 특정 할 일 하나를 조회하는 GET API를 만든다.

- `FastAPI(title="Lesson 03")`: API 앱을 만들고 문서에 표시될 제목을 지정한다.
- `tasks`: 정수 ID를 키로 사용하는 딕셔너리다. 현재 ID 1인 할 일 하나가 들어 있다. `done=False`는 아직 완료하지 않았다는 뜻이다.
- `@app.get(...)`: 해당 주소로 GET 요청이 오면 바로 아래 함수를 실행하도록 등록하는 데코레이터다.
- `/tasks/stats`: `len(tasks)`로 저장된 할 일 개수를 반환한다.
- `/tasks/{task_id}`: URL의 해당 부분을 `task_id`로 받는다. 예를 들어 `/tasks/1`에서는 정수 `1`을 받는다.

`task_id: Annotated[int, Path(ge=1)]`은 타입과 FastAPI가 사용할 검증 정보를 함께 적은 것이다.

- `int`: 정수로 해석할 수 있어야 한다.
- `Path(...)`: URL 경로 매개변수의 조건을 지정한다.
- `ge=1`: greater than or equal, 즉 1 이상이어야 한다.
- `Annotated`: 타입에 추가 정보를 붙인다. 실제 요청 변환과 검증은 FastAPI가 수행한다.

검증을 통과하면 함수가 실행된다. `task_id not in tasks`는 딕셔너리의 키에 해당 ID가 없는지 확인한다. 없으면 `raise HTTPException(...)`으로 실행을 중단하고 404 응답을 보낸다. 있으면 해당 할 일 딕셔너리를 반환하며, FastAPI가 이를 JSON 응답으로 변환한다.

## 예제

아래는 제공된 코드와 공식 문서를 바탕으로 정리한 예상 응답이다. 로컬 서버에서 실행해 확인한 결과는 아니다.

| GET 요청 경로 | 예상 상태 | 응답 또는 이유 |
| --- | --- | --- |
| `/tasks/stats` | 200 | `{"total": 1}` |
| `/tasks/1` | 200 | `{"id": 1, "title": "FastAPI basics", "done": false}` |
| `/tasks/2` | 404 | `{"detail": "Task not found"}` |
| `/tasks/0` | 422 | 1 이상 조건을 만족하지 않음 |
| `/tasks/abc` | 422 | 정수로 해석할 수 없음 |

## 헷갈리기 쉬운 점

- 이 예제에서는 `/tasks/stats`를 `/tasks/{task_id}`보다 먼저 등록해야 한다. 순서를 바꾸면 `stats`가 `task_id` 자리로 매칭되고 정수 검증에서 422 오류가 발생한다. 타입 검증 실패 후 다음 경로로 다시 시도하지 않는다.
- 422는 요청한 ID의 형식이나 범위가 잘못된 경우이고, 여기서 직접 발생시키는 404는 형식은 맞지만 해당 데이터가 없는 경우다.
- `/` 경로는 등록하지 않았으므로 서버가 실행 중이어도 루트 주소에 GET 요청을 보내면 기본적으로 404가 나온다.
- 파이썬의 `False`는 JSON에서는 `false`로 표현된다.
- `tasks`는 메모리 안의 데이터이므로 데이터베이스처럼 영구 저장되지 않는다.

## 후속 질문과 답변

### 2026-10-20: 출력은 어디에 어떻게 나타나는가?

질문: “이 코드를 넣으면 output 이 어떻게 나타나는 거야?”

답변: 이 코드는 `print()`가 없으므로 필요한 패키지가 설치된 환경에서 `py main.py`로 그대로 실행하면 보통 콘솔 출력 없이 종료된다. 앱과 경로를 정의할 뿐 서버를 시작하는 코드는 없기 때문이다. 파일명을 `main.py`로 저장했다고 가정하고, 해당 환경에 Uvicorn이 설치되어 있다면 파일이 있는 폴더에서 다음 명령으로 서버를 시작할 수 있다.

```powershell
python -m uvicorn main:app --reload
```

`main`은 `main.py` 모듈, `app`은 코드의 FastAPI 앱 변수다. 가상 환경을 사용한다면 그 환경의 Python으로 실행한다.

서버가 시작되면 터미널에는 시작 및 요청 처리 로그가 표시되고, 브라우저에서 주소에 접속하면 JSON 응답을 볼 수 있다. 아래 내용은 코드에 따른 예상 응답이며 실제 실행 결과는 아니다. 브라우저에 따라 줄바꿈과 들여쓰기는 다를 수 있다.

- `http://127.0.0.1:8000/tasks/stats`: `{"total":1}`
- `http://127.0.0.1:8000/tasks/1`: `{"id":1,"title":"FastAPI basics","done":false}`
- `http://127.0.0.1:8000/tasks/2`: `{"detail":"Task not found"}` (404)
- `http://127.0.0.1:8000/`: `{"detail":"Not Found"}` (404, 루트 경로 미등록)

`http://127.0.0.1:8000/docs`에서는 API 문서를 열고 요청을 시험할 수 있다. `return`으로 반환한 값은 요청한 브라우저 등의 클라이언트로 전달되며, 자동으로 `print()`처럼 콘솔에 출력되는 것은 아니다.

### 2026-10-20: HTTPException은 무엇인가?

질문: 사용자가 `HTTPException`이라는 코드 용어를 제시했다. 기존 코드에서 이 용어의 의미를 묻는 것으로 해석했다.

답변: `HTTPException`은 FastAPI에서 요청한 쪽에 HTTP 오류 응답을 보내기 위해 사용하는 예외 클래스다. `HTTP`는 웹의 요청과 응답에 사용하는 통신 규칙이고, `Exception`은 예외라는 뜻이다. 파이썬 내장 기능이 아니라 `from fastapi import HTTPException`으로 가져온다.

```python
if task_id not in tasks:
    raise HTTPException(status_code=404, detail="Task not found")
return tasks[task_id]
```

- `HTTPException(...)`: 상태 코드와 설명을 담은 예외 객체를 만든다.
- `raise`: 그 예외를 발생시켜 현재 함수의 정상 실행 흐름을 중단한다.
- `status_code=404`: 요청한 할 일이 없다는 HTTP 상태 코드를 지정한다.
- `detail="Task not found"`: 요청한 쪽에 보낼 오류 설명을 지정한다.

제공된 코드에서 `/tasks/2`를 요청하면 ID 2가 없으므로 FastAPI의 기본 예외 처리가 HTTP 상태 404와 아래 JSON 본문을 응답한다. 이는 코드와 공식 문서를 바탕으로 한 예상 응답이며 직접 실행한 결과는 아니다.

```json
{"detail": "Task not found"}
```

이 경우 뒤의 `return tasks[task_id]`는 실행되지 않는다. 서버 전체가 종료되는 것은 아니며 다른 요청은 계속 처리할 수 있다. `HTTPException`은 `return`이 아니라 `raise`와 함께 사용한다. 상태 코드 404는 응답 본문과 별도의 HTTP 응답 정보다.

## 참고 자료

- [FastAPI: Path Parameters — 타입 변환, 검증, 경로 선언 순서](https://fastapi.tiangolo.com/tutorial/path-params/)
- [FastAPI: Path Parameters and Numeric Validations — Annotated, Path, ge](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/)
- [FastAPI: Handling Errors — HTTPException](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [FastAPI: First Steps — 서버 실행과 브라우저 응답 확인](https://fastapi.tiangolo.com/tutorial/first-steps/)
