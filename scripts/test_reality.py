from reality.kube_client import KubeClient
from reality.engine import RealityEngine
from reality.parser import parse_tasks
from reality.renderer import enrich_markdown

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

# Pretty print results as JSON for easy inspection
print(json.dumps({"message": "Parsing week-05.md"}))
with open("docs/journal/week-05.md") as f:
    content = f.read()

tasks = parse_tasks(content)
results = engine.evaluate(tasks)
# print(json.dumps(results, indent=2))
print(enrich_markdown(results))