## ADDED Requirements

### Requirement: ruff is configured as the pipeline linter
The `pipeline/` directory SHALL contain a `pyproject.toml` (under `[tool.ruff]`) that configures ruff to enforce PEP 8 (E/W rules) and pyflakes (F rules) across all `.py` files. The `ruff` package SHALL be pinned in `pipeline/requirements.txt`.

#### Scenario: Developer checks for PEP 8 violations
- **WHEN** a developer runs `ruff check .` from inside `pipeline/`
- **THEN** the command exits zero if all Python sources are clean, or exits non-zero and prints each violation with file, line number, and rule code

#### Scenario: Developer auto-fixes style issues
- **WHEN** a developer runs `ruff check --fix .` from inside `pipeline/`
- **THEN** ruff rewrites all auto-fixable violations in-place and reports any remaining issues that require manual attention

### Requirement: Existing pipeline code is lint-clean at the time of rollout
All `.py` files in `pipeline/` SHALL conform to the ruff ruleset before this change is archived.

#### Scenario: Agent verifies lint cleanliness before archiving
- **WHEN** an agent runs `ruff check .` from inside `pipeline/` as part of the pre-archive gate
- **THEN** the command exits zero with no violations reported
