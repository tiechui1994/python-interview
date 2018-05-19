"""
 简单的装饰器模式, 只是被装饰的函数带参数
"""


def deco(f):
    def wrapper(name):
        print("start")
        f(name)
        print("end")

    return wrapper


@deco
def func(name):
    print("Hello", name)


# 手动设置装饰器
# target = deco(func)
# target('www')
func("name")  # deco(func("name"))
