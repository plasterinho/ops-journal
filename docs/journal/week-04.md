# Week 04 -- From Self-Mutating CD to Enterprise GitOps

## Starting Point

At the beginning of Week 04, the system looked like this:

-   App code and Kubernetes manifests lived in the same repository.
-   GitHub Actions built the Docker image.
-   CI updated `kustomization.yaml` directly.
-   ArgoCD auto-synced from the same repository.
-   Every commit to `main` resulted in an automatic deployment.

This was fully functional **Continuous Deployment**. It worked, but it wasn't realistic.

The app repository owned both:

-   Product (code)
-   Logistics (deployment state)

That boundary felt wrong.

------------------------------------------------------------------------

## The Core Architectural Question

Should the application repository be allowed to mutate its own
deployment state?

The answer became obvious: no.

In real systems:

-   Product teams build artifacts.
-   Platform/ops control deployment state.
-   Deployment requires approval.
-   Git is the contract.

That realization triggered the biggest architectural shift so far.

------------------------------------------------------------------------

## Phase 1 -- Introduce Artifact Layer Properly

Before splitting repositories, we stabilized:

-   Docker image built in GitHub Actions
-   Images pushed to GHCR
-   Kustomize overlay injected immutable SHA tag
-   ArgoCD reconciled automatically
-   No manual image loading in Minikube

At that point, the system was deterministic and fully declarative.

We tagged it:

`week-4-cd-baseline`

That marked the end of the "self-mutating CD" phase.

------------------------------------------------------------------------

## Phase 2 -- Split Product and Logistics

We created a new repository:

`cluster-config`

New structure:

```text
cluster-config/
├── apps/
│ └── ops-journal/
├── environments/
│ └── local/
└── argocd/
```

ArgoCD was reconfigured to point to `cluster-config` instead of the app
repo.

A reconciliation occurred (new ReplicaSet was created), but the
deployment remained stable.

From that moment:

The app repository stopped being the source of truth for deployment. That was the real boundary shift.

------------------------------------------------------------------------

## Phase 3 -- Remove Self-Mutation

Kubernetes manifests were removed from the app repository.

CI stopped mutating its own repository.

The app repository now only:

-   Builds images
-   Pushes to GHCR

Nothing else. Deployment intent moved entirely to `cluster-config`.

------------------------------------------------------------------------

## Phase 4 -- Introduce Approval Gate

Instead of auto-deploying:

1.  CI builds image.
2.  CI opens Pull Request in `cluster-config`.
3.  Human approves PR.
4.  Merge triggers Argo reconciliation.
5.  Deployment rolls.

This changed the model from:

`Continuous Deployment`

to:

`Continuous Delivery with approval gate`

This was immediately visible:

-   PR appeared in `cluster-config`
-   Argo did nothing
-   After merge → Argo synced instantly
-   Deployment rolled smoothly

That moment validated the design.

------------------------------------------------------------------------

## Observations

### 1. Argo Is Pure Reconciliation

Argo does not care how a change arrives. If Git changes, Argo reconciles. That decoupling is powerful.

### 2. Deployment Is Now Explicit

Deployment is no longer a side effect of code - it is a deliberate Git change in a separate repository.

That separation is enterprise-realistic.

### 3. Clean Ownership Model Emerged

App repo: - Build responsibility

Infra repo: - Deployment responsibility

Argo: - Continuous reconciliation

Kubernetes: - Runtime only

The system now has proper responsibility boundaries.

------------------------------------------------------------------------

## Lessons Learned

-   Kustomize image matching is strict and string-based.
-   YAML structure errors in GitHub Actions are unforgiving.
-   Argo may recreate ReplicaSets when Application spec changes.
-   Self-mutating repos are convenient but architecturally fragile.
-   Splitting repos clarifies ownership and control.

------------------------------------------------------------------------

## Current Architecture

High-level flow:

``` mermaid
flowchart TD

    Dev[Developer] -->|merge to main| AppRepo[ops-journal-app]

    AppRepo -->|CI build| Image[Docker Image sha-xxxxx]
    AppRepo -->|PR| InfraRepo[cluster-config]

    InfraRepo -->|merge PR| Argo[ArgoCD]

    Argo -->|sync| K8s[Kubernetes]
    K8s -->|pull| GHCR[GHCR Registry]
```

------------------------------------------------------------------------

## Maturity Level After Week 04

-   Immutable image builds
-   Registry-backed deployments
-   Multi-repo GitOps model
-   Approval-gated promotion
-   Fully declarative cluster state

The system now resembles a realistic enterprise GitOps setup rather than
a learning demo.

------------------------------------------------------------------------

## What's Next

Potential next steps:

-   Multi-environment promotion (dev → staging → prod)
-   Branch protection rules
-   Argo sync policies per environment
-   Infrastructure hardening

Week 04 marks the transition from experimentation to platform design.
