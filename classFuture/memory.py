"""
内存管理: 观察者模式, 说明顶定义__del__()方法的危害
"""

import weakref


class Account(object):
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.observers = set()

    def __del__(self):
        print('wwww')
        for obj in self.observers:
            obj.close()
        del self.observers

    def register(self, observer):
        self.observers.add(observer)

    def unregister(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for obj in self.observers:
            obj.update()

    def withdraw(self, amt):
        self.balance -= amt
        self.notify()


class AccountObserver(object):
    def __init__(self, account):
        self.account = weakref.ref(account)  # 创建weakref
        account.register(self)

    def __del__(self):
        account = self.account()
        if account:
            del self.account

    def update(self):
        print('Balance is %0.2f' % self.account.balance)

    def close(self):
        print('Account is no used')


a = Account('Jone', 1000.00)
a_ob = AccountObserver(a)
