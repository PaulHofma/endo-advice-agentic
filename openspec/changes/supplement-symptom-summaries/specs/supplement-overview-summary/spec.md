## ADDED Requirements

### Requirement: Pipeline generates an overview summary for each supplement
After generating supplement×symptom summaries, the pipeline SHALL generate one `supplement_summary` row per supplement. The summary SHALL synthesise across all supplement×symptom summaries for that supplement, giving readers an at-a-glance view of the overall evidence picture.

#### Scenario: Supplement with multiple symptom summaries
- **WHEN** a supplement has supplement×symptom summaries for three symptoms
- **THEN** the supplement summary synthesises across all three, highlighting where evidence is strongest and where it is limited

#### Scenario: Supplement with no verified findings
- **WHEN** a supplement has no verified findings (and therefore no supplement×symptom summaries)
- **THEN** the pipeline still generates a supplement summary explicitly stating that no evidence was found in current research for this supplement

#### Scenario: Summary is regenerated on every pipeline run
- **WHEN** the pipeline runs
- **THEN** all existing `supplement_summaries` rows are deleted and regenerated from current supplement×symptom summaries

### Requirement: Supplement overview summary is displayed at the top of the supplement detail page
The supplement overview summary SHALL be rendered at the top of the supplement detail page, before any symptom sections or individual findings.

#### Scenario: User lands on supplement page
- **WHEN** a user navigates to a supplement's detail page
- **THEN** the first content they see is the supplement overview summary
