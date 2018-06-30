"""
对象的方法:
    1.对象的创建和销毁
    __new__(cls, ...)    创建新实例时调用的类方法
    __init__(self, ...)  初始化新实例时调用

    __del__(self)        销毁实例时调用

    *2. 对象字符串表示(基础方法)
    __format__(self, format_spec)  创建格式化后的表示(调用者是format(),或者字符串的format())
    __repr__(self)                 创建对象的字符串表示(对象集合时字符串的表示, 或者单个对象时调用repr()时的表示)
    __str__(self)                  创建简单的字符串表示(单个对象的字符串表示[当没有定义__str__,会调用__repr__], 或者是str()创建字符串的结果)

    3. 基础方法
    __bytes__(self)  字节数组的"非正式"值, 即: bytes(object)
    __bool__(self)  为真值测试返回True或False 即: bool(object)
    __hash__(self)  计算整数的散列索引, 即: hash(object)

    4. 对象的private,protected,public变量
    self.__name  属于private变量
    self._name   属于protected变量
    self.name    属于public变量

    *5. 属性访问(类定义的方法)
    try:
        return self.__getattribute__(item)
    except AttributeError as e:
        if hasattr(object, '__getattr__'):
            return self.__getattr__(item)
        else:
            raise e

    __getattribute__(self, item)
    无条件被调用,通过实例访问属性. 如果class中定义了__getattr__(),则__getattr__()不会被调用(除非显示调用
    或引发AttributeError异常)

    __getattr__(self, item)
    当一般位置找不到attribute的时候, 会调用getattr, 返回一个值或AttributeError异常.

    应用:
        1.实现getattr用作实例属性的获取和拦截
        2.自定义getattribute的时候防止无限递归(因为getattribute在访问属性的时候一直会被调用,自定义的
        getattribute方法里面同时需要返回相应的属性,通过self.__dict__取值会继续向下调用getattribute,
        造成循环调用)

    __setattr__(self, name, value)  设置self.name = value 即: object.name = value
    __delattr__(self, name) 删除属性self.name  即: del object.name
    __dir__(self) 列出所有属性和方法  即: dir(object)

    *6. 描述符类(参考class_feature里面的descriptor)
    __get__(self, instance, owner)
    如果class定义了它,则这个class就可以称为descriptor. owner是所有者的类,instance是访问descriptor的实例,
    如果不是通过实例访问,而是通过类访问的话, instance则为None.(descriptor的实例自己访问自己是不会触发__get__,
    而会触发__call__,只有descriptor作为其它类的属性才有意义) (所以下文的d是作为C2的一个属性被调用)

    __set__(self, instance, value)
    __delete__(self, instance)

    6. 用于索引操作(字典,切片)
    __getitem__(self, key)  返回self[key]
    __setitem__(self, key, value)  self[key] = value
    __delitem__(self, key)  删除self[key]
    __missing__(self, key)  为缺失的键提供默认值

    切片操作实现的基础是 __getitem__, __setitem__, __delitem__

    7. 行为方式与迭代器类似的类
    __iter__(self) 返回迭代对象   iter(seq)
    __next__(self) 返回迭代对象的下一个元素  next(seq)
    __reversed__(self) 序列反转 reversed(seq)

    8. 序列类似的类
    __len__(self)  返回self的长度, 即: len(object)
    __contains__(self, item) 如果item在self中,返回True, 否则返回False, 即: item in object

    8. 可调用接口
    __call__(self, ...)  可以模拟函数的行为. [模拟函数的对象可以用于创建仿函数(functor)或代理(proxy)]

    9. 上下文管理协议
    with context [as var]:
        statements
    执行with语句时, 就会调用__enter__()方法. 该方法的返回值被放入有可选的as var说明符指定的变量中. 只要控制流离开
    with语句相关的语句块,就会立即调用__exit__()方法.
    __exit__() 方法接收当前异常的类型,值和追踪作为参数.

    __enter__(self)
    __exit__(self, type, value, tb)

    *10. 可序列化的类
    __copy__(self)   浅层复制
    __deepcopy__(self, memodict={}) 深层复制
    __getstate__(self)  在picking之前获取对象的状态. pickle.dump(x, file)
    __reduce__(self)  序列化某对象  pickle.dump(x, file)
    __reduce_ex__(self, protocol_version)  列化某对象(新 pickling 协议) pickle.dump(x, file, protocol_version)
    __getnewargs__(self) 控制unpacking过程中对象的创建方式  pickle.load(file)
    __setstate__(self, state) 在unpacking之后还原对象的状态, pickle.load(file)

    11. 神奇的内容
    __slots__(cls)  只定义特定计划的某些属性
    __get__(self, instance, owner)
    __set__(self, instance, value)
    __delete__(self, instance)
    __instancecheck__(self, instance) isinstance(x, Class) 控制某个对象是否是该Class的实例
    __subclasscheck__(self, subclass) issubclass(Class, ParentClass) 控制某个类是否是该Class的子类
    __subclasshook__(cls, subclass)  issubclass(Class, BaseClass) 控制某个类是是否是该抽象基类的子类
"""


class Object(object):
    def __iter__(self):
        pass

    def __next__(self):
        pass

    def __init__(self, name, age):
        self.__name = 'www'
        self.name = name
        self.age = age

    def string(self):
        return self.__name

    def __str__(self):
        return '$name=%s, age=%s$' % (self.name, self.age)

    def __repr__(self):
        return '<name=%s, age=%s>' % (self.name, self.age)

    def __getattr__(self, item):
        if item is '__name':
            return self.__name
        return self.__getattr__(item)


def test_object():
    obj = Object('zhangsan', 22)
    print(obj)  # $name=zhangsan, age=22$
    print(repr(obj))  # <name=zhangsan, age=22>

    objs = [
        Object('zhangsan', 21),
        Object('lisi', 32)
    ]
    print(objs)  # [<name=zhangsan, age=21>, <name=lisi, age=32>]

    f = [1, 2, 3, 3]
    print(f)
    print(eval(repr(f)))

    # obj.__getattribute__('__name') 抛出AttributeError异常
    # obj.__setattr__('__name', 'yy') 没有任何作用
    # obj.__delattr__('__name') 抛出AttributeError异常

    obj.__setattr__('name', 'yy')
    print(obj.name)
    obj.__delattr__('name')
    # print(obj.name)  抛出AttributeError异常


class DistanceFrom(object):
    def __init__(self, origin):
        self.origin = origin

    def __call__(self, x):
        return abs(x - self.origin)


def test_distance():
    nums = [1, 12, 33, 100]
    nums.sort(key=DistanceFrom(10))  # 按照与10的距离排序
    print(nums)


class Attribute(object):
    def __init__(self, name):
        self.name = name

    def __getattribute__(self, item):
        print('__getattribute__')
        return object.__getattribute__(self, item)

    def __getattr__(self, item):
        print('__getattr__')
        if item is not 'name':
            return 'default'

    def attribute(self, item):
        try:
            return self.__getattribute__(item)
        except AttributeError as e:
            if hasattr(object, '__getattr__'):
                return self.__getattr__(item)
            else:
                raise e


def test_attribute():
    attribute = Attribute('qq')
    print(attribute.attribute('qq'))


if __name__ == '__main__':
    test_attribute()
