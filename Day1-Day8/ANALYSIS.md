# 기존 코드 분석과 방명록 적용

확인일: 2026-10-23

## 분석 범위

실제 존재하는 Day1, Day2, Day3, Day4, Day6, Day7, Day8의 소스 목록과 import를 조사하고, 아래 대표 구현 및 관련 테스트를 읽었습니다. Day3와 Day4의 확장자가 없는 학습 코드도 포함했습니다. **Day5 폴더는 없으므로 그날의 학습 내용은 추정하지 않습니다.**

## 문법과 알고리즘 연결

| 폴더 | 확인한 문법·처리 방식 | 대표 파일 | 방명록에 적용 |
| --- | --- | --- | --- |
| Day1 | 변수, 문자열, 숫자 변환, if, for, while, 리스트 append, 함수, f 문자열 | `Day1/day1-1.py`~`day1-5.py`, `Day1/even_sum_and_count/calculate_even_sum_and_count.py` | 입력값 보관, 조건 검사, 목록을 반복해서 HTML로 출력 |
| Day2 | 논리 연산, 단락 평가, 딕셔너리, 언패킹, continue, zip, 컴프리헨션, set, sorted, 문자열 join | `Day2/Day2_am/day2-5.py`, `day2-6.py`, `Day2/Day2_pm/day2_1.py`~`day2_5.py` | 글 한 건을 이름·내용으로 취급하고 잘못된 입력을 먼저 거부 |
| Day3 | 함수와 return, 타입 힌트, 클래스, property, 상속, 추상 클래스, dataclass, enumerate, split, strip, try/except | `Day3/day3_1`, `day3_2`, `day3_3`, `day3_4`, `day3_4_1`, `day3_5`, `day3_6`, `day3-7` | 함수별로 저장·조회·화면 생성을 나누고 공백 입력과 저장 실패 처리 |
| Day4 | random, 리스트 인덱스, 대입 | `Day4/day4_1`, `Day4/test.py` | 임의 번호 대신 SQLite 기본 키 사용. 추가 알고리즘은 필요하지 않음 |
| Day5 | 폴더 없음 | 해당 없음 | 분석 제외 |
| Day6 | Pydantic BaseModel·Field·validator, FastAPI 경로, HTTP 오류, CRUD, 메모리 저장소 | `Day6/ch03_field/demo.py`, `ch04_validator/demo.py`, `ch07_fastapi/app.py`, `ch08_project/store.py` | 서버와 입력 검증 재사용. 메모리 dict를 SQLite 파일로 대체 |
| Day7 | async/await, asyncio.gather, HTTPX, 일반 함수와 비동기 함수 비교, HTML·정적 파일 제공 | `Day7/01/main.py`, `Day7/02/main.py`, `Day7/03/main2.py`, `Day7/shop_demo/app.py` | HTML 응답 제공 경험 활용. 작은 SQLite 작업은 일반 def로 처리 |
| Day8 | Query·Path 범위, 요청 본문 검증, 상태 코드, pytest·TestClient, 경계값과 연속 요청 검증 | `Day8/lesson_02_parameter/main.py`, `lesson_03_body_validation/main.py`, `lesson_08_final_verification/test_api.py` | 정상 등록, 공백 거부, 최대 길이, 저장 실패 후 상태 유지 테스트 |

## 기존 알고리즘에서 가져올 원칙

1. Day1의 짝수 합처럼 목록을 순회하며 결과를 구성합니다. 글 출력에 복잡한 자료구조는 필요 없습니다.
2. Day2의 역할 검사처럼 허용하지 않는 입력을 먼저 거부합니다.
3. Day3의 `strip()`과 예외 처리처럼 빈 글을 검사하고 오류를 사용자에게 설명합니다.
4. Day6의 `Field`와 검증 함수를 활용해 글 길이를 제한합니다.
5. Day8의 연속 요청 테스트처럼 실패한 등록이 저장된 글의 수나 내용을 바꾸지 않는지 확인합니다.

최신순 조회는 Python에서 전체 글을 읽어 `sorted()`하는 대신 SQLite의 `ORDER BY id DESC LIMIT ... OFFSET ...`으로 필요한 부분만 가져오는 안입니다. SQL 조회와 페이지 나누기는 새 학습 요소이므로 확인 후 구현합니다.

## 재사용할 기술과 줄일 요소

- 유지: Python, FastAPI, Pydantic, Uvicorn, HTML, 소량의 CSS, 함수 중심 코드.
- 데이터 저장: 사용자가 지정한 Python 표준 라이브러리 `sqlite3`와 파일 하나.
- 테스트: 기존 Day8의 pytest·TestClient·HTTPX를 개발 검증에만 사용.
- 화면: HTML form, input, textarea, button, 링크로 구성. JavaScript 없이 서버가 완성된 HTML을 반환.
- 최소 기능: 글 등록, 최신순 목록, 페이지 이동.
- 최초 버전에는 로그인, 비밀번호, 수정·삭제, 파일 업로드, 관계 테이블, 외부 API, ORM, 백그라운드 작업을 넣지 않는 안을 제안합니다.

Day8의 requirements에는 `fastapi==0.115.12`, `pydantic==2.11.5`, `uvicorn==0.34.2`, `httpx==0.28.1`, `pytest==8.3.5`가 있습니다. 이것은 기존 학습 환경의 기록이며, 새 앱의 설치·호환성 검증을 마쳤다는 뜻은 아닙니다.

## 원본을 그대로 복사하면 안 되는 지점

학습 코드는 일부 오류를 포함합니다. 이 작업에서 원본은 수정하지 않았습니다.

- `Day3/day3_3:37`: 읽기 전용 `ast.parse` 검사에서 `unmatched ']'` 문법 오류를 확인했습니다. `pipeline` 목록 선언이 완성되어 있지 않습니다.
- `Day1/even_sum_and_count/calculate_even_sum_and_count.py`: 1~100 짝수 합의 assert 기대값이 2250입니다. 올바른 합은 2550이므로 테스트 기대값을 재사용하면 안 됩니다. 이 파일을 실행해 확인한 결과는 아닙니다.
- `Day2/Day2_pm/day2_3.py`: `re.escapte`라는 오타가 보입니다. 올바른 API는 `re.escape`입니다.
- `Day4/day4_1`: 첫 값을 마지막 값으로 대입한 다음 마지막 값에 첫 값을 넣으면 원래 첫 값은 사라집니다. 두 값을 교환한 결과가 아닙니다.
- `Day8/lesson_08_final_verification/main.py`: 좌석을 먼저 차감하고 부족한지 검사합니다. 실패한 요청이 상태를 바꿀 수 있어, 방명록에서는 검증 후 저장하고 실패 시 롤백해야 합니다.

소스의 구문을 읽기 전용으로 검사했으며, 원본의 입력 대기·서버 실행을 모두 수행한 것은 아닙니다. 아직 방명록 코드가 없어 방명록 실행 테스트 결과도 없습니다.
