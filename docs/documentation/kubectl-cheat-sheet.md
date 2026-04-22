# Kubernetes Cheat Sheet (Ops Journal)

A minimal set of commands for deploying, debugging, and interacting with the cluster.

---

## 🔍 Inspecting Resources

```bash
# List pods
kubectl get pods -n <namespace>

# List all resources
kubectl get all -n <namespace>

# Describe a pod (events, errors, probes)
kubectl describe pod <pod-name> -n <namespace>

# Show logs
kubectl logs <pod-name> -n <namespace>

# Logs from specific container
kubectl logs <pod-name> -c <container-name> -n <namespace>

# Logs from previous crash
kubectl logs <pod-name> -c <container-name> --previous -n <namespace>
```

---

## 🧠 Debugging

```bash
# Exec into container
kubectl exec -it <pod-name> -n <namespace> -- sh

# Run temporary debug pod
kubectl run tmp-shell --rm -it --image=busybox -- sh

# Check open ports inside container
netstat -tlnp
# or
ss -tlnp
```

---

## 🌐 Networking & Connectivity

```bash
# Port forward service
kubectl port-forward svc/<service-name> 8080:80 -n <namespace>

# Port forward pod
kubectl port-forward <pod-name> 9113:9113 -n <namespace>

# Test service from inside cluster
wget -qO- http://<service>.<namespace>.svc.cluster.local:<port>
```

---

## 🚀 Deployments & Rollouts

```bash
# Check rollout status
kubectl rollout status deployment <name> -n <namespace>

# Restart deployment
kubectl rollout restart deployment <name> -n <namespace>

# Rollback to previous version
kubectl rollout undo deployment <name> -n <namespace>
```

---

## ⚙️ Editing & Applying

```bash
# Apply manifest
kubectl apply -f <file.yaml>

# Edit resource live (not GitOps-friendly)
kubectl edit deployment <name> -n <namespace>

# Delete resource
kubectl delete -f <file.yaml>
```

---

## 📦 Images & Versions

```bash
# Check image used by pod
kubectl get pod <pod-name> -o jsonpath="{.spec.containers[*].image}"

# Force image refresh (if using same tag)
kubectl rollout restart deployment <name>
```

---

## 🧪 Metrics & Health

```bash
# Test metrics endpoint via port-forward
curl localhost:9113/metrics

# Test from inside cluster
kubectl exec -it <pod> -- curl localhost:9113/metrics
```

---

## 🧭 Namespaces

```bash
# List namespaces
kubectl get ns

# Set default namespace (temporary)
kubectl config set-context --current --namespace=<namespace>
```

---

## 🧹 Cleanup

```bash
# Delete pod (it will be recreated if managed by Deployment)
kubectl delete pod <pod-name> -n <namespace>

# Delete temporary debug pod
kubectl delete pod tmp-shell
```

---

## 🧠 Notes

* Pods are ephemeral — don’t rely on them sticking around
* Always debug via:

  1. logs
  2. describe
  3. exec
* If something “worked before”, it was likely a transient state
* Prefer GitOps changes over `kubectl edit`

---
