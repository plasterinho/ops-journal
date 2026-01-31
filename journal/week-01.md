# Week 01 – The Journal Exists

> Theme: Foundations & Truth  
> Goal: Make the journal exist as a real, running system.

---

## Core Tasks

### [ ] Create Ops Journal repository structure

**Description**  
Create a clean, minimal repository structure that separates:
- documentation (human intent)
- journal data (app input)
- application code
- deployment manifests

**Evidence (required)**
- Commit hash introducing the structure
- Tree output of repository root

---

### [ ] Define Week 1 learning tasks as data

**Description**  
Write Week 1 tasks in Markdown so they can be consumed by the Ops Journal application. Tasks must not be hardcoded in application logic.

**Acceptance criteria**
- Tasks are expressed as Markdown
- Checkbox syntax is used
- Placeholders for evidence exist

**Evidence (required)**
- Link to `journal/week-01.md`

---

### [ ] Deploy static Ops Journal renderer to Minikube

**Description**  
Run a minimal application in Minikube that reads journal data from the repository and renders it as HTML.

**Acceptance criteria**
- At least one Pod is running
- Application reads Markdown at runtime
- UI reflects journal content

**Evidence (required)**
- Screenshot of rendered journal
- `kubectl get pods` output
- Commit hash adding Kubernetes manifests

---

## Stretch Tasks (optional)

### [ ] Add minimal styling

**Description**  
Apply basic styling to improve readability. No frameworks required.

**Evidence (optional)**
- Screenshot comparison before / after

---

## Reflection (mandatory)

Answer briefly:

- What felt slower than expected?
- What felt easier than expected?
- What did you consciously *not* build?

---

## Notes

This week should feel intentionally small.
If it feels impressive, too much was built.

