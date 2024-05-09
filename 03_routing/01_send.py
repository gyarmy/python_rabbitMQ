import time
import pika
import random

from pika.exchange_type import ExchangeType

# RabbitMQ 连接参数
credentials = pika.PlainCredentials('demo002', 'demo002')
parameters = pika.ConnectionParameters('192.168.40.201', 5672, 'vhost002', credentials)

# 连接到 RabbitMQ
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# 声明一个直接类型的交换器
# channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
channel.exchange_declare(exchange='direct_logs', exchange_type=ExchangeType.direct)

# 模拟不同类型的路由键
severity_levels = ['info', 'warning', 'error']

characters = ['刘备', '关羽', '张飞', '赵云', '马超', '黄忠', '魏延', '诸葛亮', '庞统', '姜维']

try:
    for i in range(10):  # 发送10条消息
        severity = random.choice(severity_levels)  # 随机选择一个路由键
        send_message = f"{random.choice(characters)}: {i}"
        message = f"Log: {severity} #{send_message}"
        channel.basic_publish(exchange='direct_logs',
                              routing_key=severity,
                              body=message)
        print(f" [x] Sent {severity}: {message}")
        time.sleep(3)
finally:
    # 关闭连接
    connection.close()
