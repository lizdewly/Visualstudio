# uvicon 명령 인식 오류 해결

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 답변 | [답변 보기](#답변) |
| 예제 | [예제 보기](#예제) |
| 헷갈리기 쉬운 점 | [주의점 보기](#헷갈리기-쉬운-점) |
| `-m`의 의미 | [후속 질문 보기](#후속-질문과-답변) |

- 최초 기록일: 2026-10-22
- 수정일: 2026-10-22
- 분류: Python, Coding
- 핵심 용어: uvicorn, 오타, 명령 인식 오류, FastAPI

## 질문

`'uvicon'은(는) 내부 또는 외부 명령, 실행할 수 있는 프로그램, 또는 배치 파일이 아닙니다.`라는 오류가 나온다.

## 답변

입력한 `uvicon`에는 `r`이 빠져 있다. FastAPI 서버를 실행하는 프로그램 이름은 `uvicorn`이다. 오류 메시지는 Windows가 입력한 이름의 명령을 찾지 못했다는 뜻이다.

## 예제

터미널의 현재 폴더가 `Day_7`이면 다음 명령으로 실행한다.

```powershell
python -m uvicorn main:app --reload
```

현재 폴더가 프로젝트 루트인 `Visualstudio`이면 다음 명령을 사용한다.

```powershell
python -m uvicorn main:app --reload --app-dir Day_7
```

- `main`은 `main.py` 모듈을 뜻한다.
- `app`은 파일에 정의된 `app = FastAPI()` 객체를 뜻한다.
- `--reload`는 코드 변경 시 서버를 자동으로 다시 불러오게 한다.
- `python -m`은 선택된 파이썬 환경에 설치된 모듈을 실행한다.

`No module named uvicorn`이 나오면 해당 파이썬 환경에 설치한다.

```powershell
python -m pip install uvicorn
```

명령어는 안내용이며 이번 답변에서 서버 실행이나 패키지 설치는 하지 않았다.

## 헷갈리기 쉬운 점

- 가상환경을 사용 중이면 그 환경을 활성화한 터미널에서 실행한다.
- `python` 명령을 사용할 수 없고 Python 런처를 사용하는 환경이면 `python` 대신 `py`를 사용할 수 있다.
- 명령을 찾지 못하는 오류와 `No module named uvicorn`은 다르다. 후자는 실행한 파이썬 환경에서 패키지를 찾지 못했다는 뜻이다.

## 후속 질문과 답변

### 2026-10-22: `-m`의 m은 무슨 약자이며 무슨 뜻인가?

`m`은 module(모듈)을 뜻한다. `python -m 모듈이름`은 해당 파이썬의 모듈 검색 경로에서 모듈을 찾아 프로그램으로 실행하라는 의미다. 모듈은 파이썬 코드를 담은 단위이며, 보통 `.py` 파일 하나를 떠올리면 된다. 실행을 지원하는 패키지도 이 방식으로 실행할 수 있다.

```powershell
python -m uvicorn main:app --reload
```

- `python`: 사용할 파이썬을 실행한다.
- `-m uvicorn`: 그 파이썬으로 uvicorn을 찾아 실행한다.
- `main:app --reload`: 실행된 uvicorn에 전달할 인자다.

| 명령 | 의미 |
| --- | --- |
| `python main.py` | 파일 경로를 지정해 실행 |
| `python -m uvicorn` | 모듈 이름으로 찾아 실행 |
| `python -m pip install httpx` | 해당 파이썬의 pip를 실행해 httpx 설치 |

`- m`처럼 띄우지 않고 `-m`으로 붙여 쓴다. `-m` 뒤에는 일반적으로 `.py` 확장자 없이 모듈 이름을 쓴다. `-m`은 설치 옵션이 아니며, 설치는 위 예제의 `pip install`이 담당한다.

앞선 설명 보충: `-m`은 설치된 외부 패키지에만 쓰는 옵션이 아니다. 파이썬 표준 라이브러리나 검색 가능한 로컬 모듈도 실행할 수 있다. 위 명령들은 설명용이며 이번 답변에서 실행하지 않았다.

### 2026-10-22: 철자가 맞는 `uvicorn`도 명령으로 인식되지 않는 이유는?

오류는 Windows가 실행할 `uvicorn` 명령을 찾지 못했다는 의미다. 설치되지 않았거나, 설치된 실행 파일의 폴더가 현재 터미널의 PATH(명령을 찾는 폴더 목록)에 없을 때 발생할 수 있다.

이번에 실제 확인한 결과:

- 프로젝트 `.venv`의 파이썬에서 `pip show uvicorn` 실행 결과는 `Package(s) not found: uvicorn`이었다.
- 도구 환경의 기본 `python`에서도 같은 결과였다.
- `.venv/Scripts/uvicorn.exe`가 없었다.
- 도구 환경에서 `python`은 프로젝트 가상환경이 아닌 기본 설치를 가리켰다. 사용자가 열어 둔 별도 터미널의 활성화 상태까지 확인한 것은 아니다.

따라서 확인한 프로젝트 가상환경에는 uvicorn 설치가 필요하다. 프로젝트 루트 `Visualstudio`에서 다음 명령을 순서대로 실행하면 가상환경을 명시해서 설치하고 서버를 실행할 수 있다.

```powershell
.\.venv\Scripts\python.exe -m pip install uvicorn
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --app-dir Day_7
```

위 설치와 서버 실행 명령은 안내만 했으며 이번 답변에서 실행하지 않았다. `-m`은 설치되지 않은 모듈을 자동으로 설치하지 않는다.

`activate.bat`를 편집기에서 여는 것만으로 가상환경이 활성화되지는 않는다. CMD에서는 해당 터미널에서 `.venv\Scripts\activate.bat`를 실행해야 한다. PowerShell의 활성화 스크립트는 `.\.venv\Scripts\Activate.ps1`이다. 위처럼 가상환경의 파이썬 경로를 직접 지정하면 활성화 없이도 그 환경을 사용할 수 있다.

### 2026-10-22: CMD 환경에서 서버를 재시작하려면?

기존 서버를 실행한 터미널에서 Ctrl+C로 종료하고 `main.py`를 저장한다. CMD에서 다음 명령을 한 줄씩 실행한다.

```bat
cd /d "C:\Users\김세원\Visualstudio"
.venv\Scripts\activate.bat
python -m uvicorn main:app --reload --app-dir Day_7
```

`cd /d`는 드라이브가 달라도 지정한 폴더로 이동한다. `activate.bat`는 현재 CMD에서 가상환경을 활성화한다. 서버 실행 중에는 이 창을 열어 둔다.

새 CMD 창에서 측정 코드를 실행하려면 다음과 같이 입력한다.

```bat
cd /d "C:\Users\김세원\Visualstudio"
.venv\Scripts\activate.bat
python Day_7\probe.py
```

새 터미널은 가상환경 활성화 상태를 공유하지 않으므로 각각 활성화한다. `No module named uvicorn` 오류가 나오면 활성화된 CMD에서 `python -m pip install uvicorn`으로 설치한 뒤 서버 실행 명령을 다시 입력한다. 이번 답변에서는 CMD 명령을 안내만 했으며 서버 재시작이나 설치를 수행하지 않았다.

### 2026-10-22: 서버 실행 시 WinError 10013 발생

사용자는 활성화된 가상환경에서 `python -m uvicorn main:app --reload --app-dir Day_7` 실행 시 WinError 10013을 보고했다. 이는 소켓 접근 권한 거부를 뜻하며, 다른 프로그램의 독점적인 포트 사용 등으로도 발생할 수 있다. 오류 번호만으로 원인을 단정할 수 없다.

직접 소켓을 잠시 바인딩해 확인한 결과 `127.0.0.1:8000`은 WinError 10048(주소 사용 중), `127.0.0.1:8001`은 성공했다. 테스트 소켓은 즉시 닫았다. IPv4 TCP 제외 포트 목록에는 항목이 없었다. 따라서 이번 확인 시점에는 8000번 포트 충돌이 확인되었고, 8001번은 바인딩 가능했다. 점유 프로세스는 확인하지 않았다.

CMD에서 다른 포트로 실행하는 명령:

```bat
python -m uvicorn main:app --reload --app-dir Day_7 --host 127.0.0.1 --port 8001
```

이 경우 `Day_7/probe.py`의 `base_url`도 `http://127.0.0.1:8001`로 변경해야 한다. 브라우저 확인 주소는 `http://127.0.0.1:8001/health`다. 이번 답변에서는 서버 실행이나 probe.py 변경은 하지 않았다. 8001 바인딩 성공은 확인 시점의 결과이며 이후 사용 가능 여부를 보장하지 않는다.

참고: [Microsoft Windows 소켓 오류 설명](https://github.com/MicrosoftDocs/win32/blob/docs/desktop-src/WinSock/windows-sockets-error-codes-2.md).

## 참고 자료

- [Day_7/main.py](../Day_7/main.py): `app = FastAPI()` 정의 확인.
