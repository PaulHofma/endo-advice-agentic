## Why

Research findings currently capture only a plain-language claim and an abstract excerpt, leaving readers with no way to assess how a supplement was used (dosage, duration) or how much to trust the evidence (study type, sample size). Adding structured clinical and methodological fields to each finding makes the information genuinely actionable for people who cannot interpret raw papers.

## What Changes

- Add six structured fields to the `findings` table: `dosage`, `duration`, `study_type`, `sample_size`, `placebo_controlled`, `safety_notes`
- Extend the synthesis prompt to extract these fields from the abstract where present
- Add a PMC full-text fallback for `dosage`: when the abstract does not report a dosage, attempt to retrieve the open-access full text via Entrez and extract from the Methods section
- All fields are nullable — missing data is stored as `null` and rendered honestly to the reader

## Capabilities

### New Capabilities
- `finding-clinical-detail`: Each finding carries structured clinical metadata — dosage, duration, study type, sample size, placebo flag, and safety notes — sourced from the abstract or PMC full text, with null representing genuinely absent data.

### Modified Capabilities
- `research-pipeline`: The synthesis stage extracts additional structured fields; a new PMC fallback module is added for dosage recovery.

## Impact

- **Database**: New Flyway migration adds six nullable columns to `findings`
- **Pipeline**: `synthesis.py` prompt extended; new `pmcfetch.py` module; `load_findings.py` updated to write new fields
- **Backend**: `Finding` JPA entity and API response updated to expose new fields
- **Frontend**: Finding detail view updated to render dosage, duration, study quality, and safety notes
- **Dependencies**: No new external dependencies (BioPython Entrez already in use)
