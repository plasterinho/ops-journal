# Week 01 – The Journal Exists

> Theme: Foundations & Truth  
> Goal: Make the journal exist as a real, running system.

---

## Core Tasks

### [x] Create Ops Journal repository structure

**Description**  
Create a clean, minimal repository structure that separates:
- documentation (human intent)
- journal data (app input)
- application code
- deployment manifests

**Evidence (required)**
- Commit hash introducing the structure

```bash
$ git log --oneline --max-count=10
e288357 Initialize Week 01 journal with tasks and reflections
f631734 Add README.md with directory information
91c14c0 Add ops_journal_week_1_concretization.md
041abb7 Add 12-Week Platform Engineering Roadmap document
5180a23 Create ops_journal_tracksuit_hopper_readme.md
608d9d5 Initial commit
```

- Tree output of repository root
```bash
 tree -L 3
.
├── Dockerfile
├── documentation
│   ├── ops_journal_12_week_roadmap_data.md
│   ├── ops_journal_tracksuit_hopper_readme.md
│   ├── ops_journal_week_1_concretization.md
│   └── README.md
├── journal
│   ├── evidence
│   │   └── week-01
│   ├── README.md
│   └── week-01.md
├── k8s
│   ├── deployment.yaml
│   └── service.yaml
├── mkdocs.yml
└── README.md
```
---

### [x] Define Week 1 learning tasks as data

**Description**  
Write Week 1 tasks in Markdown so they can be consumed by the Ops Journal application. Tasks must not be hardcoded in application logic.

**Acceptance criteria**
- Tasks are expressed as Markdown
- Checkbox syntax is used
- Placeholders for evidence exist

**Evidence (required)**
- Link to `journal/week-01.md`
[week-01.md](week-01.md)
---

### [x] Deploy static Ops Journal renderer to Minikube

**Description**  
Run a minimal application in Minikube that reads journal data from the repository and renders it as HTML.

**Acceptance criteria**
- At least one Pod is running
- Application reads Markdown at runtime
- UI reflects journal content

**Evidence (required)**
- Screenshot of rendered journal
![minikube](evidence/week-01/minikube-ui.png)
- `kubectl get pods` output
```bash
kubectl get pods | grep ops-journal
ops-journal-6c4479d95b-9j594        1/1     Running   0               120m
```
- Commit hash adding Kubernetes manifests
```bash
aa27831  add kubernetes deployment and service definition
```

---

## Stretch Tasks (optional)

### [x] Add minimal styling

**Description**  
Apply basic styling to improve readability. No frameworks required.

**Evidence (optional)**
- Screenshot comparison before / after

---

## Reflection (mandatory)

Answer briefly:

- What felt slower than expected? Jumping through the hoops with GitHub, Docker, MkDocs, Kubernetes - SSH key issues, rebuilding and redeploying the image without changing the tags, etc.
- What felt easier than expected? Minikube was surprisingly willing to cooperate.
- What did you consciously *not* build? No Go or Express application - this is not part of this exercise.



---

## Notes

This week should feel intentionally small.
If it feels impressive, too much was built.

