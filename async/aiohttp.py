"""
aiohttp:
"""
import asyncio

import aiohttp
import redis


def get_redis():
    conn_pool = redis.ConnectionPool(host='127.0.0.1', db=0, port=6379)
    return redis.Redis(connection_pool=conn_pool)


rcon = get_redis()


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            print(response.status)
            return await response.text()


async def do_some_work(x):
    print("Waiting ", x)
    try:
        ret = await fetch(url="http://127.0.0.1:5000/{}".format(x))
        print(ret)
    except Exception as e:
        try:
            print(await fetch(url="http://127.0.0.1:5000/error"))
        except Exception as e:
            print(e)
    else:
        print("Done {}".format(x))
