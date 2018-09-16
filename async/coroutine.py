"""
协程调度
"""
import random
import time


def get_data():
    """返回0到9之间的3个随机数,模拟异步操作"""
    return random.sample(range(100), 3)


def consume():
    """显示每次传入的整数列表的动态平均值"""
    running_sum = 0
    data_items_seen = 0

    while True:
        print('Waiting to consume')
        data = yield  # channel传递的数据, 阻塞
        data_items_seen += len(data)
        running_sum += sum(data)
        print('Consumed, the running average is {}'.format(running_sum / float(data_items_seen)))


def produce(channel):
    """生产者, channel是通信的信道"""
    while True:
        data = get_data()  # 获取数据
        print('Produced {}'.format(data))
        channel.send(data)  # 发送数据
        yield  # 阻塞


if __name__ == '__main__':
    consumer = consume()
    consumer.send(None)
    producer = produce(consumer)

    start = time.time()
    for _ in range(1000000):
        print('Producing...')
        next(producer)
    end = time.time()
    print((end - start))
