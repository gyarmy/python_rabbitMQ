# -*- coding: utf-8 -*-
# @Time    : 2024/5/8 14:18
# @Author  : GyArmy

import pika
import time
import random

# 连接到 RabbitMQ
credentials = pika.PlainCredentials('demo001', 'demo001')
virtual_host = 'vhost001'
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.40.201', 5672, virtual_host, credentials))
channel = connection.channel()

# 创建队列
channel.queue_declare(queue='hello')

# 三国人物列表
characters = ['刘备', '关羽', '张飞', '赵云', '马超', '黄忠', '魏延', '诸葛亮', '庞统', '姜维']

try:
    while True:
        random_number = random.randint(1, 100)  # 生成一个随机数
        # 从三国人物列表中随机选择一个人物
        random_character = random.choice(characters)
        # 发送消息
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=str(random_character + ' ' + str(random_number)))
        print(f" [x] Sent '{random_number}'")
        time.sleep(2)  # 每2秒发送一次
finally:
    # 关闭连接
    connection.close()