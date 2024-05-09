import pika
import random
import time

# RabbitMQ 连接参数
credentials = pika.PlainCredentials('demo003', 'demo003')
parameters = pika.ConnectionParameters('192.168.40.201', 5672, 'vhost003', credentials)

# 连接到 RabbitMQ
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# 声明一个头交换器
channel.exchange_declare(exchange='headers_logs', exchange_type='headers')

# 发送消息
headers = {
    'category': 'info',
    'type': 'report'
}

channel.basic_publish(exchange='headers_logs',
                      routing_key='',  # 对于头交换器，路由键将被忽略
                      body='Header Message: Reporting Info',
                      properties=pika.BasicProperties(headers=headers))

print(f" [x] Sent message with headers: {headers}")

# 关闭连接
connection.close()
