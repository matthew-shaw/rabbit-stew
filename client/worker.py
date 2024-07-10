import os

from rabbit_client import Consumer

if __name__ == "__main__":
    # Create a consumer client instance
    consumer = Consumer(host=os.environ.get("RABBIT_HOST", ""))

    # Create a direct exchange
    consumer.declare_exchange(name="tasks", type="direct")

    # Create a queue and bind it to the exchange
    consumer.declare_queue(name="tasks")
    consumer.bind_queue(exchange="tasks", queue="tasks")

    # Start consuming messages
    consumer.consume_messages(queue="tasks")
