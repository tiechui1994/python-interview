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
code = add.__code__ # 编译的字节码
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