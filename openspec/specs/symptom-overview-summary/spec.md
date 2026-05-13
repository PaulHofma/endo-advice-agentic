### Requirement: Pipeline generates an overview summary for each symptom
After generating supplement×symptom summaries, the pipeline SHALL generate one `symptom_summary` row per symptom that has at least one supplement×symptom summary. The symptom summary SHALL synthesise across all supplement×symptom summaries for that symptom, helping users understand which supplements have the strongest evidence for their specific symptom.

#### Scenario: Symptom with multiple supplement summaries
- **WHEN** a symptom has supplement×symptom summaries for three different supplements
- **THEN** the symptom summary synthesises across all three, highlighting which supplements have the most evidence and which are preliminary

#### Scenario: Summary is regenerated on every pipeline run
- **WHEN** the pipeline runs
- **THEN** all existing `symptom_summaries` rows are deleted and regenerated from current supplement×symptom summaries

### Requirement: Symptom overview summary is displayed at the top of the symptom page
The symptom overview summary SHALL be rendered at the top of the symptom detail page, before the per-supplement sections.

#### Scenario: User navigates to a symptom page
- **WHEN** a user selects a symptom from the symptom navigation
- **THEN** the first content they see is the symptom overview summary, orienting them to the overall supplement evidence landscape for that symptom
