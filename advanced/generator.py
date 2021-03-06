"""
生成器与yield:
    函数使用yield关键字可以定义生成器对象. 生成器是一个函数,它生成一个值的序列,以便在迭代中使用.

    调用next()时, 生成器函数将不断执行语句,直到遇到yield语句为止. yield语句在函数执行停止的地方产生一个
    结果,并返回产生的结果,然后停止执行,直到再次调用next()方法.

    通常情况不会在生成器上直接调用next()方法, 而是在for语句,sum() 或者一些使用序列的其他操作中使用它.
"""


def countdown(n):
    print("counting down from %d" % n)
    while n > 0:
        yield n
        n -= 1


c = countdown(10)  # c是一个generator对象, 该生成器对象(实现了__next__()函数)在被next()调用时执行函数.
print(next(c))  # 或者是 c.__next__()
print(sum(countdown(100)))

"""
协程与yield表达式:
    在函数内, yield语句还可以用作出现在赋值运算符右边的表达式. 以这种方式使用yield语句的函数称为协程,
    它的执行是为了响应发送给它的值. 行为十分类似生成器.

    协程的运行一般是无限期的,除非它被显示关闭或者自己退出. 使用close() 可以关闭输入值的流.
    关闭后, 如果继续给协程发送值,就会引发StopIteration异常退出. 同时在协程内部引发GeneratorExit异常.
    如果yield表达式中提供了值, 协程可以使用yield语句同时接收和发出返回值.
"""


def receive():
    print("ready")
    while True:
        n = (yield)
        print("Got %s" % n)


r = receive()
print(r)
# __next__()的初始调用是必不可少的, 这样协程才能执行可通向第一个yield表达式的是语句. 在这里协程会挂起
# 等待相关生成器对象r的send()方法给它发送一个值. 传递给send()的值由协程中的(yield) 表达式返回. 接收
# 到值后,协程就会执行语句,直到遇到下一条yield语句.
r.__next__()
r.send('www')
r.close()  # 关闭输入值的流, 再次发送值(即r.send(5)),会引发异常 StopIteration


def receiver():
    print('Ready')
    try:
        while True:
            n = (yield)
            print("Got %s" % n)
    except GeneratorExit:
        print("GeneratorExit")


re = receiver()
re.__next__()
re.send('X')
re.close()
try:
    re.send('Y')
except StopIteration:
    print('StopIteration')


def receiver():
    print('Ready')
    result = None
    while True:
        # 第一次执行的时候, 返回值result为None, 当send()的值到达后, n 接收发送的值, 然后赋值给
        # result, 同时返回result
        n = (yield result)
        result = n
        print("Got %s" % n)


rec = receiver()
rec.__next__()
print(rec.send('www.weibo.com'))
print(rec.send('www.google.com'))

"""
例子:
"""

import os
import fnmatch
import gzip
import bz2
import sys

"""
例子说明:
    在此例中, 每个协程都发送数据给在它们的target参数中指定的另外一个协程. 执行完全由将数据发送到第一个协程
    find_files()中来驱动的. 接下来,这个协程将数据转入下一阶段. 此例的关键地方, 即协程管道永远保持活动状态,
    直到它显示调用close()方法为止. 因此, 只要需要,程序可以不断的给协程注入数据.

    协程可用于实现某种形式的并发. 例如一个集中式的任务管理器或事件循环, 可以安排并将数据发送到成百上千个用于
    执行各种处理任务的协程中. 输入数据"被发送"到协程中这个事实还说明,若程序使用消息队列和消息传递在组件之间
    进行通信, 协程可以很容易的与之在一起混合使用.
"""


def coroutine(func):
    def start(*args, **kwargs):
        g = func(*args, **kwargs)
        next(g)
        return g

    return start


@coroutine
def find_files(target):
    while True:
        topdir, pattern = (yield)
        for path, dirname, filelist in os.walk(topdir):
            for name in filelist:
                if fnmatch.fnmatch(name, pattern):
                    target.send(os.path.join(path, name))


@coroutine
def opener(target):
    while True:
        name = (yield)
        if name.endswith('.gz'):
            f = gzip.open(name)
        elif name.endswith('.bz2'):
            f = bz2.BZ2File(name)
        else:
            f = open(name)
        target.send(f)


@coroutine
def cat(target):
    while True:
        f = (yield)
        for line in f.readlines():
            target.send(line)


@coroutine
def grep(pattern, target):
    while True:
        line = (yield)
        if pattern in line:
            target.send(line)


@coroutine
def printer():
    while True:
        line = (yield)
        sys.stdout.write(line)


if __name__ == '__main__':
    finder = find_files(opener(cat(grep('import', printer()))))
    finder.send({'/home/quinn/Documents/python/python-learn', 'scope.py'})
