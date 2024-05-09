import pika
import time
import random

# RabbitMQ 连接参数
credentials = pika.PlainCredentials('demo001', 'demo001')
parameters = pika.ConnectionParameters('192.168.40.201', 5672, 'vhost001', credentials)

# 连接到 RabbitMQ
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# 声明一个扇出类型的交换器
channel.exchange_declare(exchange='gyarmy', exchange_type='fanout')

# 三国人物列表
characters = ['刘备', '关羽', '张飞', '赵云', '马超', '黄忠', '魏延', '诸葛亮', '庞统', '姜维']

try:
    while True:
        random_number = random.randint(1, 100)  # 生成一个随机数
        send_message = f"{random.choice(characters)}: {random_number}"
        channel.basic_publish(exchange='gyarmy',
                              routing_key='',  # 在扇出交换器中，routing_key 会被忽略
                              body=str(send_message))
        print(f" [x] Sent '{send_message}'")
        time.sleep(3)  # 每3秒发送一次
finally:
    # 关闭连接
    connection.close()