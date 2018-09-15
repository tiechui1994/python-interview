"""
抽象类

抽象类定义:
# metaclass=abc.ABCMeta 表示使用的元类
# @abc.abstractmethod, @abc.abstractclassmethod, @abc.abstractstaticmethod 分别定义抽象的方法,类方法,静态方法
# @abc.abstractproperty 定义抽象属性方法

class Abstract(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod  # 定义抽象方法
    def get(self, name):
        pass

    @abc.abstractclassmethod  # 定义抽象类方法
    def classmethod(self, name):
        pass

抽象类实现方式一:
# 继承Abstract
# 必须实现所有的抽象方法(抽象方法, 抽象类方法, 抽象静态方法, 抽象属性方法), 否则会抛出TypeError

class Concrete(Abstract):
    def set(self, name, value):
        setattr(self, name, value)

    def get(self, name):
        return getattr(self, name)

    @classmethod
    def classmethod(cls, name):
        return getattr(cls, name)

抽象类实现方式二(不能称为实现):
# Abstract.register(Concrete) 将实现的类Concrete注册到Abstract, 此时Abstract和Concrete有父子关系,
# 但是却没有父子的事实. 当且仅当Concrete实现了Abstract中定义的所有的抽象方法, 即有父子之实
class Concrete(object):
    def get(self, name):
        return getattr(self, name)

    @classmethod
    def classmethod(cls, name):
        return getattr(cls, name)

Abstract.register(Concrete)

## 对比
方式一: 不需要注册,但是通过抽象类的__subclasses__() 方法找到所有的实现子类
方式二: 注册, 抽象类无法找到实现的子类


实现方式三:
# 抽象类实现 __subclasshook__(cls, subclass) 方法, 控制subclass类是否是抽象类cls的子类
class Abstract(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod  # 定义抽象方法
    def get(self, name):
        pass

    @abc.abstractclassmethod  # 定义抽象类方法
    def classmethod(self, name):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        pass

例子: Hashable抽象类(只有一个抽象方法__hash__())
# __mro__属性  定义了抽象类解析子类的顺序列表(C3算法)
@classmethod
def __subclasshook__(cls, C):
    if cls is Hashable:                 # 当前类是Hashable的情况下
        for B in C.__mro__:             # 遍历子类C的继承的父类
            if "__hash__" in B.__dict__:
                if B.__dict__["__hash__"]:
                    return True
                break
    return NotImplemented

例子: Iterable
@classmethod
def __subclasshook__(cls, C):
    if cls is Iterable:
        if any("__iter__" in B.__dict__ for B in C.__mro__):
            return True
    return NotImplemented
"""

"""
检查子类和父类关系:
issubclass(Concrete, Abstract)  检测Concrete是不是Abstract的子类(上面的三种实现方式均可返回True)
isinstance(instance, Abstract)  检测instance是不是Abstract是实例(必须要完整的实现Abstract的抽象方法,才能返回True)
"""
import abc
import collections.abc


class Abstract(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, name):
        pass

    @abc.abstractclassmethod
    def classmethod(self, name):
        pass


# class Concrete(Abstract):
#     def set(self, name, value):
#         setattr(self, name, value)
#
#     def get(self, name):
#         return getattr(self, name)
#
#     @classmethod
#     def classmethod(cls, name):
#         return getattr(cls, name)

class Concrete(object):
    def get(self, name):
        return getattr(self, name)

    @classmethod
    def classmethod(cls, name):
        return getattr(cls, name)


Abstract.register(Concrete)

concrete = Concrete()


class Object(object):
    pass


print(issubclass(Object, collections.Hashable), Object.__mro__)
