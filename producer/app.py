import os

from flask import Flask, Response, request

from client.rabbit_client import Producer

app = Flask(__name__)

# Create a producer client instance
producer = Producer(host=os.environ.get("RABBITMQ_HOST", ""))

# Create a direct exchange
producer.declare_exchange(
    name=os.environ.get("RABBITMQ_EXCHANGE", ""),
    type=os.environ.get("RABBITMQ_EXCHANGE_TYPE", "direct"),
)


@app.post("/v1/tasks")
def create_task():
    """Create a new task."""

    task = request.json

    # Publish messages to the exchange
    producer.publish(
        exchange=os.environ.get("RABBITMQ_EXCHANGE", ""),
        routing_key=task["worker"],
        message=request.data,
    )

    return Response(status=202)
