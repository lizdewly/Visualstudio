# 무료 배포 조사와 절차

공식 문서 확인일: 2026-10-23 (Asia/Seoul)

이 문서는 배포 준비 안내입니다. 로컬 앱 구현·패키지 설치·28개 테스트·브라우저 검증을 완료했습니다. 외부 서비스의 계정 가입, 패키지 설치, 사이트 생성, 공개 배포는 수행하지 않았습니다. 아래 명령은 검증한 앱을 호스팅 계정으로 옮길 때 사용하는 예시입니다.

## 후보 비교

| 후보 | Python 서버 / SQLite 파일 | 이번 프로젝트 판단 |
| --- | --- | --- |
| PythonAnywhere Beginner | 무료 Python 웹 앱과 파일 공간 제공. SQLite 사용 가능. FastAPI용 ASGI 배포는 베타 | 우선 검토 후보. 계정에서 ASGI 무료 사용 가능 여부와 만료 연장 방법을 확인한 뒤 선택 |
| Render Free Web Service | FastAPI 실행 가능. 로컬 SQLite 파일은 재시작·재배포·절전 시 사라짐. 무료 인스턴스에 영구 디스크 연결 불가 | 데이터가 유지되는 방명록용으로 부적합. 폐기 가능한 시연에만 적합 |

Render가 무료 Python 서버를 제공한다는 것과 SQLite 데이터를 영구 보관한다는 것은 다릅니다. 이 앱을 Render Free에 그대로 올리면 기록 보존 조건을 만족하지 못합니다. [Render 무료 제한](https://render.com/docs/free)

PythonAnywhere는 모든 계정에 SQLite를 제공하지만 클라우드 파일 시스템의 성능 때문에 운영용 DB로 권장하지 않습니다. 여기서는 소규모 학습용 방명록의 후보로만 평가합니다. [DB 안내](https://help.pythonanywhere.com/pages/KindsOfDatabases/)

## PythonAnywhere 무료 범위

- 무료 계정: 웹 앱 1개, 웹 워커 1개, 디스크 512 MiB, 콘솔 2개, CPU 할당량 100초, 웹 앱 만료 주기 1개월.
- CPU 초 제한은 콘솔·작업 실행에 적용되며 웹 앱 요청의 실행 시간과는 구분됩니다.
- 무료 계정의 외부 인터넷 접근에는 제한이 있습니다. 방명록 기능은 외부 API 없이 구성합니다.
- 유료 사용자 도메인 대신 제공되는 기본 도메인을 사용합니다.

출처: [무료 계정 기능](https://help.pythonanywhere.com/pages/FreeAccountsFeatures/), [가격 및 CPU 설명](https://www.pythonanywhere.com/pricing/)

**FastAPI 관련 제한:** 공식 ASGI 안내에는 베타 기능이며 명령/API와 장기 가격이 확정되지 않았다고 명시되어 있습니다. 따라서 영구 무료라고 보장할 수 없습니다. 정적 파일 매핑도 지원하지 않으므로 CSS는 FastAPI의 `StaticFiles` 등으로 제공합니다. [ASGI 공식 안내](https://help.pythonanywhere.com/pages/ASGICommandLine/)

## PythonAnywhere 배포 순서

1. Beginner 무료 계정을 선택합니다. 계정에서 ASGI 사용 조건과 현재 무료 제공 여부를 확인합니다. 유료 전환을 요구하면 그 단계에서 중단합니다.
2. `main.py`, `requirements.txt`, `templates/index.html`, `static/style.css`를 같은 폴더 구조로 `/home/YOURUSERNAME/guestbook`에 업로드합니다. 로컬 `.venv`, 캐시, 테스트 DB는 업로드하지 않습니다. 앱은 첫 시작 때 `data/guestbook.db`를 생성하므로 이 폴더에 쓰기 권한이 있어야 합니다.
3. Bash 콘솔에서 해당 계정이 지원하는 Python 버전을 선택해 가상 환경을 만들고 실행 의존성만 설치합니다. 아래 `python3.10`은 공식 ASGI 안내의 예시이며, 프로젝트 요구 버전과 계정 제공 버전을 함께 확인합니다.

```bash
mkvirtualenv guestbook --python=python3.10
cd /home/YOURUSERNAME/guestbook
pip install --no-cache-dir -r requirements.txt
```

4. 설치 후 공간을 확인합니다. 소스 외에 가상 환경, DB, 로그가 모두 디스크 사용량에 포함됩니다.

```bash
du -sh /home/YOURUSERNAME/.virtualenvs/guestbook /home/YOURUSERNAME/guestbook
```

5. 공식 CLI 방식에는 계정 API 토큰과 배포용 `pythonanywhere` 패키지가 추가로 필요합니다. 이는 앱의 실행 라이브러리와 구분되는 배포 도구이며, 실제 사용 전에 추가 확인받습니다. Account → API token에서 발급하되 토큰을 소스나 기록 문서에 적지 않습니다. [토큰 발급 안내](https://help.pythonanywhere.com/pages/GettingYourAPIToken/)

6. ASGI 안내에 따라 새 Bash 콘솔에서 CLI를 준비하고 사이트를 생성합니다. `YOURUSERNAME`은 실제 계정명으로 바꾸며 EU 계정은 해당 지역 도메인으로 바꿉니다.

```bash
pip install --upgrade pythonanywhere
pa website create --domain YOURUSERNAME.pythonanywhere.com --command '/home/YOURUSERNAME/.virtualenvs/guestbook/bin/uvicorn --app-dir /home/YOURUSERNAME/guestbook --uds ${DOMAIN_SOCKET} main:app'
pa website get --domain YOURUSERNAME.pythonanywhere.com
```

이 명령은 Linux Bash용입니다. `${DOMAIN_SOCKET}`은 플랫폼이 제공하는 값으로, 위처럼 작은따옴표 안에 그대로 둡니다. Windows 로컬 서버에는 이 소켓 옵션을 사용하지 않습니다.

7. 제공된 HTTPS 주소에서 글 등록·목록·CSS·한글 표시를 확인합니다. 서버를 재시작한 뒤 같은 글이 남아 있는지도 확인합니다. ASGI 사이트의 관리 화면은 일반 Web 화면과 다를 수 있습니다.
8. 웹 앱 만료일과 연장 방법을 계정 관리 화면/지원 안내에서 확인하고, 디스크·로그 사용량을 주기적으로 점검합니다. ASGI에 일반 웹 앱의 연장 UI가 그대로 제공된다고 가정하지 않습니다.
9. 운영 DB 경로를 유지하고 재배포 시 새 빈 DB로 덮어쓰지 않습니다. 백업은 쓰기를 중단한 상태에서 파일을 내려받거나 SQLite 백업 기능을 이용합니다.

ASGI 생성·조회 명령 출처: [공식 배포 절차](https://help.pythonanywhere.com/pages/ASGICommandLine/). 이 절차는 문서 확인 결과이며 계정에서 실증한 배포 결과가 아닙니다.

## 무료 범위 유지 계획

- 앱에 구현한 상한: 글 1,000개, 이름 20자, 내용 500자, 한 페이지 10개, 요청 16 KiB.
- 실행 환경 하나와 웹 워커 하나만 사용하고 이미지 업로드, 외부 저장소, 예약 작업을 추가하지 않습니다.
- 개발용 테스트 패키지를 배포 환경에 설치하지 않습니다.
- 조회를 위한 자동 새로고침이나 절전 방지 요청을 만들지 않습니다.
- 앱의 글 수 제한은 저장량을 줄이지만, 무제한 트래픽·스팸을 해결하지는 않습니다. 공개 학습용 범위에서 실제 사용량을 확인해야 합니다.
- 무료 플랜의 현재 조건이 맞지 않으면 자동으로 유료 플랜이나 다른 DB를 선택하지 않고 다음 구성을 사용자와 정합니다.

로컬 측정값: 실행용 소스 네 파일은 합계 15,525바이트이고 테스트 도구를 포함한 Windows 가상 환경은 약 33.75 MiB였습니다. Linux 호스팅의 설치 크기·로그·기존 파일은 다르므로, 512 MiB 안에 들어간다는 최종 판단은 배포 계정에서 설치 후 다시 측정해야 합니다. 트래픽·호스팅 만료 정책은 소스 크기와 별개입니다.

이번 조사에서 **기존 FastAPI 유지 + SQLite 보존 + 장기 무료 보장**을 모두 확정할 수 있는 서비스는 확인하지 못했습니다. PythonAnywhere는 조건부 후보이며, Render Free는 기록 보존 요건 때문에 제외합니다.
