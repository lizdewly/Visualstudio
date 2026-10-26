# 방명록 코드 읽기

## 먼저 읽을 순서

1. `templates/index.html`: 이름과 내용을 입력받는 `<form>`을 봅니다. `method="post"`와 `action="/entries"`가 어디로 전송할지 정합니다.
2. `main.py`의 `GuestbookEntry`: Pydantic이 앞뒤 공백을 제거하고 길이를 확인합니다.
3. `create_entry`: 입력 검증 → 저장 → 303 이동 순서를 봅니다.
4. `save_entry`: SQL의 `?`에 입력값을 따로 전달해 저장합니다.
5. `home`, `read_entries`, `render_guestbook`: DB에서 글을 읽고 HTML로 바꾸는 순서를 봅니다.

## 요청 한 번이 지나가는 길

```text
브라우저 HTML form
  → POST /entries
  → 요청 형식과 16 KiB 제한 검사
  → FastAPI Form으로 name, message 읽기
  → GuestbookEntry로 공백·길이 검사
  → SQLite 글 수 검사와 INSERT
  → 303 응답
  → 브라우저 GET /?saved=true
  → 최신 글 10개 조회 → HTML 화면
```

입력 오류는 422, 글 수 한도 초과는 409, 요청 크기 초과는 413, 지원하지 않는 요청 형식은 415, DB 작업 실패는 503으로 응답합니다. 정상 등록의 응답은 303이며, 이동한 목록은 200입니다.

## SQL과 테이블

`initialize_db()`는 서버 시작 때 테이블이 없으면 만듭니다. 이미 있으면 기존 글을 지우지 않습니다. 테이블은 `guestbook` 하나이고 외래 키가 없습니다.

```python
connection.execute(
    "INSERT INTO guestbook (name, message, created_at) VALUES (?, ?, ?)",
    (entry.name, entry.message, created_at),
)
```

위 코드는 원리를 설명하는 발췌입니다. 실제 작성 시각은 `save_entry()`에서 생성합니다. 입력값으로 SQL 문장을 직접 조합하지 않기 때문에 따옴표나 SQL처럼 보이는 글도 데이터로 저장합니다.

`BEGIN IMMEDIATE`는 글 수 확인과 INSERT 사이에 다른 쓰기 요청이 끼어들지 않도록 합니다. 그래야 999개일 때 동시에 두 요청이 들어와도 1,001개로 늘어나지 않습니다. 연결의 `with` 블록은 성공하면 commit, 예외가 나면 rollback하며, 바깥 `closing(...)`은 연결을 닫습니다.

페이지가 2라면 `(2 - 1) * 10 = 10`개를 건너뛰고 다음 10개를 읽습니다. `ORDER BY id DESC`는 큰 글 번호부터 가져옵니다. 글 삭제 기능이 없으므로 새 글의 번호가 최신순 기준이 됩니다.

## HTML 문자열과 안전한 표시

`string.Template`의 `$entries`, `$name` 등은 서버가 값을 채우는 자리입니다. JavaScript 변수가 아닙니다. Template은 자동으로 HTML을 보호하지 않으므로 사용자 입력은 `html.escape()`한 뒤 넣습니다.

예를 들어 `<script>`를 입력해도 화면에서는 그 문자열이 보입니다. SQL에 값을 따로 전달하는 처리와 HTML 특수문자 처리는 서로 다른 단계이며 둘 다 필요합니다.

## 조금 더 익힐 부분

- `lifespan`: 서버가 켜질 때 DB를 준비하는 FastAPI 방식입니다.
- `LimitRequestBody`: 폼을 해석하기 전에 요청의 실제 바이트 수를 검사하는 클래스입니다. 일반 화면 코드보다 복잡한 이유는 `Content-Length` 헤더가 없는 요청도 제한하기 위해서입니다.
- `async` 미들웨어: 브라우저가 보낸 본문을 받는 부분에만 사용합니다. 짧은 SQLite 저장·조회 경로는 일반 `def` 함수입니다.
- 테스트의 `tmp_path`와 `monkeypatch`: 실제 방명록 파일 대신 테스트 전용 DB를 사용하도록 경로를 잠시 바꿉니다.

## 실제 참고한 문서

- [FastAPI Form 입력](https://fastapi.tiangolo.com/tutorial/request-forms/)
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html)
