# Week 07 — Observability + GitOps Convergence (Final)

## Goals

We have automated verification of system state. This week, we bring observability under GitOps control while preserving those checks.

## Tasks

- [x] Prometheus is deployed from Git <!-- id: deploy-prometheus -->
- [x] Grafana is deployed from Git <!-- id: deploy-grafana -->
- [x] The Prometheus datasource, the Observability dashboard, and all its panels are configured in Git <!-- id: deploy-dashboards -->
- [x] System checks from Week 6 are exposed as Prometheus metrics <!-- id: system-metrics -->
- [x] Additional task: ClusterConfig includes a bootstrap loaded directly from Git, with no need to clone the repository <!-- id: bootstrap -->

## Evidence

Grafana dashboard with working panels (including metrics reflecting system state and checks)

![Grafana dashboard](evidence/week-07/grafana-dashboard.png)

Prometheus graph confirming that the exported reality-check metrics are present and queryable was captured during validation, but the dedicated screenshot has not been committed to `docs/journal/evidence/week-07/` yet.

## Summary

Week 07 solidified the platform’s transition from “things running in Kubernetes” to a self-configuring, Git-driven system.

The core achievement is that observability is now fully declarative:

- Prometheus deployment is managed from Git  
- Grafana deployment, datasources, dashboards, and panels are all defined in Git  
- Week 6 reality checks are exported as custom Prometheus metrics  
- ArgoCD continuously reconciles the desired state  

In parallel, bootstrap was refined into a repeatable entry point: a minimal script that installs ArgoCD and hands over control to GitOps via a root application.

At this point, the system can be recreated from scratch with:

bootstrap → ArgoCD → full platform state

---

## What Was Built

### 1. Fully GitOps-managed observability

The observability stack is now entirely defined in the repository:

- Prometheus (deployment + config)
- Grafana (deployment + ingress)
- Grafana datasources (ConfigMap)
- Grafana dashboards and panels (JSON → ConfigMap → provisioning)

This removed all manual UI configuration.

Result:

Observability = code, not clicks

---

### 2. Grafana provisioning pipeline

A complete pipeline was established:

Git (JSON dashboards)
→ ConfigMap
→ mounted into Grafana
→ provisioning config
→ dashboards available in UI

Key fixes along the way:

- corrected volume mounts (YAML structure issue)
- ensured ConfigMaps exist before pod startup
- resolved datasource placeholders (__inputs → static datasource)
- validated JSON formatting

Outcome:

Dashboards are reproducible and version-controlled

---

### 3. Prometheus integration

Prometheus is now:

- deployed declaratively
- accessible within the cluster
- wired as a Grafana datasource via provisioning

This enables dashboards to work without any manual wiring.

---

### 4. Reality-engine checks exported as custom metrics

The system checks introduced in Week 6 were extended into Prometheus metrics by reusing the existing Python-based reality engine.

The first implementation lived inside the main `ops-journal` image:

- a small Python exporter loaded the Week 6 checks file
- the exporter evaluated those checks through `RealityEngine`
- results were exposed as Prometheus gauges such as total checks by status, per-task status, cache age, and scrape success

This was the key conceptual step:

reality verification → machine-readable metrics → dashboardable platform state

---

### 5. Metrics service moved into its own container

Running the exporter inside the application image worked as a first proof of concept, but it mixed static-site serving with Python runtime concerns.

To make the deployment cleaner, the exporter was moved into a dedicated `ops-journal-metrics` container:

- the main container remained responsible for serving the MkDocs site through NGINX
- the new metrics container ran only the Python exporter
- the Kubernetes service exposed the metrics endpoint for Prometheus scraping

This separation made the deployment easier to reason about and aligned better with the single-purpose container model.

The split across repositories became clearer as well:

- `ops-journal` owns the exporter code, metrics image, and image build workflow
- `cluster-config` owns the deployment, service wiring, probes, and Prometheus scrape path

---

### 6. ArgoCD bootstrap and root application

Bootstrap flow:

1. Create namespace
2. Install ArgoCD (server-side apply)
3. Wait for readiness
4. Apply root application

The root application points to the repo and recursively defines all apps.

This establishes:

kubectl → bootstrap only  
ArgoCD → owns the platform

---

### 7. Bootstrap reliability improvements

Enhancements included:

- Kubernetes version alignment (v1.35.1)
- handling CRD apply issues via server-side apply
- fixing missing application paths in bootstrap
- improving Minikube compatibility
- enabling a no-clone bootstrap path

Goal achieved:

One command → working cluster → self-managed state

---

## Observability → SLO (first step)

A first, pragmatic SLO was introduced based on available metrics.

Given only NGINX exporter metrics:

rate(nginx_http_requests_total[5m])

The SLO is defined as:

Service is considered available if it processes requests continuously.  
Target: 99% of time windows have non-zero request rate.

This is intentionally simple, but establishes:

Observability → expectations → measurable health

---

## Problems Encountered

### 1. ArgoCD instability

- missing argocd-secret
- Dex crash loops
- repo-server failing due to non-idempotent ln -s

Resolution:

- reset namespace when needed
- vendor install manifest
- remove problematic copyutil initContainer

Key lesson:

Installation manifests are not always safe to treat as black boxes

---

### 2. GitOps vs manual changes

Applying changes via kubectl led to confusion due to ArgoCD reconciliation.

Takeaway:

Git is the only source of truth once ArgoCD is active

---

### 3. Grafana provisioning pitfalls

Issues included:

- missing volume mounts due to YAML structure
- pods stuck in ContainerCreating due to missing ConfigMaps
- invalid JSON dashboards
- unresolved datasource placeholders

Takeaway:

Declarative config increases reliability, but reduces tolerance for mistakes

---

### 4. Local networking limitations

Attempts to expose services via MetalLB were inconsistent due to:

- Minikube Docker driver
- host networking constraints
- WSL interaction

Final approach:

- use SSH/X11 or port-forwarding for access
- accept local networking as “good enough”

---

### 5. Custom metrics rollout issues

The custom metrics path worked conceptually, but a few deployment details blocked them from showing up in Prometheus at first.

Problems included:

- the first dedicated metrics image was missing Python dependencies needed by the exporter
- the metrics image had to be built with the correct Dockerfile path and repository root as build context so it could copy both `metrics/` and `reality/`
- after introducing the separate metrics container, the Kubernetes service still exposed port `9113 -> 9113`, so Prometheus kept scraping the NGINX exporter instead of the new Python exporter on port `8000`
- readiness and liveness probes had to be aligned with the actual metrics endpoint

Resolution:

- add a dedicated `metrics/requirements.txt`
- build the metrics image from `./metrics/Dockerfile` with `context: .`
- keep the service port at `9113` for Prometheus, but retarget it to container port `8000`
- add probes on `/metrics` to make failures visible earlier

Key lesson:

When a scrape target exists but the wrong container answers, the problem looks like “metrics are missing” even though Prometheus itself is working correctly

---

## Current State

The platform now supports:

- reproducible cluster bootstrap
- ArgoCD-managed application lifecycle
- fully declarative observability stack
- Grafana dashboards and datasources from Git
- custom Prometheus metrics generated from the reality engine
- basic SLO definition

All core components are:

version-controlled + automatically reconciled

---

## What Changed Conceptually

This week marked a transition:

From:

Deploying tools

To:

Designing a platform that maintains itself

Key shifts:

- imperative → declarative
- UI configuration → Git configuration
- “is it running?” → “is it meeting expectations?”

---

## Next Steps

Natural continuation areas:

- richer SLOs (status codes, latency, and alert thresholds)
- alerting (Alertmanager)
- environment separation (dev/prod overlays)
- ArgoCD self-management (Argo managing its own install)
- adding a committed Prometheus graph screenshot to the Week 07 evidence set

---

## Reflection

This week involved a lot of friction:

- YAML structure issues
- GitOps reconciliation surprises
- networking inconsistencies
- brittle installation defaults

But those issues exposed the real constraints of operating a platform.

The outcome is significant: the system is now coherent, reproducible, and largely self-managing.
