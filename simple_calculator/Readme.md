# 두 수 계산기

두 숫자를 입력하고 **계산하기**를 누르면 덧셈·뺄셈·곱셈·나눗셈 결과를 한 화면에서 보여주는 학습용 웹 앱입니다.
FastAPI, Uvicorn, Python, HTML, CSS로 구현했습니다. 요청의 `unicorn`은 FastAPI 실행 서버인 `uvicorn`으로 해석했습니다.

## 실행 방법 — Windows PowerShell

아래 명령은 계산기 폴더에서 실행합니다.

```powershell
cd "C:\Users\김세원\Visualstudio\simple_calculator"
```

현재 작업 환경에는 `.venv`와 필요한 패키지를 설치해 두었습니다. 바로 실행하려면:

```powershell
.\.venv\Scripts\python.exe main.py
```

브라우저에서 [계산기 열기](http://127.0.0.1:8000)를 선택하세요.
터미널을 계속 열어 두고 사용하며, 종료할 때는 해당 터미널에서 `Ctrl+C`를 누릅니다.
`index.html`을 직접 열지 말고 서버 주소로 접속해야 계산 기능이 작동합니다.
주소 표시줄이 `file:///.../index.html`이거나 VS Code Live Server 주소라면
FastAPI가 계산 요청을 처리하지 못합니다. 위 Python 명령으로 서버를 실행한 뒤
`http://127.0.0.1:8000`으로 접속하세요. 연결이 거부되면 서버 터미널이 종료되었는지 확인하세요.

다른 컴퓨터에서 처음 실행할 때는 Python을 설치한 다음 아래 순서로 준비합니다.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

`py` 명령이 없다면 첫 줄의 `py`를 `python`으로 바꾸세요.
가상 환경을 활성화하는 스크립트 없이 해당 환경의 Python을 직접 실행하므로 PowerShell 실행 정책 변경은 필요하지 않습니다.

개발 중 자동 재시작이 필요하면:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

8000번 포트가 이미 사용 중이면 기존 서버를 종료하거나 다른 포트를 사용하세요.

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --port 8001
```

이 경우 브라우저 주소도 `http://127.0.0.1:8001`로 변경합니다.
`ModuleNotFoundError`가 나오면 위의 가상 환경 Python으로 패키지 설치와 실행을 했는지 확인하세요.

## 사용 방법

1. 첫 번째 숫자와 두 번째 숫자를 입력합니다.
2. **계산하기**를 누르거나 입력칸에서 Enter를 누릅니다.
3. 네 가지 결과를 확인합니다.
4. **초기화**를 누르면 입력과 결과를 비웁니다.

`12`와 `3`을 입력하면 차례로 `15`, `9`, `36`, `4`가 나옵니다.
뺄셈은 첫 번째 수 − 두 번째 수, 나눗셈은 첫 번째 수 ÷ 두 번째 수입니다.

## 파일 구성과 역할

| 파일 | 역할 |
| --- | --- |
| `main.py` | FastAPI 경로, 입력 검증, 사칙연산, HTML 응답, 서버 실행 |
| `index.html` | 숫자 입력 폼과 결과를 넣을 화면 틀 |
| `static/style.css` | 색상·간격·결과 카드 및 작은 화면용 배치 |
| `requirements.txt` | 검증에 사용한 FastAPI·Uvicorn 버전 |
| `test_calculator.py` | 표준 라이브러리 unittest와 HTTP 요청을 이용한 검증 |

브라우저가 `/`를 요청하면 입력 화면을 보여줍니다. HTML 폼은 두 값을
`/calculate?first=12&second=3` 형태로 전달합니다. Python이 값을 검사하고 계산한 뒤
결과가 들어간 HTML을 돌려줍니다. 계산할 때 페이지가 새로 로드됩니다.
별도의 JavaScript, 데이터베이스, 템플릿 패키지는 사용하지 않습니다.

FastAPI는 웹 요청을 함수에 연결하고, Uvicorn은 앱을 실행하여 브라우저 요청을 받습니다.
`HTMLResponse`는 결과를 웹 화면으로 전달합니다.
Python 표준 라이브러리의 `string.Template`이 HTML의 자리표시자를 바꿉니다.

## 입력 규칙과 오류 처리

- 음수와 소수를 지원하며, 앞뒤 공백은 제거합니다.
- 정수부는 1~12자리, 소수부는 최대 10자리까지 허용합니다.
- 소수는 `0.5`처럼 씁니다. `.5`, `1.`, 쉼표, 지수 표기는 허용하지 않습니다.
- 빈칸, 문자, `NaN`, 무한대, 자리 수 초과 입력은 한국어 안내와 HTTP 400으로 응답합니다.
- 두 번째 숫자가 0이면 나눗셈 카드에 안내를 표시합니다. 다른 세 연산은 정상 처리합니다.
- `Decimal`을 사용하므로 `0.1 + 0.2` 결과가 `0.3`으로 표시됩니다.
- 덧셈·뺄셈·곱셈은 유효숫자 50자리 정밀도로 계산하여 허용된 입력의 결과를 담습니다.
- 나눗셈은 유효숫자 **5자리**로 반올림합니다. 소수점 아래 5자리라는 뜻은 아닙니다.
  예: `1 ÷ 3 = 0.33333`, `2 ÷ 3 = 0.66667`, `123456 ÷ 1 = 123460`.
  기본 ROUND_HALF_EVEN 규칙을 사용하며, 정확히 중간인 경우 마지막 남길 숫자가 짝수가 되도록 반올림합니다.
  불필요한 소수점 이하 끝자리 0은 생략하므로 `4`를 `4.0000`으로 표시하지 않습니다.
- 사용자 입력을 HTML에 다시 표시할 때 `escape()`로 특수 문자를 변환합니다.
- GET 방식이라 입력 숫자가 주소 표시줄과 브라우저 방문 기록에 남을 수 있습니다.
- 서버는 내 컴퓨터의 `127.0.0.1`에서 실행됩니다.

## 검증 결과

2026-10-20, Windows / Python 3.13.15 / FastAPI 0.150.0 / Uvicorn 0.54.0에서 확인했습니다.

- `py -m py_compile simple_calculator/main.py simple_calculator/test_calculator.py`: 프로젝트 루트에서 실행, 통과.
- `test_calculator.py`: 실제 Uvicorn 서버를 임시 포트에서 실행하여 **6개 테스트 모두 통과**.
- 정상 정수, 음수, 소수, 0, 앞뒤 공백, 작은 소수, 큰 정수, 순환소수 검증.
- 0 나누기, 잘못된 입력, 누락된 값, HTML 입력 이스케이프 검증.
- 초기 HTML과 CSS의 HTTP 200 응답 확인.
- `main.py`를 직접 실행하여 8000번 포트의 서버 시작 로그 확인.

브라우저 확인 도구가 지연되어 실제 화면 배치와 클릭 동작의 시각적 검증은 완료하지 못했습니다.
위 결과는 문법 및 실제 HTTP 요청 검증 범위이며 모든 상황에서 오류가 없다는 보장은 아닙니다.

계산기 폴더에서 다시 검증하려면:

```powershell
py -m py_compile main.py test_calculator.py
.\.venv\Scripts\python.exe test_calculator.py
```

테스트 서버는 테스트 종료 후 자동으로 종료됩니다.

## 참고

- [FastAPI 공식 문서: HTMLResponse](https://fastapi.tiangolo.com/advanced/custom-response/#html-response)
