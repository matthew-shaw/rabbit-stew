import ssl

import pika


class PikaClient:
    def __init__(self, host):
        ssl_context = ssl.create_default_context(cafile="/ssl/ca_certificate.pem")
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.load_cert_chain(
            "/ssl/client_exchange_certificate.pem", "/ssl/client_exchange_key.pem"
        )

        parameters = pika.URLParameters(host)
        parameters.ssl_options = pika.SSLOptions(context=ssl_context)

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def declare_queue(self, queue_name):
        print(f"Trying to declare queue({queue_name})...")
        self.channel.queue_declare(queue=queue_name)

    def close(self):
        self.channel.close()
        self.connection.close()


class Producer(PikaClient):
    def send_message(self, exchange, routing_key, body):
        channel = self.connection.channel()
        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body)
        print(
            f"Sent message. Exchange: {exchange}, Routing Key: {routing_key}, Body: {body}"
        )


class Consumer(PikaClient):
    def consume_messages(self, queue):
        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)

        self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=True
        )

        print(" [*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()
