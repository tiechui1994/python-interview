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
    fstat(fd) 返回文件描述符fd的状态.
    fdsync(fd) 强制将fd中已写入的内容写入磁盘. 注意:如果使用不带缓存IO的对象(file对象),那么在调用fsync()函数之前
               需要先清除数据.
    ftruncate(fd, length) 截取对应文件描述符fd的文件.从而让该文件的大小最多不超过length个字节(Unix)
    lseek(fd, pos, how) 将文件描述符fd的当前位置设置为pos. how的取值如下: SEEK_SET用于设置相对文件的开始处的
                        位置. SEEK_CUR用于设置相对当前文件描述符的位置. SEEK_END用于设置相对文件结尾的位置
    open(file, flags, mode), flags按位OR(O_RDONLY|O_WRONLY|O_RDWR|O_APPEND|O_DSYNC)
    openpty() 打开一台伪终端并返回PTY和TTY的一对文件描述符(master, slave)[Unix)
    pipe() 创建一个管道, 可用于与另外一进程建立单向通信.返回一对文件描述符(r,w), 分别用于读取和写入. 此函数同城在执行
           fork()函数之前调用. 在fork()函数之后,发送进程将关闭管道的读取端,而接收进程将关闭管道的写入端.至此管道被激
           活, 可以使用read()和write()函数将数据从一个进程发送到另外一个进程(UNIX)

    read(fd, n) 从文件描述符fd读取最多n个字节. 返回一个字节字符串
    write(fd, str) 将字符串str写入到文件描述符fd
"""


def __file_description__():
    pass


"""
文件与目录:
    access(path, accessmode) 检查此进程访问文件path的读取/写入/执行的权限. R_OK(读取), W_OK(写入), X_OK(执行), F_OK(存在).
                             访问得到授权返回1,否则返回0
    chflags(path, flags)  修改path上的文件标志. 以UF_开头的标志可以由任何用户设置, 以SF_开头的标志只能是超级用户才能修改.
        stat.UF_NODUMP 不转储文件                  stat.SF_ARCHIVED 文件可以存档
        stat.UF_IMMUTABLE 文件是只读的             stat.SF_IMMUTABLE 文件是只读的
        stat.UF_APPEND 文件只支持追加操作          stat.APPEND 文件只支持追加操作
        stat.UF_OPAQUE 目录是不透明的              stat.NOUNLINK 文件不能被删除或重命名
        stat.UF_NOUNLINK 文件不能被删除或重命名     stat.SF_SNAPSHOT 文件是一个快照文件

    chmod(path, mode)
    chown(path, uid, gid)
    lchmod(path, mode)   针对路径是符号链接
    lchown(path, uid, gid)  针对路径是符号链接
    link(src, dest) 硬链接

    listdir(path) 返回包含目录路径中各项名称的列表. 如果路径是Unicode编码的,结果列表将只包含Unicode字符串. 如果路径是字节字符串,
                  那么所有的文件名都以字节字符串列表的形式返回.

    makedev(major, minor) 创建原始的设备编号(Unix)
    makeidrs(path, mode, exist_ok) 递归创建目录. 如果叶子目录已存在或者无法创建,引发OSError
    mkdir(path, mode) 创建模式为数字mode的目录, 默认是模式是0777
    mkfifo(path, mode) 创建模式是数字的FIFO(命名管道), 默认模式是0666
    mknod(path, modem device) 创建特殊文件. mode是文件的权限和类型. 而device是使用os.makedev()函数创建的原始设备编号. 设置文件
                              的访问权限时,mode参数接收的参数与open()相同

    pathconf(path, name) 返回与路径名称path相关的可配置的系统参数

    symlink(src, dst) 创建指向src的名为dst的软链接(注意src和dest的目录格式一致)
    readlink(path) 返回一个路径,代表"符号链接path"指向的路径(UNIX)

    unlink(path) 删除"文件路径"
    remove(path) 删除"文件路径",与unlink()函数相同
    removedirs(path) 递归删除目录(空目录).递归删除叶子目录,对应于最右边路径部分的目录将被删除.
    rmdir(path) 删除目录路径(空目录)

    rename(src, dest) 将文件或目录重命名(注意src和dest的目录格式一致)
    renames(old, new) 递归的目录重命名和文件重命名函数. 首先会尝试创建命名路径所需的中间目录, 重命名之后,将使用removedirs()函数
                      删除对应于旧名称最右边路径部分的目录.

    utime(path, (atime, mtime)) 设置文件的访问时间和修改时间. 时间参数使用time.time()函数返回的数字来指定.
    walk(top, topdown, oneerror, followlinks) 创建一个生成器对象来遍历整棵目录树. top是指定目录的顶级, topdown是一个布尔值,用于
                                              指示是由上而下(默认)还是由下而上来遍历目录. 返回的生成器将生成元组(dirpath, dirnames, filenames)
                                              dirpath是一个字符串,包含通向目录的路径, dirnames是dirpath中所有的子目录. filenames
                                              是dirpath中文件的一个列表. oneerror是一个接收单参数的函数. 默认该函数什么也不做.
"""


def __file_and_dir__():
    s = os.readlink('/home/quinn/Desktop/a/b.md')
    print(s)
    # os.makedirs('/home/quinn/Desktop/a/b', mode=775, exist_ok=True)

"""
进程管理:
    abort() 生成发送给调用进程的SIGABORT信号. 除非使用处理器捕捉信号, 否则进程默认将以错误终止.

    execv(path, args) 使用参数args执行程序path,替代当前进程(即Python解释器).
    execve(path, args, env) 执行一个很像execv()的新程序, 但另外还接受一个字典env, 定义了程序运行的环境
    execvp(path, args) 很像execv(path, args), 但在目录列表中搜索可执行文件的过程中将复制shell的动作. 字典列表从enviro['PATH']中获取.

    execl(path, arg0, arg1, ...) 等价于execv(path, (arg0, arg1, ...)) 函数
    execle(path, arg0, arg1, ..., env) 等价于execve(path, (arg0, arg1, ...), env) 函数
    execlp(path, arg0, arg1, ...) 等价于execvp(path, (arg0, arg1, ...)函数

    _exit(n) 使用状态n立即退回到系统,同时不执行任何清理动作. 这同城只在由fork()函数创建的子进程中完成. 这与调用sys.exit()不相同,
             sys.exit()函数会正常关闭解释器. 退出代码n依赖于应用程序.
        EX_OK 没有错误
        EX_USAGE 错误的命令用法
        ...

    fork() 创建一个子进程. 在新创建的子进程中返回0, 在原始进程中返回子进程的进程ID. 子进程是原始进程的克隆,它们共享众多资源.
    forkpty() 创建一个子进程,并使用一台新的伪终端作为子进程的控制终端. 返回值(pid,fd) 其中pid在子进程中为0, 而fd是伪终端的主端的
              文件描述符.(UNIX)
    kill(pid, sig) 发送信号sig到进程pid. signal模块可以查找信号名称的列表
    killpg(pgid, sig) 发送信号sig到进程组pgid

    nice(increment) 提高进程的调度优先级("niceness"). 返回一个新的niceness. 用户一般只能降低进程的优先级, 只有root权限才可以提高
                    优先级

    plock(op) 将程序段锁在内存中, 从而防止它们被交换. op的值是一个整数.
    popen(command, mode, bufsize) 给名称打开一条管道. 返回值是连接到管道的打开文件对象. 根据模式是'r'(默认),还是'w', 读入或写入
                                  这个文件对象. 命令的退出状态由返回的文件对象的close()方法返回, 如果退出状态是0, 则返回None

    spawnv(mode, path, args) 在新进程中执行程序, 以命令行参数的形式传递args中指定的参数. args可以是列表或元组. args的第一个元素
                             是程序的名称. mode可以是以下值:
        P_WAIT  执行程序并等待它终止.
        P_NOWAIT 执行程序并返回进程句柄
        P_OVERLAY 执行程序并销毁调用进程(同exec函数)
        P_DETACH执行程序病从此程序分离.调用程序继续执行,但不会等等进程中创建的进程
    spawnve(mode, path, args, env)

    spawnl(mode, path, arg1, ..., argn)
    spawnle(mode, path, arg1, ..., argn, env)
    spawnlp(mode, file, arg1, ..., argn)  使用PATH环境变量的设置查找file(UNIX)

    startfile(path, operation) 运行文件和path相关的应用程序. 这样执行的动作在Windows Explorer中双击文件相同. 在应用程序运行之后,
                               函数就返回. 此外不能等待完成或者从应用程序活动退出代码. path的值是相对当前目录而言. operation是一
                               个可选的字符串,用于指定打开path时执行的动作, 默认值是'open', 'prinit', 'edit', explore', 'find'
    
    system(command)  在子shell中执行command(字符串). 在UNIX上,返回值和wait()函数一样是进程的退出状态.
    wait([pid]) 等待一个子进程完成并返回包含其进程ID和退出状态的元组. 退出状态是一个16位数字,其低位字节是终止进程的信号编号,而高位
                字节则是退出状态(如果信号编号是0). 如果生成了核心文件,就会设置低位字节的高位. pip参数指定了要等待的进程. 如果省略,
                当人员子进程退出时, wait()函数就会返回.

    waitpid(pid, options) 等待进程ID位pid的子进程的状态出现变化,就返回包含其进程ID和退出状态只是的一个元组(pid, status), 编码与\
                          wait()函数中相同.
                          options对应常规操作应该是0或者WNOHANG,以避免当没有子进程状态可用时出现挂起.此函数还可以收集只为某些原因
                          而停止执行的子进程的相关信息.
                          将options设置为WCONTINUED时,可以从一个"停止之后通过任务控制恢复操作的子进程"收集信息.
                          将options设置为WUNTRACED, 可用从一个"已经停止,但尚在未报告状态信息的子进程"收集信息.
    wait3([options]) 同waitpid(), 但此函数将等待所有子进程张的变化. 返回(pid, status,rusage). rusage包含resource.getrusage()
                    函数返回的资源使用信息.

    wait4(pid, options) 同waitpid(), 返回的元组与wait3()返回的相同.
    以下是使用waitpid(), wait3(), wait4()返回的进程状态码作为参数,检查进程的状态:
        WCOREDUMP(status) 如果是进程转储核心, 返回True
        WIFEXITED(status) 如果进程使用exit()系统调用退出,返回True
        WEXITSTATUS(status) 如果WIFEXITED(status)是True, 就返回exit()系统调用的整数参数, 否则返回值毫无意义
        WIFCONTINUED(status) 如果进程已经从任务控制停止恢复, 返回True
        WIFSIGNALED(status) 如果进程由于信号而退出, 返回True
        WIFSTOPPED(status) 如果进程已经停止,返回True
        WSTOPSIG(status) 返回导致进程停止的信号
        WTERMSIG(status) 返回导致进程退出的信号

"""
if __name__ == '__main__':
    __file_and_dir__()
    print(os.times())
