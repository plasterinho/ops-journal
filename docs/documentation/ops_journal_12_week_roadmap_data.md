# Ops Journal – 12-Week Platform Engineering Roadmap (Data)

This document defines the learning roadmap as **data**, not prose. It is intended to be rendered by Ops Journal and evolved carefully.

---

## Track

id: platform-engineering-12w
title: Platform Engineering – Ops Journal Track
duration_weeks: 12

---

## Phase 1 – Foundations & Truth

goal: "Everything is real, inspectable, and boring."

### Week 01
id: week-01
name: "The Journal Exists"

core_tasks:
- id: w01-t01
  title: "Create Ops Journal repository"
  description: "Initialize Git repository and commit initial structure."

- id: w01-t02
  title: "Define Week 1 tasks in Markdown"
  description: "Write tasks for Week 1 as Markdown data, including checkboxes and placeholders for evidence."

- id: w01-t03
  title: "Deploy static Ops Journal renderer to Minikube"
  description: "Run a minimal renderer (Go server or NGINX) in Minikube that serves the journal content."

stretch_tasks:
- id: w01-s01
  title: "Add basic styling"
  description: "Apply minimal CSS or Tailwind to make the journal readable and clean."

---

### Week 02
id: week-02
name: "Networking & Exposure"

core_tasks:
- id: w02-t01
  title: "Install NGINX Ingress Controller"
  description: "Deploy NGINX Ingress Controller into the cluster."

- id: w02-t02
  title: "Expose Ops Journal via Ingress"
  description: "Create Service and Ingress resources to access the journal via HTTP."

- id: w02-t03
  title: "Enable TLS for Ops Journal"
  description: "Configure TLS (self-signed acceptable) for Ingress endpoint."

stretch_tasks:
- id: w02-s01
  title: "Add path-based routing"
  description: "Serve Ops Journal under a specific URL path."

---

### Week 03
id: week-03
name: "GitOps Begins"

core_tasks:
- id: w03-t01
  title: "Install Argo CD"
  description: "Deploy Argo CD into the cluster using recommended manifests."

- id: w03-t02
  title: "Move Ops Journal manifests into Git"
  description: "Store Kubernetes manifests for Ops Journal in a Git repository."

- id: w03-t03
  title: "Deploy Ops Journal via Argo CD"
  description: "Create Argo CD Application to manage Ops Journal deployment."

stretch_tasks:
- id: w03-s01
  title: "Observe drift"
  description: "Intentionally change a live resource and watch Argo CD detect and correct drift."

---

## Phase 2 – Interaction & Delivery

goal: "The journal is used, not just viewed."

### Week 04
id: week-04
name: "Interaction via Git"

core_tasks:
- id: w04-t01
  title: "Add UI action to mark task as done"
  description: "Expose a UI control that initiates task completion workflow."

- id: w04-t02
  title: "Generate pull request from UI"
  description: "UI action creates a branch and PR updating task state in Git."

- id: w04-t03
  title: "Display PR status in UI"
  description: "Show whether the task PR is open, merged, or closed."

stretch_tasks:
- id: w04-s01
  title: "Pre-fill PR template"
  description: "Automatically include evidence checklist in PR description."

---

### Week 05
id: week-05
name: "CI & Validation"

core_tasks:
- id: w05-t01
  title: "Add CI pipeline for journal"
  description: "Run checks on task definitions and Markdown structure."

- id: w05-t02
  title: "Block invalid task changes"
  description: "Prevent merge of malformed or incomplete task updates."

- id: w05-t03
  title: "Expose CI status in UI"
  description: "Display CI success or failure next to tasks."

stretch_tasks:
- id: w05-s01
  title: "Fail CI on missing evidence"
  description: "Require evidence links for completed tasks."

---

### Week 06
id: week-06
name: "Reality Checks"

core_tasks:
- id: w06-t01
  title: "Read cluster state from app"
  description: "Grant read-only access to Kubernetes API."

- id: w06-t02
  title: "Validate service existence"
  description: "Automatically confirm required Services exist."

- id: w06-t03
  title: "Show verified vs claimed state"
  description: "Visually distinguish system-verified tasks from manual claims."

stretch_tasks:
- id: w06-s01
  title: "Validate ingress reachability"
  description: "Perform HTTP checks against Ingress endpoints."

---

## Phase 3 – Observability & Reliability

goal: "Trust the system by seeing it."

### Week 07
id: week-07
name: "Metrics"

core_tasks:
- id: w07-t01
  title: "Install Prometheus"
  description: "Deploy Prometheus stack into the cluster."

- id: w07-t02
  title: "Expose Ops Journal metrics"
  description: "Add application metrics endpoint."

- id: w07-t03
  title: "Create Grafana dashboard"
  description: "Visualize basic Ops Journal metrics."

stretch_tasks:
- id: w07-s01
  title: "Define basic SLO"
  description: "Document availability or latency target."

---

### Week 08
id: week-08
name: "Logs & Traces"

core_tasks:
- id: w08-t01
  title: "Install Loki"
  description: "Deploy Loki and log collectors."

- id: w08-t02
  title: "Add structured logging"
  description: "Emit structured logs with request identifiers."

- id: w08-t03
  title: "Link logs from UI"
  description: "Provide direct links from tasks to relevant logs."

stretch_tasks:
- id: w08-s01
  title: "Add basic tracing"
  description: "Instrument requests with traces."

---

### Week 09
id: week-09
name: "Failure & Recovery"

core_tasks:
- id: w09-t01
  title: "Induce pod failure"
  description: "Manually kill pods and observe recovery."

- id: w09-t02
  title: "Break ingress configuration"
  description: "Introduce and fix routing errors."

- id: w09-t03
  title: "Document incident"
  description: "Record failure, detection, and resolution."

stretch_tasks:
- id: w09-s01
  title: "Measure recovery time"
  description: "Track time to detect and recover from failure."

---

## Phase 4 – Platform Thinking

goal: "Earn abstraction."

### Week 10
id: week-10
name: "Policy & Security"

core_tasks:
- id: w10-t01
  title: "Introduce policy engine"
  description: "Deploy OPA or Kyverno."

- id: w10-t02
  title: "Enforce resource limits"
  description: "Require CPU and memory limits for workloads."

- id: w10-t03
  title: "Apply policies to Ops Journal"
  description: "Dogfood policies on the journal itself."

stretch_tasks:
- id: w10-s01
  title: "Audit policy violations"
  description: "Expose violations via UI or logs."

---

### Week 11
id: week-11
name: "Tracksuit Hopper Emerges"

core_tasks:
- id: w11-t01
  title: "Introduce backend API"
  description: "Create a control-plane-style backend service."

- id: w11-t02
  title: "Decouple rendering from data"
  description: "Move logic out of Markdown-only rendering."

- id: w11-t03
  title: "Ops Journal becomes a client"
  description: "UI consumes Tracksuit Hopper API."

stretch_tasks:
- id: w11-s01
  title: "Version API"
  description: "Introduce explicit API versioning."

---

### Week 12
id: week-12
name: "Productization"

core_tasks:
- id: w12-t01
  title: "UI polish"
  description: "Improve layout, navigation, and readability."

- id: w12-t02
  title: "Write project documentation"
  description: "Explain system architecture and learning outcomes."

- id: w12-t03
  title: "End-to-end demo"
  description: "Demonstrate the full journey from Week 1 to Week 12."

stretch_tasks:
- id: w12-s01
  title: "External feedback"
  description: "Share the project and collect feedback."
