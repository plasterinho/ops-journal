FROM python:3.11-slim

WORKDIR /app

COPY metrics/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY reality ./reality
COPY docs/journal/week-06.checks.yaml ./docs/journal/week-06.checks.yaml
COPY metrics/metrics_server.py ./metrics_server.py

ENV OPS_JOURNAL_CHECKS_FILE=/app/docs/journal/week-06.checks.yaml

CMD ["python", "metrics_server.py"]
