"""
懒加载属性
"""


class LazyProperty(object):
    def __init__(self, func):
        print('__init__', func)
        self.func = func

    def __get__(self, instance, owner):
        print('__get__', self, instance, owner)
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value

    def __set__(self, instance, value):
        print('__set__')
        if instance is None:
            return self
        else:
            setattr(instance, self.func.__name__, value)


class Property(object):
    def __init__(self, name):
        self.name = name

    @LazyProperty
    def set(self, name='world'):
        self.name = name


if __name__ == '__main__':
    print('---------')
    p = Property('1111')
    print(p.set('qq'))
