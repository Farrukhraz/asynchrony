import aiohttp
import asyncio
from time import time
from collections import deque


def save_image(data):
    img_path = f'./img/{str(time())}.jpg'
    with open(img_path, 'wb') as img:
        img.write(data)


async def get_sever_response(url, session):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        save_image(data)


async def main():
    tasks = deque()
    url = 'https://loremflickr.com/320/240'

    async with aiohttp.ClientSession() as session:
        for i in range(10):
            task = asyncio.create_task(get_sever_response(url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    t = time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print(f"Took {time() - t} seconds.")



