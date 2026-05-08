## Context

The repository is a greenfield project with three components (Python pipeline, Kotlin/Spring Boot backend, React frontend) and no documentation. Anyone new to the project — including the author returning after a break — has no entry point.

## Goals / Non-Goals

**Goals:**
- Single README.md at the repo root covering all three components
- Explain project purpose and intended audience
- Cover local setup end-to-end (prerequisites, docker-compose, running each component)
- Document the operator pipeline workflow (run → review → load)

**Non-Goals:**
- API reference documentation (that belongs in code or a separate doc)
- Deployment / hosting instructions (out of scope for MVP)
- Contributing guidelines or code style docs

## Decisions

### 1. Single root README rather than per-component READMEs

A monorepo with three components could have a README per directory. For this project's scale, a single root README is easier to maintain and gives a complete picture in one place. Per-component READMEs can be added later if the components grow significantly.

### 2. Structure: overview → architecture → setup → usage

Standard README ordering: why the project exists first, then architecture diagram / description, then how to get it running, then day-to-day usage (running the pipeline). This serves both first-time readers and returning users who just need a specific command.

## Risks / Trade-offs

- **Goes stale**: README is prose, not code — it won't fail CI if it drifts. → Mitigated by keeping commands close to the actual config files so they're easy to spot-check.

## Open Questions

*(none — scope is well-defined)*
