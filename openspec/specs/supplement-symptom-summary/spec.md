### Requirement: Pipeline generates a summary for each supplement×symptom pair with findings
After findings are loaded, the pipeline SHALL generate one `supplement_symptom_summary` row for every (supplement, symptom) pair that has at least one verified finding. Each summary SHALL contain a plain-language synthesis of all findings for that pair and a structured `evidence_strength` value.

#### Scenario: Pair with multiple findings
- **WHEN** a supplement has three verified findings for a given symptom
- **THEN** the pipeline generates one summary synthesising across all three, noting dosage range, study types, and consistency of results

#### Scenario: Pair with a single finding
- **WHEN** a supplement has exactly one verified finding for a given symptom
- **THEN** the pipeline generates a summary accurately reflecting the limited evidence base (e.g., "one small observational study")

#### Scenario: Pair with no findings
- **WHEN** a supplement has no verified findings for a given symptom
- **THEN** no `supplement_symptom_summary` row is created for that pair

### Requirement: Evidence strength is rated for each supplement×symptom pair
Each `supplement_symptom_summary` SHALL include an `evidence_strength` field with one of four values: `strong`, `moderate`, `preliminary`, or `conflicting`. The pipeline SHALL derive this from the number of studies, their types (RCT vs observational), and whether results are consistent.

#### Scenario: Multiple RCTs with consistent results
- **WHEN** two or more RCTs report consistent findings for the same supplement×symptom pair
- **THEN** `evidence_strength` is set to `strong` or `moderate`

#### Scenario: Single observational study
- **WHEN** only one observational study exists for the pair
- **THEN** `evidence_strength` is set to `preliminary`

#### Scenario: Studies with contradictory results
- **WHEN** findings for the same pair report contradictory outcomes
- **THEN** `evidence_strength` is set to `conflicting`

### Requirement: Supplement×symptom summary is regenerated on every pipeline run
The pipeline SHALL DELETE all existing `supplement_symptom_summaries` rows and regenerate them from current findings on every run.

#### Scenario: New finding added for an existing pair
- **WHEN** the pipeline runs and a new verified finding exists for a supplement×symptom pair
- **THEN** the summary for that pair is regenerated to reflect the updated evidence

### Requirement: Supplement×symptom summary appears on both supplement and symptom pages
The same `supplement_symptom_summary` content SHALL be rendered on the supplement detail page (grouped under the relevant symptom section) and on the symptom page (grouped under the relevant supplement section).

#### Scenario: Rendered on supplement page
- **WHEN** a user views a supplement's detail page
- **THEN** each symptom section shows the supplement×symptom summary above the individual findings

#### Scenario: Rendered on symptom page
- **WHEN** a user views a symptom page
- **THEN** each supplement section shows the supplement×symptom summary above the individual findings
