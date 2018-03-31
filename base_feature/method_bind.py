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
