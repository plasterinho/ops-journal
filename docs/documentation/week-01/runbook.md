# Week 01 Runbook – Ops Journal Foundations

This runbook describes how to reproduce Week 01 from scratch.

It assumes a clean system and no prior setup.

---

## Scope

This runbook covers:
- building Ops Journal with MkDocs
- containerizing it with NGINX
- running it locally
- deploying it to Minikube

It does NOT cover:
- Ingress
- TLS
- GitOps
- CI/CD

---

## Requirements

### Mandatory
- Linux
- Git
- Docker
- kubectl
- Minikube
- Python 3
- pip

### Optional / Convenience
- gh (GitHub CLI)
- Markdown editor (e.g. Apostrophe)
- tree (file listing utility)

---

## Repository setup

    git clone git@github.com:plasterinho/ops-journal.git
    cd ops-journal

---

## Build documentation site

Install MkDocs (user-local):

    pip3 install --user mkdocs mkdocs-material

Ensure binary is on PATH:

    export PATH=$HOME/.local/bin:$PATH

Build static site:

    mkdocs build

Expected result:
- site/ directory exists
- contains static HTML

---

## Run locally with Docker

Build image:

    docker build -t ops-journal:0.1 .

Run container:

    docker run -p 8080:80 ops-journal:0.1

Verify:
- open http://localhost:8080
- Ops Journal UI loads

---

## Deploy to Minikube

Point Docker to Minikube:

    eval $(minikube docker-env)

Rebuild image inside Minikube:

    docker build -t ops-journal:0.1 .

Apply Kubernetes manifests:

    kubectl apply -f k8s/

Restart deployment (if already running):

    kubectl rollout restart deployment ops-journal

Access service:

    kubectl port-forward svc/ops-journal 8080:80

Verify:
- UI is visible
- content matches local build

---

## Troubleshooting

### Old content still visible
- ensure image was built after running `eval $(minikube docker-env)`
- check image hash:

        kubectl describe pod <pod-name>

### Port-forward errors
- broken pipe errors are expected
- ignore if UI renders correctly

---

## Clean-up (optional)

Delete resources:

    kubectl delete -f k8s/

Unset Minikube Docker environment:

    eval $(minikube docker-env -u)

---

## Notes

- Image tag reuse is intentional for Week 01
- No image registry is involved
- This runbook prioritizes clarity over automation
