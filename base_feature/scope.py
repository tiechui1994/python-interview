"""
作用域:
    local(局部作用域) -> enclosing(函数范围作用域) ->global(全局作用域)->build-in(内建对象作用域)

"""

i = 0


def f():
    # print(i)  变量i是局部变量,但是在print语句使用它的时候,它还未被绑定到任何对象之上,所以抛出异常(UnboundLocalError)
    i = 0


"""
对于模块代码而言,代码在执行之前,没有经过什么预处理,但是对于函数体而言,代码在运行之前已经经过了一个预处理,
因此不论名字绑定发生在作用域的哪个位置,它都能感知出来.Python虽然是一个静态作用域语言,但是名字查找确实动
态发生的,因此直到运行的时候,才会发现名字方面的问题.

在Python中,名字绑定在所属作用域中引入新的变量,同时绑定到一个对象.名字绑定发生在以下几种情况之下:
    1.参数声明:参数声明在函数的局部作用域中引入新的变量;
    2.赋值操作:对一个变量进行初次赋值会在当前作用域中引入新的变量,后续赋值操作则会重新绑定该变量;
    3.类和函数定义:类和函数定义将类名和函数名作为变量引入当前作用域,类体和函数体将形成另外一个作用域;
    4.import语句:import语句在当前作用域中引入新的变量,一般是在全局作用域;
    5.for语句:for语句在当前作用域中引入新的变量(循环变量);
    6.except语句:except语句在当前作用域中引入新的变量(异常对象).

在Python中,类定义所引入的作用域对于成员函数是不可见的,这与C++或者Java是很不同的,因此在Python中,
成员函数想要引用类体定义的变量,必须通过self或者类名来引用它.

嵌套作用域的加入,会导致一些代码编译不过或者得到不同的运行结果,在这里Python解释器会帮助你识别这些
可能引起问题的地方,给出警告.

locals函数返回所有的局部变量,但是不会返回嵌套作用域中的变量,实际上没有函数会返回嵌套作用域中的变量
"""
x = 10
a = lambda: x


def say():
    return x


b = say

print(a.__code__.co_code == b.__code__.co_code)  # 代码等价

"""
for语句:for语句在当前作用域中引入新的变量(循环变量)
Python名字绑定发生在作用域的哪个位置,它都能感知出来
"""
li = [lambda: j for j in range(10)]
print(len(li))  # 10
print(li[0]())  # 9
print(li[0].__closure__[0].cell_contents)
print(li[0].__code__.co_freevars)  # 闭包使用的变量名集合
