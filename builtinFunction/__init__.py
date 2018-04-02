"""
内置函数:
    1. 数学计算类内置函数:
        abs(num)
        complex(real, imag) 复数
        divmod(m, n) m/n 的商和余数
        pow(x, y) x^y
        pow(x, y, z) (x^y)%z
        round(float, n) 四舍五入,保留n位小数
        sum(iterable, start=0) iterable求和

        bin(n) 二进制
        oct(n) 八进制
        hex(n) 十六进制

        chr(n)  数字 -> Unicode
        ord(char) Unicode -> 数字

    2. 集合内置类函数
        enumerate(iterable, start)  创建一个枚举对象,其中start是枚举的开始值(默认是0),
                                其__next__()方法可以返回下一个值(tuple)

        iter()  迭代器,属于高级特性
        max(iterable, *[default=obj, key=func]) -> value  default值是当iterable没有任何元素可迭代
                                                          的返回值, key是回调函数,参数是当前迭代的元素
        max(arg1, arg2, *args, *[, key=func]) -> value

        max(iterable, *[default=obj, key=func]) -> value
        max(arg1, arg2, *args, *[, key=func]) -> value

        sorted() 排序,属于高级特性

    3. 逻辑运算
        all(iterable)  所有的元素都为真,则为真, 空迭为为真. [元素是0, None, '', False,则为假]
        any(iterable)  任何一个元素为真,则为真, 空迭代为假.
"""

print(all([None,1]))
print(any([None,1]))

print(all([]))
print(any([]))