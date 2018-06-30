"""
python 当中一切都是对象
"""
import copy

"""引用问题"""


def ref():
    a = 10
    b = a
    a = 11
    a_is_b = a is b  # 比较内存地址(True)
    a_same_b = a == b  # 比较值

    b = 12  # 此时b不在引用a
    a_is_equal_b = a is b  # (False)


"""拷贝问题"""


def _copy():
    x = [1, 2, [3, 4]]
    y = x  # 引用, 此时通过x或者y都可以修改列表

    z = list(x)  # 浅层次拷贝[对象独立, 元素只是进行了浅层次的复制(字面值拷贝和对象的引用拷贝)]
    # z = copy.copy(x)
    x_is_z = x is z  # (False)

    z.append(100)  # z修改,x未修改
    print(x, z)
    z[2][0] = 1000  # x,z同时修改
    print(x, z)

    p = copy.deepcopy(x)  # 深层次拷贝[对象独立, 元素深层次拷贝]
    p[2][1] = 'www'
    print(x, p)


if __name__ == '__main__':
    _copy()
