# 구현·실행 검증 기록

기준일: 2026-10-27 (Asia/Seoul). 로컬 Windows, Python 3.13.15, Flask 3.1.3, Flask-WTF 1.3.0, Werkzeug 3.1.9. 실제 설치 버전은 `requirements.txt`에 고정했다.

## 수행한 검증

| 항목 | 결과 및 근거 |
| --- | --- |
| 가상환경·의존성 | 프로젝트 .venv 생성 및 설치 완료, `python -m pip check` 통과 |
| Python 문법 | `python -m compileall -q app tools tests wsgi.py run.py` 통과 |
| 자동 테스트 | HTTPS 인증·관리자 CLI 포함 최종 **16개 모두 통과**, 2.953초 |
| 배포 패키지 독립 실행 | ZIP을 별도 임시 폴더에 풀고 그 안의 코드로 전체 16개 테스트 실행, `PACKAGE_OK` 확인. 런타임 DB·비밀 설정 제외 검사 통과 |
| 브라우저 실제 흐름 | 회원가입 → 로그인 → 글 작성 → 상세 → 댓글 작성 → 본인 수정 성공 |
| 프로세스 재시작 | 실제 서버를 종료·재시작한 후 기존 글과 댓글이 브라우저에 유지되는 것 확인 |
| 화면 | 인앱 브라우저에서 목록·빈 상태·회원 폼·작성·상세·수정 화면 확인, `docs/preview.png` 저장 |
| 브라우저 콘솔 | 최종 목록 화면 warn/error 로그 없음 |
| 배포 보안 모드 | WSGI 별도 프로세스 import, debug off, Secure/HttpOnly/SameSite 쿠키, 비밀 설정 URL 비노출 자동 검증 |
| 영속성·복구 | 초기화 재실행 비파괴, 앱 재생성 후 보존, 삭제한 규칙 미복원, SQLite 백업 복구와 세션 폐기 자동 검증 |

## 테스트 범위

최종 패키지 검증 출력: `Ran 16 tests in 2.953s`, `OK`, `PACKAGE_OK: source-only archive, isolated tests and WSGI import passed.` 소스 코드 검증 후 이 결과 문서만 갱신하여 ZIP을 다시 생성했다.

`tests/test_app.py`는 실제 CSRF 토큰과 SQLite 임시 DB를 사용한다. CSRF를 끄고 테스트하지 않는다.

- R1: 가입 검증·정규화 이메일 중복·해시 저장·재시작 후 재로그인
- R2~R3: 로그인 실패·성공·만료·로그아웃 후 쿠키 재사용 거부
- R4: 비밀번호 찾기 미구현(향후 기능)
- R5~R5-3: 글 CRUD·공백 거부·0/1/10/11/21개 페이지·안정 정렬·잘못된 page 보정·삭제 후 페이지 보정·작성자 권한·위조 작성자 거부
- R5-4: 댓글 분리·공백/비로그인 거부·게시글 삭제 시 연결 댓글 제거
- R5-5: 리터럴 특수문자·반복/겹친 키워드·정상 문장·Unicode 오프셋·HTML 이스케이프·일반 응답 원문 비노출
- R5-5-1: 관리자 규칙 추가/중복/공백/삭제·일반 사용자 접근 거부·기존 글 재마스킹·DB 영속성
- 운영: 백업·복구·이전 세션 폐기·설정 누락 시 실행 거부·반복 인증 제한·HTTPS CSRF 및 관리자 CLI

초기 표현 조사 19개와 출처는 `docs/masking-sources.md`에 기록했다. 테스트에서 정상 문장 오탐 사례를 일부 확인했지만 모든 맥락·신조어를 검증한 것은 아니다.

## 실행 명령

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m compileall -q app tools tests wsgi.py run.py
.\.venv\Scripts\python.exe tools/package.py
.\.venv\Scripts\python.exe tools/check_package.py
```

가상환경의 ensurepip, 패키지 다운로드, 임시 DB 테스트가 기본 실행 제한으로 실패하여 필요한 명령은 허용된 확장 권한으로 다시 실행했다. 애플리케이션 코드를 변경해서 제한을 우회한 것이 아니다.

## 미수행 또는 제한된 검증

- 사용자가 PythonAnywhere 계정·URL이 없다고 답변하여 실제 업로드, PythonAnywhere Linux 웹 워커, TLS, Web Reload, 계정 디스크 권한 테스트는 미수행.
- 로컬 WSGI 테스트는 실제 PythonAnywhere에서의 배포 성공을 의미하지 않는다.
- 현재 브라우저 뷰포트에서 시각 검증을 수행했다. 모바일 375px·다른 브라우저·운영체제별 글꼴의 별도 실기기 검증은 미수행. 반응형 CSS는 구현했다.
- 동시 사용자 부하 시험·외부 침투 테스트·이메일 주소 소유권 확인은 수행하지 않았다.
- SNS 로그인·비밀번호 찾기는 승인된 현재 범위에서 제외했다.

실행 중 생성한 로컬 테스트 계정·글과 사용자가 추가한 데이터는 `.runtime`에 보존했다. 배포 ZIP에는 DB와 비밀 설정을 포함하지 않는다. DB를 삭제해 화면을 초기화하지 않았다.
