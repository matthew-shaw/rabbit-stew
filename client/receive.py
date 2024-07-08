from pika_client import Consumer

if __name__ == "__main__":
    consumer = Consumer("amqps://exchange:5671")
    consumer.declare_queue("greeting")
    consumer.consume_messages("greeting")
    consumer.close()
