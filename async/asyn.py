import time
import asyncio

"""
Python协程:
    协程的方式,调度来自用户,用户可以在函数中yield一个状态.使用协程可以实现高效的并发任务.
    Python的在3.4中引入了协程的概念,可是这个还是以生成器对象为基础, 3.5则确定了协程的语法.

asyncio的使用: 实现协程的不仅仅是asyncio,tornado和gevent都实现了类似的功能.
    event_loop事件循环: 程序开启一个无限的循环,程序员会把一些函数注册到事件循环上.
当满足事件发生的时候,调用相应的协程函数.

    coroutine协程: 协程对象,指一个使用async关键字定义的函数,它的调用不会立即执行函数,而是会返回一个协程对象.
协程对象需要注册到事件循环,由事件循环调用.

    task任务: 一个协程对象就是一个原生可以挂起的函数,任务则是对协程进一步封装,其中包含任务的各种状态.

    future: 代表将来执行或没有执行的任务的结果.它和task上没有本质的区别.

    async/await关键字: python3.5用于定义协程的关键字, async定义一个协程,await用于挂起阻塞的异步调用接口.
"""


def simple():
    async def do_some_work(x):
        time.sleep(1)
        print('Waiting: ', x)

    start = time.time()
    coroutine = do_some_work(10000)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(coroutine)

    print('TIME: ', time.time() - start)


"""
async关键字定义一个协程(coroutine), 协程是一种对象. 协程不能直接运行, 需要把协程对象加入到事件循环当中,
然后事件循环在适当的时候调用协程.

task 和 future的联系:
    task是future的一个future的子类

asyncio.get_event_loop() 获取一个事件循环
loop.create_task(coroutine) 构建一个task, task在加入事件循环之前是pending状态.
asyncio.ensure_future(coroutine) 构建一个task
    task.add_done_callback(callback) task绑定回调函数, 回调的最后一个参数是future对象(task)

loop.run_until_complete(coroutine) 将协程对象包装成一个task对象, 然后注册到事件循环, 并启动事件循环.
"""

"""
阻塞和await:
    使用async可以定义协程对象, 使用await可以针对耗时的操作进行挂起, 如同yield一样, 函数让出控制权.
    协程遇到await,事件循环将会挂起该协程,执行别的协程,直到其他协程也挂起或者执行完毕,在进行下一个协程的执行.

    协程的目的是让IO操作异步化.
"""


def await_simple():
    async def do_some_work(x):
        print("Waiting: ", x)
        await asyncio.sleep(x)
        return 'Done after {}s'.format(x)

    start = time.time()
    coroutine = do_some_work(2)
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(coroutine)
    loop.run_until_complete(task)
    print('Task result: ', task.result())
    print("Time: ", time.time() - start)


"""
并发 和 并行:
    并发: 多个任务需要同时执行.
    并行: 同一时刻多个任务执行.

asyncio实现并发, 需要多个协程来完成任务, 每当有任务阻塞的时候就await, 然后其他协程继续工作.
创建多个协程的列表, 然后将这些协程注册到事件循环当中.

asyncio.wait(tasks) 接收tasks列表
asyncio.gather(*tasks) 接收一堆task
"""


def concurrent_simple():
    async def do_some_work(x):
        print("Waiting: ", x)
        await asyncio.sleep(x)
        return 'Done after {}s'.format(x)

    start = time.time()
    tasks = [
        asyncio.ensure_future(do_some_work(1)),
        asyncio.ensure_future(do_some_work(2)),
        asyncio.ensure_future(do_some_work(4))
    ]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    for task in tasks:
        print('Task ret: ', task.result())
    print("Time: ", time.time() - start)


"""
协程的调用和组合十分灵活,尤其是对于结果的处理,如何返回,如何挂起,需要逐渐积累经验和前瞻的设计
"""


async def do_work(x):
    print("Waiting: ", x)
    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)


def nested_concurrent_simple_1():
    """构建新的协程, 并在协程内处理结果"""

    async def nested_func():
        tasks = [
            asyncio.ensure_future(do_work(1)),
            asyncio.ensure_future(do_work(2)),
            asyncio.ensure_future(do_work(4))
        ]

        dones, pendings = await asyncio.wait(tasks)
        for task in dones:
            print('Task ret: ', task.result())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(nested_func())


def nested_concurrent_simple_2():
    """构建新的协程, 在构建的协程外处理结果(不同于 1 )"""

    async def nested_func():
        tasks = [
            asyncio.ensure_future(do_work(1)),
            asyncio.ensure_future(do_work(2)),
            asyncio.ensure_future(do_work(4))
        ]
        return await asyncio.gather(*tasks)

    loop = asyncio.get_event_loop()
    dones, pendings = loop.run_until_complete(nested_func())
    for task in dones:
        print('Task ret: ', task.result())


def nested_concurrent_simple_3():
    """构建新的协程, 在构建的协程内处理结果"""

    async def nested_func():
        tasks = [
            asyncio.ensure_future(do_work(1)),
            asyncio.ensure_future(do_work(2)),
            asyncio.ensure_future(do_work(4))
        ]
        for task in asyncio.as_completed(tasks):
            result = await task
            print('Task ret: ', result)

    loop = asyncio.get_event_loop()
    done = loop.run_until_complete(nested_func())


"""
协程停止:
    future对象的状态
        Pending
        Running
        Done
        Canceled

    当future创建的时候, task为Pending, 时间循环调用执行的时候是running,调用完毕是done
    如果需要停止事件循环, 就需要先把task取消, 此时状态是canceled

    asyncio.Task可以获取事件循环的task
"""


def stop_loop():
    async def do_some_work(x):
        print('Waiting: ', x)
        await asyncio.sleep(x)
        return 'Done after {}s'.format(x)

    tasks = [
        asyncio.ensure_future(do_some_work(2)),
        asyncio.ensure_future(do_some_work(4)),
        asyncio.ensure_future(do_some_work(8))
    ]

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt:
        print(asyncio.Task.all_tasks())  # 所有的task
        # print(asyncio.gather(*asyncio.Task.all_tasks()).cancel()) # 包装处理, 和下面的处理效果相同
        for task in asyncio.Task.all_tasks():  # 4个task, wait() + 3个do_some_work()
            print(task.cancel())
        loop.stop()
        loop.run_forever()
    finally:
        loop.close()


stop_loop()
