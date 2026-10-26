import asyncio
import time
from fastapi import FastAPI
app = FastAPI() #이것만 있어도 백엔드/서버 생성이 가능 , app가 서버객체 

def legacy_lookup():
    ''' 기존 동기 라이브러리의 느린 조회를 흉내내는 함수 '''
    time.sleep(2) #2초 delay
    return {'name' : '학습자'} #{'key' :'value'}

@app.get("/health")
def health(): #health 서버가 살아있는지 체크용
    return {'status' :'ok'}

@app.get('/bad')
async def bad():
    #의도된 버그 (실행은 되는데 의도와 다르게 실행되는 것=버그): 비동기함수에서 동기함수를 직접호출
    user = legacy_lookup()
    return {'route':'bad', "user":user}

@app.get('/good') #외부 api 호출시 무조건 비동기로
async def good():
    #실제 api 호출을 흉내.. 응답을 기다리는 시간을 흉내
    await asyncio.sleep(2)
    return {'route':'good', "user":{"name":'학습자'}}
