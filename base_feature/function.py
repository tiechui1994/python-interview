"""
函数:
    1. 如果函数定义中存在带有默认的参数, 该参数及其所有后续参数都是可选的.
       使用可变对象作为默认值可能导致意料之外的行为(为了防止此种现象发生, 最好使用None)

    2. 调用函数时,函数参数仅仅是引用传入对象的名称. 参数传递的基本语义和其他编程语言中已知的
       方式不完全相同.
"""


def append(x, items=[]):
    items.append(x)
    return items

def insert(x, items = None) :
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