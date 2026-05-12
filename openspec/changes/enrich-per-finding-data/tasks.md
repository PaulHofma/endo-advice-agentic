## 1. Database Migration

- [ ] 1.1 Write Flyway migration `V6__enrich_findings.sql` adding six nullable columns to `findings`: `dosage TEXT`, `duration TEXT`, `study_type VARCHAR(20)`, `sample_size INT`, `placebo_controlled BOOLEAN`, `safety_notes TEXT`
- [ ] 1.2 Verify migration applies cleanly against the running Docker Postgres instance

## 2. Pipeline — PMC Fallback Module

- [ ] 2.1 Create `pipeline/pmcfetch.py` with a function `fetch_pmc_dosage(pmid: str) -> str | None` that: looks up PMCID for the given PMID via Entrez elink, fetches full-text XML via `efetch(db="pmc")`, and asks Claude to extract the dosage from the Methods section
- [ ] 2.2 Return `None` (not an error) when no PMC version exists or dosage is not found in Methods
- [ ] 2.3 Add a small rate-limit sleep (0.4s) between Entrez calls, consistent with `verification.py`

## 3. Pipeline — Synthesis Extension

- [ ] 3.1 Extend the `RawFinding` dataclass in `synthesis.py` to include: `dosage`, `duration`, `study_type`, `sample_size`, `placebo_controlled`, `safety_notes`
- [ ] 3.2 Update `_build_synthesis_prompt` to instruct Claude to extract all six new fields alongside the existing claim/excerpt/pmid/symptom fields; include null-handling rules (no guessing)
- [ ] 3.3 Update the JSON parsing in `run_synthesis` to read the new fields from Claude's output
- [ ] 3.4 After synthesis, call `pmcfetch.fetch_pmc_dosage(pmid)` for any finding where `dosage` is null; update the finding in place

## 4. Pipeline — Loader Update

- [ ] 4.1 Update `load_findings.py` to write all six new fields to the database when inserting findings

## 5. Backend — Entity and API

- [ ] 5.1 Update the `Finding` JPA entity to add the six new nullable fields with appropriate Kotlin types (`String?`, `Int?`, `Boolean?`)
- [ ] 5.2 Update the Finding DTO / API response to expose the new fields
- [ ] 5.3 Run `./gradlew test` to confirm no regressions

## 6. Frontend — Finding Detail View

- [ ] 6.1 Update the TypeScript Finding type to include the six new nullable fields
- [ ] 6.2 Render dosage and duration in the finding card when non-null
- [ ] 6.3 Render study type and sample size as a compact credibility indicator (e.g., "RCT · n=75") when non-null
- [ ] 6.4 Render safety notes in a visually distinct section when non-null
- [ ] 6.5 Confirm null fields render gracefully (no empty sections or "undefined" text)
