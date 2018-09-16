"""
进程间通信: 管道和消息队列,使用消息传递实现的
"""
import multiprocessing

"""
队列:
    Queue([maxsize]) 创建共享的进程队列.maxsize是队列允许的最大项数.省略则无大小限制.底层队列使用管道和锁实
        现.另外,还需要运行支持线程以便将队列中的数据传输到底层管道当中.

    方法:
        cancel_join_thread() 不会在进程退出时自动链接后台进程.这可以防止join_thread()方法阻塞.
        close() 关闭队列,防止队列中加入更多数据.调用此方法时,后台线程将继续写入那些已入队列但尚未写入的数据.
            但将在此方法完成时马上关闭.如果队列被垃圾回收,将自动调用此方法.关闭队列不会在队列消费者中产生任何
            类型是数据结束信号或异常.

        empty() 如果队列为空,则返回True.如果其他进程或线程正在往队列中添加项,结果是不可靠的.
        full() 如果队列已满,返回True

        get([block,timeout]) 返回队列当中一个项.如果队列为空,此方法将阻塞,直到队列有项可用为止.block用于控
            制阻塞行为,默认是True,如果设置为False,将引发Queue.Empty异常.timeout是可选的超时时间,用在阻塞模
            式当中.
        get_nowait() 等价get(False)

        join_thread() 连接队列的后台线程.此方法用于在调用close()方法之后,等待所有队列项背心消耗.默认情况下,
            此方法由不是队列的原始创建者的所有进程调用.调用cancel_join_thread()方法可以禁止此种行为.

        put(item,[block,timeout]) 将item放入队列.如果队列已满,此方法将阻塞至有空间可用为止.block控制阻塞行
            为,默认是True.
        put_nowait(item) 等价于put(item,False)

        qsize() 返回当前队列中项的正确数量.此函数的结果并不可靠.


    JoinableQueue([maxsize]) 创建可连接的共享进程队列.是一个Queue对象,但队列允许项的消费者通知生产者项已经
        被成功处理.通知进程是使用共享的信号和条件变量实现的.
    方法:
        task_done() 消费者使用此方法发送信号,表示get()返回的项已经被处理.如果调用此方法的次数大于从队列中删
            除的项的数量,将引发ValueError

        join() 生产者使用此方法进行阻塞,直到队列中是所有项均被处理.阻塞将持续到为每个队列中的项均调用
            task_done()为止.
"""


def consumer(input_queue):
    while True:
        item = input_queue.get()  # 出队列
        print(item)
        input_queue.task_done()  # 通知生产者,当前项已被处理掉


def producer(sequence, output_queue):
    for item in sequence:
        output_queue.put(item)


"""
核心: 放入队列中的每个项都会被序列化,然后通过管道或套接字连接发送给进程.一般来说,发送数量较少的大对象比发送大
    量小对象更好.
"""


def main():
    """
    生产者: 主进程Main
    消费者: 新创建的进程consumer_process(后台进程)
    """
    queue = multiprocessing.JoinableQueue()
    consumer_process = multiprocessing.Process(target=consumer, args=(queue,))
    consumer_process.daemon = True
    consumer_process.start()  # 启动进程

    sequence = [1, 2, 3, 4]
    producer(sequence, queue)  # 生产者
    queue.join()  # 阻塞,保证队列当中的所有项被处理掉


"""
管道:
    Pipe([duplex]) 在进程之间创建一条管道,并返回元祖(conn1,conn2),其中conn1和conn2是表示管道两端的
        Connection对象.默认情况下,管道是双向的.如果将duplex设置为False,conn1只能用于接收,而conn2只能用于
        发送.必须在创建和启动使用管道的Process对象之前调用Pipe()方法
        
    Connection方法:
        close() 关闭连接.如果c被回收,将自动调用此方法.
        fileno() 返回连接使用的整数文件描述符

        poll([timeout]) 如果连接上的数据可用,返回True.timeout指定等待的最长时间.

        recv() 接收send()方法返回的对象.如果连接的另一端已经关闭,再也不存在任何数据,将引发EOFError异常
        recv_bytes([maxlength]) 接收send_bytes()发送的一条完整的字节消息.如果进入的消息超过maxlength,
            引发IOErro,并且在连接上无法进行进一步读取.
        recv_bytes_into(buffer,[offset]) 接收一条完整的字节消息,并把它保存在buffer对象中,该对象支持可
            写入的缓存区域接口(即bytearray对象或者类似的对象),offset指定缓存区中放置消息处的字节位移.返
            回值是收到的字节数.如果消息长度大于可用的缓存区空间,将引发BufferTooShort.

        send(obj) obj是与序列化兼容的任意对象
        send_bytes(buffer,[offset,size]) 
"""


def pipe_consumer(pipe):
    input_conn, output_conn = pipe
    input_conn.close()  # 消费者关闭了input端,使用output通信
    while True:
        try:
            item = output_conn.recv()
        except EOFError:
            break
        print(item)
    print("Consumer done")


def pipe_producer(sequence, send_conn):
    for item in sequence:
        send_conn.send(item)


"""
特别注意管道端点的正确管理问题.如果生产者或消费者中没有使用管道的某个端点,就应该将其关闭.
管道是由操作系统进行引用计数的,必须在所有进程中关闭管道后才能生成EOFError异常.因此,在生产者中关闭管道不会
有任何效果,除非消费者也关闭了相同的管道端点.
"""


def pipe_main():
    (input_conn, output_conn) = multiprocessing.Pipe()
    consumer_process = multiprocessing.Process(target=pipe_consumer,
                                               args=((input_conn, output_conn),))
    consumer_process.start()

    # 生产者关闭了output端,使用input通信
    output_conn.close()
    sequence = [1, 2, 3, 4]
    pipe_producer(sequence, input_conn)
    input_conn.close()  # 很关键,只有生产者关闭了input端,消费者才可能产生产生EOFError

    consumer_process.join()


if __name__ == '__main__':
    pipe_main()
