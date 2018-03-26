import time
import datetime

# 生成时间戳
var = time.time()
print(var)

# 生成格式化的时间字符串
var = time.ctime()
print(var)
var = time.strftime('%Y-%m-%d %H:%M:%S')
print(var)

# 生成结构化时间
var = time.gmtime()
print(var)
var = time.localtime()
print(var)

# 时间戳转结构化时间
var = time.gmtime(time.time())
print(var)
var = time.localtime(time.time())
print(var)

# 时间戳转格式化时间字符串
var = time.ctime(time.time())
print(var)

# 结构化时间转时间戳
var = time.mktime(time.localtime())
print(var)

# 结构化时间转格式化的时间字符串
var = time.strftime('%Y-%m-%d', time.gmtime())  # 参数说明: 格式化字符串和结构化时间
print(var)
var = time.asctime(time.localtime())
print(var)

# 格式化的时间字符串转结构化时间
var = time.strptime('2018-11-12', '%Y-%m-%d')
print(var)
var = time.strptime('Sun Feb 11', '%a %b %d')
print(var)

# 格式化时间转时间戳
var = time.mktime(time.strptime('Sun Feb 11 11:21:47 2018', "%a %b %d %H:%M:%S %Y"))
print(var)
var = time.mktime(time.strptime('2018-02-11 11:23:57', "%Y-%m-%d %H:%M:%S"))
print(var)

# datetime.datetime
var = datetime.datetime.now()
print(var)
var = datetime.datetime(year=2018, month=1, day=3)
print(var)

# datetime.timedelta
var = datetime.timedelta(days=5, seconds=1, microseconds=22222, minutes=11, hours=11, weeks=1)
print(var)

# datetime.date
var = datetime.date(year=2018, month=1, day=3)
print(var)

# datetime.time
var = datetime.time(hour=4, minute=32, second=23, microsecond=22222)
print(var)

# 字符串转datetime对象
var = datetime.datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
print(var)
var = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
print(var)

# 时间戳转datetime对象
var = datetime.datetime.fromtimestamp(time.time())
print(var)
var = datetime.datetime.utcfromtimestamp(time.time())
print(var)

# datetime对象转格式化时间字符
var = datetime.datetime(2018, 1, 5, 15, 19, 59).strftime("%Y-%m-%d %H:%M:%S")
print(var)

# datetime对象转结构化时间
var = datetime.datetime(2018, 1, 5, 15, 19, 59).timetuple()
print(var)
