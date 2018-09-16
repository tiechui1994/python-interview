"""
pickle模块: 将Python对象序列化为适合在文件中存储, 可通过网络传输或可置于数据库中的字节流.

dump(object, file [, protocol]) 将object的序列化表示转存到文件对象file当中. protocol设置数据输出格式,
    协议0是基于文件的格式并向后兼容最早的Python版本; 协议1是二进制协议并且也兼容更早的Python版本;

    协议2是较新的协议, 提供了更高效的类和实例化序列; 协议3(默认)是用于Python3.0增加的,并且不向后兼容,支持
    bytes.

    协议4是Python3.4当中添加的, 它增加了对非常大的对象,pickling更多种类的对象和一些数据格式优化的支持
    如果object不支持序列化,则引发pickle.PicklingError异常

dumps(object [, protocol]) 返回序列化的字符串

load(file)  从文件对象file当中加载并返回一个对象的序列化表示形式. 自动检测协议. 如果该文件包含无法解码的损毁
    数据, 则引发pickle.UnpicklingError异常. 如果检测到文件结尾,引发EOFError.

loads(string)  从字符串读取一个对象的序列化表示形式
注意: 如果序列化一个以上的Python对象,只需要多次重复调用dump()和load(). 进行多次调用时,只需要确保load()的调用
    顺序和写入文件的dump()调用顺序一致即可.

问题: 使用涉及循环或共享引用的复杂结构数据时, 使用dump()和load()会存在问题. 共享对象会被存储多份

Pickler(file, [, protocol]) 创建序列化对象, 利用指定的序列化protocol将数据写入到文件对象file中
    方法:
        dump(object) 序列化存储存储. 在将object转储之后,内存当中会记住它是身份(内存id). 如果接下来使用dump
            操作写入相同的对象(内存id不变),则保存前面已经转储对象的引用,而不是写新的副本. (注意,此时序列化的
            内容是内存当中保存的对象, 对应属性的更改不气任何作用)

        clear_memo() 清除用于追踪前面已转储的内部字典.

UnPickler(file) 创建反序列化对象
    方法:
        load() 加载对象到内存. 还原一个实例时,不会调用类方法__init__, 而是通过其他方式和还原的实例数据
            重建该实例. 序列化后是数据只包含相关类和模块的名称.

注:
对实例的限制是相应的类定义必须放在模块的顶层(即没有嵌套类). 另外,如果该实例的类定义在__main__当中, 那么
反序列化以保存的对象之前必须手动重新加载这个类的定义, 因为在反序列时,解释器无法指定如何将必要的类定义自动
载回到__main__中.

通常不必再做什么就可以将用户定义类与pickle一起使用. 但是,类可以通过实现特殊方法__getstate__()和__setstate__()
来定义可保存和还原其状态的自定义的方法. __getstate__() 必须返回表示对象状态的可序列对象, __setstate__()
接收已序列化的对象并还原其状态. 如果没有定义这些方法,则默认行为是序列化实例的底层__dict__属性. 应注意如果
定义了这些方法,那么copy模块也将使用它们实现深浅复制操作.
"""
import os
import pickle


class Serial(object):
    def __init__(self, _id, name, age):
        self._id = _id
        self.name = name
        self.age = age


file = os.path.split(__file__)[0] + '/stu.dump'


def origin_dump_load():
    with open(file, mode='wb') as fd:
        serial = Serial(10, '张三', 22)
        print(serial)
        pickle.dump(serial, fd, protocol=pickle.HIGHEST_PROTOCOL)

        print(serial)
        serial.age = 44
        pickle.dump(serial, fd, protocol=pickle.HIGHEST_PROTOCOL)

    print(os.path.getsize(file))

    with open(file, mode='rb') as fd:
        while True:
            try:
                serial = pickle.load(fd)
                print(serial, serial.age)
            except EOFError:
                break


def pickler_dump_load():
    with open(file, mode='wb') as fd:
        serial = Serial(10, '张三', 22)
        pickler = pickle.Pickler(fd, protocol=pickle.HIGHEST_PROTOCOL)
        print(serial)
        pickler.dump(serial)

        serial.age = 44
        pickler.clear_memo()
        print(serial)
        pickler.dump(serial)

    print(os.path.getsize(file))

    with open(file, mode='rb') as fd:
        unpickler = pickle.Unpickler(fd)
        while True:
            try:
                serial = unpickler.load()
                print(serial, serial.age)
            except EOFError:
                break


if __name__ == '__main__':
    # origin_dump_load()
    pickler_dump_load()
