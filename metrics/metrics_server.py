import os
import time

import yaml
from prometheus_client import REGISTRY, start_http_server
from prometheus_client.core import GaugeMetricFamily

from reality.engine import RealityEngine
from reality.kube_client import KubeClient

DEFAULT_CHECKS_FILE = "docs/journal/week-06.checks.yaml"
DEFAULT_PORT = 8000
STATUS_VALUES = ("PASS", "FAIL", "INVALID", "UNKNOWN")


def load_tasks(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except Exception as e:
        print(f"Error loading tasks from {path}: {e}")
        data = {}
    return data.get("tasks", [])


class RealityChecksCollector:
    def __init__(self, checks_file, ttl=30):
        self.checks_file = checks_file
        self.ttl = ttl
        self.engine = None

    def _get_engine(self):
        if self.engine is None:
            self.engine = RealityEngine(KubeClient(), ttl=self.ttl)
        return self.engine

    def collect(self):
        checks_total = GaugeMetricFamily(
            "ops_journal_reality_checks_total",
            "Reality check results grouped by status.",
            labels=["status"],
        )
        check_status = GaugeMetricFamily(
            "ops_journal_reality_check_status",
            "Reality check status per task.",
            labels=["task_id", "check_type", "status"],
        )
        cache_ttl = GaugeMetricFamily(
            "ops_journal_reality_engine_cache_ttl_seconds",
            "Reality engine cache TTL in seconds.",
        )
        cache_age = GaugeMetricFamily(
            "ops_journal_reality_engine_cache_age_seconds",
            "Age of the cached reality engine results in seconds.",
        )
        scrape_success = GaugeMetricFamily(
            "ops_journal_reality_scrape_success",
            "Whether the exporter could evaluate the configured checks.",
        )

        cache_ttl.add_metric([], float(self.ttl))

        status_counts = {status: 0 for status in STATUS_VALUES}

        try:
            engine = self._get_engine()
            tasks = load_tasks(self.checks_file)
            try:
                results = engine.evaluate(tasks)
            except Exception as e:
                import traceback
                print(f"Error during reality engine evaluation: {e}")
                traceback.print_exc()

            scrape_success.add_metric([], 1.0)
            cache_age.add_metric([], 0.0 if engine.last_run == 0 else max(0.0, time.time() - engine.last_run))

            for task in results:
                verification = task.get("verification") or {}
                status = verification.get("status", "UNKNOWN")
                if status not in status_counts:
                    status = "UNKNOWN"

                status_counts[status] += 1
                check_def = task.get("check") or {}
                check_type = check_def.get("type", "INVALID")
                task_id = task.get("id", "unknown")

                check_status.add_metric([task_id, check_type, status], 1.0)
        except Exception as e:
            print(f"Error occurred while evaluating tasks: {e}")
            scrape_success.add_metric([], 0.0)
            cache_age.add_metric([], 0.0)
            status_counts["UNKNOWN"] += 1

        for status, count in status_counts.items():
            checks_total.add_metric([status], float(count))

        yield checks_total
        yield check_status
        yield cache_ttl
        yield cache_age
        yield scrape_success


if __name__ == "__main__":
    print("=== METRICS SERVER START ===")
    print(f"Checks file exists: {os.path.exists(DEFAULT_CHECKS_FILE)}")
    checks_file = os.getenv("OPS_JOURNAL_CHECKS_FILE", DEFAULT_CHECKS_FILE)
    port = int(os.getenv("PORT", str(DEFAULT_PORT)))
    ttl = int(os.getenv("OPS_JOURNAL_CACHE_TTL", "30"))

    REGISTRY.register(RealityChecksCollector(checks_file=checks_file, ttl=ttl))
    start_http_server(port)
    print(f"Prometheus metrics server started on port {port} using {checks_file}")

    while True:
        time.sleep(3600)
