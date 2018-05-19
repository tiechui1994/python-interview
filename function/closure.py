import dis


def foo():
    m = 3
    n = 5

    def bar():
        a = 4
        return m + n + a

    return bar


bar = foo()
print(bar.__code__)
print(dis.dis(bar))
print(bar.__closure__)
