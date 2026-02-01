# Week 1 – Concretization

**Theme:** The Journal Exists  
**Phase:** Foundations & Truth

This document defines *exactly* what Week 1 means, what is allowed, and what is explicitly forbidden. It is a guardrail against overbuilding.

---

## Week 1 Goal

By the end of Week 1:

> Ops Journal exists as a running workload in Minikube, rendering learning data from Git, and can be accessed reliably by a human.

Nothing more. Nothing less.

---

## Definition of Done (non-negotiable)

Week 1 is complete **only if all of the following are true**:

### 1. Git repository exists and is clean
- Repository initialized
- Clear directory structure
- At least one meaningful commit (not "initial commit")

### 2. Learning data is stored as data
- Week 1 tasks are written in Markdown
- Tasks include:
  - title
  - checkbox state
  - placeholder for evidence
- No hardcoded tasks in application code

### 3. Ops Journal renders the data
- A running process reads Markdown files
- HTML is generated dynamically at runtime
- Changes in Git are reflected after redeploy

### 4. Application runs in Kubernetes
- At least one Pod running in Minikube
- Exposed via a Kubernetes Service
- Accessible via `kubectl port-forward`

### 5. You can point to it
- A URL (even localhost via port-forward) is documented
- A screenshot exists as evidence

---

## Explicit Non-Goals (hard no)

The following are **forbidden in Week 1**, even if easy:

- Ingress
- TLS
- Argo CD
- CI pipelines
- Databases
- Authentication
- Writing back to Git
- JavaScript frameworks
- Kubernetes operators or CRDs

If any of these appear, Week 1 has failed.

---

## Allowed Implementation Choices

You may choose **one** from each category:

### Language / Runtime
- Go (preferred)
- Anything else you already know well

### Rendering approach
- Server-side HTML templates
- Markdown → HTML rendering

### Styling
- Plain HTML
- Minimal embedded CSS

Clean > clever.

---

## Minimal Repository Structure (example)

```
ops-journal/
├── journal/
│   └── week-01.md
├── app/
│   ├── main.go
│   └── templates/
├── deploy/
│   ├── deployment.yaml
│   └── service.yaml
└── README.md
```

This is illustrative, not prescriptive.

---

## Evidence to collect

By the end of the week, the following evidence must exist in Git:

- Screenshot of rendered journal
- `kubectl get pods` output
- Commit hash that introduced the running app

---

## Reflection (mandatory)

At the end of Week 1, write a short reflection answering:

- What felt slower than expected?
- What felt easier than expected?
- What temptation to overbuild did you consciously resist?

This reflection is part of the learning artifact.

---

## Success smell

Week 1 should feel *almost disappointingly simple*.

If it feels impressive, you probably did too much.

