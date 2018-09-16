"""
进程:
    进程间通信: 最常见的方式是消息传递.(管道,网络套接字) 还可以使用依赖于内存映射区域(mmap),借助内存映射,进程
    可以创建共享的内存区域.
"""
import multiprocessing
import time

"""
multiprocessing: 为在子进程中运行的任务,通信和共享数据,以及执行各种形式的同步提供支持.进程没有任何共享状态.

进程:
    Process([group,target,name,args,kwargs]) 此类表示运行在一个子进程中的任务.应该使用关键字参数来指定构
        造函数中的参数.target是当进程启动时执行的可调用对象.args是传递给target的位置参数元组.kvargs是传递
        给target的关键字参数的字典.name是为进程指定描述性名称的字符串.group参数未使用,值始终是None

    Process实例的方法:
        authkey 进程的身份验证键.除非显示设定,这是由os.urandom()生成的32字符的字符串.这个键的用途涉及网络连
            接的底层进程间通信提供安全.
        daemon 一个布尔标志.指示进程是否是后台进程.当创建它的Python进程终止时,后台进程将自动终止.另外禁止后
            台进程创建自己的新进程.p.daemon必须在使用p.start()函数启动进程之前设置.
        exitcode 进程的整数退出代码
        name 进程名称

        is_alive() 进程仍然运行?
        join([timeout]) 等待进程终止.timeout是可选的超时期限.进程可以被连接无数次,但是如果连接自身则会出错.

        run() 进程启动时运行的方法.默认情况下,会调用传递个Process构造函数的target.定义进程的另一种方法是继承
            Process类,并重写run()函数

        start() 启动进程.这将运行代表进程的子进程,并调用该子进程中的run()方法

        terminate() 强制终止进程.如果调用此函数,进程p将立即终止,同时不会进程任何清理动作.如果进程p创建了它自
            己的子进程,这些进程会变成僵尸进程.使用此方法需要小心,如果p保存了一个锁或参与了进程间通信,那么终止
            它可能会导致死锁或IO损坏.

"""


def clock(internal):
    while True:
        print("The time is %s" % time.ctime())
        time.sleep(internal)


if __name__ == '__main__':
    p = multiprocessing.Process(target=clock, args=(3,))
    p.start()
    while True:
        print(time.ctime())
        time.sleep(1)
