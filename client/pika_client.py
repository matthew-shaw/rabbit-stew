import logging
import ssl
import time
from typing import Literal

import pika  # type: ignore

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)


class PikaClient:
    """Base class with methods common to Producer and Consumer subclasses."""

    def __init__(self, host: str) -> None:
        """Creates a connection to the RabbitMQ host exchange over TLS with mutual SSL authentication"""
        ssl_context = ssl.create_default_context(cafile="/ssl/ca_certificate.pem")
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.load_cert_chain("/ssl/client_exchange_certificate.pem", "/ssl/client_exchange_key.pem")

        parameters = pika.URLParameters(host)
        parameters.ssl_options = pika.SSLOptions(context=ssl_context)

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def declare_exchange(self, name: str, type: Literal["direct", "fanout", "topic", "headers"]) -> None:
        logging.info(f"Trying to declare exchange({name})...")
        self.channel.exchange_declare(exchange=name, exchange_type=type)

    def declare_queue(self, name: str, exclusive=False) -> None:
        logging.info(f"Trying to declare queue({name})...")
        self.channel.queue_declare(queue=name, exclusive=exclusive, durable=True)

    def close(self) -> None:
        self.channel.close()
        self.connection.close()


class Producer(PikaClient):
    def publish(self, exchange: str, routing_key: str, message: str) -> None:
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )
        logging.info(f"Sent message. Exchange: {exchange}, Routing Key: {routing_key}, Body: {message}")


class Consumer(PikaClient):
    def bind_queue(self, exchange: str, queue: str) -> None:
        logging.info(f"Trying to bind queue({queue}) to exchange({exchange})...")
        self.channel.queue_bind(exchange=exchange, queue=queue)

    def consume_messages(self, queue: str) -> None:
        def callback(ch, method, properties, body):
            logging.info(f"[x] Received {body}")
            time.sleep(2)  # Sleep to simulate real message processing happening here
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logging.info(f"[x] Acknowledged {body}")

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue, on_message_callback=callback)

        logging.info("[*] Waiting for messages...")
        self.channel.start_consuming()
