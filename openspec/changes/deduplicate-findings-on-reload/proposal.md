## Why

Re-running the pipeline against the same supplement produces duplicate `findings` rows because there is no uniqueness constraint on `(supplement_id, pmid)`. Since the pipeline is LLM-driven, re-runs are expected — both to fix extraction quality and to refresh stale data — so duplicates accumulate silently across runs.

## What Changes

- Add a unique constraint on `findings(supplement_id, pmid)` so the same paper cannot produce two rows for the same supplement.
- Change the `findings` INSERT in `load_findings.py` to `ON CONFLICT (supplement_id, pmid) DO UPDATE SET ...` for all volatile columns (`plain_language_summary`, `evidence_snapshot`, `dosage`, `duration`, `study_type`, `sample_size`, `placebo_controlled`, `safety_notes`).
- Keep `citations` and `finding_symptoms` INSERTs as `ON CONFLICT DO NOTHING` — they are already correct once tied to the stable finding ID.
- Add a `pmid` column to `findings` to support the unique constraint (currently PMID only lives on `citations`).

## Capabilities

### New Capabilities

- `idempotent-finding-load`: The pipeline loader can be re-run any number of times against the same or overlapping review files without producing duplicate findings; re-runs update existing findings with the latest extracted data.

### Modified Capabilities

- `citation-integrity`: Citation uniqueness is still `(finding_id, pmid)`, but now finding IDs are stable across re-runs, so the constraint behaves correctly on repeat loads.

## Impact

- **Database**: New Flyway migration — adds `pmid` column to `findings`, adds `UNIQUE (supplement_id, pmid)` constraint.
- **Pipeline**: `load_findings.py` — the findings INSERT becomes an upsert.
- **Backend/API**: Read-only; no changes needed.
- **Existing data**: If duplicates already exist in the DB, the migration will need to deduplicate before adding the constraint.
