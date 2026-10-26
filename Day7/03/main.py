# uvicorn Day_07.03.main:app --reload (--port 8000 생략가능)
from fastapi import FastAPI
import httpx
import os

app = FastAPI()
BASE_URL = 'http://127.0.1:9000'

@app.get('/health') # 외부에서 호출하는 것은 비동기로 하되, 안에서 구동은 동기적으로
async def health():
    return {'status': 'ok'}

import asyncio
from time import perf_counter

async def fetch(client, item_id):
    response = await client.get(f'/items/{item_id}')
    response.raise_for_status() #404등의 에러가 발행하면 멈추게 예외를 발생시킴
    return response.json() #".json" 이면 disctionary 로 반환됨 

@app.get('/summary') #비동기 순차실행
async def summary():
    start = perf_counter()
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=3, trust_env=False) as client:
        items = []
        for item_id in [1, 2, 3]:
            items.append(await fetch(client, item_id)) #외부 api를 호출한 결과를 fetch에 담겠다. append->  items 로
    return {'items': items, 'elapsed': round(perf_counter() - start, 3)} #f는 문자를 출력시 지정 

@app.get('/labels') #비동기 병렬실행
async def labels():
    ids = [1, 2, 3]
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=3, trust_env=False) as client:
        tasks = [fetch(client, item_id) for item_id in ids]
        completed = []
        for task in asyncio.as_completed(tasks): #완료된 작업부터 받겠다. 
            completed.append(await task)
    return [{'requested_id': item_id, 'data': data}
            for item_id, data in zip(ids, completed)]
