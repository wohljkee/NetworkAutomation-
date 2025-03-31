import time

import aiohttp
import asyncio
import random


async def sleep():
    print('function before')
    await asyncio.sleep(random.randint(1,10))
    async with aiohttp.ClientSession() as session:
        response = await session.request('GET', 'http://worldtimeapi.org/api/timezone/America')
    print(await response.text())


async def main():
    task = await asyncio.gather(*(sleep() for _ in range(10)))


if __name__ == '__main__':
    star_time = time.time()
    print(star_time)
    asyncio.run(main())
    end_time = time.time()
    print(end_time - star_time)