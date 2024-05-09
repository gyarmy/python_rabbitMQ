import pika
import random
import time

# RabbitMQ 连接参数
credentials = pika.PlainCredentials('demo002', 'demo002')
parameters = pika.ConnectionParameters('192.168.40.201', 5672, 'vhost002', credentials)

# 连接到 RabbitMQ
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# 声明一个主题类型的交换器
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
characters = ['刘备', '关羽', '张飞', '赵云', '马超', '黄忠', '魏延', '诸葛亮', '庞统', '姜维']

# 示例路由键
severity_levels = ['info', 'warning', 'error']
components = ['database', 'server', 'network']

try:
    for i in range(100):  # 发送10条消息
        severity = random.choice(severity_levels)
        component = random.choice(components)
        routing_key = f"{component}.{severity}"
        send_message = f"{random.choice(characters)}: {i}"
        message = f"Log: {routing_key} #{send_message}"
        channel.basic_publish(exchange='topic_logs',
                              routing_key=routing_key,
                              body=message)
        print(f" [x] Sent {routing_key}: {message}")
        time.sleep(3)
finally:
    # 关闭连接
    connection.close()
