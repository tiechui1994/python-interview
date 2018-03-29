"""
函数:
    1. 如果函数定义中存在带有默认的参数, 该参数及其所有后续参数都是可选的.
       使用可变对象作为默认值可能导致意料之外的行为(为了防止此种现象发生, 最好使用None)

    2. 调用函数时,函数参数仅仅是引用传入对象的名称. 参数传递的基本语义和其他编程语言中已知的
       方式不完全相同.

    3. 作用域规则
       每执行一个函数时, 就会创建新的局部命名空间. 该命名空间代表一个局部环境, 其中包含函数参数的名称和
       在函数体内赋值的变量名称. 解析名称: 局部命名空间 -> 全局命名空间(函数定义模块) -> 内置命名空间 -> NameError

       使用静态作用域绑定嵌套函数中的变量. 即, 解析名称时首先检查局部作用域, 然后由内而外一层层检查外部嵌套
       函数定义的作用域. 如果找不到匹配, 最后将搜索全局命名空间和内置命名空间.
"""


def append(x, items=[]):
    items.append(x)
    return items


def insert(x, items=None):
    if items is None:
        items = []
    items.append(x)
    return items


# 以下的调用和 print(append('x'),append('y')) 结果是不一致的
print(append('x'))
print(append('y'))

# 以下的调用和 print(insert('x'),insert('y')) 结果是一致的
print(insert('x'))
print(insert('y'))


def countdown(start):
    n = start

    def display():
        print('T-minus %d' % n)

    def decrement():
        nonlocal n
        n -= 1
        print('The n is %d' % n)


    while n > 0:
        display()
        decrement()


countdown(10)
