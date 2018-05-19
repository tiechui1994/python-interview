"""
signal: 信号, 通常对应异步事件,包括定时器到期,等操作
"""
import signal
import socket

"""
alarm(time) 如果time非0,就会安排在time秒内将SIGALARM信号发送给程序. 以前安排的任何警报都会被取消. 如果time为0, 不会安排任何警报,
            而且会取消以前设置的所有警报. 返回值为以前安排的所有警报之前所余的秒数. 如果没有安排警报则返回0

pause() 进入睡眠状态,直到收到下一个信号为止
set_wakeup_fd(fd) 设置文件描述符fd, 当接收到信号时会在它上面写入一个'\0'字节. 接着使用该信号,通过类似select模块中的函数来处理轮询
                  文件描述符的程序中信号. 必须以非阻塞模式打开fd描述的文件,此函数才会生效.
setitimer(which, seconds, [, internal]) 将内部定时器设为seconds秒之后生成一个信号,并在此之后每internal秒重复发出信号. 这两个参数
         被指定为浮点数. which参数是ITIMER_REAL则生成SIGALRM, ITIMER_VIRTUAL则生成SIGVTALARM, ITIMER_PROF生成SIGPROF. seconds
         置为0将清除定时器.

signal(signalnum, handler) 将信号signalnum的信号处理器设置为函数handler. handler接收两个参数(信号编号和帧对象). 将handler指定为
                           SIG_IGN, SIG_DEF分别代表忽略信号和使用默认的信号处理器. 启动线程时,只能从主线程调用此函数.

"""


def handler(signum, frame):
    print(dir(frame))
    print('Timeout!')
    raise IOError('Host not responding')


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
signal.signal(signal.SIGALRM, handler)  # 注册信号处理器
signal.alarm(5)  # 在time秒之内发送SIGALRM信号
sock.connect(('www.google.com', 80))  # 阻塞调用
signal.alarm(0)  # 清除SIGALRM信号
