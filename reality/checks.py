# --- Imports ---
# Logging
import logging

logger = logging.getLogger(__name__)

def service_exists(kube, params):
    """Check if a service exists in the cluster.
    Expects params to contain:
    - name: The name of the service to check
    - namespace: (optional) The namespace to check in (default: "default")
    """

    # Extract parameters
    name = params["name"]
    namespace = params.get("namespace", "default")

    logger.debug(f"Checking if service '{name}' exists in namespace '{namespace}'")

    # Check if the service exists
    service = kube.get_service(
        name=name, namespace=namespace)
    if service:
        return {
            "status": "PASS", 
            "message": f"Service '{name}' exists.",
            "details": {"name": name, "namespace": namespace}
        }
    return {
        "status": "FAIL",
        "message": f"Service '{name}' does not exist.",
        "details": {"name": name, "namespace": namespace}
        }

def ingress_exists(kube, params):
    """Check if an ingress exists in the cluster.
    Expects params to contain:
    - name: The name of the ingress to check
    - namespace: (optional) The namespace to check in (default: "default")
    """

    name = params["name"]
    namespace = params.get("namespace", "default")
    details = {"name": name, "namespace": namespace}

    logger.debug(f"Checking if ingress '{name}' exists in namespace '{namespace}'")

    ingress = kube.get_ingress(
        name=name, namespace=namespace)
    if ingress:
        return {
            "status": "PASS", 
            "message": f"Ingress '{name}' exists.",
            "details": details
        }
    return {
        "status": "FAIL",
        "message": f"Ingress '{name}' does not exist.",
        "details": details
    }

def pod_count(kube, params):
    """Check the number of pods matching a label selector in a namespace.
    Expects params to contain:
    - namespace: (optional) The namespace to check in (default: "default")
    - label_selector: (optional) The label selector to match (default: "")
    - min_count: (optional) The minimum number of pods required (default: 0)
    """

    namespace = params.get("namespace", "default")
    label_selector = params.get("label_selector", "")
    min_count = params.get("min_count", 0)


    logger.debug(f"Checking pod count in namespace '{namespace}' with label selector '{label_selector}' (minimum required: {min_count})")

    pods = kube.list_pods(namespace=namespace, label_selector=label_selector)
    count = len(pods)
    details = {"namespace": namespace, "label_selector": label_selector, "min_count": min_count, "count": count}

    if count >= min_count:
        return {
            "status": "PASS",
            "message": f"Found {count} pods.",
            "details": details
        }
    return {
        "status": "FAIL",
        "message": f"Only found {count} pods (minimum required: {min_count}).",
        "details": details
    }

def pod_ready(kube, params):
    """Check if at least one pod matching a label selector is in Ready state in a namespace.
    Expects params to contain:
    - namespace: (optional) The namespace to check in (default: "default")
    - label_selector: (optional) The label selector to match (default: "")
    """

    namespace = params.get("namespace", "default")
    label_selector = params.get("label_selector", "")

    logger.debug(f"Checking if any pods are ready in namespace '{namespace}' with label selector '{label_selector}'")

    pods = kube.list_pods(namespace=namespace, label_selector=label_selector)
    ready_count = 0
    for pod in pods:
        for condition in pod.status.conditions or []:
            if condition.type == "Ready" and condition.status == "True":
                ready_count += 1
                break

    details = {"namespace": namespace, "label_selector": label_selector, "ready_count": ready_count, "total_count": len(pods)}

    if ready_count > 0:
        return {
            "status": "PASS",
            "message": f"Found {ready_count} ready pods.",
            "details": details
        }
    return {
        "status": "FAIL",
        "message": f"No ready pods found.",
        "details": details
    }