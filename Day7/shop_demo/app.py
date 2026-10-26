import asyncio
import time
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# 원래 Day_7/main.py와 구분하기 위해 모듈 이름을 app.py로 지정합니다.
app = FastAPI(title="장바구니 연구소")
folder = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=folder / "static"), name="static")

# 실제 결제나 외부 서비스 호출 없이, 조회에 걸리는 시간만 재현합니다.
services = [
    {"name": "재고 확인", "value": "주문 가능 · 재고 12개"},
    {"name": "배송 조회", "value": "내일 도착 예정 · 무료 배송"},
    {"name": "리뷰 조회", "value": "★ 4.8 / 5 · 리뷰 128개"},
]


@app.get("/")
def home():
    return FileResponse(folder / "static" / "index.html")


@app.get("/api/health")
async def health():
    return {"status": "ok"}


def lookup_sync(service, delay, start):
    """일반 함수: 지금 실행 중인 스레드에서 기다립니다."""
    started = time.perf_counter() - start
    time.sleep(delay)
    return {**service, "started": started, "ended": time.perf_counter() - start}


async def lookup_async(service, delay, start):
    """기다리는 동안 이벤트 루프가 다른 작업을 진행할 수 있습니다."""
    started = time.perf_counter() - start
    await asyncio.sleep(delay)
    return {**service, "started": started, "ended": time.perf_counter() - start}


@app.get("/api/sync")
def sync_checkout(delay: float = Query(1, ge=0.2, le=3)):
    # FastAPI는 일반 def 경로를 스레드풀에서 실행합니다.
    # 조회 3개는 순차 처리하지만 서버의 이벤트 루프는 막지 않습니다.
    start = time.perf_counter()
    results = []
    for service in services:
        results.append(lookup_sync(service, delay, start))
    return {"mode": "sync", "elapsed": time.perf_counter() - start, "results": results}


@app.get("/api/async")
async def async_checkout(delay: float = Query(1, ge=0.2, le=3)):
    start = time.perf_counter()
    results = await asyncio.gather(
        *(lookup_async(service, delay, start) for service in services)
    )
    return {"mode": "async", "elapsed": time.perf_counter() - start, "results": results}


@app.get("/api/blocking")
async def blocking_checkout(delay: float = Query(1, ge=0.2, le=3)):
    # 의도된 나쁜 예: async 함수에서 time.sleep을 실행하면 루프가 막힙니다.
    start = time.perf_counter()
    results = []
    for service in services:
        results.append(lookup_sync(service, delay, start))
    return {"mode": "blocking", "elapsed": time.perf_counter() - start, "results": results}
