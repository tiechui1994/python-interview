"""
 装饰器带参数
"""


def log(level):
    def inner(f):
        def wrapper(name):
            print(level, "start")
            f(name)
            print(level, "end")

        return wrapper

    return inner


@log("INFO")
def oper(name):
    print("Hello," + name)


oper("Java")
