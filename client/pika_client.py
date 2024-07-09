import logging
import ssl
import time

import pika

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)


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
        self.channel.queue_declare(queue=queue_name, durable=True)

    def close(self):
        self.channel.close()
        self.connection.close()


class Producer(PikaClient):
    def publish(self, exchange, routing_key, body):
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=body,
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )
        logging.info(f"Sent message. Exchange: {exchange}, Routing Key: {routing_key}, Body: {body}")


class Consumer(PikaClient):
    def consume_messages(self, queue):
        def callback(ch, method, properties, body):
            logging.info(f"[x] Received {body}")
            time.sleep(2)  # Sleep to simulate real message processing happening here
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logging.info(f"[x] Acknowledged {body}")

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue, on_message_callback=callback)

        logging.info("[*] Waiting for messages...")
        self.channel.start_consuming()
