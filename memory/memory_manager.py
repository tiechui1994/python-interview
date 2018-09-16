"""
内存管理:
    内存管理机制的辅助模块gc
        gc.disable()  暂停自动垃圾回收
        gc.collect()  执行一次的垃圾回收,返回垃圾回收所找到无法达到的对象的数量.可以输入参数,0代表只检查
            第一代的对象,1代表检查一,二代的对象, 2代表检查一,二,三代的对象, 默认参数是2
        gc.set_threshold()  设置Python垃圾回收的阈值
        gc.set_debug() 设置垃圾回收的调试标记, 调试信息被写入std.error
        gc.get_count() 获取当前自动执行垃圾回收的计数器,返回一个长度为3的列表

        objgraph.count(typename) 对于给定类型, 返回Python垃圾回收器正在跟踪的对象个数

    垃圾回收机制:
        引用计数机制为主，标记-清除和分代收集两种机制为辅的策略.
        在Python当中,所有能够引用其他对象的对象都被称为容器. 因此只有容器之间才可能形成循环引用.Python的
        垃圾回收机制利用了这个特点来寻找需要被释放的对象.

        Python将每个容器都链到了一个双向链表(可以快速删除和插入对象)中.
        Python垃圾回收释放对象的步骤:
            ①对于每一个容器对象,设置一个gc_refs的值, 并将其初始化为该对象的引用计数值.

            ②对于每一个容器对象,找到所有其引用的对象,将被引用对象的gc_refs值减1.

            ③执行完步骤②以后所有的gc_refs值还大于0的对象都被非容器对象引用着,至少存在一个非循环引用,因
            此不能释放这些对象,将它们放入另外一个集合

            ④在步骤③中不能被释放的对象,如果它们引用着某个对象,被引用的对象也是不能被释放的,因此将这些对
            象也存放入另外一个集合当中.

            ⑤此时还剩下的对象都是无法到达的对象,现在可以释放这些对象了.


        值得注意的是,如果一个Python对象含有__del__这个方法,Python的垃圾回收机制即使发现该对象不可到达也不
        会释放他.原因是__del__这个方式是当一个Python对象引用计数为0即将被删除前调用用来做清理工作的.由于垃
        圾回收找到的需要释放的对象中往往存在循环引用的情况,对于循环引用的对象a和b,应该先调用哪一个对象的
        __del__是无法决定的,因此Python垃圾回收机制就放弃释放这些对象,转而将这些对象保存起来,通过gc.garbage
        这个变量访问.程序员可以通过gc.garbage手动释放对象,但是更好的方法是避免在代码中定义__del__这个方法.


        除此之外,Python还将所有对象根据'生存时间'分为3代(从0到2).所有新创建的对象都分配为第0代.当这些对象经
        过一次垃圾回收仍然存在则会被放入第1代中. 如果第1代中的对象在一次垃圾回收之后仍然存在则被放入第2代.
        对于不同代的对象Python的回收的频率也不一样.可以通过gc.set_threshold(threshold0[, threshold1[, threshold2]])
        来定义.当Python的垃圾回收器中"新增的对象数量"减去"删除的对象数量"大于threshold0时,Python会对第0代
        对象执行一次垃圾回收.
        每当第0代被检查的次数超过了threshold1时,第1代对象就会被执行一次垃圾回收.
        每当第1代被检查的次数超过了threshold2时,第2代对象也会被执行一次垃圾回收.

    调优手段:
        手动垃圾回收(Python开发游戏, 在一局游戏开始关闭GC,游戏结束手动GC, 可以避免游戏的卡顿, 但是可能存在
        内存溢出)调高垃圾回收阈值(一定程度上避免内存溢出, 可能减少可观的垃圾回收开销)
        避免循环引用
            手动解循环引用(编写解开循环引用的代码, 并且在对象使用结束不在需要的时候调用)
            使用弱引用(不增加引用的计数) 例如 a = weakref.ref(b)
"""
import gc
import objgraph

gc.disable()


class A(object):
    pass


class B(object):
    pass


def only_create_objects():
    a = A()
    b = B()


print('=' * 50)
only_create_objects()
print(objgraph.count('A'))
print(objgraph.count('B'))
gc.collect()


def create_and_ref_objects():
    """
    a和b相互引用对方, 形成了一个循环引用. 由此会导致a,b的引用计数都不为0.
    """
    a = A()
    b = B()
    a.child = b
    b.parent = a


print('\n', '=' * 50)
create_and_ref_objects()
print(objgraph.count('A'))
print(objgraph.count('B'))

gc.collect()
print(objgraph.count('A'))
print(objgraph.count('B'))



