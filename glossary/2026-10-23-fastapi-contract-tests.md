# FastAPI 4차시: 계약에서 도출한 pytest 테스트

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문](#질문) |
| 답변과 테스트 표 | [답변](#답변) |
| 계약과 차이 | [검토](#계약과-차이) |
| 실행 확인 | [실행 확인](#실행-확인) |

- 최초 기록일: 2026-10-23
- 수정일: 2026-10-23
- 분류: AI, Python, Coding
- 핵심 용어: 업무 계약, pytest, TestClient, 경계값, 엄격한 정수, 회귀

## 질문

FastAPI 4차시 README, main.py, test_api.py와 저장된 OpenAPI 스냅샷이 있으면 읽고 계약과 차이를 표시해 달라. 현재 반환값을 정답으로 복사하지 말고 업무 계약에서 정상·허용 끝값·경계 밖·누락·타입·핵심 회귀를 선별하여 표를 먼저 제시한 뒤 test_generated.py를 작성해 달라. TestClient와 `from main import app`을 사용하고 main.py와 test_api.py는 수정하지 않는다. 로컬 Python 3.12이며 외부 API나 DB는 없다. 자체 검토와 실제 실행 결과를 구분한다.

## 답변

업무 계약은 POST /quotes에 엄격한 정수 amount 1~100000을 전달하는 것이다. 10000 이상이면 1000원 정액 할인, 미만이면 할인 0원이다. 성공 상태는 200이며 본문은 amount, discount, payable이다. payable은 amount에서 discount를 뺀 값이다. 입력 오류는 422다.

성공 본문은 표에서 `(amount, discount, payable)` 순서로 줄여 썼지만 테스트에서는 세 키를 가진 JSON 객체 전체를 비교한다. 오류 본문은 업무 계약에 정의되어 있지 않으므로 특정 메시지나 detail 구조를 강제하지 않는다. 각 행은 독립 요청이다.

| ID | 입력(JSON) | 사전 상태 | 요청 순서 | 기대 상태 | 기대 본문 | 근거 |
| --- | --- | --- | --- | --- | --- | --- |
| N01 | `{"amount":5000}` | 없음 | POST 1회 | 200 | `(5000,0,5000)` | 정상: 할인 없음 |
| N02 | `{"amount":20000}` | 없음 | POST 1회 | 200 | `(20000,1000,19000)` | 정상: 정액 할인 |
| E01 | `{"amount":1}` | 없음 | POST 1회 | 200 | `(1,0,1)` | 허용 최솟값 |
| E02 | `{"amount":100000}` | 없음 | POST 1회 | 200 | `(100000,1000,99000)` | 허용 최댓값·정액 할인 |
| R01 | `{"amount":9999}` | 없음 | POST 1회 | 200 | `(9999,0,9999)` | 할인 경계 바로 아래 |
| R02 | `{"amount":10000}` | 없음 | POST 1회 | 200 | `(10000,1000,9000)` | 핵심 회귀: 경계 포함 |
| R03 | `{"amount":10001}` | 없음 | POST 1회 | 200 | `(10001,1000,9001)` | 할인 경계 바로 위 |
| B01 | `{"amount":0}` | 없음 | POST 1회 | 422 | 계약 미지정 | 하한 바로 밖 |
| B02 | `{"amount":100001}` | 없음 | POST 1회 | 422 | 계약 미지정 | 상한 바로 밖 |
| M01 | `{}` | 없음 | POST 1회 | 422 | 계약 미지정 | amount 누락 |
| M02 | 본문 없음 | 없음 | POST 1회 | 422 | 계약 미지정 | 입력 전체 누락 |
| T01 | `{"amount":"10000"}` | 없음 | POST 1회 | 422 | 계약 미지정 | 숫자 문자열 거부 |
| T02 | `{"amount":10000.0}` | 없음 | POST 1회 | 422 | 계약 미지정 | 정수값 실수도 거부 |
| T03 | `{"amount":1.5}` | 없음 | POST 1회 | 422 | 계약 미지정 | 소수 거부 |
| T04 | `{"amount":true}` | 없음 | POST 1회 | 422 | 계약 미지정 | 불리언을 정수로 받지 않음 |
| T05 | `{"amount":null}` | 없음 | POST 1회 | 422 | 계약 미지정 | null 거부 |
| T06 | `{"amount":[]}` | 없음 | POST 1회 | 422 | 계약 미지정 | 배열 거부 |
| T07 | `{"amount":{}}` | 없음 | POST 1회 | 422 | 계약 미지정 | 객체 거부 |

DB 초기화, 중복 생성, 순서 충돌, 외부 API 장애는 상태 저장이나 외부 연동이 없는 이번 계약에 해당하지 않아 제외했다. 추가 필드 처리나 인증 등 계약에 없는 정책도 임의로 만들지 않았다.

## 계약과 차이

- main.py는 `amount > 10000`을 사용한다. 계약의 '이상'과 달라 10000에서 할인이 빠진다. 코드 독해상 R02 실패가 예상되지만 이번에 pytest로 확인한 결과는 아니다.
- README의 업무 계약은 200이지만 중간 경로 표에는 201 / 422가 적혀 있다. 사용자 계약과 README 업무 계약의 200을 적용했다.
- test_api.py의 정상 기대값은 계약과 일치한다. 제공 오류 검사는 detail의 loc도 검사한다. 새 테스트는 업무 계약이 보장한 422만 검사한다.
- 제공 테스트에 없는 실수·불리언·null·배열·객체와 본문 전체 누락을 추가했다.
- 해당 차시 폴더에 openapi_snapshot.json이 없어 저장 명세 대조는 수행하지 못했다. 스냅샷을 새로 만들거나 읽은 것으로 취급하지 않았다.
- 생성 파일 첫 줄은 `from main import app`이며 각 표 행을 pytest ID 또는 M02 함수명으로 연결했다. 성공 기대값은 명시적인 상수로 작성하고 구현의 할인 함수를 재사용하지 않았다. xfail이나 skip으로 핵심 실패를 숨기지 않았다.
- main.py와 test_api.py는 수정하지 않았다.

## 실행 확인

실제 실행 도구에서 `py -3.12 --version`은 해당 런타임을 찾지 못했다. `py --list`는 Python 3.13만 표시했고 프로젝트 루트 가상환경은 Python 3.13.15였다.

아래 명령은 `Day8/lesson_04_ai_test_cases` 폴더에서 실행했다.

| 실제 명령 | 실제 결과 |
| --- | --- |
| `py -m py_compile test_generated.py` | 문법 검사 성공 |
| `..\..\.venv\Scripts\python.exe -m pytest -q test_generated.py -p no:cacheprovider` | `No module named pytest`, 테스트 시작 못 함 |
| `py -m pytest -q test_generated.py -p no:cacheprovider` | `No module named pytest`, 테스트 시작 못 함 |

따라서 pytest 통과/실패 개수와 Python 3.12에서의 동작은 미확인이다. 설치된 Python 3.12 실습 환경에서는 차시 폴더에서 `python -m pytest -q test_generated.py`로 실행한다. 이는 안내 명령이며 이번에 성공적으로 실행한 명령이 아니다.

## 참고 자료

- [실습 README](../Day8/lesson_04_ai_test_cases/README.md)
- [현재 구현](../Day8/lesson_04_ai_test_cases/main.py)
- [제공 테스트](../Day8/lesson_04_ai_test_cases/test_api.py)
- [제공 설계표](../Day8/lesson_04_ai_test_cases/TEST_CASES.md)
- [생성 테스트](../Day8/lesson_04_ai_test_cases/test_generated.py)
