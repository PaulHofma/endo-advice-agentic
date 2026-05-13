## Context

The project has three code layers: a Kotlin/Spring Boot backend, a Python pipeline, and a React/TypeScript frontend. Only the frontend has a linter today (ESLint via `npm run lint`). The backend uses Gradle and the pipeline has no tooling config at all. The change-completion gate (verification-before-completion skill + CLAUDE.md) currently mentions tests but not linting.

## Goals / Non-Goals

**Goals:**
- Integrate ktlint into the Gradle build for the backend with zero-friction `ktlintCheck` / `ktlintFormat` tasks.
- Add ruff for the pipeline, configured to enforce PEP 8 (E/W rules) and common style rules, runnable via `ruff check pipeline/`.
- Update CLAUDE.md and the `verification-before-completion` skill to gate archiving on all three linters passing clean.

**Non-Goals:**
- CI/CD pipeline setup (no GitHub Actions or similar configured yet).
- Strict type-checking beyond what ruff covers (mypy is out of scope).
- Auto-fix enforcement in git hooks — linting is a manual gate, not a commit hook.

## Decisions

### Backend: ktlint via `jlleitschuh/ktlint-gradle`

**Decision:** Use the `jlleitschuh/ktlint-gradle` Gradle plugin rather than running ktlint as a standalone binary.

**Rationale:** Keeps linting inside the existing `./gradlew` workflow developers already use; no separate install step. The plugin exposes `ktlintCheck` (CI gate) and `ktlintFormat` (auto-fix) tasks. It follows standard Kotlin coding conventions without requiring a custom ruleset — appropriate for a project at this stage.

**Alternative considered:** Detekt — more configurable, supports custom rules and static analysis beyond formatting, but is heavier and overkill for a small codebase that just needs consistent style.

### Pipeline: ruff

**Decision:** Use ruff (not flake8) as the PEP 8 linter.

**Rationale:** ruff is orders of magnitude faster than flake8, written in Rust, and is now the community-recommended replacement. It covers the same E/W rule set (pycodestyle) plus F (pyflakes) out of the box. Config lives in `pyproject.toml` under `[tool.ruff]` alongside any future packaging metadata — a single file.

**Alternative considered:** flake8 — the classic choice, but slower, requires separate plugins for rules ruff includes natively, and is in maintenance mode.

### Config location: `pipeline/pyproject.toml`

**Decision:** Place the ruff config in `pipeline/pyproject.toml` rather than the repo root.

**Rationale:** There is no repo-level Python packaging. Scoping config to `pipeline/` keeps it close to the code it governs and avoids polluting the root. Running `ruff check .` from inside `pipeline/` is the natural invocation.

### Completion gate: CLAUDE.md + verification-before-completion skill

**Decision:** Update both CLAUDE.md (human-readable reference) and the `verification-before-completion` skill (agent-enforced gate).

**Rationale:** CLAUDE.md is the authoritative source of project conventions for both humans and agents. The verification skill is what agents must invoke before declaring work done; updating it ensures the gate is enforced automatically without relying on memory.

## Risks / Trade-offs

- **Existing code may have lint violations** — first `ktlintCheck` and `ruff check` runs will likely flag issues in current files. These must be fixed as part of this change before the gate can be turned on. → Mitigation: run auto-fix (`ktlintFormat`, `ruff check --fix`) first, then manually review residual issues.
- **ruff version drift** — ruff moves fast; pinning the version in `requirements.txt` prevents surprises. → Pin to a specific version (e.g. `ruff==0.4.x`).
- **ktlint and existing code style** — ktlint enforces trailing commas, import ordering, etc. The auto-formatter handles most of this, but some patterns may require manual cleanup. → Accept the one-time churn; the codebase is small.

## Migration Plan

1. Add ktlint plugin to `backend/build.gradle.kts`; run `./gradlew ktlintFormat` to auto-fix; resolve any remaining violations; verify `./gradlew ktlintCheck` passes.
2. Add `pyproject.toml` with ruff config to `pipeline/`; add `ruff` to `pipeline/requirements.txt`; run `ruff check --fix .` from `pipeline/`; resolve residual issues; verify `ruff check .` passes clean.
3. Update CLAUDE.md to list all three lint commands in the completion-gate section.
4. Update the `verification-before-completion` skill to require linting as a step before archiving.

No rollback risk — linting is additive and does not affect runtime behavior.

## Open Questions

- None — tool choices are clear given project scale and existing conventions.
