## ADDED Requirements

### Requirement: Finding loads are idempotent on supplement + PMID
The system SHALL treat `(supplement_id, pmid)` as the unique identity of a finding. Loading a finding whose supplement + PMID already exists in the database SHALL update the existing row rather than inserting a new one.

#### Scenario: Re-loading the same review file
- **WHEN** a review file is loaded a second time without changes
- **THEN** no new `findings` rows are created and row counts remain the same

#### Scenario: Re-loading with improved extraction
- **WHEN** a review file is loaded after the pipeline has produced an improved claim or clinical detail for an existing PMID + supplement
- **THEN** the existing finding row is updated with the new values and no duplicate row is created

### Requirement: Upsert preserves finding identity
On conflict, the system SHALL retain the original `id` and `created_at` of the finding. Only pipeline-derived columns (`plain_language_summary`, `evidence_snapshot`, `dosage`, `duration`, `study_type`, `sample_size`, `placebo_controlled`, `safety_notes`) SHALL be overwritten.

#### Scenario: Finding ID is stable across re-runs
- **WHEN** a finding is loaded, then the same supplement + PMID is loaded again
- **THEN** the finding's `id` is unchanged
- **THEN** citations and `finding_symptoms` linked to that `id` remain intact

### Requirement: `findings` table stores PMID
Each finding row SHALL include the PMID of its primary supporting paper. This column SHALL be NOT NULL and SHALL participate in the `UNIQUE (supplement_id, pmid)` constraint.

#### Scenario: Finding is inserted with PMID
- **WHEN** a finding is loaded from a review entry
- **THEN** the `findings.pmid` column contains the PMID from that entry

### Requirement: Symptom links survive re-load
Re-loading a finding SHALL NOT remove existing `finding_symptoms` links. New symptom links from the re-load SHALL be added; existing ones SHALL be preserved.

#### Scenario: Symptom link preserved on re-run
- **WHEN** a finding already linked to a symptom is re-loaded with the same symptom
- **THEN** the `finding_symptoms` row is unchanged (not duplicated, not deleted)
