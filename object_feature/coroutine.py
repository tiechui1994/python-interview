"""
(yield from iterator) ==>

for x in iterator:
    yield x
"""


def yield_function():
    def bottom():
        return (yield 42)

    def middle():
        return (yield from bottom())

    def top():
        return (yield from middle())

    gen = top()
    value = next(gen)
    print(value)  # Prints '42'.
    try:
        value = gen.send(value * 2)
    except StopIteration as exc:
        value = exc.value
    print(value)  # Prints '84'.


import asyncio


@asyncio.coroutine
def countdown(number, n):
    while n > 0:
        print('T-minus', n, '({})'.format(number))
        yield from asyncio.sleep(1)
        n -= 1


loop = asyncio.get_event_loop()
tasks = [
    asyncio.async(countdown("A", 2)),
    asyncio.async(countdown("B", 3))]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
