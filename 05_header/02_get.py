import pika

# RabbitMQ 连接参数
credentials = pika.PlainCredentials('demo003', 'demo003')
parameters = pika.ConnectionParameters('192.168.40.201', 5672, 'vhost003', credentials)

# 连接到 RabbitMQ
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# 声明头交换器
channel.exchange_declare(exchange='headers_logs', exchange_type='headers')

# 为消费者创建一个独立的队列
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# 绑定队列到交换器，设置匹配的头信息
bind_headers = {
    'category': 'info',
    'type': 'report',
    'x-match': 'all'  # 可以设置为'all'或'any'
}
channel.queue_bind(exchange='headers_logs', queue=queue_name, arguments=bind_headers)

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()} with headers: {properties.headers}")

channel.basic_consume(queue=queue_name,
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
