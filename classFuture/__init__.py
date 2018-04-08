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

    数据封装:
        默认情况下, 类的所有的属性和方法都是public的. 这意味着对它们的访问没有任何限制, 还有,在基类中定义的所有的内容
        都会被派生类继承,并且可从派生类内进行访问.
        类中所有的以双下划线开头的名称都会自变形(自动增加前缀'_类名'), 从而使属性和方法私有化.

        class A(object):
            def __init__(self):
                self.__x = 3  # 变形为 self._A__x

            def __spam(self): # 变形为_A__spam()
                pass

        使用上述的方法没有真正意义阻止对类的"私有"属性进行访问. 特别是如果已知类名和相应私有属性
        的名称, 则可以使用稍作变形的名称来访问它们. 通过重定义__dir__方法, 类可以降低这些属性的
        可见性, __dir__()方法提供了检查对象的dir()函数所返回的名称列表.

    对象内存管理: (详细参考memory)
        定义 __new__ 方法的原因:
            ① 该类可能继承自一个基类, 该基类的实例是不变的. [如果定义的对象继承自不变的内置类型,
            (整数, 字符串或元组等),常常会遇到这种情况, 因为__new__()是唯一在创建实例之前执行的
            方法, 也是唯一可以修改值的地方(可以在__init__()中修改, 但这时修改可能为时已晚)

             class UpperStr(str):
                def __new__(cls, value = ''):
                    return str.__new__(cls, value.upper())

            ② 另外主要的用途是在定义元类时使用.

        创建实例之后,实例将由引用计数器来管理. 如果引用计数器到达0, 实例将立即销毁. 当实例销毁时,
        解释器首先查找与对象关联的__del__()方法并调用它.而实际上, 很少有必要为类定义__del__()方法.
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
