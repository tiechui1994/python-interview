"""
字典键的隐式转换
"""


def dict_implicit_convert():
    dicts = dict()
    dicts[5.5] = "Ruby"
    dicts[5.0] = "Java"
    dicts[5] = "Python"

    print(dicts[5], dicts[5.0])  # 都是python


"""
生成器执行时间的差异:
    在生成器表达式里, in操作是在声明表达式求值的, if是在运行期求值的.
"""


def generate_exec_diff():
    array = [1, 8, 15]
    g = (x for x in array if array.count(x) > 0)
    array = [2, 8, 17]

    print(list(g))  # [8]


"""
列表表达式迭代删除item
    1. del删掉的的变量, 而不是变量指向的数据
    2. 对于一个正在迭代对象进行修改不是一个很好的选择, 正确的做法是建立一份该深层拷贝来进行迭代. 然后进行相关操作
"""


def loop_delete_item():
    one = [1, 2, 3, 4]
    two = [1, 2, 3, 4]
    three = [1, 2, 3, 4]
    four = [1, 2, 3, 4]
    five = [1, 2, 3, 4, [5, 6]]

    for key, item in enumerate(one):
        del item  # del删除的是item变量, 而不是变量指向的数据

    for key, item in enumerate(two):
        two.remove(item)  # [2,4]

    for key, item in enumerate(three[:]):
        three.remove(item)  # []

    for key, item in enumerate(four):
        four.pop(key)  # [2,4]

    for item in five[:]:
        five.remove(item)

    print(one, two, three, four, five)


"""
else操作:
    1. for循环的else是当for条件为false的时候执行的语句
    2. try中的else是当没有异常的时候执行
"""

"""
内存泄露:
    1. for循环可以使用使用他们的命名空间的变量, 并将他们自己定义的循环变量保存下来
    for x in range(3):
        if x == 1:
            print(x)
    print(x) // 2

    2. 如果在全局命名空间里显示定义for循环变量, 则循环变量会重新绑定到现有变量上
    x = 1
     for x in range(3):
        if x == 1:
            print(x)
    print(x) // 2

    3. 列表解析表达式的循环变量不会泄露.
    x = 1
    list = [x for x in range(3)]
    print(x) // 1
"""

"""
列表的 .+ 与 +=
    a += b     // 在a的基础上做extend操作
    a = a + b  // 生成一个新的对象并建立新一个新引用
"""

"""
for循环机制:
    每次迭代到下一项的时候都会解包一次
"""

if __name__ == '__main__':
    # dict_implicit_convert()
    # generate_exec_diff()
    loop_delete_item()
    x = range(10)
    print(x)
    x, y = 10, 20
    max_value = x if x > y else y
    print(max_value)
    print(40 - 3 ** 2 + 11 // 3 ** 2 * 8)

