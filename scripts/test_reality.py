from reality.kube_client import KubeClient
from reality.engine import RealityEngine

# Hardcoded tasks for testing
tasks = [
    {
        "text": "Deploy service",
        "claimed": True,
        "check": {
            "type": "service_exists",
            "name": "ops-journal",
            "namespace": "default"
        }
    },
    {
        "text": "Expose ingress",
        "claimed": True,
        "check": {
            "type": "ingress_exists",
            "name": "ops-journal",
            "namespace": "default"
        }
    },
    {
        "text": "Check pod readiness",
        "claimed": True,
        "check": {
            "type": "pod_ready",
            "label_selector": "app=ops-journal",
            "namespace": "default"
        }
    }
]

kube = KubeClient()
engine = RealityEngine(kube)

results = engine.evaluate(tasks)

for t in results:
    print(t)