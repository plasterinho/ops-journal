# ops_journal_week_02_gitops_and_environments.md

## Week 02 --- GitOps & Environment Modeling

### Status

**Completed, with intentional conflict observed**

------------------------------------------------------------------------

## Starting point

At the beginning of Week 02:

-   A local Kubernetes cluster was running
-   The `ops-journal` application was deployed imperatively
-   Platform components were installed manually
-   There was no GitOps controller
-   No environment separation existed

The goal of this week was not to add features, but to change **how the
system is operated**.

------------------------------------------------------------------------

## What was introduced

### GitOps controller

-   Argo CD was installed into the `argocd` namespace
-   No ingress or external exposure was configured
-   Access was done via port-forwarding
-   Initially, Argo CD managed no workloads

This established a control plane that: - is not on the request path -
continuously enforces desired state - reacts to drift instead of manual
actions

------------------------------------------------------------------------

### Repository structure

A clear separation was introduced between applications and platform
configuration.

**Applications:** - `apps/ops-journal/base` -
`apps/ops-journal/overlays/dev` - `apps/ops-journal/overlays/staging` -
`apps/ops-journal/overlays/prod`

**GitOps configuration:** - `platform/gitops/ops-journal-dev-app.yaml` -
`platform/gitops/ops-journal-staging-app.yaml`

Key decisions: - Application manifests are owned by the application
structure - Argo CD Application CRs are treated as platform
configuration - GitOps configuration is not mixed with application YAML

------------------------------------------------------------------------

### Kustomize

Kustomize was introduced as a **YAML composition tool**, not a
deployment mechanism.

-   `base` defines the canonical application manifests
-   `overlays` define environment-specific differences
-   Rendering was validated locally using `kubectl kustomize`
-   Deprecated syntax was replaced with the modern `patches` syntax

Kustomize's role is limited to: - assembling manifests - making
differences explicit - producing plain Kubernetes YAML for Argo CD to
consume

------------------------------------------------------------------------

## Environment differentiation

Two environments were modeled:

-   **dev**
    -   1 replica
-   **staging**
    -   2 replicas

This difference was implemented exclusively via overlay patches.\
No changes were made to base manifests.

------------------------------------------------------------------------

## GitOps ownership

Two Argo CD Applications were created:

-   `ops-journal-dev`
-   `ops-journal-staging`

Both Applications: - point to the same Git repository - target the same
Kubernetes cluster - target the same namespace - manage the same
Kubernetes resources

This setup was intentional.

------------------------------------------------------------------------

## Observed behavior

### Drift correction

-   Manual changes such as scaling replicas were reverted automatically
-   Deleted resources were recreated
-   Git was confirmed as the source of truth

------------------------------------------------------------------------

### Reconciliation conflict

Once both Applications were active:

-   The cluster consistently showed **2 replicas**
-   `ops-journal-staging` was **Synced / Healthy**
-   `ops-journal-dev` was **OutOfSync / Progressing**

Argo CD showed: - successful sync attempts - immediate drift detection -
continuous reconciliation loops

This occurred because: - two Applications declared **different desired
states** - both attempted to own the same resources

No misconfiguration occurred.\
This was a valid but unsafe architecture.

------------------------------------------------------------------------

## Failure modes analyzed

### Git unavailable

-   The cluster continues running on the last known desired state
-   No new changes or rollbacks are possible

### Argo CD unavailable

-   Applications keep running
-   Desired state is no longer enforced
-   Manual changes persist

### Manual deletion of resources

-   Resources are recreated only if Argo CD is running

------------------------------------------------------------------------

## Key learnings

-   GitOps enforces desired state, it does not define ownership
-   Multiple sources of truth are possible unless prevented by design
-   Environments are **boundaries**, not labels
-   Sharing a namespace across environments is unsafe
-   GitOps makes architectural mistakes visible instead of hiding them

------------------------------------------------------------------------

## Why this setup is unsafe for production

-   Controllers can fight over the same resource
-   Last-writer-wins behavior is non-deterministic
-   OutOfSync states can become permanent
-   Human intervention is required to infer intent

This is acceptable for learning.\
It is not acceptable for production.

------------------------------------------------------------------------

## Conclusion

Week 02 shifted the system from **imperative control**\
to **declarative, continuously reconciled control**.

The intentional conflict demonstrated why: - environment isolation is
mandatory - platform boundaries must be explicit - GitOps amplifies both
good and bad design choices

------------------------------------------------------------------------

## Next steps

Week 03 will introduce: - namespace-level isolation - one Application
per namespace - removal of reconciliation conflicts - the foundation for
self-service

Week 02 is considered complete only because the conflict was observed,
understood, and documented.
