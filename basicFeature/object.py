"""
对象的方法:
    1.对象的创建和销毁
    __new__(cls, ...)    创建新实例时调用的类方法
    __init__(self, ...)  初始化新实例时调用

    __del__(self)        销毁实例时调用

    2. 对象字符串表示
    __format__(self, format_spec)  创建格式化后的表示(调用者是format(),或者字符串的format())
    __repr__(self)                 创建对象的字符串表示(对象集合时字符串的表示, 或者单个对象时调用repr()时的表示)
    __str__(self)                  创建简单的字符串表示(单个对象的字符串表示[当没有定义__str__,会调用__repr__], 或者是str()创建字符串的结果)

    3. 对象的测试与散列的特殊方法
    __bool__(self)  为真值测试返回True或False
    __hash__(self)  计算整数的散列索引

    4. 对象的private,protected,public变量
    self.__name  属于private变量
    self._name   属于protected变量
    self.name    属于public变量

    5. 属性访问(对象可以直接调用的方法) [protected和public]
    __getattribute__(self, name)  返回self.name, 找不到则抛出AttributeError异常
    __setattr__(self, name, value)  设置self.name = value
    __delattr__(self, name) 删除属性self.name

    6. 属性访问(类定义的方法)
    __getattribute__(self, item)
    __getattr__(self, item)
    __setattr__(self, name, value)  设置self.name = value
    __delattr__(self, name) 删除属性self.name

    7. 序列和映射方法
    __len__(self)            返回self的长度
    __getitem__(self, key)  返回self[key]
    __setitem__(self, key, value)  self[key] = value
    __delitem__(self, key)  删除self[key]
    __missing__(self, key)  为缺失的键提供默认值
    __contains__(self, item) 如果item在self中,返回True, 否则返回False

    切片操作实现的基础是 __getitem__, __setitem__, __delitem__

    8. 迭代
    __iter__(self) 返回迭代对象
    __next__(self) 返回迭代对象的下一个元素

    9. 可调用接口
    __call__(self, ...)  可以模拟函数的行为. [模拟函数的对象可以用于创建仿函数(functor)或代理(proxy)]

    10. 上下文管理协议
    with context [as var]:
        statements
    执行with语句时, 就会调用__enter__()方法. 该方法的返回值被放入有可选的as var说明符指定的变量中. 只要控制流离开
    with语句相关的语句块,就会立即调用__exit__()方法.
    __exit__() 方法接收当前异常的类型,值和追踪作为参数.

    __enter__(self)
    __exit__(self, type, value, tb)

    11. 可序列化
    __copy__(self)   浅层复制
    __deepcopy__(self, memodict={}) 深层复制
    __getstate__(self)  在picking之前获取对象的状态. pickle.dump(x, file)
    __reduce__(self)  序列化某对象  pickle.dump(x, file)
    __getnewargs__(self) 控制unpacking过程中对象的创建方式  pickle.load(file)
    __setstate__(self, state) 在unpacking之后还原对象的状态, pickle.load(file)

    12. 神奇的内容
    __slots__(cls)  只定义特定计划的某些属性
    __get__(self, instance, owner)
    __set__(self, instance, value)
    __delete__(self, instance)
"""


class Object(object):
    @staticmethod
    def __slots__(cls):
        pass

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


nums = [1, 12, 33, 100]
nums.sort(key=DistanceFrom(10))  # 按照与10的距离排序
print(nums)
