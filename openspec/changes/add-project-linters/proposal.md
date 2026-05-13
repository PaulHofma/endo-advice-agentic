## Why

The backend (Kotlin) and pipeline (Python) have no static analysis configured, making it easy for style inconsistencies and simple errors to accumulate undetected. The frontend already has ESLint, but linting is not gated as a required step before archiving a change — all three layers should be clean before any change is considered done.

## What Changes

- Add **ktlint** to the Kotlin/Spring Boot backend via the `jlleitschuh/ktlint-gradle` Gradle plugin, enforcing the standard Kotlin coding conventions.
- Add **ruff** to the Python pipeline as a PEP 8–compliant linter and formatter checker.
- Update the **change-completion criteria** (verification-before-completion skill and CLAUDE.md) to require that all three linters (BE, FE, pipeline) pass clean before a change may be archived.

## Capabilities

### New Capabilities

- `backend-linting`: ktlint integrated into the Gradle build; `./gradlew ktlintCheck` lints all Kotlin sources and `./gradlew ktlintFormat` auto-fixes formatting.
- `pipeline-linting`: ruff configured in `pyproject.toml` (or `ruff.toml`); `ruff check pipeline/` enforces PEP 8 and common style rules across all pipeline Python files.

### Modified Capabilities

- `agent-conventions-frontend`: Extend the agent-facing conventions to include the full linting gate — all three linters (BE ktlint, FE ESLint, pipeline ruff) must pass before a change is archived.

## Impact

- **Backend**: `backend/build.gradle.kts` gains the ktlint plugin; existing Kotlin source files may need minor formatting fixes on first run.
- **Pipeline**: New `pyproject.toml` (or `ruff.toml`) config at the repo root or `pipeline/`; existing `.py` files may need minor PEP 8 fixes.
- **Frontend**: No setup change — ESLint already present via `npm run lint`.
- **Workflow**: `verification-before-completion` skill and `CLAUDE.md` updated to list linting as a required pre-archive step alongside tests.
- **No API or schema changes.**
