# 방명록 검증 결과

확인일: 2026-10-23 (Asia/Seoul)

## 실행 환경

- Windows / Python 3.13
- FastAPI 0.159.1, Pydantic 2.14.1, Uvicorn 0.54.0
- python-multipart 0.0.32
- 개발 검증: pytest 8.3.5, HTTPX 0.28.1

FastAPI·Pydantic·Uvicorn은 작업 공간의 기존 가상 환경에서 확인한 버전과 맞추고, 이 프로젝트의 독립 `.venv`에 설치했습니다. Day8의 과거 requirements 파일은 변경하지 않았습니다.

## 자동 검증

실제로 실행한 명령:

```powershell
py -m py_compile main.py test_guestbook.py
.\.venv\Scripts\python.exe -m pytest test_guestbook.py -q --basetemp=.test-tmp
.\.venv\Scripts\python.exe -m pip check
```

- Python 구문 검사: 통과.
- pytest: **28 passed, 1 warning in 0.76s**.
- pip check: **No broken requirements found.**

| 검사 | 확인한 결과 |
| --- | --- |
| 빈 목록과 CSS | HTML 200, CSS 200, JavaScript 없음 |
| 글 등록과 새로고침 | POST 303 → 목록 200, 새로고침 후 글 1개 유지 |
| 입력 검증 | 누락·공백·길이 초과·널 문자 거부, 기존 글 유지 |
| 경계값 | 이름 1/20자와 내용 1/500자 허용 |
| HTML/SQL 특수문자 | 태그는 문자로 표시, SQL처럼 보이는 내용도 그대로 저장 |
| 오류 폼 | 반영된 입력값도 이스케이프 |
| 목록 | 최신순, 페이지당 10개, 마지막 페이지와 잘못된 번호 처리 |
| 용량 상한 | 1,000개일 때 신규 등록 거부, 기존 기록 보존 |
| 동시 등록 | 999개에서 2개 동시 저장 시 하나만 성공, 최종 1,000개 |
| 저장 실패 | 강제 INSERT 실패 시 503, DB에 새 글 없음, 이후 재시도 성공 |
| 재시작 | 앱 수명 주기 종료 후 다시 시작해 같은 파일의 글 조회 성공 |
| 단일 테이블 | `guestbook`만 존재하고 외래 키 없음 |
| 요청 크기 | Content-Length 유무와 관계없이 16 KiB 초과 거부, 정확한 경계 허용 |
| 요청 형식 | JSON·첨부 파일 요청 거부 |

경고 1건은 Starlette 1.9.0의 TestClient에서 기존 HTTPX 사용을 향후 중단할 예정이라는 안내입니다. 테스트는 모두 통과했습니다. 요청에 맞춰 기존 HTTPX를 유지했고 새 테스트 라이브러리는 추가하지 않았습니다.

초기 테스트 실행은 Windows 제한 환경의 임시 폴더 접근 오류로 완료하지 못했으며, 실행 권한 승인 후 다시 검증했습니다. 이후 빈 입력 테스트가 폼 헤더를 보내지 않는 문제 한 건을 고쳐 위 최종 결과를 얻었습니다.

## 실제 브라우저 검증

로컬 Uvicorn 서버와 별도 `data/preview.db`로 Chrome에서 확인했습니다.

- 빈 목록 → 이름·내용 입력 → 글 남기기 → 성공 안내와 저장된 글 표시.
- URL이 `/?saved=true`로 이동하고 입력 폼이 초기화됨.
- 한국어, 줄바꿈, 작성 시각, CSS 표시 확인.
- 좁은 화면 크기를 적용해 입력 폼 레이아웃 확인. 관찰된 `scrollWidth` 341, `innerWidth` 354로 가로 넘침 없음. 브라우저 배율의 영향이 있어 요청한 뷰포트 값과 실제 CSS 폭은 달랐습니다.
- 화면 확인 후 뷰포트 설정을 원래대로 복구함.

캡처: [일반 화면](preview.jpg), [좁은 화면](preview-mobile.jpg).

## 확인 범위와 남은 배포 작업

- 로컬 앱 실행과 데이터 보존을 검증했으며, 외부 호스팅 계정의 배포·재시작은 아직 확인하지 않았습니다.
- 계정의 무료 ASGI 제공 여부, 디스크 사용량, 만료 연장 방식 확인 후 [DEPLOYMENT.md](DEPLOYMENT.md)의 절차를 적용해야 합니다.
- 테스트는 학습용 소규모 앱의 기능 검증이며, 무제한 트래픽이나 스팸을 견디는 부하 검증은 아닙니다.
