import os

from rabbit_client import Consumer

if __name__ == "__main__":
    # Create a consumer client instance
    parents = Consumer(host=os.environ.get("RABBIT_HOST", ""))

    # Create a direct exchange
    parents.declare_exchange(name="chores", type="direct")

    # Create a queue and bind it to the exchange
    parents.declare_queue(name="parents_tasks")
    parents.bind_queue(exchange="chores", queue="parents_tasks", binding_key="parents")

    # Start consuming messages
    parents.consume_messages(queue="parents_tasks")
