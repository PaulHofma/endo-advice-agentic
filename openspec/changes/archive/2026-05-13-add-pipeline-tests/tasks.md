## 1. Project Setup

- [x] 1.1 Create `pipeline/tests/` directory and empty `__init__.py`
- [x] 1.2 Add `pytest` and `pytest-mock` to a new `pipeline/requirements-dev.txt`
- [x] 1.3 Add `pytest.ini` at `pipeline/` root with `testpaths = tests` and `pythonpath = .`
- [x] 1.4 Add `pipeline/tests/conftest.py` with shared fixtures: `make_pubmed_article`, `make_raw_finding`, `make_verified_finding`

## 2. Synthesis Tests

- [x] 2.1 Create `pipeline/tests/test_synthesis.py`
- [x] 2.2 Test: happy path — Claude returns valid JSON, `run_synthesis` returns populated `RawFinding` list
- [x] 2.3 Test: no PubMed results — returns empty list without calling Claude
- [x] 2.4 Test: no usable abstracts after fetch — returns empty list without calling Claude
- [x] 2.5 Test: Claude returns invalid JSON — returns empty list, prints parse error
- [x] 2.6 Test: Claude references unknown PMID — skips that entry, returns others
- [x] 2.7 Test: all clinical fields null in Claude response — `RawFinding` has all None clinical fields
- [x] 2.8 Test: PMC fallback applied when dosage is null — `fetch_pmc_dosage` called; dosage updated on finding
- [x] 2.9 Test: PMC fallback skipped when `fetch_pmc_dosage` returns None — dosage stays None, no error

## 3. Verification Tests

- [x] 3.1 Create `pipeline/tests/test_verification.py`
- [x] 3.2 Test: Claude returns `verified` verdict — `VerifiedFinding.verdict == Verdict.VERIFIED`
- [x] 3.3 Test: Claude returns `flagged` verdict — `VerifiedFinding.verdict == Verdict.FLAGGED`
- [x] 3.4 Test: `fetch_abstract` returns None — verdict is `REJECTED` with "PMID not found" reason
- [x] 3.5 Test: Claude returns unparseable JSON — verdict is `FLAGGED` with parse error reason
- [x] 3.6 Test: empty input list — returns empty list without calling Claude

## 4. PMC Fetch Tests

- [x] 4.1 Create `pipeline/tests/test_pmcfetch.py`
- [x] 4.2 Test: PMCID found, full text fetched, Claude returns dosage — `fetch_pmc_dosage` returns dosage string
- [x] 4.3 Test: `_get_pmcid` returns None — `fetch_pmc_dosage` returns None without fetching text
- [x] 4.4 Test: Claude returns "null" string — `fetch_pmc_dosage` returns None
- [x] 4.5 Test: `Entrez.elink` raises exception — `_get_pmcid` returns None, no propagation

## 5. Review Writer Tests

- [x] 5.1 Create `pipeline/tests/test_review_writer.py`
- [x] 5.2 Test: `write_review_file` — verified finding has `approved: true`, flagged/rejected have `approved: false`
- [x] 5.3 Test: `write_review_file` — empty findings list writes file with "*(none)*" placeholders
- [x] 5.4 Test: `write_consolidated_review_file` — two supplements produce two `## Supplement:` headings
- [x] 5.5 Test: `write_consolidated_review_file` — supplement with empty findings shows "*(no findings produced)*"
- [x] 5.6 Test: `write_consolidated_review_file` — failed topic produces `— FAILED` section with error text

## 6. Load Findings Tests

- [x] 6.1 Create `pipeline/tests/test_load_findings.py`
- [x] 6.2 Test: `parse_review_file` — returns only `approved: true` entries from mixed file
- [x] 6.3 Test: `parse_review_file` — skips malformed JSON blocks
- [x] 6.4 Test: `parse_review_file` — returns empty list when no approved entries exist
- [x] 6.5 Test: `load_findings` — new entry triggers supplement INSERT, finding INSERT, citation INSERT, symptom INSERT (via mock cursor)
- [x] 6.6 Test: `load_findings` — malformed entry (empty PMID) is skipped, function continues
- [x] 6.7 Test: `load_findings` — citation count returns 0 → `RuntimeError` raised and transaction rolled back
- [x] 6.8 Test: `load_findings` — entry without `suggested_symptom` skips symptom upsert
- [x] 6.9 Test: `load_findings` — empty entry list returns immediately without opening DB connection

## 7. Pipeline CLI Tests

- [x] 7.1 Create `pipeline/tests/test_pipeline_cli.py`
- [x] 7.2 Test: `_resolve_topics` with `--topic` only — returns single-item list
- [x] 7.3 Test: `_resolve_topics` with multiple `--topics` — returns all topics in order
- [x] 7.4 Test: `_load_topics_file` — reads non-blank, non-comment lines from a temp file
- [x] 7.5 Test: `_resolve_topics` deduplicates repeated topics
- [x] 7.6 Test: `_resolve_topics` with no input — raises `ValueError`
- [x] 7.7 Test: `main()` with `ENDO_API_KEY` absent — prints error to stderr and calls `sys.exit(1)` before synthesis
- [x] 7.8 Test: `_run_topic` exception — returns `(topic, None, error_string)` tuple

## 8. Slug Utility Tests

- [x] 8.1 Add slug tests to `test_load_findings.py` (or a small `test_utils.py`)
- [x] 8.2 Test: `slug_from_name("Pelvic Pain")` → `"pelvic-pain"`
- [x] 8.3 Test: `slug_from_name("Omega-3 (Fish Oil)")` → `"omega-3-fish-oil"`

## 9. Verification Pass

- [x] 9.1 Run `pytest` from `pipeline/` — all tests pass with no environment variables set
- [x] 9.2 Confirm no production module files were modified
- [x] 9.3 Document in `pipeline/tests/README.md`: the rule that all new pipeline functionality must ship with tests covering happy path, edge cases, and error paths
