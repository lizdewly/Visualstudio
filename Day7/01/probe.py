#요청 3개를 동시에 보내는 경우 
import asyncio
from time import perf_counter     
import httpx #httpx 외부 api 호출 가능
#import math
async def request_one(client, path,number):
    start = perf_counter()
    response = await client.get(path)
    response.raise_for_status()
    elapsed = perf_counter() - start  #elapsed 얼마나 걸렸는지, perf_counter 현재 시간정보
    # math 도 추가 가능
    print(f'{path}요청 {number}: {response.status_code}, {elapsed:.2f}')
    return response.json()

async def compare(client,path):
    print(f'\n{path}: 요청 3개 시작')
    start = perf_counter()
    await asyncio.gather(
        request_one(client, path,1),
        request_one(client, path,2),
        request_one(client, path,3)
    )
    print(f'전체 완료 시간: {perf_counter() - start:.2f}초')

async def main():
    async with httpx.AsyncClient(
        base_url = "http://127.0.0.1:8000", 
        #이 URL 을 호출하는 코드, 호출 경로/bad, /good 동시에 실행
        timeout = 20.0,
        trust_env = False #외부판매용 아님
    )as client:
        await compare(client, '/bad') #여기서 client 는 browser를 지칭함
        await compare(client, '/good')
if __name__ == '__main__':
    asyncio.run(main()) 
    