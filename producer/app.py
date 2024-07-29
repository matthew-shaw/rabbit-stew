import json
import os

from flask import Flask, Response, request
from jsonschema import ValidationError, validate

from client.rabbit_client import Producer

# Create a Flask app instance
app = Flask(__name__)

# Create a producer client instance
producer = Producer(host=os.environ.get("RABBITMQ_HOST", ""))

# Create a direct exchange
producer.declare_exchange(
    name=os.environ.get("RABBITMQ_EXCHANGE", ""),
    type=os.environ.get("RABBITMQ_EXCHANGE_TYPE", ""),
)

# Define request schema
task_schema = {
    "type": "object",
    "properties": {
        "task": {"type": "string"},
        "worker": {"type": "string"},
    },
    "required": ["task", "worker"],
}


@app.post("/v1/tasks")
def create_task():
    """Create a new task."""

    # Validate request body against schema
    try:
        validate(request.json, task_schema)
    except ValidationError as e:
        return Response(
            json.dumps({"message": e.message}, separators=(",", ":")),
            mimetype="application/json",
            status=400,
        )

    task = request.json

    # Publish messages to the exchange
    producer.publish(
        exchange=os.environ.get("RABBITMQ_EXCHANGE", ""),
        routing_key=task["worker"],
        message=request.data,
    )

    return Response(status=202)
