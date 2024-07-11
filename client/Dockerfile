FROM python:3.12-slim

RUN useradd appuser

WORKDIR /home/appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt rabbit_client.py tasks.py parent.py kid.py ./
COPY ssl/ca_certificate.pem ssl/client_broker_certificate.pem ssl/client_broker_key.pem /ssl/
RUN pip install -r requirements.txt \
    && chown -R appuser:appuser ./ \
    && chown -R appuser:appuser /ssl/

USER appuser