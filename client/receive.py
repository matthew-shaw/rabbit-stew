from pika_client import Consumer

if __name__ == "__main__":
    receive = Consumer("amqps://exchange:5671")
    receive.declare_queue("hello")
    receive.consume_messages("hello")
    receive.close()
