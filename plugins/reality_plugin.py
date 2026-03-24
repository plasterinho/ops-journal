from reality.parser import parse_tasks
from reality.engine import RealityEngine
from reality.kube_client import KubeClient

# Create Kubernetes client and Reality engine instances
kube = KubeClient()
engine = RealityEngine(kube)

def on_page_markdown(markdown, page, config, files):
    """ MkDocs plugin hook to enrich markdown content with verification results. """
    
    tasks = parse_tasks(markdown)
    results = engine.evaluate(tasks)

    # naive replace (good enough for now, but could be improved with a proper markdown parser
    enriched = markdown
    
    for task in results:
        if task.get("verification"):
            status = task["verification"]["status"]
            msg = task["verification"]["message"]

            icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
            enriched = enriched.replace(
                task["text"],
                f"{task['text']}  \n  {icon} {status}: {msg}"
            )
    return enriched