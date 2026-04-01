from reality.kube_client import KubeClient
from reality.engine import RealityEngine
from reality.parser import parse_tasks
from reality.renderer import enrich_markdown
import yaml

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

def load_checks(path):
    """Loads check definitions from a YAML file."""
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    return {t["id"]: t["check"] for t in data.get("tasks", [])}

kube = KubeClient()
engine = RealityEngine(kube)

# Pretty print results as JSON for easy inspection
print(json.dumps({"message": "Parsing week-06.md"}))
with open("docs/journal/week-06.md") as f:
    content = f.read()

tasks = parse_tasks(content)

check_map = load_checks("week-06.checks.yaml")

for task in tasks:
    task_id = task.get("id")
    task["check"] = check_map.get(task_id)

if task_id and task["check"] is None:
    print(f"[WARN]: No check found for task ID '{task_id}'")

results = engine.evaluate(tasks)
# print(json.dumps(results, indent=2))
print(enrich_markdown(results))