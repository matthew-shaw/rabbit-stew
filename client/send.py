from pika_client import Producer

if __name__ == "__main__":
    send = Producer("amqps://exchange:5671")
    send.declare_queue("hello")
    send.send_message(exchange="", routing_key="hello", body=b"Hello World!")
    send.close()
