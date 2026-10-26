"""운영 DB 대신 테스트마다 별도의 임시 SQLite 파일을 사용합니다."""

import sqlite3
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from html import escape

import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "guestbook.db")
    with TestClient(main.app) as test_client:
        yield test_client


def rows():
    with closing(sqlite3.connect(main.DB_PATH)) as connection:
        return connection.execute("SELECT name, message FROM guestbook ORDER BY id").fetchall()


def fill_database(count):
    with closing(sqlite3.connect(main.DB_PATH)) as connection:
        with connection:
            connection.executemany(
                "INSERT INTO guestbook (name, message, created_at) VALUES (?, ?, ?)",
                [(f"이름{i}", f"내용{i}", "2026-10-23T12:00:00+09:00") for i in range(count)],
            )


def test_empty_page_and_stylesheet(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "아직 남겨진 글이 없어요" in response.text
    assert '<form action="/entries" method="post"' in response.text
    assert "<script" not in response.text
    assert client.get("/static/style.css").status_code == 200
    assert client.get("/docs").status_code == 404
    assert client.get("/data/guestbook.db").status_code == 404


def test_register_redirect_and_refresh(client):
    response = client.post("/entries", data={"name": "  방문자  ", "message": "  반갑습니다\n좋은 하루!  "}, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/?saved=true"
    page = client.get(response.headers["location"])
    assert "글을 등록했습니다" in page.text
    assert "반갑습니다\n좋은 하루!" in page.text
    client.get(response.headers["location"])
    assert rows() == [("방문자", "반갑습니다\n좋은 하루!")]


@pytest.mark.parametrize("data", [
    {},
    {"name": "방문자"},
    {"message": "안녕"},
    {"name": "", "message": "안녕"},
    {"name": " \t ", "message": "안녕"},
    {"name": "방문자", "message": "\n\t "},
    {"name": "가" * 21, "message": "안녕"},
    {"name": "방문자", "message": "가" * 501},
    {"name": "가\x00나", "message": "안녕"},
    {"name": "방문자", "message": "가\x00나"},
])
def test_invalid_input_does_not_change_records(client, data):
    client.post("/entries", data={"name": "기존", "message": "보존할 글"})
    response = client.post("/entries", data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 422
    assert "이름은 1~20자" in response.text
    assert rows() == [("기존", "보존할 글")]


@pytest.mark.parametrize("name, message", [("가", "나"), ("가" * 20, "나" * 500)])
def test_valid_length_boundaries(client, name, message):
    response = client.post("/entries", data={"name": name, "message": message}, follow_redirects=False)
    assert response.status_code == 303
    assert rows() == [(name, message)]


def test_html_and_sql_are_treated_as_text(client):
    name = '\"><b>방문자</b>'
    message = "<script>alert('x')</script>\n'); DROP TABLE guestbook; -- & $name"
    client.post("/entries", data={"name": name, "message": message})
    response = client.get("/")
    assert escape(name) in response.text
    assert escape(message) in response.text
    assert "<script>" not in response.text
    assert rows() == [(name, message)]
    # 잘못된 입력을 다시 폼에 표시할 때도 태그와 따옴표를 이스케이프합니다.
    invalid_message = "</textarea><script>alert(1)</script>" + "가" * 500
    rejected = client.post("/entries", data={"name": name, "message": invalid_message})
    assert rejected.status_code == 422
    assert escape(invalid_message) in rejected.text
    assert '<script>' not in rejected.text


def test_latest_first_and_pagination(client):
    fill_database(11)
    first = client.get("/")
    assert first.text.count('<article class="entry">') == 10
    assert first.text.index("<h3>이름10</h3>") < first.text.index("<h3>이름9</h3>")
    assert "<h3>이름0</h3>" not in first.text
    assert '/?page=2#entries' in first.text
    second = client.get("/?page=2")
    assert second.text.count('<article class="entry">') == 1
    assert "<h3>이름0</h3>" in second.text
    assert 'rel="next"' not in second.text
    assert "2 / 2 페이지" in client.get("/?page=999").text


@pytest.mark.parametrize("page", ["0", "-1", "abc", "1.5", "1001"])
def test_invalid_page_number(client, page):
    response = client.get("/", params={"page": page})
    assert response.status_code == 422
    assert "text/html" in response.headers["content-type"]


def test_full_guestbook_preserves_existing_entries(client):
    fill_database(main.MAX_ENTRIES)
    response = client.post("/entries", data={"name": "추가", "message": "가득 찬 후 요청"})
    assert response.status_code == 409
    assert "가득 찼습니다" in response.text
    saved = rows()
    assert len(saved) == main.MAX_ENTRIES
    assert saved[0] == ("이름0", "내용0")
    assert saved[-1] == ("이름999", "내용999")


def test_concurrent_writes_cannot_exceed_capacity(client):
    fill_database(main.MAX_ENTRIES - 1)
    entry = main.GuestbookEntry(name="마지막", message="한 자리")
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(main.save_entry, [entry, entry]))
    assert sorted(results) == [False, True]
    assert len(rows()) == main.MAX_ENTRIES


def test_storage_failure_and_retry(client):
    with closing(sqlite3.connect(main.DB_PATH)) as connection:
        connection.execute("CREATE TRIGGER fail_write BEFORE INSERT ON guestbook BEGIN SELECT RAISE(ABORT, 'test failure'); END")
    response = client.post("/entries", data={"name": "방문자", "message": "저장 실패"})
    assert response.status_code == 503
    assert "저장소를 사용할 수 없습니다" in response.text
    assert "test failure" not in response.text
    assert rows() == []
    with closing(sqlite3.connect(main.DB_PATH)) as connection:
        connection.execute("DROP TRIGGER fail_write")
    assert client.post("/entries", data={"name": "방문자", "message": "재시도"}, follow_redirects=False).status_code == 303
    assert rows() == [("방문자", "재시도")]


def test_single_table_and_persistence_after_restart(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "persistent.db")
    with TestClient(main.app) as first:
        first.post("/entries", data={"name": "기록", "message": "재시작 후에도 남아요"})
    with TestClient(main.app) as restarted:
        assert "재시작 후에도 남아요" in restarted.get("/").text
    with closing(sqlite3.connect(main.DB_PATH)) as connection:
        tables = connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        assert tables == [("guestbook",)]
        assert connection.execute("PRAGMA foreign_key_list(guestbook)").fetchall() == []


def test_oversized_request_with_and_without_content_length(client):
    body = b"name=test&message=" + b"x" * main.MAX_BODY_BYTES
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    assert client.post("/entries", content=body, headers=headers).status_code == 413

    def chunks():
        yield body[:100]
        yield body[100:]

    response = client.post("/entries", content=chunks(), headers=headers)
    assert "content-length" not in response.request.headers
    assert response.status_code == 413
    assert rows() == []


def test_request_at_byte_limit_is_accepted(client):
    prefix = b"name=test&message=hello&unused="
    body = prefix + b"x" * (main.MAX_BODY_BYTES - len(prefix))
    response = client.post("/entries", content=body, headers={"Content-Type": "application/x-www-form-urlencoded"}, follow_redirects=False)
    assert response.status_code == 303
    assert rows() == [("test", "hello")]


def test_unsupported_body_types(client):
    assert client.post("/entries", json={"name": "이름", "message": "내용"}).status_code == 415
    assert client.post("/entries", files={"message": ("file.txt", b"hello")}).status_code == 415
    assert rows() == []
