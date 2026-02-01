# Platform control model

## Purpose of this document

This document describes **how control is structured in the platform**.
It explains who is allowed to change what, through which mechanisms, and
with which guarantees.

This is not a week-specific document. It defines stable control rules
that should remain valid as the platform evolves.

------------------------------------------------------------------------

## Control layers

The platform is controlled through distinct layers, each with a clear
responsibility.

### Git (intent layer)

-   Git expresses *intent*
-   All desired state is declared in Git
-   Git history is the authoritative audit log
-   Promotion, rollback, and change approval happen in Git

Git answers the question: What should the system look like?

------------------------------------------------------------------------

### GitOps controller (enforcement layer)

-   Argo CD enforces the desired state declared in Git
-   It continuously reconciles intent with reality
-   It has no business logic and no environment awareness
-   It does not infer intent or resolve conflicts

Argo CD answers the question: Does reality match what Git declares?

------------------------------------------------------------------------

### Kubernetes (execution layer)

-   Kubernetes executes the desired state
-   It schedules pods, manages ReplicaSets, and maintains runtime health
-   It does not know about environments, promotion, or Git

Kubernetes answers the question: How do I run what I was told to run?

------------------------------------------------------------------------

## Control flow

The control flow is strictly one-directional:

Git → Argo CD → Kubernetes

There is no supported reverse flow.

-   Kubernetes state must not be used to infer intent
-   Argo CD status must not be used as a source of truth
-   Only Git defines the desired state

------------------------------------------------------------------------

## Authority model

### What is authoritative

-   Git is authoritative for desired state
-   Argo CD is authoritative for reconciliation
-   Kubernetes is authoritative for runtime status

Each layer has authority only within its scope.

------------------------------------------------------------------------

### What is not authoritative

-   Manual kubectl changes
-   Argo CD UI actions without Git changes
-   Cluster state observed directly in Kubernetes

These actions may be useful for debugging, but they do not define
intent.

------------------------------------------------------------------------

## Change types and their paths

### Application changes

Examples: - image version updates - replica count changes -
configuration changes

Path: Git commit → Argo CD reconciliation → Kubernetes rollout

------------------------------------------------------------------------

### Platform changes

Examples: - GitOps Application definitions - namespace layout - control
boundaries

Path: Git commit → Argo CD reconciliation → Kubernetes changes

Platform changes are higher risk and must be reviewed carefully.

------------------------------------------------------------------------

## Ownership and isolation

### Ownership rules

-   A resource must have exactly one owner
-   Ownership is defined by the Argo CD Application
-   Overlapping ownership is an architectural error

The platform does not attempt to arbitrate ownership conflicts.

------------------------------------------------------------------------

### Isolation rules

-   Environments must be isolated by namespace or cluster
-   Sharing namespaces across environments is prohibited
-   Isolation is enforced by structure, not convention

Without isolation, control loops interfere with each other.

------------------------------------------------------------------------

## Failure behavior

### Git unavailable

-   Intent is frozen
-   The system continues operating with last known state
-   No promotion or rollback is possible

### Argo CD unavailable

-   Enforcement is paused
-   Manual changes persist
-   The system may drift until reconciliation resumes

### Kubernetes failure

-   Runtime behavior degrades
-   Control layers above remain intact
-   Recovery depends on Kubernetes mechanisms

------------------------------------------------------------------------

## Design implications

-   Control is explicit, not implicit
-   Safety comes from structure, not tooling
-   Tooling amplifies both good and bad design
-   Ambiguity in control leads to instability

------------------------------------------------------------------------

## Summary

-   Git defines intent
-   Argo CD enforces intent
-   Kubernetes executes intent
-   Ownership must be singular
-   Isolation is mandatory
-   Control flows in one direction only
