# Swagger UI와 API 테스트

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 답변 | [답변 보기](#답변) |
| 실행 확인 | [실행 확인](#실행-확인) |
| assert 쉽게 이해하기 | [후속 질문](#후속-질문과-답변) |

- 최초 기록일: 2026-10-23
- 수정일: 2026-10-23
- 분류: Python, Coding
- 핵심 용어: Swagger UI, API, TestClient, OpenAPI

## 질문

“swagger and api test” — 현재 Day8/lesson_02_parameter 예제를 기준으로 Swagger와 API 테스트를 설명하고 확인한다.

## 답변

Swagger UI는 API 설명을 보고 직접 요청을 보내는 웹 화면이다. API 테스트는 요청에 대한 상태 코드와 응답 내용이 기대한 결과와 맞는지 확인하는 작업이다. Swagger에서 수동으로 하거나 TestClient와 pytest로 자동화할 수 있다.

프로젝트 루트의 PowerShell에서 서버를 실행한다.

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir Day8/lesson_02_parameter --reload
```

브라우저에서 http://127.0.0.1:8000/docs 를 열고 `GET /items/{item_id}` → `Try it out` → 값 입력 → `Execute` 순서로 실행한다. 실제 결과는 `Server response`에서 확인한다. 문서의 예시 응답 자체가 테스트 결과는 아니다.

`item_id=1, qty=3`이면 코드상 예상 결과는 상태 200, `{"item_id":1,"qty":3,"total":3000}`이다. `item_id=0`이나 `qty=6`은 422가 예상된다. 수량 생략 실험은 `/items/1`처럼 쿼리 문자열 없이 요청해야 한다.

## 실행 확인

Windows의 기본 Python과 루트 .venv 모두 pytest가 없어 pytest 실행은 실패했다. .venv의 TestClient로 `/docs` 응답 상태 200과 Swagger UI 초기화 코드 포함 여부, `/items/1`의 실제 응답 `{"item_id":1,"qty":2,"total":2000}`을 확인했다. 브라우저 화면 렌더링이나 실제 HTTP 서버 검증은 이번에 수행하지 않았다.

실습 계약은 수량 생략 시 1개지만 현재 main.py에는 기본값 2가 있다. README에서 의도한 학습용 오류라고 명시한다. 수정하려면 qty 선언 끝의 `= 2`를 `= 1`로 바꾸면 된다. 이번 요청에서는 학습용 코드를 수정하지 않았다.

## 후속 질문과 답변

### 2026-10-23: assert를 쉽게 다시 설명해 줘

질문: “assert 에 대해 다시 설명해줘. 쉽게”

`assert`는 “이 조건이 맞는지 확인해!”라는 검사다. 조건이 참이면 조용히 다음 줄로 넘어가고, 거짓이면 `AssertionError`를 발생시킨다. 이 오류를 처리하지 않으면 실행이 중단된다. pytest에서는 해당 테스트를 실패로 기록하고 보통 다른 테스트를 계속 실행한다.

```python
total = 3000
assert total == 3000  # 맞으므로 통과
assert total == 5000  # 틀리므로 AssertionError 발생
```

위 코드는 설명용이며 이번 답변에서 실행하지 않았다. `==`는 같은지 비교하는 기호이며 값을 넣는 `=`와 다르다.

API 테스트의 `assert response.status_code == 200`은 “실제 응답 상태가 200인지 확인해!”라는 뜻이다. 실제 값이 200이면 통과하고 422이면 실패한다. assert가 응답을 200으로 바꾸는 것은 아니다.

```python
assert total == 5000, "합계가 예상과 달라요"
```

쉼표 뒤에는 실패할 때 보여 줄 설명을 넣을 수 있다. 주로 개발 중 예상과 실제가 맞는지 검사할 때 사용한다. Python의 `-O` 옵션으로 생략될 수 있으므로 필수 사용자 입력 검증을 assert에만 맡기지는 않는다.

## 참고 자료

- [FastAPI 공식 문서: First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [실습 README](../Day8/lesson_02_parameter/README.md)
- [기존 API 테스트](../Day8/lesson_02_parameter/test_api.py)
