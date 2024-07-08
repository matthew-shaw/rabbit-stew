import logging
import ssl

import pika

logging.basicConfig(level=logging.INFO)


class PikaClient:
    def __init__(self, host):
        ssl_context = ssl.create_default_context(cafile="/ssl/ca_certificate.pem")
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.load_cert_chain("/ssl/client_exchange_certificate.pem", "/ssl/client_exchange_key.pem")

        parameters = pika.URLParameters(host)
        parameters.ssl_options = pika.SSLOptions(context=ssl_context)

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def declare_queue(self, queue_name):
        logging.info(f"Trying to declare queue({queue_name})...")
        self.channel.queue_declare(queue=queue_name)

    def close(self):
        self.channel.close()
        self.connection.close()


class Producer(PikaClient):
    def send_message(self, exchange, routing_key, body):
        channel = self.connection.channel()
        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body)
        logging.info(f"Sent message. Exchange: {exchange}, Routing Key: {routing_key}, Body: {body}")


class Consumer(PikaClient):
    def consume_messages(self, queue):
        def callback(ch, method, properties, body):
            logging.info(" [x] Received %r" % body)

        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

        logging.info(" [*] Waiting for messages...")
        self.channel.start_consuming()
