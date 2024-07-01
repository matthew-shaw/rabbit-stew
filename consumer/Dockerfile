FROM python:3.12-slim

RUN useradd appuser

WORKDIR /home/appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt receive.py ./
RUN pip install -r requirements.txt \
    && chown -R appuser:appuser ./

USER appuser