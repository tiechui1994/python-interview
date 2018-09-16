"""
with相关概念:
    上下文管理协议(Context Management Protocol): 包含方法__enter__()和__exit__(),支持该协议的对象要实现
    这两个方法.

    上下文管理器(Context Manager): 支持上下文管理协议的对象，这种对象实现了__enter__()和__exit__()方法.
        上下文管理器定义执行with语句时要建立的运行时上下文,负责执行with语句块上下文中的进入与退出操作.通常
        使用with语句调用上下文管理器,也可以通过直接调用其方法来使用.

    运行时上下文(runtime context)：由上下文管理器创建,通过上下文管理器的__enter__()和__exit__()方法实现,
        __enter__()方法在语句体执行之前进入运行时上下文,__exit__()在语句体执行完后从运行时上下文退出.with
        语句支持运行时上下文这一概念.

    上下文表达式(Context Expression)：with语句中跟在关键字with之后的表达式,该表达式要返回一个上下文管理器
        对象.

    语句体(with-body)：with语句包裹起来的代码块,在执行语句体之前会调用上下文管理器的__enter__()方法,执行完
        语句体之后会执行__exit__()方法.

    with context_expression [as target(s)]:
        with-body


with语句执行流程:
    context_manager = context_expression
    exit = type(context_manager).__exit__
    value = type(context_manager).__enter__(context_manager)
    exc = True   # True表示正常执行,即便有异常也忽略; False表示重新抛出异常,需要对异常进行处理
    try:
        try:
            target = value  # 如果使用了as子句
            with-body     # 执行with-body
        except:
            # 执行过程中有异常发生
            exc = exit(context_manager, *sys.exc_info())
            # 如果__exit__返回True，则异常被忽略; 如果返回False,则重新抛出异常
            # 由外层代码对异常进行处理
            if not exec:
                raise
    finally:
        # 正常退出; 或者通过statement-body中的break/continue/return语句退出; 或者忽略异常退出
        if exc:
            exit(context_manager, None, None, None)
        # 缺省返回None, None在布尔上下文中看做是False


    1. 执行context_expression, 生成上下文管理器context_manager

    2. 调用上下文管理器的__enter__()方法; 如果使用了as子句,则将__enter__()方法的返回值赋值给as子句中的
       target(s)

    3. 执行语句体with-body

    4. 不管是否执行过程中是否发生了异常,执行上下文管理器的__exit__()方法,__exit__()方法负责执行"清理"工作,
       如释放资源等.

       如果执行过程中没有出现异常,或者语句体中执行了语句break/continue/return,则以None作为参数调用
       __exit__(None, None, None);

       如果执行过程中出现异常,则使用sys.exc_info得到的异常信息为参数调用__exit__(exc_type, exc_value,
       exc_traceback);

    5. 出现异常时,如果__exit__(type, value, traceback)返回 False,则会重新抛出异常,让with之外的语句逻辑
       来处理异常,这也是通用做法;如果返回 True,则忽略异常,不再对异常进行处理.
"""

"""
自定义上下文管理器:(实现__enter__和__exit__)
    context_manager.__enter__(): 进入上下文管理器的运行时上下文,在语句体执行前调用.with语句将该方法的返回
        值赋值给as子句中的target,如果指定了as子句的话
    context_manager.__exit__(exc_type, exc_value, exc_traceback): 退出与上下文管理器相关的运行时上下文,
        返回一个布尔值表示是否对发生的异常进行处理. 参数表示引起退出操作的异常.
            如果退出时没有发生异常,则3个参数都为None,同时返回True.
            如果发生异常,返回True表示不处理异常,否则会在退出该方法后重新抛出异常以由with语句之外的代码逻辑进行处理.
            如果该方法内部产生异常,则会取代由statement-body中语句产生的异常.(最终抛出的异常是该方法内部抛出的异常)
"""


class ContextProtocol(object):
    def __init__(self, tag):
        self.tag = tag

    def __enter__(self):
        print('__enter__')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__')
        if exc_tb is None:
            print('normal')
            return True
        else:
            raise Exception('exit inner exception')


try:
    with ContextProtocol('tag') as f:
        print('exec body')
        raise Exception('body exception')
except Exception as e:
    print(e)  # exit inner exception

"""
contextlib 模块:
    contextlib模块提供了3个对象: 装饰器contextmanager, 函数nested和上下文管理器closing. 用这些对象,可以对
    已有的生成器函数或者对象进行包装,加入对上下文管理协议的支持,避免了专门编写上下文管理器来支持with语句

    contextmanager: 用于对生成器函数进行装饰,生成器函数被装饰以后,返回的是一个上下文管理器,其__enter__()和
        __exit__()方法由contextmanager负责提供.被装饰的生成器函数只能产生一个值,否则会导致异常RuntimeError;
        产生的值会赋值给as子句中的target


    closing: 上下文自动关闭块末尾的内容. closing 适用于提供了 close() 实现的对象
        with closing(<module>.open(<arguments>)) as f:
            <block>

        实现:
            def __init__(self, thing):
                self.thing = thing
            def __enter__(self):
                return self.thing
            def __exit__(self, *exc_info): // 亮点
                self.thing.close()

    ContextDecorator: 上下文管理器 + 装饰器 (此类既实现了装饰功能,也实现了上下文管理协议),此类的实例相当于
        contextmanager

    class context(ContextDecorator):
        def __enter__(self):
          return self

       def __exit__(self, *exc):
          return False

    @context()
    def say():
        print('hello')

    say()可以按照上下文管理器的方式运行

    等价于=>  with context():
                print('hello')
"""

from contextlib import contextmanager, ContextDecorator


@contextmanager
def demo():
    print('Code before yield-statement executes in __enter__')
    # 生成器函数的只能产生一个值
    for i in range(0, 1):
        yield '*** contextmanager %d ***' % i
    print('Code after yield-statement executes in __exit__')


with demo() as value:
    print(value)


class BaseContextManger(ContextDecorator):
    def __enter__(self):
        print('enter')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit')
        return True


base_context = BaseContextManger()


@base_context
def f():
    print('hello')

f()
