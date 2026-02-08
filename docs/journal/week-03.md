# Week 03 — First Real GitOps Environment

## Context

Starting point (end of Week 02):
* Applications deployed via Argo CD
* Per-application Argo CD Applications (ops-journal-dev, ops-journal-staging)
* Repository structure centered around apps/
* Manual reconciliation and structural drift possible

Goal for Week 03:
* Move from “Argo CD is installed” to “GitOps is the control plane”
* Introduce environment-level ownership
* Make Git the only source of truth for workloads

------------------------------

## Key Design Decision
### From per-app GitOps to per-environment GitOps

Old mental model:
* One Argo CD Application per workload
* Apps decide where and how they deploy

New mental model:
* One Argo CD Application per environment
* Environments decide what runs
* Workloads are passive and environment-agnostic

Reasoning:
* Clear ownership boundaries
* Avoid split-brain reconciliation
* Mirrors real platform-team vs app-team responsibilities

-------------------------------

## Repository Restructure (v2)

Structural changes
* apps/ → deprecated
* workloads/ introduced as the home for application manifests
* environments/ introduced as composition and intent
* platform/gitops/ used for Argo CD Application definitions

Key insight:
> Structure reflects ownership, not convenience.

-------------------------------

## Wiring the First Environment: local

### Environment composition with Kustomize

* `environments/local/` acts as the GitOps root
* Environment selects workloads via directory-based Kustomize composition
* No raw Kubernetes manifests in the environment layer

Important Kustomize rule learned:
* Files are resources
* Directories are composition
* Only kustomization.yaml is an entry point

Several errors occurred here, all due to misunderstanding this rule.

-------------------------------

## Argo CD Integration

### Application definition

* One Argo CD Application named `local`
* Explicitly pinned to branch `week3-repo-v2`
* Path: `environments/local`
* Automated sync with prune and self-heal enabled

Critical learning:
* `targetRevision: HEAD` means *default branch*, not “current work”
* Argo CD failures are deterministic and reproducible with `kustomize build`

-------------------------------

## Debugging Journey (What Actually Went Wrong)

* Filename mismatches - it's better to agree on a single naming convention (`.yml` vs `.yaml`)
* Treating a `Kustomization` file as a resource
* Missing `kustomization.yaml` inside a directory - all of the files stored `environments` should be named `kustomization.yaml` 
* Argo CD pointing at the wrong Git branch

Meta-observation:

> Every Argo CD error corresponded to a real, local Kustomize failure or Git mismatch.

-------------------------------

## Cleanup of Legacy GitOps Apps

* Deleted `ops-journal-dev` and `ops-journal-staging`
* Removed per-app Argo CD Application manifests
* Ensured single ownership of Kubernetes resources

Outcome:
* No reconciliation fights
* `local` envirojnment became the sole owner
* Cluster state and repo state aligned 1:1

-------------------------------

## Validation of GitOps Control Loop

* Verified `kustomize build environments/local` locally
* Verified Argo CD Application spec via Kubernetes CRD
* Confirmed reconciliation without manual `kubectl apply`
* Confirmed automatic reconciliation after manual changes:
  * ran `kubectl scale deployment ops-journal --replicas=2`
  * observed Argo CD revert to a single replica

-------------------------------

## What Changed Conceptually

Before Week 03:
* Git as deployment input
* Argo CD as a delivery tool

After Week 03:
* Git as the control plane
* Argo CD as an enforcement mechanism
* Environments as first-class concepts

-------------------------------

## What This Unlocks Next
* Adding `staging` and `prod` environments predictably
* Promotion via Git, not copy-paste
* Clear platform/app team boundaries
* Safe experimentation via branches

-------------------------------

## Open Questions / Future work
* Align `dev` vs `local` naming
* Namespace-per-environment
* Branch-per-environment vs directory-per-environment
* Where environment-specific policy should live

-------------------------------

## Summary

In Week 03 I moved from "using Argo CD" to actually operating with GitOps by restructuring the repository around ownership and wiring the first environment (`local`) end-to-end. I replaced per-application Argo CD Applications with a single environment-level Application, made `environments/local` the GitOps reconciliation root, and treated workloads as passive, environment-agnostic inputs. Most of the work was not adding features but removing ambiguity: fixing Kustomize composition mistakes, aligning file and directory semantics, pinning Argo CD to the correct Git branch, and deleting legacy applications that caused split ownership. The key outcome is that Git is now the only write path for the `local` environment, Argo CD enforces desired state deterministically, and the platform structure reflects how responsibility is actually divided in real systems. This week marked the point where the setup stopped being “a Kubernetes lab” and became a minimal but coherent platform control plane.

-------------------------------

## If I had to do this again

If I were starting Week 03 again, I would begin by clearly deciding **who owns what** before touching any YAML: environments own reconciliation, workloads are passive inputs, and GitOps applications should map to environments, not apps. I would wire a single environment end-to-end first (including Argo CD, Kustomize composition, and branch pinning) before attempting multiple environments, and I would verify every Argo CD error locally with `kustomize build` instead of debugging in the UI. I would also explicitly pin Argo CD to a non-default branch from the start to avoid confusion between “work in progress” and “current truth”, and delete legacy GitOps applications as soon as a new ownership model is introduced to prevent split-brain reconciliation. Finally, I would accept that most of the difficulty comes not from Kubernetes itself, but from learning how tools enforce rules exactly as specified, and treat those failures as signals that the platform model is becoming real.
