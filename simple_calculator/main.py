from decimal import Decimal, localcontext
from html import escape
from pathlib import Path
import re
from string import Template

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="두 수 계산기")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
PAGE = Template((BASE_DIR / "index.html").read_text(encoding="utf-8"))


def read_number(text):
    # 정수부 12자리, 소수부 10자리까지 허용한다.
    text = text.strip()
    if not re.fullmatch(r"[+-]?[0-9]{1,12}(?:\.[0-9]{1,10})?", text):
        raise ValueError("숫자를 확인해 주세요. 정수부 12자리, 소수부 10자리까지 입력할 수 있습니다.")
    return Decimal(text)


def display_number(number):
    if number == 0:
        return "0"
    text = format(number, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def render_page(first="", second="", results="", error="", status_code=200):
    # 사용자의 입력을 HTML에 다시 넣을 때 특수 문자를 안전하게 변환한다.
    html = PAGE.substitute(
        first=escape(first[:64], quote=True),
        second=escape(second[:64], quote=True),
        results=results,
        error=f'<p class="error" role="alert">{escape(error)}</p>' if error else "",
    )
    return HTMLResponse(html, status_code=status_code)


@app.get("/", response_class=HTMLResponse)
def home():
    return render_page()


@app.get("/calculate", response_class=HTMLResponse)
def calculate(first: str = "", second: str = ""):
    try:
        a = read_number(first)
        b = read_number(second)
    except ValueError as error:
        return render_page(first, second, error=str(error), status_code=400)

    # Decimal은 0.1 + 0.2 같은 십진 소수 계산에 적합하다.
    with localcontext() as context:
        context.prec = 50
        values = [
            ("덧셈", "+", display_number(a + b)),
            ("뺄셈", "−", display_number(a - b)),
            ("곱셈", "×", display_number(a * b)),
        ]
        # 나눗셈만 유효숫자 5자리로 반올림한다.
        context.prec = 5
        values.append(
            ("나눗셈", "÷", display_number(a / b) if b != 0 else "0으로 나눌 수 없습니다")
        )

    cards = ""
    for label, symbol, value in values:
        cards += (
            f'<article class="result"><h3>{label} <span>{symbol}</span></h3>'
            f'<p class="expression">{display_number(a)} {symbol} {display_number(b)}</p>'
            f'<p class="value">{value}</p></article>'
        )
    results = f'<section aria-labelledby="results-title"><h2 id="results-title">계산 결과</h2><div class="results">{cards}</div></section>'
    return render_page(first, second, results=results)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
