# Week 05 -- CI & Validation

## Goal

Introduce enforceable documentation standards and automated validation.
Ensure that every iteration of the journal declares intent and provides
evidence, and that this structure is enforced via CI before changes can
be merged.

This week formalizes the idea that:

> Documentation is an enforceable contract.

------------------------------------------------------------------------

## What Was Implemented

### 1. Validation Script

A custom `validate-weeks.js` script was introduced to validate:

- Top-level title format: `# Week <number> – <title>`
- Presence of `## Goal` section
- Presence of `## Evidence` section
- At least one bullet item inside the Evidence section
- Consistency between filename (`week-XX.md`) and title week number
- Section order (`Goal` must appear before `Evidence`)

The validator outputs per-file errors and a final summary.

------------------------------------------------------------------------

### 2. Node Environment Stabilization

WSL environment was corrected to ensure Linux-based Node execution using
`nvm`. This eliminated Windows/UNC path issues and aligned local runtime
with GitHub CI.

Node 20 installed and set as default via `nvm`.

------------------------------------------------------------------------

### 3. GitHub Actions Integration

A GitHub Actions workflow was added to:

- Checkout repository
- Install dependencies
- Run `npm run validate`

Pull requests now fail if journal structure does not meet contract
requirements.

------------------------------------------------------------------------

### 4. Governance Layer Introduced

The system now enforces:

- Explicit intent per iteration
- Required proof of execution
- Structural consistency across all weeks
- Deterministic naming convention

This establishes CI as a policy enforcement layer rather than a passive
check.

------------------------------------------------------------------------

## Environment State After Week 05

- **Dev** auto-updates via pinned SHA tag updated by GitHub Action.
- **Staging** auto-syncs but uses a manually pinned image tag.
- **Prod** requires manual sync and uses a pinned image tag.

No promotion automation introduced yet. Environment separation remains
deliberate and controlled.

------------------------------------------------------------------------

## Evidence

- Validation script passes locally: `All 4 week documents valid.`
- Pull request created via bot credentials.
- CI validation executed successfully.
- PR approved and merged.
- Dev environment updated automatically via Argo CD.
- Staging and Prod remained unchanged (as expected due to pinned
    tags).

------------------------------------------------------------------------

## Architectural Outcome

Week 05 establishes:

- CI as a guardrail, not a suggestion.
- Documentation as a formalized contract.
- Structural validation as part of the platform control plane.
- Clear separation between content changes and image promotion.

The platform now prevents structural drift before it reaches the
cluster.

------------------------------------------------------------------------

## Retrospective Reflection

Week 05 felt deceptively small on paper and surprisingly foundational in practice.

What started as “let’s add validation” turned into something much more important: defining what the journal actually is. The moment the validator failed every file was a quiet turning point. It forced a clarification of structure, intent, and expectations. That friction wasn’t a setback — it was governance arriving.

This week introduced a real control layer into the system. Not just CI as a checkbox, but CI as a gate. Documentation now has a contract. Structure is enforced. Intent must be declared. Evidence must be provided. And merges are blocked if those standards are not met. That shift alone changes the nature of the project.

There was also an unexpected but valuable detour into environment drift. Fixing the Node runtime in WSL highlighted how subtle inconsistencies between local and CI environments can surface in surprising ways. It was a practical reminder that platform work often begins with eliminating ambiguity.

On the deployment side, the separation between Dev, Staging, and Prod became clearer. Dev moves continuously. Staging and Prod remain intentionally controlled. No accidental promotion occurred. No hidden automation leaked across boundaries. The system behaved exactly as designed. That predictability is a quiet success.

Most importantly, this week formalized something that was previously implicit: the journal is no longer just a narrative record. It is a governed artifact inside a platform. It has structure, validation, and policy enforcement. That elevates it from documentation to infrastructure-adjacent truth.

Week 05 didn’t introduce flashy features. It introduced discipline. And discipline is what makes the later complexity sustainable.
