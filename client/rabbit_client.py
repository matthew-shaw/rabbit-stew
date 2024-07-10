import logging
import ssl
import time
from typing import Literal

import pika  # type: ignore

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)


class RabbitClient:
    """Base class with methods common to Producers and Consumers."""

    def __init__(self, host: str) -> None:
        """Creates a secure connection to the RabbitMQ host with TLS and mutual SSL authentication"""
        ssl_context = ssl.create_default_context(cafile="/ssl/ca_certificate.pem")
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.load_cert_chain("/ssl/client_broker_certificate.pem", "/ssl/client_broker_key.pem")

        parameters = pika.URLParameters(host)
        parameters.ssl_options = pika.SSLOptions(context=ssl_context)

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        logging.info(f"Established secure connection to: '{host}'")

    def declare_exchange(self, name: str, type: Literal["direct", "fanout", "topic", "headers"]) -> None:
        """Creates a new exchange with a given name and type."""
        self.channel.exchange_declare(exchange=name, exchange_type=type)
        logging.info(f"Declared exchange: '{name}'...")

    def declare_queue(self, name: str, exclusive=False) -> None:
        """Creates a new durable queue with a given name."""
        self.channel.queue_declare(queue=name, exclusive=exclusive, durable=True)
        logging.info(f"Declared queue: '{name}'...")

    def close(self) -> None:
        """Closes the channel and connection."""
        self.channel.close()
        self.connection.close()
        logging.info("Closed connection")


class Producer(RabbitClient):
    """Producer clients publish messages."""

    def publish(self, exchange: str, routing_key: str, message: str) -> None:
        """Publishes a message with a routing key to an exchange."""
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )
        logging.info(f"Sent message '{message}' to exchange '{exchange}' with routing key '{routing_key}'")


class Consumer(RabbitClient):
    """Consumer clients bind queues and consume messages."""

    def bind_queue(self, exchange: str, queue: str, binding_key: str) -> None:
        """Binds an existing queue to an exchange."""
        self.channel.queue_bind(exchange=exchange, queue=queue, routing_key=binding_key)
        logging.info(f"Bound queue '{queue}' to exchange '{exchange}' with binding key '{binding_key}'...")

    def consume_messages(self, queue: str) -> None:
        """Starts consuming messages from a queue."""

        def callback(ch, method, properties, body):
            logging.info(f"Received message: '{body}'")
            time.sleep(2)  # Sleep to simulate real message processing happening here
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logging.info(f"Acknowledged message: '{body}'")

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue, on_message_callback=callback)

        logging.info(f"Waiting for messages on queue: '{queue}'...")
        self.channel.start_consuming()
