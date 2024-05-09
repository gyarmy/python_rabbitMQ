# -*- coding: utf-8 -*-
# @Time    : 2024/5/8 14:15
# @Author  : GyArmy

import pika

# 连接到 RabbitMQ
credentials = pika.PlainCredentials('demo001', 'demo001')
virtual_host = 'vhost001'
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.40.201', 5672, virtual_host, credentials))
channel = connection.channel()

# 确保队列存在
channel.queue_declare(queue='hello')

# 定义接收消息的回调函数
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())

# 设置消费者
channel.basic_consume(queue='hello',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()




