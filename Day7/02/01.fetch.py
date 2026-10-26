import asyncio
import os
import sys
import httpx

BASE_URL = "https://jsonplaceholder.typicode.com" #서버경로

async def main(todo_id):
    async with httpx.AsyncClient(
        base_url=BASE_URL,
        timeout=10.0,
    ) as client:
        response = await client.get(f"/posts/{todo_id}") #페이지경로 /post/1
        print(response, type(response), response.json())
        jsondata = response.json()
        print("\n\n",jsondata['title'])

if __name__=='__main__':
    asyncio.run (main(1))

#200 OK : Success 