"""
描述符:
    描述符是一种具有"捆绑行为"的对象属性. 访问(获取、设置和删除)它的属性时, 实际是调用特殊的方法(__get__(),
    __set__(),__delete__()). 也就是说,如果一个对象定义了这三种方法的任何一种,它就是一个描述符.

    属性访问的默认行为是从对象的字典中获取、设置或删除属性. 例如，a.x的查找链以a.__dict__['x']开始，然后查找
    type(a).__dict__['x'],再继续查找除元类之外的type(a)的所有基类.
    
    三个方法(协议):
        __get__(self, instance, owner) 获取属性时调用,返回设置的属性值,通常是__set__中的value,或者附加的其他组合值.
        __set__(self, instance, value) 设置属性时调用,返回None.
        __delete__(self, instance)  删除属性时调用,返回None
        其中, instance是这个描述符属性所在的类的实例, 而owner是描述符实例所在的类.

    __dict__ (每个对象均具备该属性)该属性作用: 字典类型,存放本对象的属性,key(键)即为属性名, value(值)即为属性的值,
    形式为{attr_key : attr_value}, 该属性和__getattribute__, __getattr__, __setattr__ 存在关系.

    对象属性的访问顺序:
        ①.实例属性
        ②.类属性
        ③.父类属性
        ④.__getattr__()方法

    魔法方法：__get__(), __set__(), __delete__()
    方法的原型为：
        ① __get__(self, instance, owner)
        ② __set__(self, instance, value)
        ③ __delete__(self, instance)
        self是描述符实例, instance是描述符属性的实例, owner是描述符属性的类

    属性的调用方法顺序:
        obj.x => obj.__getattribute__('x') => type(obj).__dict__['x'].__get__(obj, type(obj))
        其通过优先级链来实现，该优先级链给数据描述器优先于实例变量，实例变量优先于非数据描述器，
        并且将最低优先级分配给__getattr__()(如果提供的话).

        Object.x => type.__getattribute__(Object, 'x') => Object.__dict__['x].__get__(None, Object)
        "type.__getattribute__ 方法"
        def __getattribute__(self, key):
            v = object.__getattribute__(self, key)
            if hasattr(v, '__get__'):
                return v.__get__(None, self)
            return v

    实例对象[对象属性]的字典中有与定义的描述符[类属性]有相同名字的对象时,描述符优先,会覆盖掉实例属性. python会改写默认的行为,
    去调用描述符的方法来代替. [在类的__dict__中保留该属性, 在实例的__dict__中去除该属性]

    数据描述符: 同时实现了__get__和__set__方法
    非数据描述符: 只实现了__get__方法

    描述符正常工作的条件:
        1. 把描述符放在类的层次上
        2. 确保实例的数据只属于实例本身[描述符类的实现方面], 即instance和属性进行绑定(instance添加自己的属性(标签), 使用字典管理instance)
        3. 注意不可哈希的描述符所有者(针对使用了字典管理instance)


    描述符的调用:
        1.描述符被__getattribute__方法调用(覆盖__getattribute__会让描述符无法自动调用)
        2.描述符只适用于新式类，即继承object的类
        3.object.__getattribute__ 和 type.__getattribute__ 调用__get__方法不一样
        4.数据描述符优先于实例的字典,对于相同名字的会覆盖
        5.实例的字典优先于非数据描述符.但不会覆盖。
        6.对于数据描述符,python中property就是一个典型的应用.

"""
import types


class Descriptor(object):
    cls_val = 1

    def __init__(self):
        self.ins_val = 10


print(Descriptor.__dict__)  # {'cls_val': 1}

des = Descriptor()
print(des.__dict__)  # {'ins_val': 10}

# 更改实例des的属性cls_val,只是新增了该属性,并不影响类Descriptor的属性cls_val
des.cls_val = 100
print(des.__dict__)  # {'ins_val': 10, 'cls_val': 100}
print(Descriptor.__dict__)  # {'cls_val': 1}

# 更改类 Descriptor 的属性cls_val, 并不影响实例des的的cls_val
Descriptor.cls_val = 11
print(Descriptor.__dict__)  # {'cls_val': 11}
print(des.__dict__)  # {'ins_val': 10, 'cls_val': 100}
print("\n\n")


# 结论: 实例属性并不包含类的属性

class TypeProperty(object):
    def __get__(self, instance, owner):
        print('__get__')
        print('self \t\t', self)
        print('instance: \t', instance)
        print('owner \t\t', owner)
        print('=' * 70, "\n")

    def __set__(self, instance, value):
        print('__set__')
        print('self \t\t', self)
        print('instance: \t', instance)
        print('value \t\t', value)
        print('=' * 70, "\n")


class FooType(object):
    x = TypeProperty()

    def __init__(self):
        self.x = 100


print('Access Class Property')
# cls_x = FooType.x
# cls_x = type.__getattribute__(FooType, 'x')
# cls_x = FooType.__dict__['x'].__get__(None, FooType)


print('Access Instance Property')


# foo = FooType()
# ins_y = foo.y
# ins_y = foo.__getattribute__('y')
# ins_y = FooType.__dict__['y'].__get__(foo, FooType) 尝试调用


# ins_x = foo.x
# ins_x = foo.__getattribute__('x')
# ins_x = FooType.__dict__['x'].__get__(foo, FooType) 尝试调用


def descriptor_attrs(obj):
    """
    返回对象的描述符相关的属性
    :param obj:
    :return:
    """
    return set(['__get__', '__set__', '__delete__']).intersection(dir(obj))


def is_descriptor(obj):
    """
    判断obj是否是描述符对象或描述符类
    :param obj:
    :return:
    """
    return bool(descriptor_attrs(obj))


def data_descriptor_attrs(obj):
    """
    数据描述符属性
    :param obj:
    :return:
    """
    return set(['__set__']) & set(dir(obj))


def is_data_descriptor(obj):
    """
    判断数据描述符
    :param obj:
    :return:
    """
    return bool(is_descriptor(obj)) & bool(data_descriptor_attrs(obj))


print(dir(object))
print(is_descriptor(int))

"""
案例Property: @property的等价实现, 一个描述符对象
"""


class Property(object):
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    """
    getter, setter, deleter 这三个方法在使用@的时候调用(@x.setter)
    """

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)


"""
案例函数Function的实现:
"""


class Function(object):
    def __get__(self, obj, objtype=None):
        return types.MethodType(self, obj, objtype)


class D(object):
    def f(self, x):
        return x


d = D()

# 通过类字典访问不会调用__get__, 它只是返回底层函数对象.
print(D.__dict__['f'])  # <function D.f at 0x00000052ED7652F0>
# 来自类带点访问调用__get __(), 它只是返回底层不变的函数对象.
print(D.f)  # <function D.f at 0x00000052ED7652F0>
# 来自实例带点访问调用__get __(), 它返回包装在绑定方法对象中的函数.
print(d.f)  # <bound method D.f of <__main__.D object at 0x00000063D3597048>>

# 在绑定方法对象函数的内部, 绑定方法存储底层函数,绑定实例和绑定实例的类.
print(d.f.__func__)  # 底层函数
print(d.f.__class__)  # 绑定实例的类
print(d.f.__self__)  # 绑定实例

"""
非数据描述器提供了一个简单的机制用于将绑定函数变换为方法的常见模式.
函数具有__get__()方法,以便在作为属性访问时可以将它们转换为方法.非数据描述器将obj.f(*args)调用转换成f(obj， *args).
调用klass.f(*args)变为f(*args).
    --------------------------------------------------------------------
    | Transformation	|   Called from an Object |  Called from a Class|
    --------------------------------------------------------------------
    | function	        |   f(obj, *args)	      |  f(*args)           |
    --------------------------------------------------------------------
    | staticmethod	    |   f(*args)	          |  f(*args)           |
    --------------------------------------------------------------------
    | classmethod	    |   f(type(obj), *args)	  |  f(klass, *args)    |
    --------------------------------------------------------------------

    静态方法返回底层函数没有更改. 调用c.f或C.f等效于直接查找object.__getattribute__(c, "f")或者
    object.__getattribute__(C, "f"). 因此,该函数从一个对象或一个类同样可访问.


"""


class StaticMethod(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, objtype=None):
        return self.f


"""
类方法: 类方法的一个用途是创建替代类构造函数
"""


class ClassMethod(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)

        def newfunc(*args):
            return self.f(klass, *args)

        return newfunc


class E(object):
    def f(cls, x):
        return cls.__name__, x

    f = classmethod(f)


print("=" * 50, '\n')
print(E.f(3))
print(E().f(3))
