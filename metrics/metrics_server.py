from prometheus_client import start_http_server, Counter
import time
import random

REQUESTS = Counter(
    "ops_journal_requests_total",
    "Total number of requests received",
    ["env"]
)

def simulate_traffic():
    while True:
        for env in ["dev", "staging", "prod"]:
            REQUESTS.labels(env=env).inc(random.randint(0, 2))
        time.sleep(2)

if __name__ == "__main__":
    start_http_server(8000)
    print("Prometheus metrics server started on port 8000")
    simulate_traffic()