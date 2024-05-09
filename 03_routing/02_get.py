import pika

# RabbitMQ 连接参数
credentials = pika.PlainCredentials('demo002', 'demo002')
parameters = pika.ConnectionParameters('192.168.40.201', 5672, 'vhost002', credentials)

# 连接到 RabbitMQ
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# 声明直接交换器
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# 为消费者创建一个独立的队列
result = channel.queue_declare(queue='001', exclusive=True)
queue_name = result.method.queue

# 绑定队列到交换器，指定关心的路由键
routing_keys = ['error']  # 这里只关心错误消息
for routing_key in routing_keys:
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=routing_key)

def callback(ch, method, properties, body):
    print(f" [x] Received {method.routing_key}: {body.decode()}")

channel.basic_consume(queue=queue_name,
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
