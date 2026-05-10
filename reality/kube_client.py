# Imports
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from kubernetes.config.config_exception import ConfigException

# The KubeClient class provides a simple interface for interacting with the Kubernetes API.
# It abstracts away the details of authentication and API calls, allowing
# other parts of the code to easily retrieve information about Kubernetes
# resources such as services, pods, and ingresses. The client is designed
# to work both in-cluster (when deployed as a pod) and locally (for development
# purposes) by automatically selecting the appropriate configuration method.
class KubeClient:
    def __init__(self):
        # Prefer in-cluster credentials for deployed workloads and fall back
        # to the local kubeconfig for development.
        try:
            config.load_incluster_config()
        except ConfigException:
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
