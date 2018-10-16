import asyncio
import time
import random
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from multiprocessing import Value, Lock

"""
多进程 + event_loop
"""
total = Value("d", 0.0)
lock = Lock()


async def do_work(messages: list) -> set:
    async def fetch():
        """
        运行一个耗时的job, 这里的job可以并发执行
        """
        runtime = random.randint(1, 40) / 100
        global total, lock
        with lock:
            total.value += runtime
        time.sleep(runtime)

    ids = set()
    for mid in messages:
        await fetch()
        time.sleep(0.0001)
        if random.random() > 0.5:
            ids.add(mid)

    return ids


def run_warper(function, *args):
    """
    包装一个function, 这个function可以是一个协程函数, 也可以是一个普通函数, 返回一个 Future 对象
    """
    loop = asyncio.new_event_loop()
    try:
        coroutine = function(*args)
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coroutine)
    finally:
        loop.close()


def main():
    start = time.time()

    loop = asyncio.get_event_loop()
    messages = list(range(0, 10000))
    tasks = []
    step = 10000 // 15
    executor = ProcessPoolExecutor(max_workers=16)  # 事件循环执行器, 默认是 ThreadPoolExecutor(1)
    for i in range(16):
        # 直接获取的 coroutine
        # task = do_work(messages[i * step:(i + 1) * step])
        #
        # 获取Future, 这里的do_work是普通函数
        # task = loop.run_in_executor(executor, do_work, messages[i * step:(i + 1) * step])

        # run是普通函数, 使用run包裹协程do_work
        task = loop.run_in_executor(executor, run_warper, do_work, messages[i * step:(i + 1) * step])
        tasks.append(task)

    # 执行
    dones = loop.run_until_complete(asyncio.gather(*tasks))
    ids = set()
    for done in dones:
        ids = ids.union(done)

    print("花费 %0.2f s 删除了 %d 封邮件" % (time.time() - start, len(ids)))


if __name__ == '__main__':
    main()
    print(total.value)
