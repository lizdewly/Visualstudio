# PythonAnywhere 배포·보존·복구 안내

확인일: 2026-10-27. 이 문서는 실제 생성된 코드와 명령에 대응합니다. 계정·URL이 없다는 사용자 답변에 따라 원격 업로드나 Web Reload는 실행하지 않았습니다.

## 1. 무료 플랜에 맞춘 구성

Flask WSGI 앱 1개와 SQLite 파일을 사용합니다. 공식 안내상 무료 계정은 웹앱 1개·워커 1개·디스크 512 MiB·웹앱 만료 주기 1개월입니다. 신규 무료 계정에는 MySQL과 일일 예약 작업이 제공되지 않으므로 이 프로젝트는 두 기능에 의존하지 않습니다. 대시보드에서 만료일을 확인하고 기한 전에 연장하세요. [공식 무료 계정 기능](https://help.pythonanywhere.com/pages/FreeAccountsFeatures/)

SQLite는 모든 계정에서 사용 가능하지만 PythonAnywhere는 클라우드 파일 시스템 성능 때문에 운영 DB로 권장하지 않습니다. 이 앱은 소규모 데모용이며 사용량이 늘면 DB·요금제를 재검토하세요. [공식 DB 안내](https://help.pythonanywhere.com/pages/KindsOfDatabases)

무료 계정 외부 인터넷 접근은 허용 목록 제한이 있습니다. 앱은 외부 API·폰트 CDN·웹 검색 없이 동작합니다. 초기 표현 자료는 개발 시 조사한 파일을 포함합니다. [외부 통신 제한](https://help.pythonanywhere.com/pages/403ForbiddenError)

## 2. 소스 업로드와 가상환경

1. 로컬에서 `python tools/package.py`로 ZIP을 만듭니다.
2. PythonAnywhere Files 탭에서 ZIP을 `/home/내계정/`에 업로드합니다.
3. Bash 콘솔을 열고 아래를 실행합니다. `내계정`과 파일 경로를 실제 값으로 바꾸세요. 기존 소스가 있다면 먼저 DB와 설정 위치를 확인하고 필요한 변경 파일만 업데이트하세요.

```bash
mkdir -p /home/내계정/note-demo
unzip /home/내계정/note-demo-pythonanywhere.zip -d /home/내계정/note-demo
cd /home/내계정/note-demo
python3.13 --version
python3.13 -m venv /home/내계정/.virtualenvs/note-demo
source /home/내계정/.virtualenvs/note-demo/bin/activate
python -m pip install -r requirements.txt
python -m pip check
```

로컬에서는 Python 3.13.15로 검증했습니다. 해당 계정 시스템 이미지에서 Python 3.13을 제공하지 않는다면 먼저 Web 탭에서 지원 버전을 확인하세요. 다른 버전을 선택하면 그 버전의 가상환경으로 테스트를 다시 수행해야 합니다. **Web 탭 Python과 virtualenv Python은 일치해야 합니다.** [공식 Flask 배포 안내](https://help.pythonanywhere.com/pages/Flask/)

## 3. 소스 밖 데이터·비밀 설정 생성

```bash
python tools/setup.py --data-dir /home/내계정/note-demo-data --deployment
export NOTE_DEMO_CONFIG=/home/내계정/note-demo-data/config.json
python -m flask --app app init-db
python -m flask --app app seed-rules
python -m flask --app app auth create-admin
python -m unittest discover -s tests -v
```

`setup.py`는 비밀키를 무작위 생성하고 JSON 파일에 저장합니다. 이미 존재하면 수정하지 않습니다. Unix 데이터 폴더 권한은 700, 설정은 600으로 생성합니다. 관리자 비밀번호는 CLI에서 숨김 입력합니다. 소스 코드·문서·공유 로그에 비밀키나 비밀번호를 복사하지 마세요.

위 초기 설정 명령은 첫 배포에 한해 수행합니다. `init-db`는 비파괴적이지만, 업데이트 때 `seed-rules`를 다시 실행하면 삭제했던 초기 규칙이 재추가될 수 있습니다.

## 4. Web 탭과 WSGI

Web → Add a new web app → 무료 기본 도메인 → Manual configuration → 가상환경과 같은 Python 버전을 선택합니다.

- Source code: `/home/내계정/note-demo`
- Working directory: `/home/내계정/note-demo`
- Virtualenv: `/home/내계정/.virtualenvs/note-demo`

Web 탭의 WSGI configuration file을 열어 다음 코드를 사용합니다.

```python
import os
import sys

project = '/home/내계정/note-demo'
if project not in sys.path:
    sys.path.insert(0, project)
os.environ['NOTE_DEMO_CONFIG'] = '/home/내계정/note-demo-data/config.json'

from wsgi import application
```

Bash 콘솔의 `export`만으로 웹 워커 설정이 전달된다고 가정하면 안 됩니다. WSGI에서도 설정 경로를 지정합니다. `run.py`나 `app.run()`을 WSGI에서 실행하지 마세요.

Static files는 다음 한 항목만 설정합니다.

| URL | Directory |
| --- | --- |
| `/static/` | `/home/내계정/note-demo/app/static` |

프로젝트 루트·데이터·설정·백업 디렉터리를 정적 파일로 연결하지 마세요. HTTPS 주소를 사용하고 Web 탭에서 제공하는 Force HTTPS를 활성화합니다. 배포 모드에서는 Secure 쿠키를 사용하므로 HTTP 접속으로 인증을 테스트하면 안 됩니다.

설정 후 **Reload**를 누르고 오류 발생 시 Web 탭 Error log를 확인합니다. 비밀 설정 없이 시작하면 앱은 의도적으로 실행을 거부합니다.

## 5. 원격 배포 후 직접 확인할 항목

- HTTPS 첫 화면, CSS·아이콘 정상 표시, 브라우저 콘솔 오류 여부
- 회원가입·로그인·글 작성·댓글·수정, 다른 사용자 편집 거부
- 관리자 규칙 추가·삭제 및 기존 글에 반영
- 글·댓글·규칙을 저장한 뒤 Web Reload, 재로그인 후 그대로 유지
- `config.json`, DB 파일, 백업 파일 URL 접근 시 404
- 로그아웃 후 이전 페이지의 쓰기 동작 거부
- 휴대폰 폭 375px·태블릿 768px·데스크톱에서 줄바꿈과 버튼 접근
- 실제 계정의 만료일, 디스크 용량, DB 쓰기 잠금 오류 유무

현재 로컬 WSGI import·HTTPS 모드 쿠키·영속성은 자동 테스트로 확인했고, 위 실제 호스팅 환경 항목은 계정이 없어 미검증입니다.

## 6. 코드 업데이트

1. 현재 DB를 백업하고 다운로드합니다.
2. 코드 ZIP의 변경 파일만 소스 디렉터리에 업데이트합니다. `.runtime`, 설정 JSON, 로컬 DB를 업로드하지 않습니다.
3. 가상환경에서 필요할 때 `pip install -r requirements.txt`를 실행합니다.
4. 스키마 변경이 있다면 별도 검토된 변경 명령을 적용합니다. 현재 스키마는 version 1이며 자동 마이그레이션 기능은 없습니다.
5. Web Reload 후 저장 데이터와 사용자 흐름을 확인합니다. 초기 규칙 가져오기는 다시 실행하지 않습니다.

## 7. 백업과 복구

최소 주 1회 및 업데이트 전에 수동 백업합니다. 무료 예약 작업을 전제하지 않습니다.

```bash
cd /home/내계정/note-demo
source /home/내계정/.virtualenvs/note-demo/bin/activate
export NOTE_DEMO_CONFIG=/home/내계정/note-demo-data/config.json
python -m flask --app app backup-db /home/내계정/note-demo-data/backups/backup-20261027.sqlite3
```

이미 있는 백업 파일을 덮어쓰지 않으므로 매번 새 파일명을 사용합니다. SQLite Backup API를 사용해 실행 중 DB의 일관된 백업을 만듭니다. Files 탭에서 로컬로 다운로드한 뒤 서버 백업은 최근 3개 정도만 유지하여 512 MiB 용량을 관리하세요. 백업에는 이메일·해시·글 원문이 있으므로 공개 공유하지 않습니다.

복구는 **Web 탭에서 웹앱을 비활성화해 요청이 중단된 상태**에서 수행합니다. 별도 테스트 DB에서 먼저 연습하세요.

```bash
touch /home/내계정/note-demo-data/note-demo.sqlite3.maintenance
python -m flask --app app restore-db /home/내계정/note-demo-data/backups/backup-20261027.sqlite3 --confirm
```

복구 명령은 백업의 무결성·스키마·외래키를 확인하고 기존 DB도 `.before-restore-시각` 파일로 보존합니다. 복구 후 과거 세션은 폐기됩니다. 유지보수 파일이 남아 있으면 앱은 503을 반환합니다. 확인이 끝나면 해당 `.maintenance` 파일만 Files 탭에서 제거하고 웹앱을 활성화·Reload하세요. 재로그인해 데이터와 관리자 기능을 확인합니다.

## 8. 자주 발생하는 문제

| 증상 | 확인할 사항 |
| --- | --- |
| SECRET_KEY / DATABASE_PATH 오류 | WSGI의 NOTE_DEMO_CONFIG, JSON 절대 경로·읽기 권한 |
| 저장소 503 | init-db 실행 여부, DB 상위 폴더 쓰기 권한, maintenance 파일, 동시 쓰기 잠금 |
| 로그인 반복 또는 CSRF 오류 | HTTPS 접속, 고정 비밀키, 쿠키, 폼 새로고침, Web/venv 버전 일치 |
| Reload 후 데이터가 사라져 보임 | 서로 다른 DB 경로를 쓰고 있지 않은지, 소스 배포에 DB를 덮어썼는지 |
| ModuleNotFoundError | 가상환경 경로, requirements 설치, WSGI sys.path |
| CSS 미적용 | /static/ 매핑과 실제 app/static 폴더 |

PythonAnywhere 계정 생성·요금제 변경·실제 배포는 이번 작업에서 수행하지 않았습니다.
