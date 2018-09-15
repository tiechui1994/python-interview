"""
异步编程的基本用法:
    async def 用来定义异步函数,其内部为异步操作.
    每个线程有一个事件循环,主线程调用asyncio.get_event_loop()时会创建事件循环.
    loop.run_until_complete(fuc)添加异步fuc添加到事件循环当中, 之后事件循环会安排协同程序的执行.

"""
import time

import asyncio


def block():
    time.sleep(1)
    print('Hello World:%s' % time.time())


def block_run():
    for i in range(5):
        block()


async def unblock():
    asyncio.sleep(1)
    print('Hello World:%s' % time.time())


def unblock_run():
    loop = asyncio.get_event_loop()
    for i in range(5):
        loop.run_until_complete(unblock())


if __name__ == '__main__':
    unblock_run()

    print("==============")

    block_run()
