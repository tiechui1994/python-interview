"""
描述符:
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


foo = FooType()
z = foo.x

foo.x = 1000
# ① self: TypeProperty的实例对象，其实就是FooType的属性x
# ② instance: FooType的实例对象，其实就是foo
# ③ owner: 即谁拥有这些东西，当然是FooType这个类，它是最高统治者，其他的一些都是包含在它的内部或者由它生出来的

# z = foo.x => (直接)
# foo.__getattribute__('x') => (没有重载)
# FooType.__dict__['x'].__get__(foo, FooType)
