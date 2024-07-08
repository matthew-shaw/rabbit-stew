from pika_client import Producer

if __name__ == "__main__":
    producer = Producer("amqps://exchange:5671")
    producer.declare_queue("greeting")

    greetings = [
        "Hello",
        "Nǐn hǎo",
        "Namaste",
        "Hola",
        "Bonjour",
        "Asalaam alaikum",
        "Ciao",
        "Guten Tag",
        "Konnichiwa",
        "Hej",
    ]
    for greeting in greetings:
        producer.send_message(exchange="", routing_key="greeting", body=greeting)

    producer.close()
