from reality.kube_client import KubeClient
from reality.engine import RealityEngine
# For pretty printing with jq:
import json

# Hardcoded tasks for testing
tasks = [
    {
        "text": "Deploy service",
        "claimed": True,
        "check": {
            "type": "service_exists",
            "name": "ops-journal",
            "namespace": "ops-journal-dev"
        }
    },
    {
        "text": "Expose ingress",
        "claimed": True,
        "check": {
            "type": "ingress_exists",
            "name": "ops-journal",
            "namespace": "ops-journal-dev"
        }
    },
    {
        "text": "Check pod readiness",
        "claimed": True,
        "check": {
            "type": "pod_ready",
            "label_selector": "app=ops-journal",
            "namespace": "ops-journal-dev"
        }
    }
]

kube = KubeClient()
engine = RealityEngine(kube)

results = engine.evaluate(tasks)

# Pretty print results as JSON for easy inspection
print(json.dumps(results, indent=2))