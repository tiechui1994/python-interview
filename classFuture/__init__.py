"""
类和面向对象编程:
    特性:
        @property装饰器支持以简单属性的形式访问后面的方法,无需像平常一样添加的额外的()来调用该方法.

        这种特性使用方式遵循所谓的统一访问原则, 实际上,如果定义一个类, 尽可能保持借口的统一是不错的.
        如果没有特性,将会以简单属性(c.radius)的形式访问对象的某些属性, 而其他属性将以方法的形式(c.area())访问.

        特性还可以截获操作权, 以设置和删除属性. 这是通过向特性附加其他setter和deleter方法来实现的[这些方法的名称必须
        和原始特性的名称完全匹配].

    描述符: (详情参考descriptor)
        描述符是一个"绑定行为"的对象属性, 在描述符协议中, 它可以通过方法重写属性的访问. 这些方法有__get__(), __set__(),
        和__delete__()。如果这些方法中的任何一个被定义在一个对象中，这个对象就是一个描述符。

        使用特性后, 对属性的访问将由一系列用户定义的get, set和delete函数控制. 这种属性控制方式可以通过描述符对象
        进一步泛化. 描述符就是一个代表属性值的对象. 通过实现一个或多个特殊的__get__(), __set__(), __delete__()
        方法, 可以将描述符与属性访问机制挂钩, 还可以自定义这些操作.

        描述符只能在类级别上进行实例化. 不能通过在__init__()和其他方法中创建描述符对象来为每个实例创建描述符. 而且,
        持有描述符的类使用的属性名称比实例上存储的属性名称具有更高的优先级. 在 TypeProperty 的例子当中, 描述符对象
        接收参数name, 并且对其略加修改(前面加上下划线). 为了能让描述符在实例上存储值, 描述符必须挑选一个与它本身所用
        名称不同的名称.
"""
import math


class Circle(object):
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return math.pi * self.radius ** 2

    @property
    def perimeter(self):
        return 2 * math.pi * self.radius


c = Circle(4.0)
print(c.radius)
print(c.area)
print(c.perimeter)


class Foo(object):
    """
    特别注意: 存储属性的名称无需遵循任何约定, 但他必须与特性名称不同, 以便将它与特性的名称区分开.
    """

    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Must be a string')
        self.__name = value

    @name.deleter
    def name(self):
        raise TypeError('Can not delete name')


f = Foo('ww')
name = f.name
f.name = 'Johe'


class FooFunction(object):
    def __init__(self, name):
        self.__name = name

    def getname(self):
        return self.__name

    def setname(self, value):
        if not isinstance(value, str):
            raise TypeError('Must be a string')
        self.__name = value

    def delname(self):
        raise TypeError('Can not delete name')

    name = property(getname, setname, delname)  # 效果和Foo当中的一样.


class TypeProperty(object):
    """
    标签方式管理instance, 必须确保标签的值和TypeProperty实例变量名称不重叠
    说明: self.default 是没有改变`self.name` 属性之前访问的返回值.
         setattr() 是给instance增加属性`self.name`, 之后返回的值是属性`self.name`的值

         `self.name` 最终是绑定在属性instance(FooType实例)身上
    """

    def __init__(self, name, types, default=None):
        self.name = "_" + name
        self.type = types
        self.default = default if default else types

    def __get__(self, instance, cls):
        print(instance.__dict__)
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError('Must be a %s' % self.type)
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError('Can not delete attr')


class FooType(object):
    name = TypeProperty("name", str)
    num = TypeProperty("num", int, 42)


print('=' * 50, '\n')
print(TypeProperty.__dict__)
print(FooType.__dict__)
print(FooType().__dict__)

print('=' * 50, '\n')
ftype = FooType()
fooType = FooType()
print(ftype.name)
print(ftype.num)

print('=' * 50)
ftype.name = '1'
fooType.name = '2'
print(ftype.name)
print(fooType.name)
