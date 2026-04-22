FROM python:3.11-slim

WORKDIR /app

COPY metrics/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY reality ./reality
COPY metrics/metrics_server.py ./metrics_server.py

CMD ["python", "metrics_server.py"]
