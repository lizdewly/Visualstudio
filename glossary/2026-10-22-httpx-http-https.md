# HTTPX와 HTTP·HTTPS의 차이

## 목차

| 학습 내용 | 바로가기 |
| --- | --- |
| 질문 | [질문 보기](#질문) |
| 답변 | [답변 보기](#답변) |
| 예제 | [예제 보기](#예제) |
| 헷갈리기 쉬운 점 | [주의점 보기](#헷갈리기-쉬운-점) |

- 최초 기록일: 2026-10-22
- 수정일: 2026-10-22
- 분류: Python, Coding
- 핵심 용어: HTTPX, HTTP, HTTPS, 클라이언트, TLS, 비동기

## 질문

httpx란? http, https와의 차이는?

## 답변

HTTP와 HTTPS는 통신 규칙이고, HTTPX는 그 규칙으로 요청을 보내는 파이썬 라이브러리다.

| 이름 | 종류 | 역할 |
| --- | --- | --- |
| HTTP | 통신 프로토콜 | 클라이언트와 서버가 요청과 응답을 주고받는 규칙 |
| HTTPS | TLS로 보호되는 HTTP 통신 | 전송 내용을 암호화하고 무결성 및 서버 인증을 제공 |
| HTTPX | 파이썬 HTTP 클라이언트 라이브러리 | HTTP 또는 HTTPS로 서버에 요청을 보내고 응답을 받음 |

일반 HTTP 자체는 전송 내용을 암호화하지 않는다. HTTPX는 HTTP의 다음 버전이나 HTTPS보다 보안이 강화된 규칙이 아니다. HTTPX는 동기 요청과 비동기 요청을 모두 지원한다.

현재 `Day_7/probe.py`의 `import httpx`는 요청을 보낼 도구를 불러오는 코드다. 외부 API뿐 아니라 같은 컴퓨터에서 실행 중인 서버에도 요청을 보낼 수 있다.

## 예제

로컬 서버가 실행 중이고 `/health` 경로를 제공한다고 가정한 설명용 예제다. 이번 답변에서 실행하지 않았다.

```python
import httpx

response = httpx.get("http://127.0.0.1:8000/health")
print(response.status_code)  # 응답 상태 코드
print(response.json())      # JSON 응답을 파이썬 값으로 변환
```

`httpx.get`은 요청을 보내는 도구이고, URL의 `http://`는 사용할 통신 방식이다. HTTPS 서버에 요청할 때는 `https://` URL을 사용한다. 서버도 해당 방식을 지원해야 한다.

비동기 요청 예제:

```python
import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:8000/health")
        print(response.json())

asyncio.run(main())
```

## 헷갈리기 쉬운 점

- `httpx.get()`은 동기 호출이다. 비동기 요청에는 `AsyncClient`와 `await`를 사용한다.
- `await`는 기다리는 동안 다른 비동기 작업이 실행될 수 있게 한다. 요청 여러 개를 자동으로 동시에 시작하지는 않는다. 여러 요청을 함께 진행하려면 `asyncio.gather()` 등으로 작업을 구성한다.
- `response.json()`은 응답 내용이 JSON일 때 사용한다.
- FastAPI는 요청을 받아 처리할 API를 만드는 데 쓰이고, HTTPX는 요청을 보내는 데 쓰인다. FastAPI 서버 내부에서도 다른 서버를 호출하기 위해 HTTPX를 사용할 수 있다.

## 참고 자료

- [HTTPX 공식 문서](https://www.python-httpx.org/)
- [HTTPX 비동기 사용법](https://www.python-httpx.org/async/)
- [현재 학습 코드](../Day_7/probe.py)
