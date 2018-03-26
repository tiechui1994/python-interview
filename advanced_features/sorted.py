"""
排序函數:
    sorted(iterable, key=None, reverse=False)  key是对每个迭代对象的处理函数,
                                               str.lower()
                                               operator.itemgetter() 以tuple,或list,或dict的位置排序(可以是多个)
                                               operator.attrgetter() 以对象的属性排序(可以是多个)

                                               reverse默认是升序
"""
from operator import itemgetter, attrgetter

a = [1, -1, 2, -6, 5]

print(sorted(a))

print(sorted(a, reverse=True))

print(sorted(a, key=lambda x: x ** 2))


class item(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return '[x=%s, y=%s, z=%s]' % (self.x, self.y, self.z)

    def __repr__(self):
        return repr((self.x, self.y, self.z))


objects = [
    item(-1, 2, 3),
    item(1, 6, 3),
    item(1, -1, 3)
]
print(sorted(objects, key=attrgetter('z', 'y')))

dicts = [
    {'A': 1, 'B': 2},
    {'A': -1, 'B': 2},
    {'A': 1, 'B': 1}
]

print(sorted(dicts, key=itemgetter('A', 'B')))

