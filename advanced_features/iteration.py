"""
迭代器:
    iter(iterable) -> iterator
    iter(callable, sentinel) -> iterator 说明: callable是回调函数(没有任何参数,但是必须有返回值),在进行迭代的时候运行.
                                              sentinel是哨兵(一个确切的值),在执行迭代的时候,是迭代结束的条件(callback的返回值和sentinel值相等结束迭代)
"""

from collections import Iterable
import random

print(isinstance('ww', Iterable))
print(isinstance([1, 2, 3], Iterable))
print(isinstance((1, 2, 3), Iterable))
print(isinstance({1: 2, 2: 3}, Iterable))

"""
迭代器
"""


def add():
    return random.randrange(14)


it = iter(add, 2)
for i in it:
    print(i)

"""
杨辉三角
"""


def triangles_0():
    a = [1]
    while True:
        yield a
        a = [sum(i) for i in zip([0] + a, a + [0])]  # 首尾增加一位形成错位, 错位相加(最直接规律)


n = 0
for t in triangles_0():
    print(t)
    n = n + 1
    if n == 10:
        break


def triangles_1():
    N = [1]
    while True:
        yield N
        N.append(0)
        N = [N[i - 1] + N[i] for i in range(len(N))]  # 增加一位,打破对称, 对称位相加


n = 0
for t in triangles_1():
    print(t)
    n = n + 1
    if n == 5:
        break
