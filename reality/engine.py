# Import all checks from the checks module and make them available in the CHECKS dictionary
from reality.checks import service_exists, ingress_exists, pod_ready

CHECKS = {
    "service_exists": service_exists,
    "ingress_exists": ingress_exists,
    "pod_ready": pod_ready
}

import time

class RealityEngine:
    def __init__(self, kube_client, ttl=30):
        self.kube = kube_client
        self.ttl = ttl
        self.cache = None
        self.last_run = 0

    def evaluate(self, tasks):
        """Evaluate the given tasks and return their results. Uses caching to avoid redundant checks."""
        current_time = time.time()
        if self.cache and (current_time - self.last_run) < self.ttl:
            return self.cache
        
        results = self._run_checks(tasks)
        self.cache = results
        self.last_run = current_time
        return results

    def run_check(self, check_name, params):
        """Run a specific check by name with the given parameters.
         This is a lower-level method that can be used for ad-hoc checks outside of the main evaluation loop."""
        if check_name not in CHECKS:
            raise ValueError(f"Check '{check_name}' is not defined.")
        
        check_fn = CHECKS[check_name]
        return check_fn(self.kube, params)

    def _run_checks(self, tasks):
        """Run a list of checks and return their results.
        Each check is expected to be a dictionary with 'name' and optional 'params'.
        """
        results = []

        for task in tasks:
            check_def = task.get("check")

            # No check -> no verification
            if not check_def:
                results.append({
                    **task,
                    "verification": None
                })
                continue
            
            check_type = check_def.get("type")
            check_fn = CHECKS.get(check_type)

            if not check_fn:
                results.append({
                    **task,
                    "verification": {
                        "status": "UNKNOWN",
                        "message": f"Check type '{check_type}' is not defined."
                    }
                })
                continue

            result = check_fn(self.kube, check_def)
            results.append({
                **task,
                "verification": result
            })

        return results