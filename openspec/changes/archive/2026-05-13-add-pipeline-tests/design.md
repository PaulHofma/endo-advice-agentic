## Context

The pipeline is a multi-module Python system: `synthesis.py`, `verification.py`, `pmcfetch.py`, `pubmed.py`, `review_writer.py`, `load_findings.py`, `summarise.py`, and the `pipeline.py` CLI entry point. All business logic lives here, but there are no tests. Every module has at least one external dependency (Anthropic API, PubMed HTTP, PostgreSQL) that must be mocked for unit tests to be fast and offline-capable.

## Goals / Non-Goals

**Goals:**
- Unit-test every module in isolation by mocking all external I/O (HTTP, Anthropic SDK, psycopg2)
- Cover every spec-defined scenario as a test case
- Cover edge cases identified during code review: JSON parse failures, missing PMIDs, malformed review entries, empty topic lists, citation integrity enforcement
- Tests run offline (no API keys, no DB, no network) with `pytest`

**Non-Goals:**
- End-to-end integration tests against live services (too slow and key-dependent for CI)
- Testing `summarise.py` deeply (it is a thin LLM call over DB rows; basic smoke coverage is sufficient)
- Performance or load testing

## Decisions

### Decision: pytest + unittest.mock (no extra mocking library)
`unittest.mock` is part of the standard library and sufficient for patching `anthropic.Anthropic`, `requests.get`, `psycopg2.connect`, and Biopython's `Entrez`. Adding `pytest-mock` (provides `mocker` fixture) would improve ergonomics for parametrize scenarios. We include it as an optional dev dependency.

**Alternative considered:** `responses` library for HTTP mocking — rejected because it only covers `requests`, not Biopython Entrez which uses its own urllib calls.

### Decision: Flat `pipeline/tests/` directory, one file per production module
`test_synthesis.py`, `test_verification.py`, `test_pmcfetch.py`, `test_pubmed.py`, `test_review_writer.py`, `test_load_findings.py`, `test_pipeline_cli.py`. This maps 1:1 to production modules, making it easy to find tests for a given file.

**Alternative considered:** grouping by feature area — rejected because the module structure already reflects feature areas.

### Decision: Shared fixtures in `conftest.py`
Common objects (`RawFinding`, `PubMedArticle`, `VerifiedFinding`) are built in `conftest.py` as pytest fixtures so they don't repeat across test files.

### Decision: DB tests use an in-memory patch of `psycopg2.connect`
All `load_findings` tests mock `psycopg2.connect` and use a `MagicMock` cursor whose `fetchone`/`fetchall` return values are configured per test. This keeps DB logic fully unit-testable without a running Postgres instance.

**Alternative considered:** Testcontainers — appropriate for integration tests but over-engineered for unit coverage of the loader's branching logic.

### Decision: Claude calls are mocked at the `anthropic.Anthropic` constructor
Patching `anthropic.Anthropic` in each test returns a mock whose `.messages.create()` returns a controlled response object. This is the simplest injection point and mirrors how the production modules initialize the client.

## Risks / Trade-offs

- **Mocks drift from real APIs** → Mitigation: keep mock return shapes aligned with actual Anthropic SDK and psycopg2 return types; re-check on SDK upgrades.
- **Test coverage of prompt content** → We test that prompts contain key substrings (PMID, claim text) rather than asserting exact prompt text, to avoid brittle tests when prompts are tweaked.
- **`summarise.py` left lightly covered** → Acceptable for now; it is a thin wrapper and its behavior is exercised implicitly through load integration. Add dedicated tests when the module grows.

## Migration Plan

1. Create `pipeline/tests/` with `conftest.py` and one test file per module
2. Add `pytest` and `pytest-mock` to `requirements.txt` (or new `requirements-dev.txt`)
3. Add `pytest.ini` at `pipeline/` root pointing `testpaths = tests`
4. Verify `pytest` runs green from `pipeline/` without any env vars set

No rollback needed — test files are purely additive.

## Open Questions

- Should `requirements-dev.txt` be separate from `requirements.txt`? (Keeps prod image lean, but adds a second file to maintain.) Recommendation: separate, since the pipeline is never containerized.
