def log(level):
    print('The info level %d' % level)

    def info(f):
        def inner(name):
            print('%s start' % f.__name__)
            f(name)
            print('%s end' % f.__name__)

        return inner

    return info


def time(f):
    def inner(name):
        print('%s start' % f.__name__)
        f(name)
        print('%s end' % f.__name__)

    return inner


def say(name):
    print('=====> %s' % name)


"""
Python 函数执行的次序由左到又, 由内及外

具体的内容需要看代码层次
"""

log(2)(log(1)(say))('Java')

print('-' * 80)

time(time(say))('Python')
