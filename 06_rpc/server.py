import pika

def on_request(ch, method, properties, body):
    n = int(body)
    print(f" [.] fib({n})")
    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def fib(n):
    print(f"get command: fib({n})")
    if n == 0:
        print(f"0-> user000")
    elif n == 1:
        print(f"1-> user001")
    else:
        print(f"{n}-> user{n:03d}")
    return n

credentials = pika.PlainCredentials('demo003', 'demo003')
parameters = pika.ConnectionParameters('192.168.40.201', 5672, 'vhost003', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
