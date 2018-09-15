import os
from configparser import ConfigParser

"""
ConfigParser: 一个解析ini文件的辅助工具

ini文件格式:
# 下面的内容将被写入到配置(空格自动被忽略)
[section]
key = value
key : value

# 下面的内容将被忽略
;[section]
;key = value
#key : value

使用:
    ConfigParser() 创建一个可配置对象

    read(path) 加载配置文件到内存当中
    read_dict(dictionary) 从字典当中加载配置,dictionary实质上也是配置文件在内存的存储方式

    write(fd) 保持配置文件到硬盘

    get(section, option)  section是段, option是段当中的键值对的键, 值默认存的是字符串
    set(section, option, value)

    getbool(section, option)
    getint(section, option)

    has_section(section)
    has_option(section, option)

    remove_section(section)
    remove_option(section, option)

    sections()  获取所有的section
    options(section) 获取section当中所有的key(列表)

    add_section(section) 增加一个section
"""

base_path = os.path.split(os.path.realpath(__file__))[0]
config = ConfigParser()
config.read(os.path.join(base_path, 'config.ini'))

print(config.sections())

dictionary = {
    'user': {
        'name': 'root',
        'passwd': '1234'
    }
}
config.read_dict(dictionary=dictionary)
print(config.sections())
