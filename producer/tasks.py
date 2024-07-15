import os

from client.rabbit_client import Producer

if __name__ == "__main__":
    # Create a producer client instance
    producer = Producer(host=os.environ.get("RABBITMQ_HOST", ""))

    # Create a direct exchange
    producer.declare_exchange(
        name=os.environ.get("RABBITMQ_EXCHANGE", ""),
        type=os.environ.get("RABBITMQ_EXCHANGE_TYPE", "direct"),
    )

    # Create some household chores
    chores = [
        {"task": "Clean the bathroom", "worker": "cleaner"},
        {"task": "Clean the bedroom", "worker": "cleaner"},
        {"task": "Clean the kitchen", "worker": "cleaner"},
        {"task": "Clean the windows", "worker": "cleaner"},
        {"task": "Clear the table", "worker": "kids"},
        {"task": "Cook dinner", "worker": "parents"},
        {"task": "Do the shopping", "worker": "parents"},
        {"task": "Dry clothes", "worker": "parents"},
        {"task": "Feed the pets", "worker": "kids"},
        {"task": "Make the bed", "worker": "parents"},
        {"task": "Mop the floor", "worker": "cleaner"},
        {"task": "Mow the grass", "worker": "gardener"},
        {"task": "Prepare lunch", "worker": "parents"},
        {"task": "Put clothes away", "worker": "parents"},
        {"task": "Put the dishes away", "worker": "parents"},
        {"task": "Set the table", "worker": "kids"},
        {"task": "Take out the bins", "worker": "parents"},
        {"task": "Trim hedges", "worker": "gardener"},
        {"task": "Vacuum the floors", "worker": "cleaner"},
        {"task": "Wash clothes", "worker": "parents"},
        {"task": "Wash the dishes", "worker": "parents"},
        {"task": "Water the plants", "worker": "gardener"},
    ]

    for chore in chores:
        # Publish messages to the exchange
        producer.publish(
            exchange=os.environ.get("RABBITMQ_EXCHANGE", ""),
            routing_key=chore["worker"],
            message=chore["task"],
        )

    # Close the connection
    producer.close()
