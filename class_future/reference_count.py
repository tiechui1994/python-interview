"""
引用计数:
    sys.getrefcount(a)可以查看a对象的引用计数,但是比正常计数大1，因为调用函数的时候传入a,这会让a的引用计数+1

    导致引用计数+1的情况:
        1.对象被创建,例如a=23
        2.对象被引用,例如b=a
        3.对象被作为参数,传入到一个函数中,例如func(a)
        4.对象作为一个元素,存储在容器中,例如list1=[a,a]

    导致引用计数-1的情况:
        1.对象的别名被显式销毁,例如del a
        2.对象的别名被赋予新的对象,例如a=24
        3.一个对象离开它的作用域,例如f函数执行完毕时,func函数中的局部变量(全局变量不会)
        4.对象所在的容器被销毁,或从容器中删除对象
"""
import gc
import sys
import time


def ref_counts():
    def func(c):
        print('in func function', sys.getrefcount(c) - 1)

    print('init', sys.getrefcount(11) - 1)
    a = 11
    print('after a=11', sys.getrefcount(11) - 1)
    b = a
    print('after b=1', sys.getrefcount(11) - 1)
    func(11)
    print('after func(a)', sys.getrefcount(11) - 1)
    list1 = [a, 12, 14]
    print('after list1=[a,12,14]', sys.getrefcount(11) - 1)
    a = 12
    print('after a=12', sys.getrefcount(11) - 1)
    del a
    print('after del a', sys.getrefcount(11) - 1)
    del b
    print('after del b', sys.getrefcount(11) - 1)
    # list1.pop(0)
    # print('after pop list1',sys.getrefcount(11)-1)
    del list1
    print('after del list1', sys.getrefcount(11) - 1)


# print('\n', '=' * 50)
# ref_counts()


class A(object):
    pass


def f3():
    c1 = A()
    c2 = A()
    c1.t = c2
    c2.t = c1
    del c1
    del c2
    print(gc.garbage)
    print(gc.collect())  # 显式执行垃圾回收
    print(gc.garbage)
    time.sleep(1)


if __name__ == '__main__':
    gc.set_debug(gc.DEBUG_LEAK)  # 设置gc模块的日志
    f3()
