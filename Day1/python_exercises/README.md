# 모듈로 나눈 Python 기초 실습

상위 폴더의 `python_practice.py`를 그대로 유지하면서, 같은 실습을 모듈로
나눈 버전입니다. 각 모듈의 `run()` 함수에 실습 코드와 복습 과제가 있습니다.
외부 패키지 설치는 필요하지 않습니다.

## 실행 방법

### 브라우저에서 실습하기

이 폴더의 `index.html`을 더블 클릭해 브라우저에서 여세요.
서버나 별도 설치 없이 다섯 실습의 입력과 결과를 화면에서 확인할 수 있습니다.
계산과 게임은 HTML 안의 JavaScript로 구현했습니다. Python 코드를 직접
실행하는 방식은 아니며 기존 Python 파일은 계속 별도로 사용할 수 있습니다.

### Python으로 실습하기

Visualstudio 폴더의 터미널에서 실행하세요. 경로에 공백이 있으므로 따옴표를 사용합니다.

```powershell
python "day 1 modules/python_exercises/main.py"
```

이 폴더 안에서 터미널을 열었다면 `python main.py`로 실행하세요.
메뉴에서 1~5를 선택하고 0으로 종료합니다.
숫자 입력이 필요한 곳에는 정수를 입력하세요.
Python 실행기가 설치되어 있다면 `python` 대신 `py`를 사용할 수 있습니다.

## 파일 구성

| 파일 | 역할 |
|---|---|
| main.py | 메뉴와 실습 모듈 호출 |
| variables.py | 변수와 덧셈 |
| conditions.py | 합격 / 불합격 판단 |
| lists.py | 리스트와 짝수 출력 |
| multiplication.py | 반복문과 구구단 |
| guessing_game.py | 숫자 맞추기 게임 |

하나의 실습만 실행하려면 해당 모듈을 직접 실행하세요.

```powershell
python "day 1 modules/python_exercises/lists.py"
```

`if __name__ == "__main__":`는 파일을 직접 실행할 때만 `run()`을 호출합니다.
따라서 메뉴 파일에서 모듈을 가져올 때는 실습이 자동으로 시작되지 않습니다.

기존 통합 파일도 계속 실행할 수 있습니다.

```powershell
python "day 1 modules/python_practice.py"
```
