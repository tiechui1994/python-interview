"""
random 模块: 提供各种用于生成伪随机数的函数, 以及根据不同的实数分布来随机生成值的函数
"""
"""
种子和初始化:(控制基础随机数生成器的状态)
    seed([x]) 初始化随机数生成器. 如果省略x或x为None,则使用系统时间来设置生成器. 如果x是整数或者长整数,则使用该值.
        如果x不是整数,那么它必须是可散列的对象且将hash(x)的值作为种子
    getstate() 返回当前生成器状态的对象.
    setstate(state)  恢复随机数生成器的状态
    jumpahead(n) 如果在一行中调用了n次random(),则快速将生成器状态改为其应有的状态,n必须是非负整数

随机整数:
    getrandbits(k) 创建包含k个随机位的长整数
    randint(a,b) 返回随机整数x, a<= x <= b
    randrange(start, stop, [step]) 返回一个范围在(start,stop,step)之间的随机整数

随机序列:
    choice(seq) 从非空序列seq中返回一个随机元素
    sample(s, len) 返回长度为len的序列,它包含从序列s中随机选择的元素
    shuffle(x, [random]) 随机原地打乱"列表x"中的项, random是可选参数,指定随机生成函数. 如果提供该参数,则该参数
        是一个无参的函数,且该函数的返回值在[0.0, 1.0)范围内

实值随机分布:
    random() 返回范围[0.0, 1.0)之间的随机数
    uniform(a, b) 返回范围在[a,b) 之间的一致分布随机数

    betavariate(alpha,beta) 从Beta分布中返回一个在0和1之间的值,其中alpha > -1 而 beta > -1
    cunifvariate(mean, arc) 圆形一致分布,mean是平均角, arc是沿平均角周围居中的分布范围. 这些值必须设置在0-pi之间
        的弧度范围内.返回值范围(mean - arc/2, mean + arc/2)
    expovariate(lambd) 指数分布,lambd是由1.0除以预期均值,返回范围是[0, +OO)
    gammavariate(alpha, beta) Gamma分布,其中alpha > -1 beta > 0
    gauss(mu, sigma) 均值为mu标准偏差为sigma的高斯分布
    lognormvariate(mu, sigma) 对数分布,取该分布的自然对数的结果是均值为mu且标准差为sigma的正态分布

注意:
    1.该模块的函数非线程安全. 不同线程中设生成随机数,就应当使用锁定以防止并发访问
    2.该模块生成的随机数都是确定的,不应用于密码
    3.通过实现random.Random的子类病实现random(),seed(),getstate(),setstate()和jumpahead(), 就可以创建新的随机数生成
    器类型. 实际上,该模块的其他函数在内部都作为Random的方法实现的
    4. 该模块提供了两种生成器类--WichmannHill(早期Python版本所使用的生成器)和SystemRandom(使用系统随机数生成器os.urandom()
    生成随机数).
"""
