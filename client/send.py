from pika_client import Producer

if __name__ == "__main__":
    send = Producer("amqps://exchange:5671")
    send.declare_queue("hello")

    greetings = ["Hello", "Nǐn hǎo", "Namaste", "Hola", "Bonjour", "Asalaam alaikum", "Ciao", "Guten Tag", "Konnichiwa", "Hej"]
    for greeting in greetings:
        send.send_message(exchange="", routing_key="hello", body=greeting)
    
    send.close()
