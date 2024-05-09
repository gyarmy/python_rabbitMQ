import pika

# RabbitMQ 连接参数
credentials = pika.PlainCredentials('demo001', 'demo001')
parameters = pika.ConnectionParameters('192.168.40.201', 5672, 'vhost001', credentials)

# 连接到 RabbitMQ
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# 声明交换器
channel.exchange_declare(exchange='gyarmy', exchange_type='fanout')

# 为每个消费者创建一个独立的队列
result = channel.queue_declare(queue='002', exclusive=True)
queue_name = result.method.queue

# 将队列绑定到交换器
channel.queue_bind(exchange='gyarmy', queue=queue_name)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())

channel.basic_consume(queue=queue_name,
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()