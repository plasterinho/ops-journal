FROM python:3.11-slim

WORKDIR /app

RUN pip install prometheus_client

COPY metrics_server.py .

CMD ["python", "metrics_server.py"]