"""
进程池:
    Pool([numprocess, [initializer, initargs]])  创建工作进程池.numprocess是要创建的进程数. 省略,将使用
        cup_count()的值.initializer是每个工作进程启动时要执行的可调用对象. initargs是传递给initializer的参数元组.

    方法:
        apply(func, [args, kwargs]) 在一个池工作进程中执行函数(*args, **kwargs),然后返回结果. 此操作并不会在所有
            池工作进程中并行执行func函数.如果要使用不同参数并发地执行func函数,必须从不同进程调用apply()函数或者使用
            apply_async()函数

        apply_sync(func, [args, kwargs, callback]) 在一个池工作进程中异步执行函数(*args, **kwargs),然后返回
            结果. 此方法的 结果是AsyncResult类的实例. 稍后可用于获得最终结果. callback是可调用对象,接收输入参数. 当
            func的结果变为可用时,将立即传递给callback. callback禁止执行任何阻塞操作,否则将阻塞接收其他异步操作中的结果.

        close() 关闭进程池,防止进行进一步操作. 如果还有挂起的操作,它们将在工作进程终止之前完成.
        join() 等待所有工作进程退出. 此方法只能在close()或terminate()方法之后调用.

        imap(func, iterable, [chunksize])  map函数的版本之一,返回迭代器而非结果列表
        imap_unordered(func, iterable, [chunksize]) 同imap(),结果无序
        map(func, iterbale, [chunksize]) 将可调用对象func应用给iterable中的所有项, 然后以列表的形式返回结果.通过
            将iterable划分为多块病将工作分派给工作进程,可以并行地执行这些操作. chunksize指定每块中的项数. 如果数据量较
            大,可以增加chunksize的值来提升性能.
        map_sync(func, iterable, [chunksize, callback]) 同map(),但结果的返回是异步的.

        terminate() 立即终止所有工作进程,同时不执行任何清理或结束任何挂起操作.如果p被垃圾回收,将自动调用此方法.

        apply_sync(), map_sync()的返回值是AsyncResult实例,方法包括:
            get([timeout]) 返回结果, 如果有必要则等待结果到达.
            ready() 如果调用完成,返回True
            successful() 如果调用完成且没有任何异常,返回True. 如果在结果就绪之前调用此方法,将引发AssertionError异常
            wait([timeout]) 等待结果变为可用,timeout是可选的超时.
"""
import hashlib
import multiprocessing
import os

import time

BUFSIZE = 8192
POOLSIZE = 2

"""
使用进程池的方法统计目录下的sha512值
"""


def compute_digest(filename):
    try:
        f = open(filename, 'rb')
    except IOError:
        return None
    digest = hashlib.sha512()
    while True:
        chunk = f.read(BUFSIZE)
        if not chunk:
            break
        digest.update(chunk)
    f.close()
    return filename, digest.digest()


def build_digest_map(topdir):
    digest_pool = multiprocessing.Pool(POOLSIZE)
    allfiles = (os.path.join(path, name) for path, dirs, files in os.walk(topdir) for name in files)

    digest_maps = dict(digest_pool.imap_unordered(compute_digest, allfiles, 200))
    digest_pool.close()
    return digest_maps


if __name__ == '__main__':
    s = time.time()
    digest_map = build_digest_map("/usr/bin")
    e = time.time()
    print(len(digest_map), e - s)
