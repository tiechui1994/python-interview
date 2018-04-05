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

    __dict__ (每个对象均具备该属性) 该属性作用: 字典类型,存放本对象的属性,key(键)即为属性名, value(值)即为属性的值,
    形式为{attr_key : attr_value}

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

    属性的调用方法顺序:
        obj.x => obj.__getattribute__('x') => type(obj).__dict__['x'].__get__(obj, type(obj))
        Object.x => type.__getattribute__(Object, 'x') => Object.__dict__['x].__get__(None, Object)

    实例对象[对象属性]的字典中有与定义的描述符[类属性]有相同名字的对象时,描述符优先,会覆盖掉实例属性. python会改写默认的行为,
    去调用描述符的方法来代替. [在类的__dict__中保留该属性, 在实例的__dict__中去除该属性]

    数据描述符: 同时实现了__get__和__set__方法
    非数据描述符: 只实现了__get__方法

    描述符的调用:
        1.描述符被__getattribute__方法调用(覆盖__getattribute__会让描述符无法自动调用)
        2.描述符只适用于新式类，即继承object的类
        3.object.__getattribute__ 和 type.__getattribute__ 调用__get__方法不一样
        4.数据描述符优先于实例的字典,对于相同名字的会覆盖
        5.实例的字典优先于非数据描述符.但不会覆盖。
        6.对于数据描述符,python中property就是一个典型的应用.

"""


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
