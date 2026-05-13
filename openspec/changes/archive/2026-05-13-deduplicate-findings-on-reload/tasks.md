## 1. Database Migration

- [x] 1.1 Create `V10__idempotent_findings.sql` — add nullable `pmid VARCHAR(20)` column to `findings`
- [x] 1.2 Backfill `findings.pmid` from `citations` (`UPDATE findings f SET pmid = (SELECT pmid FROM citations WHERE finding_id = f.id LIMIT 1)`)
- [x] 1.3 Delete duplicate findings, keeping the highest `id` per `(supplement_id, pmid)` pair
- [x] 1.4 Add `NOT NULL` constraint on `findings.pmid`
- [x] 1.5 Add `UNIQUE (supplement_id, pmid)` constraint on `findings`

## 2. Pipeline Loader

- [x] 2.1 Add `pmid` to the `findings` INSERT column list in `load_findings.py`
- [x] 2.2 Change the `findings` INSERT to `ON CONFLICT (supplement_id, pmid) DO UPDATE SET plain_language_summary = EXCLUDED.plain_language_summary, evidence_snapshot = EXCLUDED.evidence_snapshot, dosage = EXCLUDED.dosage, duration = EXCLUDED.duration, study_type = EXCLUDED.study_type, sample_size = EXCLUDED.sample_size, placebo_controlled = EXCLUDED.placebo_controlled, safety_notes = EXCLUDED.safety_notes`
- [x] 2.3 Verify the upsert returns the stable `finding_id` (use `RETURNING id` — already in place, confirm it works for the update path)

## 3. Verification

- [x] 3.1 Run the migration against the dev DB and confirm no errors
- [x] 3.2 Load a review file twice and confirm `findings` row count does not increase on second load
- [x] 3.3 Load a review file with a modified claim for an existing PMID and confirm the row is updated, not duplicated
- [x] 3.4 Confirm citations and `finding_symptoms` for the upserted finding remain intact after re-load
