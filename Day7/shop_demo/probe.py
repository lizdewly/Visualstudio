import asyncio
from time import perf_counter

import httpx


async def compare(client, mode):
    start = perf_counter()
    # HTTPX로 실제 로컬 서버에 요청합니다.
    response = await client.get(f"/api/{mode}", params={"delay": 1})
    response.raise_for_status()
    data = response.json()
    print(f"{mode}: 서버 {data['elapsed']:.2f}초 / 왕복 {perf_counter() - start:.2f}초")
    for result in data["results"]:
        print(f"  {result['name']}: {result['started']:.2f} ~ {result['ended']:.2f}초")


async def main():
    # 앱 실행 포트를 바꾸면 이 주소도 함께 바꿉니다.
    async with httpx.AsyncClient(
        base_url="http://127.0.0.1:8010", timeout=30, trust_env=False
    ) as client:
        for mode in ("sync", "async", "blocking"):
            await compare(client, mode)


if __name__ == "__main__":
    asyncio.run(main())
