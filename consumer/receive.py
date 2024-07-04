import os
import ssl
import sys

import pika


def main():
    ssl_context = ssl.create_default_context(cafile="/ssl/ca_certificate.pem")
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    ssl_context.load_cert_chain("/ssl/client_exchange_certificate.pem", "/ssl/client_exchange_key.pem")

    parameters = pika.URLParameters("amqps://exchange:5671")
    parameters.ssl_options = pika.SSLOptions(context=ssl_context)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue="hello")

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
