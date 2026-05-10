#!/usr/bin/env python3

# Import standard libraries
from contextvars import ContextVar
from dataclasses import dataclass
import logging
import os
from socketserver import ThreadingMixIn
from threading import Thread
import time
from uuid import uuid4
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer, make_server

# Import third-party libraries
# VSCode complains about missing prometheus_client types, but these are covered by the requirements.txt
# and should be installed in the environment. We ignore the import error for type checking.
import yaml
try:
    from prometheus_client import REGISTRY, make_wsgi_app  # type: ignore[import]
except ImportError:
    REGISTRY = None
    make_wsgi_app = None
from prometheus_client.core import GaugeMetricFamily # type: ignore[import]

# Import local modules
from reality.engine import RealityEngine
from reality.kube_client import KubeClient

# Constants
# The file path is set to a default value, but it can be overridden
# by the OPS_JOURNAL_CHECKS_FILE environment variable.
DEFAULT_CHECKS_FILE = "docs/journal/week-06.checks.yaml"

# The port number is set to a default value, but it can be overridden
# by the PORT environment variable.
DEFAULT_PORT = 8000

# The possible status values for reality checks.
# This is used to categorize the results of the checks.
STATUS_VALUES = ("PASS", "FAIL", "INVALID", "UNKNOWN")


@dataclass(frozen=True)
class RequestContext:
    request_id: str
    method: str
    path: str


DEFAULT_REQUEST = RequestContext(request_id="unknown", method="unknown", path="unknown")
CURRENT_REQUEST = ContextVar("current_request", default=DEFAULT_REQUEST)
logger = logging.getLogger(__name__)


class ThreadingMetricsServer(ThreadingMixIn, WSGIServer):
    daemon_threads = True


class MetricsRequestHandler(WSGIRequestHandler):
    def log_message(self, format, *args):
        logger.debug(format, *args)


def build_request_context(environ):
    return RequestContext(
        request_id=environ.get("HTTP_X_REQUEST_ID") or str(uuid4()),
        method=environ.get("REQUEST_METHOD", "unknown"),
        path=environ.get("PATH_INFO", "unknown"),
    )


def build_metrics_app(registry):
    metrics_app = make_wsgi_app(registry) # type: ignore[misc]

    def app(environ, start_response):
        request = build_request_context(environ)
        token = CURRENT_REQUEST.set(request)
        response = None

        try:
            response = metrics_app(environ, start_response)
            for chunk in response:
                yield chunk
        finally:
            if hasattr(response, "close"):
                response.close()
            CURRENT_REQUEST.reset(token)

    return app


def start_metrics_server(port, registry):
    app = build_metrics_app(registry)
    httpd = make_server(
        "",
        port,
        app,
        server_class=ThreadingMetricsServer,
        handler_class=MetricsRequestHandler,
    )
    thread = Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd

# Function to load tasks from a YAML file. It reads the file, parses the YAML
# content, and returns the list of tasks. If there is an error during loading,
# it prints the error and returns an empty list.
def load_tasks(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except Exception as e:
        print(f"Error loading tasks from {path}: {e}")
        data = {}
    return data.get("tasks", [])

# The RealityChecksCollector class is responsible for collecting metrics
# related to reality checks.
class RealityChecksCollector:
    # The constructor initializes the collector with the path to the checks
    # file and the TTL for the reality engine cache.
    def __init__(self, checks_file, ttl=30):
        self.checks_file = checks_file
        self.ttl = ttl
        self.engine = None

    # The _get_engine method initializes the RealityEngine if it hasn't been
    # created yet, and returns the engine instance. The engine is created with
    # a KubeClient and the specified TTL for caching results.
    def _get_engine(self):
        if self.engine is None:
            self.engine = RealityEngine(KubeClient(), ttl=self.ttl)
        return self.engine

    # The collect method is called by the Prometheus client to gather metrics. It
    # creates several GaugeMetricFamily instances to represent different metrics,
    # such as the total number of checks by status, the status of each check, the
    # cache TTL, the age of the cache, and whether the scrape was successful. It
    # then evaluates the reality checks using the engine and populates the metrics
    # accordingly. If there are any errors during evaluation, it handles them and
    # updates the metrics to reflect the failure.
    # Finally, it yields the collected metrics to be exposed by the Prometheus server.
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

        # Set the cache TTL metric to the configured TTL value.
        # This indicates how long the reality engine will cache results before re-evaluating.
        cache_ttl.add_metric([], float(self.ttl))

        status_counts = {status: 0 for status in STATUS_VALUES}

        # Initialize an empty list to hold the results of the reality checks. This will be populated
        # after evaluating the checks with the reality engine.
        results = []

        try:
            engine = self._get_engine()
            tasks = load_tasks(self.checks_file)

            request = CURRENT_REQUEST.get()
            logger.debug(
                "request_id=%s method=%s path=%s loaded_tasks=%s checks_file=%s",
                request.request_id,
                request.method,
                request.path,
                len(tasks),
                self.checks_file,
            )

            try:
                results = engine.evaluate(tasks)
            except Exception as e:
                import traceback
                logger.exception("request_id=%s error during reality engine evaluation", request.request_id)
                print(f"request_id={request.request_id} Error during reality engine evaluation: {e}")
                traceback.print_exc()
                raise

            # If we successfully evaluated the checks, we set the scrape_success metric to 1.0 (indicating success).
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
            request = CURRENT_REQUEST.get()
            logger.exception("request_id=%s error occurred while evaluating tasks", request.request_id)
            print(f"request_id={request.request_id} Error occurred while evaluating tasks: {e}")
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
    # Configure logging to show debug messages if the DEBUG environment variable is set to "1".
    # This allows for easier troubleshooting and visibility into the server's operations when needed.
    log_level = os.getenv("LOG_LEVEL", "DEBUG" if os.getenv("DEBUG", "0") == "1" else "INFO")
    logging.basicConfig(level=getattr(logging, log_level.upper(), logging.INFO))

    # Advertise the start of the metrics server and the configuration being used.
    # This includes checking if the checks file exists, the port number, and the TTL for the reality engine cache.
    # This information is useful for debugging and confirming that the server is set up correctly.
    print("=== METRICS SERVER START ===")
    print(f"Checks file exists: {os.path.exists(DEFAULT_CHECKS_FILE)}")
    checks_file = os.getenv("OPS_JOURNAL_CHECKS_FILE", DEFAULT_CHECKS_FILE)
    port = int(os.getenv("PORT", str(DEFAULT_PORT)))
    ttl = int(os.getenv("OPS_JOURNAL_CACHE_TTL", "30"))

    # Register the RealityChecksCollector with the Prometheus REGISTRY. This allows the collector to be called
    # when Prometheus scrapes the metrics endpoint. The collector will gather the reality check metrics
    # and make them available for Prometheus to scrape.
    REGISTRY.register(RealityChecksCollector(checks_file=checks_file, ttl=ttl)) # type: ignore[union-attr]

    # Start the Prometheus metrics server on the specified port.
    # This will listen for incoming HTTP requests from Prometheus
    start_metrics_server(port, REGISTRY)
    print(f"Prometheus metrics server started on port {port} using {checks_file}")

    while True:
        time.sleep(3600)
