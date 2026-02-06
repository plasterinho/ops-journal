# Ops Journal (future: Tracksuit Hopper)

> A GitOps‑native learning journal for platform engineers.

Ops Journal is a deliberately simple, honest system for tracking a platform‑engineering learning journey. It treats **Git as the source of truth**, Kubernetes as the execution environment, and the application itself as a lightweight **control‑plane UI** over real infrastructure and workflows.

This repository documents both:

* the **learning track** (12 weeks of platform‑engineering topics), and
* the **system that visualizes and validates that learning**.

At a later stage, Ops Journal may evolve into **Tracksuit Hopper** – a more dynamic, control‑plane‑style platform. That evolution is intentional and earned, not assumed.

---

## Why this exists

Most learning projects fail for one of two reasons:

1. They are *too static* (notes, blogs, docs that are never revisited).
2. They are *too ambitious* (mini SaaS products that stall learning).

Ops Journal sits in between.

It is:

* interactive, but not CRUD‑heavy
* honest, but not slow
* boring by design, but extensible by intent

If something is not in Git, it is assumed not to exist.
If something cannot be validated against reality, it is treated as untrusted.

---

## Core principles

### 1. Git is the source of truth

All learning progress, tasks, and reflections live in Git. The application reads from Git and reacts to Git workflows. Runtime state must converge toward Git, not replace it.

### 2. Interaction ≠ mutation

User interaction triggers **workflows** (PRs, checks, validations), not silent state changes. This mirrors real platform workflows such as GitOps, Terraform, and Argo CD.

### 3. Reality beats intention

Where possible, tasks are validated against real system state (Kubernetes APIs, CI status, service reachability). Manual claims are secondary to observable facts.

### 4. Boring first, clever later

Markdown + Git + a renderer is the baseline. Any additional complexity must clearly outperform that baseline, or it does not belong.

### 5. The platform dogfoods itself

Ops Journal runs on the same platform concepts it is used to learn. Policies, observability, delivery mechanisms, and failures apply to the journal itself.

---

## What this is (and is not)

### This *is*

* A GitOps‑native learning tracker
* A lightweight internal platform UI
* A record of real, inspectable engineering work
* A foundation for future platform abstractions

### This is *not*

* A generic task‑tracking SaaS
* A productivity app
* A database‑first system
* A framework showcase

---

## High‑level architecture

```
Git Repository
  ├── Learning definitions (weeks, tasks)
  ├── Evidence (screenshots, notes)
  └── Reflections
        ↓
   Ops Journal App
        ↓
   Kubernetes (Minikube → cloud)
```

The application:

* renders learning state from Git
* exposes it via a clean web UI
* triggers Git workflows for interaction
* optionally validates claims against cluster reality

---

## Learning track overview

The learning journey is structured as a **12‑week roadmap**, grouped into four phases:

1. Foundations & Truth
2. Interaction & Delivery
3. Observability & Reliability
4. Platform Thinking

Each week contains:

* core tasks (must‑do)
* stretch tasks (optional)
* evidence requirements
* reflections

The journal UI visualizes progress across these dimensions.

---

## Evolution path

Ops Journal is intentionally minimal at the beginning.

Planned evolution:

* **Phase 1:** Static rendering from Git
* **Phase 2:** Interaction via PRs and CI
* **Phase 3:** Reality‑based validation
* **Phase 4:** Introduction of a backend control plane (Tracksuit Hopper)

Tracksuit Hopper is not a rewrite. It is a *promotion*.

---

## Non‑goals (important)

To avoid scope creep, the following are explicitly out of scope in early phases:

* Authentication and multi‑tenancy
* Billing or monetization
* Generic user management
* Feature parity with task managers

These may be explored later **only if** the learning goals are already met.

---

## Success criteria

This project is successful if:

* The learning journey is completed end‑to‑end
* The system remains deployable and understandable
* Progress can be audited months later via Git history
* Platform concepts are learned through use, not slides

Polish is optional. Truth is not.

---

## Name

**Ops Journal** is the working name for the minimal system.

**Tracksuit Hopper** is the intentionally silly name for the future, more dynamic platform layer. The name is a reminder:

> This is serious learning. The product name does not have to be.

---

## How to read this repository

This repository is intentionally structured around **three different kinds of artifacts**, each serving a different purpose:

* **`journal/`** – the factual learning log

  * what was done
  * what was completed
  * evidence and reflections
  * this is the *source of truth* for progress

* **`documentation/`** – runbooks and procedures

  * step-by-step instructions
  * prerequisites and tooling
  * troubleshooting notes
  * this is how work can be *reproduced later*

* **Application code & manifests** – the system under learning

  * MkDocs configuration
  * container image definition
  * Kubernetes manifests

If you are reviewing this repository:

* start with `journal/` to understand *what* was learned
* use `documentation/` to understand *how* it was done
* treat the code as supporting evidence, not the primary narrative

The repository evolves week by week. Earlier weeks are intentionally simpler and more explicit.

---

## Status

This repository is a living system.
Expect evolution, refactoring, and occasional intentional destruction in the name of learning.

## Repo evolution

* Week 1–2: flat / experimental structure
* Week 3: platform-oriented GitOps layout (v2)

Old paths may still exist temporarily during migration.
