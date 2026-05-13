## Why

Individual findings give readers raw research results but no synthesised picture — a user browsing Omega-3 for dysmenorrhea must read through several paper-level findings to understand the overall weight of evidence. Adding AI-generated summary layers (per supplement×symptom, per supplement, per symptom) gives readers an immediate, honest overview and enables the symptom-first navigation the product needs.

## What Changes

- New `supplement_symptom_summaries` table: one row per supplement×symptom pair, containing a plain-language synthesis of all findings for that pair and an `evidence_strength` rating (`strong`, `moderate`, `preliminary`, `conflicting`)
- New `supplement_summaries` table: one row per supplement, synthesising across all its supplement×symptom summaries; explicitly handles the "no evidence found" case
- New `symptom_summaries` table: one row per symptom, synthesising across all supplement×symptom summaries for that symptom; powers symptom-first navigation
- New pipeline stage that runs after findings are loaded and generates all three summary types; all are full-replace (DELETE + INSERT) on every run
- Backend and frontend updated to serve and render all three summary types

## Capabilities

### New Capabilities
- `supplement-symptom-summary`: Per supplement×symptom AI-generated synthesis with evidence strength rating; serves as the shared building block for both supplement and symptom pages
- `supplement-overview-summary`: Per-supplement summary across all symptoms, handling the zero-evidence case
- `symptom-overview-summary`: Per-symptom summary across all supplements, enabling symptom-first navigation

### Modified Capabilities
- `research-pipeline`: A new summarisation stage is added after the findings load step, generating all three summary types per pipeline run
- `supplement-catalog`: Supplement pages now render a top-level supplement summary and per-symptom summaries above individual findings
- `symptom-navigation`: Symptom pages now render a symptom-level summary and per-supplement summaries, enabling meaningful symptom-first browsing

## Impact

- **Database**: Three new Flyway migrations (one per summary table)
- **Pipeline**: New `summarise.py` module with three generation functions; `pipeline.py` updated to call it after `load_findings.py`
- **Backend**: Three new JPA entities, repositories, and REST endpoints
- **Frontend**: Supplement page redesigned to show summary hierarchy; symptom page extended with summary content
- **Dependencies**: None new
