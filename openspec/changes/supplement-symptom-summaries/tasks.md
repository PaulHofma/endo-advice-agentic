## 1. Database Migrations

- [x] 1.1 Write `V7__create_supplement_symptom_summaries.sql`: table with `supplement_id`, `symptom_id` (composite PK), `content TEXT NOT NULL`, `evidence_strength VARCHAR(20)`, `generated_at TIMESTAMPTZ`
- [x] 1.2 Write `V8__create_supplement_summaries.sql`: table with `supplement_id` (PK), `content TEXT NOT NULL`, `generated_at TIMESTAMPTZ`
- [x] 1.3 Write `V9__create_symptom_summaries.sql`: table with `symptom_id` (PK), `content TEXT NOT NULL`, `generated_at TIMESTAMPTZ`
- [x] 1.4 Verify all three migrations apply cleanly against the running Docker Postgres instance

## 2. Pipeline — Summarisation Module

- [x] 2.1 Create `pipeline/summarise.py` with a `run(supplement_ids: list[int] | None = None)` entry point that orchestrates all three summary generation stages
- [x] 2.2 Implement `generate_supplement_symptom_summaries()`: query all supplement×symptom pairs with findings, call Claude once per pair to synthesise findings and determine `evidence_strength`, upsert results
- [x] 2.3 Implement `generate_supplement_summaries()`: for each supplement, query its pair summaries (or note absence), call Claude to produce the overview (including the zero-evidence case), upsert result
- [x] 2.4 Implement `generate_symptom_summaries()`: for each symptom with at least one pair summary, call Claude to produce the overview, upsert result
- [x] 2.5 Each stage begins with `DELETE FROM <table>` to ensure full-replace semantics
- [x] 2.6 Add rate-limit sleep (0.4s) between Claude calls, consistent with existing pipeline modules

## 3. Pipeline — Orchestration

- [x] 3.1 Update `pipeline.py` to call `summarise.run()` as the final stage after `load_findings.py` completes
- [x] 3.2 Ensure the summary stage is included in the review output so the operator can spot obviously wrong synthesis

## 4. Backend — Entities and Repositories

- [x] 4.1 Add `SupplementSymptomSummary` JPA entity with composite key `(supplementId, symptomId)`
- [x] 4.2 Add `SupplementSummary` JPA entity keyed on `supplementId`
- [x] 4.3 Add `SymptomSummary` JPA entity keyed on `symptomId`
- [x] 4.4 Add Spring Data repositories for all three entities

## 5. Backend — API Endpoints

- [x] 5.1 Expose `supplement_symptom_summary` on the existing supplement detail endpoint (nested under each symptom section in the response)
- [x] 5.2 Expose `supplement_summary` on the supplement detail endpoint (top-level field)
- [x] 5.3 Expose `symptom_summary` on the symptom detail endpoint (top-level field)
- [x] 5.4 Expose `supplement_symptom_summary` on the symptom detail endpoint (nested under each supplement section)
- [x] 5.5 Run `./gradlew test` to confirm no regressions

## 6. Frontend — Supplement Page

- [x] 6.1 Update TypeScript types to include `supplementSummary` and `supplementSymptomSummary` fields
- [x] 6.2 Render `supplementSummary` at the top of the supplement detail page, before symptom sections
- [x] 6.3 Render `supplementSymptomSummary` at the top of each symptom section, above individual findings
- [x] 6.4 Display `evidence_strength` as a visual badge (e.g., coloured pill) alongside the pair summary

## 7. Frontend — Symptom Page

- [x] 7.1 Update TypeScript types to include `symptomSummary` and `supplementSymptomSummary` on symptom responses
- [x] 7.2 Render `symptomSummary` at the top of the symptom page, before supplement sections
- [x] 7.3 Render `supplementSymptomSummary` at the top of each supplement section on the symptom page
- [x] 7.4 Confirm null-safe rendering when summaries are absent (pipeline not yet run)
