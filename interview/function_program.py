"""
函数式编程.
1. map, filter, zip 返回的是一个可迭代一次的对象
2. map(func, *iterable) func只接受n个参数(iterable的个数),且为当前迭代到的对象item, map返回的一个迭代对象(生成器对象). 长度是最小的iterable的长度
3. filter(func_or_None, iterable) func只接受一个参数, 且这个参数是当前访问的item,但是func必须要有一个布尔返回值
4. reduce(func, iterable, init) func接收两个参数, 第一个参数的当前迭代的结果, 第二个值是当迭代到的对象item. init提供了迭代结果的初始值
5. zip(iterable, iterable, iterable...) 返回元组迭代器.长度是最小的iterable的长度

sorted(iterable, key=None, reverse=False) key是指定func只接受一个参数,即当前的item,排序规则, reverse是正序/反序.
常见的key:
    lambda item: item.lower() 或者是  lambda item: item * 1.5 针对item的数字或者字符串
    operator.itemgetter(0, 1) 针对item是集合(tuple,或list,或dict), 以tuple,或list,或dict的位置排序(可以是多个) =>
        lambda item: (item[0], item[1]) 或者是 lambda item: (item['x'], item['y'])

    operator.attrgetter('x', 'y') 针对item是对象, 以对象的属性排序(可以是多个) =>
        lambda item: (item.x, item.y)

sum(iterable) 求和

partial(func,  *args, **keywords) 偏函数,为函数func指定默认参数.
"""

import random
from collections import namedtuple

from functools import reduce


def gennerate_random_list(sequence, n):
    return [random.choice(sequence) for i in range(n)]


N_Questions = 80
N_Students = 20

ANS = gennerate_random_list('ABCD', N_Questions)
SCORE = gennerate_random_list(range(1, 6), N_Questions)
QUZE = list(zip(ANS, SCORE))

Student = namedtuple('Student', ['id', 'ans'])
students = [Student(_id + 1, gennerate_random_list('ABCD*', N_Questions)) for _id in range(N_Students)]


def cal(student):
    filtered = filter(lambda x: x[0] == x[1][0], zip(student.ans, QUZE))

    reduced = reduce(lambda x, y: x + y[1][1], filtered, 0)
    print(student.id, reduced)


list(map(cal, students))

print(list(map(lambda x, y: (x, y), [1, 2], [1])))


