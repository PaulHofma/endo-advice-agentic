## Why

The pipeline contains all core business logic (synthesis, verification, PMC fallback, review file writing, finding load, summarisation) but has no automated tests. As the pipeline grows, regressions are caught only through manual end-to-end runs — which require live API keys, a running database, and real PubMed network calls. Tests are needed now to make the logic safe to refactor and to document the expected behavior derived from the existing specs.

## What Changes

- Add a `pipeline/tests/` directory with a pytest-based test suite
- Add test fixtures and mocks that isolate each module from external dependencies (Anthropic API, PubMed/Entrez HTTP, PostgreSQL)
- Cover all spec-defined behavior across synthesis, verification, PMC fallback, review writing, database loading, and the CLI entry point
- Add a `pytest.ini` / `pyproject.toml` test configuration so tests are runnable with `pytest` from the `pipeline/` directory

## Capabilities

### New Capabilities

- `pipeline-test-suite`: Automated unit and integration tests for all pipeline modules, covering spec-defined scenarios, edge cases, and error paths

### Modified Capabilities

*(none — tests document existing behavior; no spec-level requirement changes)*

## Impact

- `pipeline/` — new `tests/` subdirectory added; no production module changes
- New dev dependencies: `pytest`, `pytest-mock` (added to `requirements.txt` or a new `requirements-dev.txt`)
- CI: tests can be run without live API keys or a database by mocking all external calls
