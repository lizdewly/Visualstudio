import os
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import psycopg
import pytest
from fastapi.testclient import TestClient
from psycopg import sql

import main


def test_missing_environment_reports_names_only(monkeypatch):
    for key in ("PGHOST", "PGDATABASE", "PGUSER", "PGPASSWORD"):
        monkeypatch.delenv(key, raising=False)
    with pytest.raises(RuntimeError, match="PGHOST.*PGDATABASE.*PGUSER.*PGPASSWORD"):
        main.get_db_config()


@pytest.fixture
def client(monkeypatch):
    if os.environ.get("GUESTBOOK_TEST_DB") != "1":
        pytest.skip("실제 DB 검증은 GUESTBOOK_TEST_DB=1과 PG 환경변수가 필요합니다.")
    schema = "guestbook_test_" + uuid4().hex
    monkeypatch.setattr(main, "DB_SCHEMA", schema)
    try:
        with TestClient(main.app) as client:
            yield client
    finally:
        with psycopg.connect(**main.get_db_config()) as connection:
            connection.execute(
                sql.SQL("DROP SCHEMA IF EXISTS {} CASCADE").format(sql.Identifier(schema))
            )


def test_form_and_json_use_postgres(client):
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/docs").status_code == 200
    response = client.post(
        "/entries", data={"name": "방문자", "message": "Supabase 저장 확인"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert "Supabase 저장 확인" in client.get("/").text
    response = client.post("/users", json={"name": "홍길동", "email": "test@example.com"})
    assert response.status_code == 201
    assert response.json()["name"] == "홍길동"
    assert response.json()["email"] == "test@example.com"
    assert client.get("/users").json() == [response.json()]
    # 새 앱 시작 과정을 거쳐도 저장된 글을 읽습니다.
    with TestClient(main.app) as restarted:
        assert "Supabase 저장 확인" in restarted.get("/").text


def test_invalid_requests_do_not_insert(client):
    response = client.post("/users", json={"name": " ", "email": "invalid@example.com"})
    assert response.status_code == 422
    assert "detail" in response.json()
    assert client.get("/users").json() == []
    assert client.post("/entries", json={"name": "a", "message": "b"}).status_code == 415
    assert client.post("/entries", data={"name": " ", "message": "b"}).status_code == 422
    assert main.read_entries(1)[1] == 0


def test_pagination_and_html_escape(client, monkeypatch):
    monkeypatch.setattr(main, "PAGE_SIZE", 1)
    main.save_entry(main.GuestbookEntry(name="첫째", message="오래된 글"))
    main.save_entry(main.GuestbookEntry(name="둘째", message="<script>alert(1)</script>"))
    first = client.get("/").text
    assert "&lt;script&gt;" in first
    assert "<script>" not in first
    assert "오래된 글" not in first
    assert "오래된 글" in client.get("/?page=2").text


def test_concurrent_writes_respect_capacity(client, monkeypatch):
    monkeypatch.setattr(main, "MAX_ENTRIES", 1)
    entry = main.GuestbookEntry(name="동시 등록", message="한 번만 저장")
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(main.save_entry, [entry, entry]))
    assert sorted(results) == [False, True]
    assert main.read_entries(1)[1] == 1


def test_database_failure_does_not_expose_credentials(client, monkeypatch):
    def broken():
        raise psycopg.OperationalError("private connection details")

    monkeypatch.setattr(main, "connect_db", broken)
    response = client.get("/")
    assert response.status_code == 503
    assert "private connection details" not in response.text
    response = client.get("/health")
    assert response.status_code == 503
    assert "private connection details" not in response.text
