import os

from client.rabbit_client import Consumer

if __name__ == "__main__":
    # Create a consumer client instance
    worker = Consumer(host=os.environ.get("RABBITMQ_HOST", ""))

    # Create a direct exchange
    worker.declare_exchange(
        name=os.environ.get("RABBITMQ_EXCHANGE", ""),
        type=os.environ.get("RABBITMQ_EXCHANGE_TYPE", "direct"),
    )

    # Create a queue and bind it to the exchange
    worker.declare_queue(name=os.environ.get("RABBITMQ_QUEUE", ""))
    worker.bind_queue(
        exchange=os.environ.get("RABBITMQ_EXCHANGE", ""),
        queue=os.environ.get("RABBITMQ_QUEUE", ""),
        binding_key=os.environ.get("RABBITMQ_BINDING_KEY", ""),
    )

    # Start consuming messages
    worker.consume_messages(queue=os.environ.get("RABBITMQ_QUEUE", ""))
