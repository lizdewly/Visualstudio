# note-demo

작은 생각을 기록하고 나누는 Flask·SQLite 게시판입니다. `design.md`의 따뜻한 종이색과 편집 디자인을 적용했습니다. 별도의 Node.js·프런트엔드 빌드·외부 DB 서비스는 필요하지 않습니다.

## 구현된 기능

- 이메일·닉네임 회원가입, 비밀번호 해시 저장, 로그인·로그아웃, DB 세션
- 제목만 표시하는 목록, 페이지당 10개, 글 작성·상세·본인 수정·삭제
- 게시글별 댓글, 관리자 키워드 추가·삭제, 제목·내용·댓글 마스킹
- SQLite 영속 저장, 비파괴 스키마 초기화, 백업·복구 명령
- CSRF·서버 권한 검사·HTML 이스케이프·로그인 시도 제한

SNS 로그인과 비밀번호 찾기는 아직 제공하지 않습니다.

## Windows에서 처음 실행

검증 환경: Python 3.13.15. 아래 명령은 프로젝트 폴더의 PowerShell에서 실행합니다. 가상환경 활성화가 필요하지 않으므로 실행 정책 변경도 필요 없습니다.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe tools/setup.py --data-dir .runtime
$env:NOTE_DEMO_CONFIG = Join-Path (Get-Location) '.runtime\config.json'
.\.venv\Scripts\python.exe -m flask --app app init-db
.\.venv\Scripts\python.exe -m flask --app app seed-rules
.\.venv\Scripts\python.exe run.py
```

브라우저에서 [http://127.0.0.1:5000](http://127.0.0.1:5000)에 접속합니다. 종료는 실행 터미널에서 `Ctrl+C`입니다. 포트가 이미 사용 중이면 기존 실행을 종료한 뒤 다시 시작하세요.

현재 작업 공간에는 `.venv`와 `.runtime` 초기 설정이 준비되어 있습니다. 다시 실행할 때는 다음 한 줄이면 됩니다.

```powershell
.\.venv\Scripts\python.exe run.py
```

로컬 확인용으로 만든 `preview@example.test` 계정과 `[화면 테스트]` 글·댓글이 `.runtime`에 있습니다. 비밀번호는 사용자용 기본 계정으로 배포하지 않습니다. 직접 회원가입해서 사용하세요. 배포 ZIP에는 `.runtime`, 해당 계정·글, 비밀 설정이 포함되지 않습니다.

## 관리자 생성

기본 관리자는 없습니다. 다음 명령에서 이메일·닉네임·새 비밀번호를 직접 입력합니다. 비밀번호는 화면에 표시되지 않습니다. 기존 일반 사용자를 자동 승격하지 않으므로 다른 이메일을 사용하세요.

```powershell
$env:NOTE_DEMO_CONFIG = Join-Path (Get-Location) '.runtime\config.json'
.\.venv\Scripts\python.exe -m flask --app app auth create-admin
```

생성한 계정으로 로그인하면 상단에 **표현 관리**가 표시됩니다.

## 저장되는 위치와 업데이트

로컬 기본 데이터는 `.runtime/note-demo.sqlite3`, 설정은 `.runtime/config.json`입니다. 로컬 편의상 저장소 내부의 제외 디렉터리를 사용하며 Git·배포 패키지에 포함하지 않습니다. PythonAnywhere에서는 반드시 소스 폴더 밖의 데이터 디렉터리를 사용합니다.

서버를 끄거나 다시 실행해도 계정·글·댓글·규칙은 유지됩니다. `init-db`는 기존 테이블·데이터를 삭제하지 않습니다. 스키마 변경을 자동으로 수행하는 마이그레이션 도구는 아니므로 미래 구조 변경은 백업 후 별도로 적용해야 합니다.

`seed-rules`는 초기 설정에서만 실행하세요. 재실행하면 관리자가 삭제했던 초기 규칙도 다시 추가할 수 있습니다. 서비스 시작이나 업데이트 시에는 실행하지 않습니다.

세션은 24시간 유효합니다. 로그아웃 또는 만료 후에는 다시 로그인해야 하며 게시글은 그대로 남습니다. 비밀키를 바꾸면 기존 로그인 쿠키가 무효화됩니다.

## 테스트와 배포 파일 생성

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe tools/package.py
.\.venv\Scripts\python.exe tools/check_package.py
```

테스트는 자동 생성한 임시 DB만 사용합니다. 테스트 환경의 임시 디렉터리 쓰기 권한이 필요합니다. 배포 파일은 `dist/note-demo-pythonanywhere.zip`입니다. `check_package.py`는 ZIP에 DB·비밀 설정이 없는지 검사하고 별도 폴더에서 앱과 WSGI를 테스트합니다. 최종 16개 테스트를 통과했습니다.

## 운영 문서

- [PythonAnywhere 배포·백업·복구](docs/deployment-pythonanywhere.md)
- [실행한 검증과 남은 배포 검증](docs/verification.md)
- [디자인 적용 기준](docs/design-implementation.md)
- [마스킹 자료 출처와 한계](docs/masking-sources.md)

의존성은 2026-10-27 실제 설치·검증한 버전으로 고정했습니다. 공개 배포 전 계정의 Python 버전·무료 플랜 조건을 다시 확인하세요. 실제 PythonAnywhere 계정이 제공되지 않아 원격 배포는 수행하지 않았습니다.
