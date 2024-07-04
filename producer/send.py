import ssl

import pika

ssl_context = ssl.create_default_context(cafile="/ssl/ca_certificate.pem")
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.load_cert_chain("/ssl/client_exchange_certificate.pem", "/ssl/client_exchange_key.pem")

parameters = pika.URLParameters("amqps://exchange:5671")
parameters.ssl_options = pika.SSLOptions(context=ssl_context)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue="hello")

channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")
print(" [x] Sent 'Hello World!'")
connection.close()
