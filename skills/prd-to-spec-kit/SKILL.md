---
name: prd-to-spec-kit
description: "Convert an approved product PRD into a Spec Kit constitution, specification, plan, tasks and acceptance tests."
---

# PRD to Spec Kit

## Preconditions

- PRD scope and product owner are identified.
- Non-goals, rights boundaries, supported environments, and success metrics are present.
- Required hardware, licenses, or customer decisions are either known or explicitly blocked.

## Workflow

1. Read the original PRD and `context/01_REQUIREMENTS_TRACEABILITY.md`.
2. Create a product constitution covering code quality, testing, documentation, licensing, privacy, compatibility, reproducibility, and release review.
3. Convert user outcomes into numbered functional and non-functional requirements.
4. Preserve non-goals and explicitly list unsupported cases.
5. Generate a technical plan with components, data flow, interfaces, dependencies, threat model, migration, and rollback.
6. Generate small tasks, each mapped to a requirement and an executable acceptance test.
7. Identify decisions that cannot be made safely and stop before implementation.
8. Run a consistency review: no task without a requirement, no requirement without a test, and no release item without rights evidence.

## Outputs

- `products/<product>/spec/constitution.md`
- `products/<product>/spec/spec.md`
- `products/<product>/spec/plan.md`
- `products/<product>/spec/tasks.md`
- `products/<product>/spec/traceability.csv`
- `products/<product>/spec/acceptance.md`

## Stop conditions

Stop and mark BLOCKED for unknown MCU/toolchain, unverified third-party license, missing asset ownership, ambiguous safety responsibility, or scope that requires a platform write action.
