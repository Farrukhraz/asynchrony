import asyncio


async def counter():                        # async == @asyncio.coroutine
    count = 1
    while True:
        print(count)
        count += 1
        await asyncio.sleep(0.4)            # await == yield from


async def say_hello_every_n_seconds():
    n = 3
    count = 0
    while True:
        if count % n == 0:
            print("Hello World!")
        count += 1
        await asyncio.sleep(1)


async def main():

    task1 = asyncio.create_task(say_hello_every_n_seconds())    # create_task == ensure_future
    task2 = asyncio.create_task(counter())


    await asyncio.gather(task1, task2)


if __name__ == '__main__':
                                # ioloop = asyncio.get_event_loop()
    asyncio.run(main())   # ==  # ioloop.run_until_complete(main())
                                # ioloop.close()

