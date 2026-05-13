## ADDED Requirements

### Requirement: All new pipeline functionality SHALL have tests
Any new function, module, or behavior added to the pipeline MUST be accompanied by tests before the implementation is considered complete. Tests SHALL cover the happy path, empty/null inputs, and any error paths introduced by the new code.

#### Scenario: New module added to pipeline
- **WHEN** a developer adds a new Python module to `pipeline/`
- **THEN** a corresponding `tests/test_<module>.py` file exists with tests covering all public functions

#### Scenario: New function added to existing module
- **WHEN** a developer adds a new function to an existing pipeline module
- **THEN** at least one test covers the function's happy path, and additional tests cover edge cases and error paths

#### Scenario: Existing test suite still passes after new code is added
- **WHEN** new functionality is added alongside its tests
- **THEN** `pytest` from `pipeline/` passes with no failures on both old and new tests

---

### Requirement: Test suite runs offline without API keys or a database
The test suite SHALL be executable with `pytest` from the `pipeline/` directory without setting `ENDO_API_KEY`, `ANTHROPIC_API_KEY`, or any database URL. All external I/O (Anthropic SDK, PubMed HTTP, Entrez, psycopg2) SHALL be mocked.

#### Scenario: Running tests with no environment variables set
- **WHEN** the developer runs `pytest` from `pipeline/` with no API keys in the environment
- **THEN** all tests pass without making any network calls or database connections

---

### Requirement: Synthesis — successful run produces structured RawFindings
The synthesis module SHALL be tested for the happy path: given mocked PubMed search results and a mocked Claude response containing valid JSON, `run_synthesis` SHALL return a list of `RawFinding` objects with all fields populated.

#### Scenario: Claude returns valid JSON findings
- **WHEN** `run_synthesis` is called with a topic, PubMed returns PMIDs, abstracts are fetched, and Claude returns a valid JSON array with a claim, excerpt, PMID, and clinical fields
- **THEN** `run_synthesis` returns one `RawFinding` per JSON entry with all fields set correctly

#### Scenario: No PubMed results
- **WHEN** `search_pubmed` returns an empty list
- **THEN** `run_synthesis` returns an empty list without calling Claude

#### Scenario: No usable abstracts
- **WHEN** PMIDs are found but `fetch_abstracts` returns an empty list
- **THEN** `run_synthesis` returns an empty list without calling Claude

#### Scenario: Claude returns invalid JSON
- **WHEN** the Claude response is not valid JSON (e.g., contains commentary text)
- **THEN** `run_synthesis` returns an empty list and logs a parse error

#### Scenario: Claude references a PMID not in the fetched article set
- **WHEN** the Claude response includes a PMID that was not in the fetched articles
- **THEN** that entry is skipped and a warning is printed; other valid entries are returned

#### Scenario: Clinical fields absent from abstract
- **WHEN** Claude returns null for dosage, duration, study_type, sample_size, placebo_controlled, and safety_notes
- **THEN** the resulting `RawFinding` has None for all those fields

---

### Requirement: Synthesis — PMC dosage fallback is attempted when dosage is null
After synthesis, for any finding with `dosage = None`, the pipeline SHALL call `fetch_pmc_dosage`. If a dosage is returned, it SHALL be written to the finding before it is returned.

#### Scenario: PMC dosage found and applied
- **WHEN** a finding has null dosage and `fetch_pmc_dosage` returns a non-null string
- **THEN** the finding's `dosage` field is updated to the returned value

#### Scenario: PMC dosage unavailable
- **WHEN** `fetch_pmc_dosage` returns None
- **THEN** the finding's `dosage` remains None and no error is raised

---

### Requirement: Verification — each finding is independently re-verified against PubMed
`run_verification` SHALL re-fetch each finding's abstract by PMID and ask Claude for a verdict. The returned `VerifiedFinding` SHALL carry the correct `Verdict` enum value and reason string.

#### Scenario: Claim is well-supported — verified verdict
- **WHEN** Claude returns `{"verdict": "verified", "reason": "...", "verified_excerpt": "..."}`
- **THEN** the `VerifiedFinding` has `verdict = Verdict.VERIFIED` and a non-empty reason

#### Scenario: Claim overstates evidence — flagged verdict
- **WHEN** Claude returns `{"verdict": "flagged", "reason": "...", "verified_excerpt": "..."}`
- **THEN** the `VerifiedFinding` has `verdict = Verdict.FLAGGED`

#### Scenario: PMID does not resolve
- **WHEN** `fetch_abstract` returns None for the finding's PMID
- **THEN** the `VerifiedFinding` has `verdict = Verdict.REJECTED` and reason "PMID not found or abstract unavailable"

#### Scenario: Claude returns unparseable JSON during verification
- **WHEN** the Claude verification response cannot be parsed as JSON
- **THEN** the finding is marked `Verdict.FLAGGED` with reason "Could not parse verification response"

#### Scenario: Empty input list
- **WHEN** `run_verification` is called with an empty list
- **THEN** it returns an empty list without calling Claude

---

### Requirement: PMC fetch — PMCID lookup and full-text extraction
`fetch_pmc_dosage` SHALL return a dosage string when a PMC full text is available and contains the dosage, or None otherwise. All Entrez and Claude calls SHALL be mockable.

#### Scenario: PMC full text available and dosage found
- **WHEN** `_get_pmcid` returns a PMCID, `_fetch_pmc_text` returns Methods text, and Claude returns a dosage string
- **THEN** `fetch_pmc_dosage` returns the dosage string

#### Scenario: No PMC entry for PMID
- **WHEN** `_get_pmcid` returns None
- **THEN** `fetch_pmc_dosage` returns None without fetching full text or calling Claude

#### Scenario: PMC full text available but dosage not determinable
- **WHEN** Claude returns the string "null" in response to the dosage extraction prompt
- **THEN** `fetch_pmc_dosage` returns None

#### Scenario: Entrez raises an exception
- **WHEN** `Entrez.elink` raises an exception
- **THEN** `_get_pmcid` returns None and no exception propagates to the caller

---

### Requirement: Review writer — single-topic review file is correctly structured
`write_review_file` SHALL produce a Markdown file with verified findings auto-approved, flagged findings non-approved, and rejected findings non-approved. Each finding SHALL be serialized as a JSON block.

#### Scenario: Mixed verdict findings produce correct approval flags
- **WHEN** `write_review_file` is called with one verified, one flagged, and one rejected finding
- **THEN** the output file contains three JSON blocks; the verified block has `"approved": true`; the flagged and rejected blocks have `"approved": false`

#### Scenario: Empty findings list
- **WHEN** `write_review_file` is called with an empty list
- **THEN** the output file is written without error and contains the "*(none)*" placeholder in all sections

---

### Requirement: Review writer — consolidated (batch) review file groups findings by supplement
`write_consolidated_review_file` SHALL produce a Markdown file with one `## Supplement:` section per topic, verdict sub-sections within each, and a failure note for any failed topics.

#### Scenario: Two supplements produce grouped sections
- **WHEN** `write_consolidated_review_file` is called with findings for two supplements and no failures
- **THEN** the output file contains two `## Supplement:` headings, each with verified/flagged/rejected sub-sections

#### Scenario: Topic produced no findings
- **WHEN** a supplement entry has an empty findings list
- **THEN** its section shows "*(no findings produced)*" rather than being silently omitted

#### Scenario: Failed topic appears in review file
- **WHEN** `failures` contains one entry
- **THEN** the review file includes a `## Supplement: <topic> — FAILED` section with the error text

---

### Requirement: Load findings — review file is parsed correctly
`parse_review_file` SHALL extract only entries with `"approved": true` from all JSON blocks in the Markdown file.

#### Scenario: Mixed approved and non-approved entries
- **WHEN** the review file contains three JSON blocks — one with `approved: true`, two with `approved: false`
- **THEN** `parse_review_file` returns a list containing only the approved entry

#### Scenario: Malformed JSON blocks are skipped
- **WHEN** the review file contains a code block with invalid JSON
- **THEN** `parse_review_file` skips that block and returns only valid approved entries

#### Scenario: No approved entries
- **WHEN** no JSON block has `approved: true`
- **THEN** `parse_review_file` returns an empty list

---

### Requirement: Load findings — supplement and finding upsert behavior
`load_findings` SHALL upsert supplements and findings correctly, enforcing the citation integrity constraint.

#### Scenario: New finding is inserted
- **WHEN** `load_findings` is called with one valid approved entry and the DB has no matching supplement/PMID
- **THEN** the supplement, finding, citation, and symptom rows are inserted via the mock cursor

#### Scenario: Malformed entry (missing PMID) is skipped
- **WHEN** an approved entry has an empty `pmid` field
- **THEN** that entry is skipped and the function continues without error

#### Scenario: Citation integrity enforcement — finding with no citation rolls back
- **WHEN** the citation INSERT does not increase the citation count (simulated via mock returning 0)
- **THEN** `load_findings` raises a `RuntimeError` with a message citing the integrity constraint

#### Scenario: Symptom link is created when suggested_symptom is present
- **WHEN** an approved entry has a non-empty `suggested_symptom`
- **THEN** the symptom upsert and `finding_symptoms` INSERT are executed on the mock cursor

#### Scenario: No approved entries — nothing written to DB
- **WHEN** `load_findings` is called with an empty list
- **THEN** no DB connection is opened and the function returns immediately

---

### Requirement: Pipeline CLI — topic resolution from all three input modes
`_resolve_topics` SHALL correctly collect topics from `--topic`, `--topics`, and `--topics-file`, and SHALL deduplicate.

#### Scenario: Single --topic flag
- **WHEN** `_resolve_topics` is called with args containing only `topic = "NAC endometriosis"`
- **THEN** it returns `["NAC endometriosis"]`

#### Scenario: Multiple --topics flags
- **WHEN** args contain `topics = [["NAC endometriosis"], ["Omega-3 endometriosis"]]`
- **THEN** `_resolve_topics` returns both topics in order

#### Scenario: Topics file is read correctly
- **WHEN** a topics file contains two non-blank, non-comment lines
- **THEN** `_load_topics_file` returns those two lines as a list, skipping blank lines and `#` comments

#### Scenario: Duplicate topics are deduplicated
- **WHEN** the same topic appears via `--topic` and `--topics`
- **THEN** `_resolve_topics` returns it only once

#### Scenario: No topics provided raises ValueError
- **WHEN** all of `--topic`, `--topics`, and `--topics-file` are absent
- **THEN** `_resolve_topics` raises a `ValueError` with a clear message

---

### Requirement: Pipeline CLI — missing API key exits early
`main()` SHALL check for the `ENDO_API_KEY` environment variable before processing any topics and exit with a non-zero code if absent.

#### Scenario: ENDO_API_KEY not set
- **WHEN** `main()` is called with `ENDO_API_KEY` absent from the environment
- **THEN** it prints an error to stderr and calls `sys.exit(1)` before running synthesis

---

### Requirement: Pipeline CLI — per-topic failure is isolated
When one topic raises an exception during `_run_topic`, the pipeline SHALL log the error, record it as a failure, and continue processing remaining topics.

#### Scenario: One topic fails in a batch, others succeed
- **WHEN** `_run_topic` raises an exception for the first topic but succeeds for the second
- **THEN** the second topic's findings are collected and the first topic's error is included in the failures list

---

### Requirement: Slug generation is deterministic and URL-safe
`slug_from_name` SHALL convert supplement or symptom names to lowercase, hyphen-separated, alphanumeric slugs.

#### Scenario: Name with spaces and mixed case
- **WHEN** `slug_from_name("Pelvic Pain")` is called
- **THEN** it returns `"pelvic-pain"`

#### Scenario: Name with special characters
- **WHEN** `slug_from_name("Omega-3 (Fish Oil)")` is called
- **THEN** it returns `"omega-3-fish-oil"`
