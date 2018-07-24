"""
面向对象:
    元组的相对不可变性:
        元组与Python集合(list, dict, set,等)一样, 保存的是对象的引用. 如果引用的元素是
        可变的, 即便元组本身不可变, 元素依然可变. 即元素的不可变性其实是指tuple数据结构
        的物理内容(即保存的引用)不可变, 与引用对象无关.
    str, bytes, int不可变性:
        str, bytes, array等单一类型序列是扁平的, 它们保存的不是引用, 而是在连续内存中保存
        数据本身(字符, 字节和数字)
"""

"""
共享传参:
    Python唯一支持的参数传递模式是共享传参.
    共享传参指函数的各个形式参数获得实参中各个引用的副本. 也就是说, 函数内部的形参是实参的别名.

    这种方案的结果是, 函数可能会修改作为参数传入的可变对象, 但是无法修改修改那些对象的标示(即不
    能把一个对象替换为另一个对象)

    不要使用可变类型作为参数的默认值.
"""

"""
弱引用:
    因为有引用, 对象才会在内存中存在. 当对象的引用数量为0时, 垃圾回收程序会把对象销毁.
    但是, 有时需要引用对象, 而不让对象存在的时间超过所需时间, 这经常用在缓存中.

    弱引用不会增加对象的引用数量. 引用的目标对象成为所指对象(referent)

weakref 模块:
    weakref.ref(object) 为某个对象创建弱引用[实现了__call__方法, 调用之是访问弱引用内容]
    weakref.finalize(object, fun) 为对象object绑定对象清理的回调函数

    weakref.WeakKeyDictionary 一种可变映射, 里面的键是对象的弱引用
    weakref.WeakValueDictionary 一种可变映射, 里面的值是对象的弱引用. 被引用的对象在程序的其他
    地方被当中垃圾回收后, 对应的键会自动从WeakValueDictionary中删除. 经常用于缓存
    weakref.WeakSet
"""
import weakref
weakref.ref()

i1 = 10
i2 = 10

s1 = 'abc'
s2 = 'abc'

b1 = b'xyz'
b2 = b'xyz'

print(i1 == i2, i1 is i2)
print(s1 == s2, s1 is s2)
print(b1 == b2, b1 is b2)

i1 = int(10)
i2 = int(10)

s1 = str('abc')
s2 = str('abc')

b1 = bytes('xyz', encoding='utf8')
b2 = bytes('xyz', encoding='utf8')

print(i1 == i2, i1 is i2)
print(s1 == s2, s1 is s2)
print(b1 == b2, b1 is b2)  # 两个对象

"""
弱引用
"""
print('====' * 20)
s1 = {1, 2, 3}
s2 = s1


def delete():
    print('good bye')


ref = weakref.finalize(s1, delete)
print(ref.alive)
del s1
print(ref.alive)
s2 = 'ABC'
