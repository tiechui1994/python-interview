"""
os.path模块
"""
import os.path as path

"""
    abspath(path) 返回路径名称path的绝对路径,同时将当前的工作目录考虑在内.
    basename(path) 返回路径path的"基本名称"
    dirpath(path) 返回path的目录名称
    commonprefix(list) 返回list当中所有字符串去最长公共前缀

    expandvars(path) 扩展path中的$name,或${name} 格式的环境变量. 不符合规范或不存在的变量名称将保持不变

    getatime(path) 返回最后一次访问path的时间(时间戳)
    getctime(path) 最后一次修改的时间
    getmtime(path) 最后一次修改的时间

    getsize(path) 返回path的大小,字节为单位

    isabs(path) 是否是绝对路径
    isfile(path) 是否是普通文件
    isdir(path) 是否是目录
    islink(path) 是否是引用的符号链接
    ismount(path) 是否是挂载点

    exists(path) 如果path引用的是现有路径,返回True. 如果path引用的是已经损坏的符号链接,返回False
    lexists(path) path存在,返回True. 对所有符号链接均返回True,即便是链接已经损坏

    join(path1, path2, ...) 将一个或多个路径智能的连接成一个路径名称
    norpath(path) 标准化路径名称. 将折叠多余(或冗长的)分隔符和上层引用.
    realpath(path) 返回path的真实路径,并去除路径中所有符号链接

    relpath(path, start) 返回从start目录到path的一条相对路径.

    sameopenfile(fd1, fd2) 打开的文件对象fd1,fd2引用同一个文件,返回True

    split(path) 将文件拆分为(head, tail)对 => (dirname(), basename())
    splittext(path) (filename, extension) 文件名和文件后缀名
"""


def __os_path__():
    print(path.expandvars('$HOME'))
    print(path.realpath('/home/quinn/Desktop/a/b.md'))  # /home/quinn/Desktop/a/b/a.md


if __name__ == '__main__':
    __os_path__()
