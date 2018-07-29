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

"""
函数的基本属性:
      __doc__
      __name__
      __dict__    函数属性的字典
      __code__    编译的字节码 [函数的详情信息]
      __defaults__  默认的参数元组
      __globals__  定义的全局命名空间的字典
      __closure__  包含于嵌套作用域相关数据的元组(cell对象元组) [存储闭包运行过程中的变量]
"""
import dis


def add(x):
    y = 10
    t = 'www'
    return x + y


print(add.__code__)
print(dir(add.__code__))
code = add.__code__  # 编译的字节码
print(code.co_argcount,  # 参数个数
      code.co_cellvars,  # cell对象(闭包函数的变量名集合)
      code.co_code,  # code内容
      code.co_lnotab,  # 字节码指令和行号的对应关系
      code.co_consts,  # 常量集合
      code.co_names,  # 所有符号名称集合
      code.co_freevars,  # 闭包用的的变量名集合
      code.co_varnames,  # 局部变量名称集合
      code.co_name,  # 模块名 | 类名 | 函数名
      code.co_nlocals,  # 局部变量个数
      code.co_stacksize,  # 栈大小
      sep='\n')
print('----')
print(dis.dis(code.co_code))
print('----')
print(dis.dis(code.co_lnotab))
print(dir(add))

"""
绑定方法: 绑定方法是可调用的对象, 它封装了函数(方法)和一个相关的实例.
         调用绑定的时,实例就会作为第一个参数(self,cls)传递给方法

非绑定方法: 非绑定方法是封装了方法函数的可调用函数, 但需要传递一个正确类型的实例作为第一个参数

实例方法: 第一个参数是self [调用者是类实例(第一个参数不需要传入), 类(第一个参数显示传入且是该类的实例)]
类方法: 第一个参数是cls,并且方法使用了@classmethod [调用者是类(第一个参数不需要传入), 类实例(第一个参数显示传入且是该类)]
普通方法: 定义在类外的方法, 或者定义在类里且使用了@staticmethod [对于类外的方法,直接调用(有时需要模块导入), 类内的静态方法可以使用类或者类实例调用]
"""


class Bind(object):
    hello = 'Hello'

    def __init__(self, name):
        self.name = name

    @classmethod
    def say_hello(cls, name):
        return '%s, %s' % (cls.hello, name)

    def say(self, prefix):
        return '%s, %s' % (prefix, self.name)

    @staticmethod
    def good(name, word):
        return '%s is very %s' % (name, word)


bind = Bind('Tom')
bind_method = bind.say
print(bind_method('Hello'))

bind_method = bind.say_hello
print(bind_method('WTO'))

unbind_method = bind.good
print(unbind_method('W3C', 'nice'))

"""
      __doc__
      __name__
      __dict__    函数属性的字典
      __code__    编译的字节码 [函数的详情信息]
      __defaults__  默认的参数元组
      __globals__  定义的全局命名空间的字典
      __closure__  包含于嵌套作用域相关数据的元组 [存储闭包运行过程中的变量]

      __self__   绑定方法的类
      __func__   绑定方法的类实例的方法
"""
