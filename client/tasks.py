from pika_client import Producer

if __name__ == "__main__":
    producer = Producer("amqps://exchange:5671")
    producer.declare_queue("tasks")

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
        producer.publish(exchange="", routing_key="tasks", body=task)

    producer.close()
