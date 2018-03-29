def count():
    fs = []
    for i in range(1, 4):
        def f():
            return i * i

        fs.append(f)
    return fs


f1, f2, f3 = count()

print(f1(), f2(), f3())


def count():
    def f(j):
        return lambda : j*j

    fs = []
    for i in range(1, 4):
        fs.append(f(i))  # f(i)立刻被执行，因此i的当前值被传入f()
    return fs

f1, f2, f3 = count()

print(f1(), f2(), f3())