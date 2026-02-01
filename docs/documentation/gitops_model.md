# GitOps control model

## Purpose of this document

This document describes **how GitOps works in this platform**, not how a
specific week was executed. It captures stable rules and expectations
that should remain true as the platform evolves.

------------------------------------------------------------------------

## Core principles

### Git is the source of truth

-   Git defines the desired state of the system
-   The cluster is expected to converge to what is declared in Git
-   Git history is the audit log
-   Rollbacks are performed by reverting commits

If something is not represented in Git, it is not authoritative.

------------------------------------------------------------------------

### Argo CD is the continuous delivery controller

-   Argo CD continuously reconciles desired state (Git) with actual
    state (cluster)
-   Argo CD is **not** on the request path
-   Application availability does not depend on Argo CD being up
-   Enforcement of desired state does depend on Argo CD being up

Argo CD does not decide *what* should run. It only enforces what Git
declares.

------------------------------------------------------------------------

### Manual changes are temporary by design

-   `kubectl apply`, `kubectl scale`, and ad‑hoc edits are not
    authoritative
-   Manual changes will be reverted when Argo CD reconciles
-   Manual intervention is acceptable only for debugging or emergency
    containment

Sustainable changes must go through Git.

------------------------------------------------------------------------

## Ownership and boundaries

### One Application owns a resource

-   A Kubernetes resource must be owned by exactly one Argo CD
    Application
-   Multiple Applications must never manage the same resource
-   GitOps does not resolve ownership conflicts

Ownership conflicts result in: - continuous reconciliation loops -
OutOfSync states - non‑deterministic cluster behavior

These are architectural errors, not tooling failures.

------------------------------------------------------------------------

### Environments are isolation boundaries

-   Environments are not labels or overlays alone
-   Environments must be isolated by:
    -   namespace, or
    -   cluster
-   Sharing a namespace across environments is unsafe

GitOps will surface environment conflicts, not prevent them.

------------------------------------------------------------------------

## Deployment and rollback model

### Deployment

-   A deployment is a Git commit
-   Changing desired state in Git triggers reconciliation
-   Argo CD applies the change automatically

### Rollback

-   A rollback is a Git revert
-   Reverting a commit restores the previous desired state
-   Argo CD enforces the reverted state automatically

UI‑based rollbacks are considered temporary and must be followed by Git
changes.

------------------------------------------------------------------------

## Failure modes

### Git unavailable

-   The cluster continues running with the last known desired state
-   No new deployments or rollbacks are possible

### Argo CD unavailable

-   Workloads continue running
-   Desired state is no longer enforced
-   Manual changes persist until Argo CD recovers

------------------------------------------------------------------------

## Non‑goals

This model does not attempt to: - prevent architectural mistakes - infer
intent from conflicting definitions - replace review or promotion
processes

GitOps enforces consistency, not correctness.

------------------------------------------------------------------------

## Summary

-   Git defines intent
-   Argo CD enforces intent
-   Architecture defines safety
-   Isolation is mandatory
-   Tooling makes problems visible, it does not hide them
