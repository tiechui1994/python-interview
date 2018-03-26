"""
集合类函数:
    enumerate(iterable, start)  创建一个枚举对象,其中start是枚举的开始值(默认是0),
                                其__next__()方法可以返回下一个值(tuple)


    iter()  迭代器,属于高级特性
    max(iterable, *[default=obj, key=func]) -> value  default值是当iterable没有任何元素可迭代
                                                      的返回值, key是回调函数,参数是当前迭代的元素
    max(arg1, arg2, *args, *[, key=func]) -> value

    max(iterable, *[default=obj, key=func]) -> value
    max(arg1, arg2, *args, *[, key=func]) -> value

    sorted() 排序,属于高级特性
"""
enu = enumerate('wy', start=1)
print(enu.__next__())
print(enu.__next__())

array = [1, 2, -3]
print(max(1, 22, -33, key=lambda x: x * x))

