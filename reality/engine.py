# Import all checks from the checks module and make them available in the CHECKS dictionary
from reality.checks import service_exists, ingress_exists, pod_ready

# A dictionary mapping check names to their corresponding functions.
# This allows the RealityEngine to look up and execute checks by name when evaluating tasks.
CHECKS = {
    "service_exists": service_exists,
    "ingress_exists": ingress_exists,
    "pod_ready": pod_ready
}

# A dictionary defining the required fields for each check type.
# This is used to validate the check definitions before running them.
# If a check definition is missing any of the required fields, it will be marked as INVALID
# with an appropriate error message.
REQUIRED_FIELDS = {
    "service_exists": ["name", "namespace"],
    "ingress_exists": ["name", "namespace"],
    "pod_ready": ["label_selector", "namespace"]
}

import time

# The RealityEngine class is responsible for evaluating reality checks based on tasks parsed from markdown.
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
        
        print(f"Running {len(tasks)} tasks")
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
            if check_def is None:
                results.append({
                    **task,
                    "verification": None
                })
                continue

            if "type" not in check_def:
                results.append({
                    **task,
                    "verification": {
                        "status": "INVALID",
                        "message": f"Check definition missing 'type': {check_def}"
                    }
                })
                continue

            if not isinstance(check_def, dict):
                results.append({
                    **task,
                    "verification": {
                        "status": "INVALID",
                        "message": f"Check is not a dict: {check_def}"
                    }
                })
                continue

            check_type = check_def.get("type")

            if not check_type:
                results.append({
                    **task,
                    "verification": {
                        "status": "INVALID",
                        "message": f"Check definition missing 'type': {check_def}"
                    }
                })
                continue
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

            required = REQUIRED_FIELDS.get(check_type, [])
            missing = [f for f in required if f not in check_def]

            if missing:
                results.append({
                    **task,
                    "verification": {
                        "status": "INVALID",
                        "message": f"Missing required fields: {missing} for '{check_type}' check. Got: {check_def}"
                    }
                })
                continue

            result = check_fn(self.kube, check_def)
            results.append({
                **task,
                "verification": result
            })

        return results