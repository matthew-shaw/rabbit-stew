from pika_client import Producer

if __name__ == "__main__":
    producer = Producer(host="amqps://exchange:5671")
    producer.declare_exchange(name="tasks", type="direct")

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
        producer.publish(exchange="tasks", routing_key="tasks", message=task)

    producer.close()
