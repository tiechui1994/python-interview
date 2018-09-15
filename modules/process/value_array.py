"""
array模块:
    定义了一个新对象类型array.该类型工作原理与列表及其相似,但是它的内容仅限于单一类型.数组的类型在创建数组时确定.
        类型编码    描述          C类型         最小大小(字节)
        'c'        8位字符        Char              1
        'b'        8位整形        signed char       1
        'B'        8为无符号整形   unsigned char    1
        'i'        整形           int              4或8
        'I'        无符号整形      unsigned int    4或8
        'l'        长整形          long            4或8
        'L'        无符号长整形    unsigned long    4或8
        'h'        16位整形        short           2
        'H'        16位无符号整形  unsigned short   2
        'f'        单精度浮点型    float            4
        'd'        双精度浮点型    double           8
        'u'        Unicode字符                     2或4

        array(typecode,initializer)
        方法:
            a.itemsize  存储在数组中项的大小(字节为单位)
            append(x)
            buffer_info()  返回(addres,length) 提供用于存储数组的缓存区的内存位置和长度
            byteswap()   在大尾与小尾之间切换数组中所有项的字节顺序,仅支持整形值
            count(x)
            extend(b)    数组合并
            fromfile(f,n) 从文件对象f中读取n个项(二进制格式),并追加到数组末尾.f必须是一个文件对象,且可读取的项大于n
            fromlist(list) 追加list
            fromstring(s) 追加字符串s中的项,s是一个二进制组成的字符串,与fromfile()读取方式相同
            index(x)   索引
            insert(i,x)
            pop([i])
            remove(x)
            reverse()
            tofile(f)  写入文件f,数据保存为二进制格式
            tolist()
            tostring()
            tounicode()   数组的类型必须是'u'



数据共享与同步: 通常,进程之间彼此是完全孤立的,唯一的通信方式是队列或管道.但可以使用两个对象来表示共享数据.
              其实,这些对象使用了共享内存(通过mmap模块)使访问多个进程成为可能.

    Value(typecode,arg1,arg2,...argN,lock)  在共享内存中创建ctypes对象.typecode要么包含array模块使用的相同类型
        代码(如'i','d'等)的字符串,要么是来自ctypes模块的类型对象(如ctypes.c_int,ctypes.c_double等).所有额外的位置
        参数arg1,arg2,将传递给指定类型的构造函数.lock是只能使用关键字调用的参数,如果是True(默认值),将创建一个新锁来保
        护对值的访问.如果传入一个现有锁,如Lock或RLock实例,该锁将用于进行同步.如果v是Value创建的共享值的实例,便可以使用
        v.value访问底层的值.eg: x=v.value v.value=xx

    Array(typecode,initializer [,lock]) 在共享内存当中创建ctypes数组.typecode描述了数组的内容,意义与Value当中
        的相同.initializer要么是设置数组初始大小的整数,要么是项序列,其值和大小用于初始化数组.lock同Value当中的含义.可
        以使用标准的Python索引,切片,迭代操作访问其内容,每种操作均由锁进行同步.对应字节字符串,具备a.value访问.

    其他同步原语:
        Lock 互斥锁
        RLock 可重入的互斥锁(同一进程可以多次获得它,同时不会造成阻塞)
        Semaphore 信号量
        BoundSemaphore 有边界的信号量
        Event 事件
        Condition 条件变量
    使用与threading类似.

    注意: 使用多进程后,不需要担心与锁,信号量或类似构造的底层同步.在某种程度上,管道的send()和receive(),以及队列的put()
          和get()已经提供了同步功能.但是,在使用数据共享(Value,Array)的时候,需要使用锁,信号量等机制进行同步操作.
"""

import multiprocessing


class FloatChannel(object):
    def __init__(self, maxsize):
        self.buffer = multiprocessing.Array('f', maxsize, lock=False)
        self.buffer_len = multiprocessing.Value('i')
        self.empty = multiprocessing.Semaphore(1)
        self.full = multiprocessing.Semaphore(0)

    def send(self, values):
        self.empty.acquire()  # 只有在缓存区为空的时候才继续
        values_length = len(values)
        self.buffer_len = values_length
        self.buffer[:values_length] = values
        self.full.release()  # 发送信号通知缓存区已满

    def receive(self):
        self.full.acquire()  # 只在缓存区已满的时候继续
        values = self.buffer[:self.buffer_len.value]
        self.empty.release()  # 发送信号通知缓存区已空
        return values


def consume(count, ch):
    for i in range(count):
        values = ch.receive()
        print('receive ', values)


def produce(count, values, ch):
    for i in range(count):
        ch.send(values)
        print('send ', values)


if __name__ == '__main__':
    ch = FloatChannel(100)
    p = multiprocessing.Process(target=consume, args=(50, ch))

    p.start()
    values = [float(x) for x in range(100)]
    produce(10, values, ch)
    print('Done')
    p.join()
