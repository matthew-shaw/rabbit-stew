import os

from rabbit_client import Consumer

if __name__ == "__main__":
    # Create a consumer client instance
    kids = Consumer(host=os.environ.get("RABBIT_HOST", ""))

    # Create a direct exchange
    kids.declare_exchange(name="chores", type="direct")

    # Create a queue and bind it to the exchange
    kids.declare_queue(name="kids_tasks")
    kids.bind_queue(exchange="chores", queue="kids_tasks", binding_key="kids")

    # Start consuming messages
    kids.consume_messages(queue="kids_tasks")
