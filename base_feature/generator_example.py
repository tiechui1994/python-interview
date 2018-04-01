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

