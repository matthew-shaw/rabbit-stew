import os

from rabbit_client import Consumer

if __name__ == "__main__":
    consumer = Consumer(host=os.environ.get("RABBIT_HOST", ""))
    consumer.declare_exchange(name="tasks", type="direct")
    consumer.declare_queue(name="tasks")
    consumer.bind_queue(exchange="tasks", queue="tasks")
    consumer.consume_messages(queue="tasks")
    consumer.close()
