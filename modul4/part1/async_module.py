import time

import aiohttp
import asyncio
import random


async def sleep():
    print('function before')
    await asyncio.sleep(random.randint(1,3))
    time.sleep(5)
    async with aiohttp.ClientSession() as session:
        response = await session.request('GET', 'https://worldtimeapi.org/api/timezone')
    print(await response.text())


async def main():
    task = await asyncio.gather(*(sleep() for _ in range(3)))


if __name__ == '__main__':
    star_time = time.time()
    print(star_time)
    try:
        asyncio.run(main())
    except:
        pass
    end_time = time.time()
    print(end_time - star_time)