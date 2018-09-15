"""
namedtuple    工厂函数用于创建具有命名字段的元组子类
deque         双向链表, 在两端可以快速添加和弹出

ChainMap      将多个dict放到一个list当中进行统一管理.
  1. update 操作只会更新第一个dict当中的元素;
  2. setdefault操作,当前仅当第一个dict不存在该key时才添加                                  |
  3. popitem, pop操作, 只会删除第一个dict

Counter       dict子类, 用于统计可迭代的集合功能.
  对一个可迭代对象进行统计,按照统计结果降序排列.(对于dict,是按照字典的值进行降序排列)

OrderedDict   dict子类, 有序字典(按照添加的顺序)

defaultdict   dict子类, 调用工厂函数来提供缺失值的子类
  传入一个工厂方法,工厂方法没有参数. 在访问dict的某个key不存在时(默认的字典抛异常), 在该dict当中添加一个key,且值为工厂方
  法产生的值.
  注意: 添加key的操作是在__getitem__当中调用__missing__完成的. 例如, dict[key]方式去获取key的值, dict.pop()方法

UserDict      对字典对象进行包装, 以便更容易的字典子类化
UserList      对列表对象进行包装,以实现更容易的列表子类化
UserString    对字符串对象包装, 以便更容易的字符串子类化
"""
