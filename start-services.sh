#!/bin/sh
set -eu

PYTHONPATH=/app python3 /app/metrics/metrics_server.py &

exec nginx -g 'daemon off;'
