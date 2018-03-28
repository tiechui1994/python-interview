"""
闭包:
    闭包(Closure)是词法闭包(Lexical Closure)的简称,是引用了自由变量的函数.
    这个被引用的自由变量将和这个函数一同存在,即使已经离开了创造它的环境也不例外.
    所以,闭包是由函数和与其相关的引用环境组合而成的实体.

在Python中创建一个闭包可以归结为以下三点:
    1. 闭包函数必须有内嵌函数
    2. 内嵌函数需要引用该嵌套函数上一级namespace中的变量.(变量:不能是任何循环变量,或者后续(在外部)会发生变化的变量.)
    3. 闭包函数必须返回内嵌函数

    形成闭包之后,闭包函数会获得一个非空的__closure__属性(如果是普通函数(不具备闭包的函数), 它的__closure__属性是None),
    这个属性是一个元组. 元组里面的对象为cell对象,而访问cell对象的cell_contents属性则可以得到闭包变量的当前值
    (即上一次调用之后的值), 而随着闭包的继续调用,变量会再次更新.
    所以可见,一旦形成闭包之后,python确实会将__closure__和闭包函数绑定作为储存闭包变量的场所.
"""


def create(pos=[0, 0]):
    def go(direction, step):
        new_x = pos[0] + direction[0] * step
        new_y = pos[1] + direction[1] * step
        pos[0] = new_x
        pos[1] = new_y
        return pos

    return go


play = create()
print(play([1, 0], 10))
print(play([0, 1], 20))


def greet(prefix):
    def greeting(name):
        print(prefix, name)

    return greeting


morning = greet("Good Morning")

print(morning)
print(morning.__annotations__)
print(morning.__closure__)
print(morning.__closure__[0].cell_contents)
print(dir(morning.__closure__[0]))


def count():
    i = 2
    fs = []

    def f():
        return i * i

    fs.append(f)
    i += 3
    return fs


f1, = count()

print(f1.__closure__[0].cell_contents)
print(f1(), 'www')


def count():
    def f(j):
        def g():
            return j * j

        return g

    fs = []
    for i in range(1, 4):
        fs.append(f(i))  # f(i)立刻被执行，因此i的当前值被传入f()
    return fs


f4, f5, f6 = count()

print(f4.__closure__[0].cell_contents)
print(f4(), f5(), f6())


def funx():
    x = 5

    def funy():
        nonlocal x
        x += 1
        return x

    return funy


a = funx()
print(a(), a(), a())

