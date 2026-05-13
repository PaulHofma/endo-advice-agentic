## Context

The pipeline loads approved findings from a review file into PostgreSQL via `load_findings.py`. Currently `findings` has no uniqueness constraint — each run does a plain `INSERT`, producing a new row even when the same PMID + supplement was loaded before. PMID only lives on `citations`, not on `findings`, so there is no DB-level anchor to deduplicate against.

## Goals / Non-Goals

**Goals:**
- Make finding loads idempotent: re-running the same review file produces exactly one finding per `(supplement_id, pmid)` pair, with the latest extracted data.
- Allow pipeline improvements to refresh existing findings automatically on re-run.
- Preserve stable `finding_id` values so citations and `finding_symptoms` remain correct.

**Non-Goals:**
- Deduplicating findings that differ by PMID but cover similar claims (not a data quality problem we're solving here).
- Purging orphaned findings from historical runs (a separate cleanup concern).
- Changing the review/approval workflow.

## Decisions

### 1. Unique key: `(supplement_id, pmid)`

The combination of supplement + paper is the natural identity of a finding. A given paper can only support one finding per supplement in our model (symptoms are linked via `finding_symptoms`, not on the finding itself).

**Alternative considered**: hash of `plain_language_summary` — rejected because LLM output is non-deterministic; the same paper on two runs would produce different hashes and still duplicate.

### 2. Add `pmid` column to `findings`

Currently PMID only lives on `citations`. To enforce the unique constraint at the `findings` level, we need PMID on the finding row itself. This also makes the finding self-describing without a join.

**Migration strategy**: add column as nullable first, backfill from `citations`, then add NOT NULL + unique constraint. If duplicate `(supplement_id, pmid)` rows already exist, the migration must deduplicate (keep the most recent by `id`) before adding the constraint.

### 3. `ON CONFLICT (supplement_id, pmid) DO UPDATE SET ...`

On conflict, overwrite all pipeline-derived columns: `plain_language_summary`, `evidence_snapshot`, `dosage`, `duration`, `study_type`, `sample_size`, `placebo_controlled`, `safety_notes`. Leave `id` and `created_at` untouched.

**Alternative considered**: `DO NOTHING` — rejected because it silently preserves stale data when the pipeline improves. Operators re-run precisely to get fresher extractions.

### 4. Citations and `finding_symptoms` stay `ON CONFLICT DO NOTHING`

With stable finding IDs, these are already correct. A re-run re-inserts the same citation for the same `(finding_id, pmid)` — the existing constraint handles it cleanly.

## Risks / Trade-offs

- **Existing duplicates block migration** → Mitigation: migration deduplicates `(supplement_id, pmid)` pairs before adding constraint, keeping the highest `id` (most recent load).
- **PMID backfill assumes 1 citation per finding** → Mitigation: current pipeline always inserts exactly one citation per finding; the backfill picks `MIN(pmid)` per `finding_id` as a safe default. Any finding with no citation is already a data integrity violation (enforced by `load_findings.py`).
- **Upsert silently drops symptom re-links on conflict** → Non-issue: `finding_symptoms` INSERT runs after the upsert returns the stable ID; `ON CONFLICT DO NOTHING` on that table means existing links are preserved and new ones added.

## Migration Plan

1. Add Flyway migration (V10):
   - Add `pmid VARCHAR(20)` nullable to `findings`.
   - Backfill from `citations` (`UPDATE findings f SET pmid = (SELECT pmid FROM citations WHERE finding_id = f.id LIMIT 1)`).
   - Delete duplicate findings, keeping the highest `id` per `(supplement_id, pmid)`.
   - Add `NOT NULL` constraint on `findings.pmid`.
   - Add `UNIQUE (supplement_id, pmid)` constraint.

2. Update `load_findings.py`:
   - Pass `pmid` into the `findings` INSERT.
   - Change to `ON CONFLICT (supplement_id, pmid) DO UPDATE SET ...`.

**Rollback**: Drop the unique constraint and `pmid` column (V11 rollback migration). The loader reverts to plain INSERT on the previous deploy.
