import time
import asyncio

async def find_users_async(n):
    find_users_async2(10)
    for i in range(1, n + 1):
        print(f'{n}명 중 {i}번 째 사용자 조회 중 ...')
        await asyncio.sleep(1)
    print(f'> 총 {n} 명 사용자 비동기 조회 완료!')

async def find_users_async2(n):
    for i in range(1, n + 1):
        print(f'{n}명 중 {i}번 째 사용자 조회 중 ...')
        await asyncio.sleep(1)
    print(f'> 총 {n} 명 사용자 비동기 조회 완료!')

asyncio.run(find_users_async(10))