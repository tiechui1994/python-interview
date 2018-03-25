"""
切片函数->切片:
    slice(stop) 默认情况下start为0
    slcie(start, stop, step) 默认情况下step为1

    x 为range,list,string,tuple, s为切片函数的结果,
    x[s] 切片操作

    等价于

    x[start:stop:step]
    x[:stop:step] start默认是0
    x[::step]  start默认是0, stop默认是x的长度
    x[:::] start默认是0, stop默认是x的长度,step默认是1

    x[strat::step] stop默认是x的长度
"""
l = list(range(0, 10))
print(l[1:4:2])  # [2]

print(l[:4:2])  # [0,2]

print(l[::2])  # [0,2,4,6,8]

print(l[1::2])  # [1,3,5,7,9]

"""
切片实现str函数的strip()
"""


def str_strip(string):
    length = len(string)
    if length > 0:
        for i in range(0, length):
            if string[i] != ' ':
                break

        j = length - 1
        while string[j] == ' ' and j > i + 1:
            j -= 1

        if string[i:j + 1] is ' ':
            return ''

        return string[i:j + 1]

    return string


print('' == str_strip('  '))
print('java ww' == str_strip('  java ww'))


def recursive_strip(string):
    if string is ' ':
        return ''

    if string[0] != ' ' and string[-1] != ' ':
        return string
    elif string[0] == ' ':
        return recursive_strip(string[1:])
    else:
        return recursive_strip(string[0:-2])


print('ww ww' == recursive_strip('  ww ww'))
