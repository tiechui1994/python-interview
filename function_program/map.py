"""
map
    map(func, *iterable): 针对iterable当中的每个元素执行func操作(參數是传入的iterable的每个元素),
                          返回操作后的iterable.
    注: 当只有两个以上(包含两个)iterable时, 使用迭代去最小个数

    reduce(function,sequence) -> value 每次执行function(包含两个参数),最终返回一个值
    reduce(function,sequence, initial) 返回value个initial组成的序列
"""

key = [1, 2, 3, 4, 5]
value = [1, 22, 33]

print(dict(map(lambda x, y: (x, y), key, value)))

from functools import reduce

array = [4, 5, 1]
initial = ['w']
res = reduce(lambda x, y: x * y, array, initial)
print(res)

num = [11, 22, 819019, 999, 17171]


def is_palindrome_number(n):
    num = str(n)

    return num[::-1] == num


is_palindrome_number(10)

print(list(filter(is_palindrome_number, num)))

"""
字符串反转操作:
"""

l = '123345'
print(l[::-1])

print(reduce(lambda x, y: y + x, l))

l = '123345'
L = list(l)
L.reverse()
print(''.join(L))

l = '123345'
L = list(l)
print(''.join(L[::-1]))
