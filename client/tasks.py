import os

from rabbit_client import Producer

if __name__ == "__main__":
    # Create a producer client instance
    producer = Producer(host=os.environ.get("RABBIT_HOST", ""))

    # Create a direct exchange
    producer.declare_exchange(name="tasks", type="direct")

    # Make up some messages
    tasks = [
        "Clean the bathroom",
        "Clean the bedroom",
        "Clean the kitchen",
        "Clean the windows",
        "Clear the table",
        "Cook dinner",
        "Do the shopping",
        "Dry clothes",
        "Feed the pets",
        "Make the bed",
        "Mop the floor",
        "Prepare lunch",
        "Put clothes away",
        "Put the dishes away",
        "Set the table",
        "Take out the bins",
        "Vacuum the floors",
        "Wash clothes",
        "Wash the dishes",
        "Water the plants",
    ]
    for task in tasks:
        # Publish messages to the exchange
        producer.publish(exchange="tasks", routing_key="tasks", message=task)

    # Close the connection
    producer.close()
