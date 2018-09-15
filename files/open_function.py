"""
open函数讲解:
    open(name, mode, buffering, encoding, errors, newline)
    name: 文件字符串路径
    mode: 打开的文件模式(参考__init__)

    buffering: 控制文件的缓冲行为. 0表示没有, 1表示进行了'行'缓冲, 负值表示采用系统的默认设置.
        其他任何正值表示使用近似缓冲区大小(字节为单位)

    encoding: 编码方式, 默认是'utf-8'

    errors: 可选,并且不能用于二进制模式，指定了编码错误的处理方式. 可选的的值如下:
        'strict': 遇到编码和解码错误时, 引发UnicodeError异常
        'ignore': 忽略无效编码
        'replace': 将无效字符替换为一个替换字符串(Unicode中的U+FFFD, 标准的字符串中的'?')
        'backslashreplace': 将无效字符替换为Python字符转义序列. 例如,将字符U+11234替换为'\u1234'
        'xmlcharrefreplace': 将无效字符替换为XML字符引用. 例如,将字符U+1234替换为'&#4660;'

    newline: 控制通用换行符模式(仅适用于文本模式). 它可以是None, '', '\n','\r', '\r\n'.
        从流读取输入时:
            如果newline为None, 则启用通用换行符模式. 输入中的行可以以'\n', '\r'或'\r\n'结尾,
        它们在返回给调用者之前被转换成'\n'.
            如果newline是'', 则启用通用换行符模式, 但"行结尾"将返回给调用者而不会转换.
            如果它具有任何其它合法值, 则输入行仅由给定字符串终止, 并且行结尾被返回给调用者而不会转换.

        将输出写入流时:
            如果newline为None, 则写入的任何'\n'字符都将转换为系统默认行分隔符os.linesep.
            如果newline是'', 则不会进行转换.
            如果newline是任何其他合法值, 写入的任何'\n'字符都将转换为给定字符串.
"""
import os

file = os.path.split(__file__)[0] + '/file.text'

with open(file, mode='r', encoding='ascii', errors='backslashreplace') as fd:
    print(fd.read())
    print(fd.readable())
    print(fd.tell())
