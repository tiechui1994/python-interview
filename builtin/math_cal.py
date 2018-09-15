"""
数学计算类内置函数:
    abs(num)
    complex(real, imag) 复数
    divmod(m, n) m/n 的商和余数
    pow(x, y) x^y
    pow(x, y, z) (x^y)%z
    round(float, n) 四舍五入,保留n位小数
    sum(iterable, start=0) iterable求和

    bin(n) 二进制
    oct(n) 八进制
    hex(n) 十六进制

    chr(n)  数字 -> Unicode
    ord(char) Unicode -> 数字
"""

print(abs(-1.1))

print(complex(1, 2))

print(divmod(23, 11))

print(pow(2, 3))

print(round(3.362627, 2))

print(sum([1, 2, 3], 9))

print(bin(10))
print(oct(10))
print(hex(0xA))

print(chr(10000))
print(ord('✐'))
