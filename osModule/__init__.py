"""
os 模块
"""
import os

"""
通用变量:
    environ 当前环境的映射对象
    linesep 当前平台上的分行符
    name  导入的依赖os的模块名称('posix', 'nt', 'dos', 'mac', 'java', 'os2', 'riscos'
    path 用于路径名称操作的依赖于OS的标准模块(模块)
"""


def __common_env__():
    print(os.environ)
    print(os.linesep == '\n')
    print(os.path)
    print(os.name)


"""
进程环境:
    chdir(path) 将当前的工作目录修改为path
    chroot(path) 修改当前进程的根目录(UNIX)
    fchdir(fd) 修改当前的工作目录(fd是已经打开目录的文件描述符[UNIX])
    getcwd() 获取当前工作目录路径(getcwdb()二进制目录路径)

    # 当前进程操作文件的权限
    geteuid() 有效的UID  => seteuid(uid)
    getegid() 有效的GID  => setegid(gid)

    # 当前执行的用户
    getuid() 真实的UID   => setuid(uid)
    getgid() 真实的GID   => setgid(gid)

    getpid() 当前进程的ID
    getppid() 当进程的父进程ID
    getpgid(pid) 当前pid进程的进程组ID  => os.setpgid(pid, pgrp)  将进程pid赋给进程组pgrp. 若pid == pgrp 进程将成为一个新的进程组主进程.
                                                                若 pid != pgrp 进程加入一个现有的组
                                                                若 pid == 0 将使用调用进程的进程ID
                                                                若 pgrp == 0  pid指定的进程将成为一个进程组主进程
    getpgrp() 当前进程的进程组ID   => setpgrp()

    getenv(name, default)
    putenv(name, value) 将环境变量name设为value. 修改将影响到以os.system(), popen(), fork(), execv() 开始的子进程.
                                                给os.environ中的赋值将自动调用putenv(). 但是调用putenv()不会更新os.enviro
    unsetenv(name)
"""


def __process_env__():
    os.chdir('/home')
    print(os.getcwd())  # 当前工作目录
    print(os.geteuid())  # root用户uid
    print(os.getegid())  # root用戶gid

    print(os.getuid())  # root用户uid
    print(os.getgid())  # root用户gid

    print(os.getppid())  # 父进程id
    print(os.getpid())  # 当前进程id
    print(os.getpgrp())  # 当前进程的组id
    print(os.getpgid(os.getppid()) == os.getpgrp())

    os.putenv('a', '/usr')
    print(os.getenv('a'))  # 值为NONE


"""
文件创建与文件描述符:
    close(fd) 关闭open(), pipe() 函数返回的文件描述符fd
    closerange(low, high)  关闭的范围是[low, high]
    dup(fd) 复制文件描述符,返回新的文件描述符, 它是进程未使用的文件描述符中编号最小的描述符.
            新的和旧的文件描述符可以交换使用. 此外, 它们还共享状态.
    dup2(oldfd, newfd) 将文件描述符oldfd赋给newfd. 如果newfd已经对应一个有效的文件描述符, 那么
            它将被首先关闭.

    fchmod(fd, mode) 修改fd相关的文件模式
    fchown(fd, uid, gid) 修改fd相关的所有者和组ID

    fdatasync(fd) 强制将文件写入fd
    fdopen(fd, mode, bufsize) 创建连接到文件描述符fd的已打开文件对象.
    fpathconf(fd, name) 返回fd相关的可配置路径名称变量. name 是一个字符串, 指定要获取值的名称.
        "PC_FILESIZEBITS" 文件的最大大小
        "PC_LINK_MAX" 文件的连接计数最大值
        "PC_MAX_CANON" 格式化输出行的最大长度, fd是一个终端
        "PC_MAX_INPUT"  输出行的最大长度, fd是一个终端
        "PC_PIPE_BUF" 管道或FIFO, 管道缓冲区大小
        "PC_PRIO_IO"  是否在fd上执行优先IO
        "PC_SYNC_IO"  是否在fd上执行同步IO
"""


def __file_content__():
    pass


if __name__ == '__main__':
    __file_content__()





































































