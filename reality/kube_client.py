# Imports
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

class KubeClient:
    def __init__(self):
        # Load the kubeconfig from the default location
        config.load_kube_config()

        # API groups
        self.core = client.CoreV1Api()
        self.networking = client.NetworkingV1Api()

    # --- Core resource helpers ---

    def get_service(self, name, namespace="default"):
        """Get a service by name in the specified namespace."""

        try:
            service = self.core.read_namespaced_service(name, namespace)
            return service
        except ApiException as e:
            if e.status == 404:
                return None
            raise

    def list_pods(self, namespace="default", label_selector=None):
        """List all pods in the specified namespace."""

        try:
            pods = self.core.list_namespaced_pod(namespace, label_selector=label_selector)
            return pods.items
        except ApiException as e:
            print(f"Exception when listing pods: {e}")
            return []
    
    # --- Networking resource helpers ---
    def get_ingress(self, name, namespace="default"):
        """Get an ingress by name in the specified namespace."""

        try:
            ingress = self.networking.read_namespaced_ingress(name, namespace)
            return ingress
        except ApiException as e:
            if e.status == 404:
                return None
            raise