"""환경변수로 Supabase에 연결하는 방명록과 사용자 API."""

import psycopg
from psycopg import sql
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool
from fastapi.exception_handlers import request_validation_exception_handler

import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path
from string import Template
from typing import Annotated

from fastapi import FastAPI, Form, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=False)
DB_SCHEMA = "kdt_api01"
PAGE_SIZE = 10
MAX_ENTRIES = 1000
MAX_BODY_BYTES = 16 * 1024
KOREA_TIME = timezone(timedelta(hours=9))
PAGE_TEMPLATE = Template((BASE_DIR / "templates" / "index.html").read_text(encoding="utf-8"))
HTML_HEADERS = {
    "Content-Security-Policy": "default-src 'none'; style-src 'self'; img-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'",
    "X-Content-Type-Options": "nosniff",
    "Cache-Control": "no-store",
}


class GuestbookEntry(BaseModel):
    # 브라우저의 required/maxlength와 별도로 서버에서도 검사합니다.
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=20)
    message: str = Field(min_length=1, max_length=500)

    @field_validator("name", "message")
    @classmethod
    def reject_null_character(cls, value: str) -> str:
        if "\x00" in value:
            raise ValueError("널 문자는 사용할 수 없습니다.")
        return value


def get_db_config():
    required = ("PGHOST", "PGDATABASE", "PGUSER", "PGPASSWORD")
    missing = [key for key in required if not os.environ.get(key)]
    if missing:
        raise RuntimeError("DB 환경변수를 설정해 주세요: " + ", ".join(missing))
    return {
        "host": os.environ["PGHOST"],
        "port": int(os.environ.get("PGPORT", "5432")),
        "dbname": os.environ["PGDATABASE"],
        "user": os.environ["PGUSER"],
        "password": os.environ["PGPASSWORD"],
        "sslmode": "require",
        "connect_timeout": 10,
    }


def connect_db():
    connection = psycopg.connect(
        **get_db_config(), row_factory=dict_row, prepare_threshold=None,
    )
    try:
        # 현재 트랜잭션에서만 스키마를 지정하여 pooler의 다른 연결에 영향을 주지 않습니다.
        connection.execute(
            sql.SQL("SET LOCAL search_path TO {}").format(sql.Identifier(DB_SCHEMA))
        )
    except BaseException:
        connection.close()
        raise
    return connection


def initialize_db():
    with connect_db() as connection:
        connection.execute(
            sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(DB_SCHEMA))
        )
        connection.execute("""
                CREATE TABLE IF NOT EXISTS guestbook (
                    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    name TEXT NOT NULL CHECK(length(name) BETWEEN 1 AND 20),
                    message TEXT NOT NULL CHECK(length(message) BETWEEN 1 AND 500),
                    created_at TEXT NOT NULL
                )
            """)


def save_entry(entry: GuestbookEntry) -> bool:
    with connect_db() as connection:
        # 글 수 확인과 저장을 직렬화하여 동시 등록에서도 한도를 지킵니다.
        connection.execute("LOCK TABLE guestbook IN SHARE ROW EXCLUSIVE MODE")
        count = connection.execute("SELECT COUNT(*) AS total FROM guestbook").fetchone()["total"]
        if count >= MAX_ENTRIES:
            return False
        connection.execute(
            "INSERT INTO guestbook (name, message, created_at) VALUES (%s, %s, %s)",
            (entry.name, entry.message, datetime.now(KOREA_TIME).isoformat(timespec="seconds")),
        )
    return True


def read_entries(page: int):
    with connect_db() as connection:
        # 개수와 목록을 같은 시점의 데이터로 읽습니다.
        connection.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY")
        total = connection.execute("SELECT COUNT(*) AS total FROM guestbook").fetchone()["total"]
        pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
        page = min(page, pages)
        entries = connection.execute(
            "SELECT id, name, message, created_at FROM guestbook ORDER BY id DESC LIMIT %s OFFSET %s",
            (PAGE_SIZE, (page - 1) * PAGE_SIZE),
        ).fetchall()
    return entries, total, page, pages


def render_guestbook(page=1, notice="", name="", message="", status_code=200):
    entries, total, page, pages = read_entries(page)
    cards = []
    for entry in entries:
        # DB에 저장된 글도 신뢰하지 않고 HTML에 넣기 직전에 이스케이프합니다.
        written_at = datetime.fromisoformat(entry["created_at"]).astimezone(KOREA_TIME)
        cards.append(
            '<article class="entry">'
            '<div class="entry-heading">'
            f'<h3>{escape(entry["name"])}</h3>'
            f'<time datetime="{escape(entry["created_at"], quote=True)}">'
            f'{written_at:%Y.%m.%d %H:%M}</time></div>'
            f'<p class="message">{escape(entry["message"])}</p></article>'
        )
    if not cards:
        cards.append('<p class="empty">아직 남겨진 글이 없어요.<br>첫 번째 인사를 남겨 주세요.</p>')

    links = []
    if page > 1:
        links.append(f'<a href="/?page={page - 1}#entries" rel="prev">← 이전</a>')
    links.append(f'<span aria-current="page">{page} / {pages} 페이지</span>')
    if page < pages:
        links.append(f'<a href="/?page={page + 1}#entries" rel="next">다음 →</a>')

    notice_html = f'<p class="notice" role="status">{escape(notice)}</p>' if notice else ""
    content = PAGE_TEMPLATE.substitute(
        notice=notice_html,
        name=escape(name, quote=True),
        message=escape(message),
        entries="\n".join(cards),
        pagination="\n".join(links),
        total=total,
        max_entries=MAX_ENTRIES,
    )
    return HTMLResponse(content, status_code=status_code, headers=HTML_HEADERS)


def error_response(message: str, status_code: int):
    # 저장소에 문제가 있어도 DB를 다시 조회하지 않고 안내를 표시합니다.
    content = (
        '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>요청 안내 · 작은 방명록</title><link rel="stylesheet" href="/static/style.css">'
        '</head><body><main class="error-page"><h1>요청을 확인해 주세요</h1>'
        f'<p role="alert">{escape(message)}</p><a href="/">방명록으로 돌아가기</a>'
        '</main></body></html>'
    )
    return HTMLResponse(content, status_code=status_code, headers=HTML_HEADERS)


class LimitRequestBody:
    """폼을 해석하기 전에 본문을 최대 16 KiB까지만 받는 작은 ASGI 미들웨어."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if (
            scope["type"] != "http"
            or scope["method"] != "POST"
            or scope["path"] != "/entries"
        ):
            await self.app(scope, receive, send)
            return

        headers = dict(scope["headers"])
        content_type = headers.get(b"content-type", b"").split(b";", 1)[0].strip().lower()
        # 파일 첨부 없는 기본 HTML form 형식만 받습니다.
        if content_type != b"application/x-www-form-urlencoded":
            response = error_response("방명록의 입력 폼으로 글을 등록해 주세요.", 415)
            await response(scope, receive, send)
            return

        body = bytearray()
        while True:
            event = await receive()
            if event["type"] == "http.disconnect":
                return
            chunk = event.get("body", b"")
            if len(body) + len(chunk) > MAX_BODY_BYTES:
                response = error_response("요청이 너무 큽니다. 16 KiB 이하로 보내 주세요.", 413)
                await response(scope, receive, send)
                return
            body.extend(chunk)
            if not event.get("more_body", False):
                break

        # 검사가 끝난 본문을 FastAPI Form에 한 번 전달합니다.
        delivered = False

        async def receive_checked_body():
            nonlocal delivered
            if not delivered:
                delivered = True
                return {"type": "http.request", "body": bytes(body), "more_body": False}
            return await receive()

        await self.app(scope, receive_checked_body, send)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_in_threadpool(initialize_db)
    await run_in_threadpool(initialize_users)
    yield


# Swagger와 기존 HTML 방명록을 함께 제공합니다.
app = FastAPI(
    title="방명록과 사용자 API 실습", 
    lifespan=lifespan,
)
app.add_middleware(LimitRequestBody)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.exception_handler(RequestValidationError)
async def invalid_request(request: Request, error: RequestValidationError):
    if request.url.path.startswith("/users"):
        return await request_validation_exception_handler(request, error)
    
    return error_response("입력 형식을 확인해 주세요. 페이지 번호는 1 이상의 정수여야 합니다.", 422)


@app.exception_handler(psycopg.Error)
async def database_error(request: Request, error: psycopg.Error):
    if request.url.path.startswith("/users") or request.url.path == "/health":
        return JSONResponse({"detail": "저장소를 사용할 수 없습니다."}, status_code=503)
    return error_response("저장소를 사용할 수 없습니다. 잠시 후 다시 시도해 주세요.", 503)


@app.get("/health")
def health():
    with connect_db() as connection:
        connection.execute("SELECT id FROM guestbook LIMIT 1").fetchone()
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home(page: Annotated[int, Query(ge=1, le=MAX_ENTRIES)] = 1, saved: bool = False):
    notice = "글을 등록했습니다. 인사를 남겨 주셔서 고맙습니다." if saved else ""
    return render_guestbook(page=page, notice=notice)


@app.post("/entries", response_class=HTMLResponse)
def create_entry(name: Annotated[str, Form()] = "", message: Annotated[str, Form()] = ""):
    try:
        entry = GuestbookEntry(name=name, message=message)
    except ValidationError:
        return render_guestbook(
            notice="이름은 1~20자, 내용은 1~500자로 입력해 주세요. 공백만 쓰거나 널 문자를 넣을 수 없습니다.",
            name=name, message=message, status_code=422,
        )
    if not save_entry(entry):
        return render_guestbook(
            notice=f"방명록이 가득 찼습니다. 최대 {MAX_ENTRIES:,}개까지 기록할 수 있습니다.",
            name=name, message=message, status_code=409,
        )
    # POST 결과 화면을 새로고침해 같은 글이 다시 등록되는 것을 줄입니다.
    return RedirectResponse(url="/?saved=true", status_code=303)

router = APIRouter(tags=["users"])


class UserCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )
    name: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=1, max_length=100)


def initialize_users():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            );
        """)


def get_user_connection(request: Request):
    return connect_db()


@router.post("/users", status_code=201)
def create_user(user: UserCreate, request: Request):
    with get_user_connection(request) as conn:
        row = conn.execute(
            """
            INSERT INTO users (name, email)
            VALUES (%s, %s)
            RETURNING id, name, email;
            """,
            (user.name, user.email),
        ).fetchone()
    return row


@router.get("/users")
def list_users(request: Request):
    with get_user_connection(request) as conn:
        rows = conn.execute("""
            SELECT id, name, email
            FROM users
            ORDER BY id;
        """).fetchall()
    return rows


app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "9000")),
    )
