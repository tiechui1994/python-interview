"""
设计模式:
    1. 单例设计
        实现方式一: 元类方式, 元类Singleton重写__call__方法
        实现方式二: 类属性方式, 重写类的__new__方法.
        区别: 带有属性的时候, 方式一是最旧的属性, 方式二是最新属性

super()函数:
    super(Child, cls) 首先找到Child的父类(就是类Parent), 然后把类Child转换为类Parent.
    super(Child, self) 首先找到Child的父类(就是类Parent), 然后把类Child的对象转换为类Parent的对象.
"""


class Singleton(type):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class Pool(object, metaclass=Singleton):
    def __init__(self, name='ww'):
        self.name = name


class Connection(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_single'):
            cls._single = super(Connection, cls).__new__(cls)
        return cls._single

    def __init__(self, name='ww'):
        self.name = name


p1 = Pool('qq')
p2 = Pool('tt')
print(p1.name, p2.name)
print(Pool.__class__, Pool.__bases__)

c1 = Connection('aa')
c2 = Connection('bb')
print(c1.name, c2.name, id(c1), id(c2))
print(Connection.__class__, Connection.__bases__)
