# Supabase 방명록을 Render에서 실행하기

`/`의 HTML 방명록과 `/users` JSON API 모두 Supabase PostgreSQL을 사용합니다.
테이블은 `kdt_api01.guestbook`, `kdt_api01.users`입니다.
DB 준비는 FastAPI lifespan에서 실행하므로 `python main.py`와 Uvicorn 실행을 모두 지원합니다.
SQLite 파일을 자동으로 읽거나 기존 글을 복사하지는 않습니다.

## 로컬 실행

가상환경이 활성화된 터미널에서 이 폴더로 이동합니다.

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env`의 예시 값을 Supabase 프로젝트의 Connect → Session pooler에 표시된 실제 값으로 바꿉니다.
비밀번호는 Database password이며 API 키가 아닙니다. 비밀번호에는 따옴표를 유지합니다.
`.env`는 Git에 포함하지 않습니다. `.env.example`에는 실제 값을 쓰지 않습니다.

```powershell
python main.py
```

방명록: http://127.0.0.1:9000/ · Swagger: http://127.0.0.1:9000/docs
운영체제 환경변수와 `.env`가 함께 있으면 운영체제 환경변수가 우선합니다.

## Render 설정

GitHub 저장소에 이 폴더의 코드를 올립니다. 실제 접속 정보는 Render에만 입력합니다.
프로젝트 전체가 GitHub 저장소에 있는 경우의 설정입니다.

| 항목 | 값 |
| --- | --- |
| Service Type | Web Service |
| Language | Python 3 |
| Root Directory | `Day12/guestbook` |
| Build Command | `python -m pip install -r requirements.txt` |
| Start Command | `python -m uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/health` |

이 폴더 내용만 별도 저장소의 최상위에 올렸다면 Root Directory는 비웁니다.
기존 Render 서비스가 `Day1-Day8`을 실행 중이면 Root Directory도 변경해야 합니다.
`$PORT`는 Render 입력란에 그대로 적고 `--reload`는 사용하지 않습니다.

서비스의 Environment → Add Environment Variable에서 다음을 입력합니다.

| Key | Value |
| --- | --- |
| PGHOST | Connect → Session pooler의 Host |
| PGPORT | `5432` |
| PGDATABASE | Connect 화면의 Database (일반적으로 `postgres`) |
| PGUSER | Connect → Session pooler의 User |
| PGPASSWORD | Database password 원문 (입력란에서는 따옴표 없이) |

Host에 `https://` 또는 전체 연결 URL을 넣지 않습니다.
`PORT`는 Render가 제공하므로 직접 추가할 필요가 없습니다.
Save, rebuild, and deploy를 선택하고 시작 로그를 확인합니다.
배포 후 서비스 주소의 `/health`에서 `{"status":"ok"}`가 나와야 합니다.
방명록에 테스트 글을 남긴 뒤 재시작 후에도 유지되는지 확인합니다.

## 테스트

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

기본 실행은 DB가 필요 없는 검사만 실행합니다. `.env`를 준비한 후
PowerShell에서 `$env:GUESTBOOK_TEST_DB = "1"`을 설정하면 실제 DB 테스트도 실행합니다.
통합 테스트는 매번 무작위 임시 스키마를 만들고 종료 시 해당 스키마만 삭제합니다.
기존 방명록 데이터와 분리되며 테스트 계정에 스키마 생성 권한이 필요합니다.

## 공식 문서

- [Render 환경변수](https://render.com/docs/configure-environment-variables)
- [Render FastAPI 배포](https://render.com/docs/deploy-fastapi)
- [Render 하위 폴더 배포](https://render.com/docs/monorepo-support)
- [Supabase DB 연결](https://supabase.com/docs/guides/database/connecting-to-postgres)
