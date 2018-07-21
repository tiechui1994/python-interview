"""
面向对象的问题
"""


class Base(object):
    def say(self):
        print('say Base')


class Child(Base):
    def say(self):
        print('say Child')


obj = Child()
obj.say()

obj.__class__ = Base
obj.say()

a = 0.0
print(bool({'a': 10}), bool(a), type(a))

"""
比较运算:
1. 可以连续比较
2. 元组, 列表的比较只是比较第一个值的大小
"""
print(3 > 2 > 2, (2, 3) < (3, 4), [1, 3] < [2, 3], {1, 22} < {2, 11})

cp = 1 + 2J
print(cp, cp.conjugate())

x, y = 100, 20

