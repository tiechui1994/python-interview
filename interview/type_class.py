"""
object与type的关系:
1. object类是所有新式类的父类
2. type是所有类的类(所属类)

object是一个新式类,可以通过object.__class__和object.__bases__来获取object所属的类和他的父类.
所属类, 即生成该对象的类
父类, 即该对象继承的类

类实例结果:
object: <class 'type'>(所属类)  没有父类
type:   <class 'type'>(所属类)  <class 'object'>(父类)

自定义类(没有任何继承):
自定义类, 所属类是<class 'type'>, 并且父类是 <class 'object'>
自定义类的实例化对象, 所属类<class 'Xxx'>，并且对象不存在父类

自定义元类:(继承元类type, 指定元类则结果和类实例的结果相同)
自定义类, 所属类是<class 'type'>, 并且父类是 <class 'type'>

思考:
调用顺序: __call__[元类] -> __new__[类] -> __init__[类]. 在__new__阶段分配内存地址.

type类:
    type(object) -> the object's type
    type(name, bases, dict) -> a new type

"""
# from pickle import Pickler
#
# print('object', object.__class__, object.__bases__)
# print('type', type.__class__, type.__bases__)
# print('list', list.__class__, list.__bases__)
# print('dict', dict.__class__, dict.__bases__)
# print('picker', Pickler.__class__, Pickler.__bases__)


class Type(type):
    def __call__(cls, *args, **kwargs):
        print('type, __call__')
        return super(Type, cls).__call__(*args, **kwargs)


class Child(metaclass=Type):
    def __new__(cls, *args, **kwargs):
        print('child, __new__')
        return super(Child, cls).__new__(cls)

    def __init__(self, name):
        print('child, __init__')
        self.name = name


child = Child('child')

