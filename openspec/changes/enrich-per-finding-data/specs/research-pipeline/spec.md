## MODIFIED Requirements

### Requirement: Synthesis agent queries PubMed for relevant studies
The synthesis agent SHALL accept a search topic (e.g., supplement name + condition) and query the PubMed Entrez API to retrieve relevant abstracts. It SHALL produce structured output containing: claim text, supporting excerpt from the abstract, PMID, a suggested symptom tag, and the following clinical/methodological fields: `dosage`, `duration`, `study_type`, `sample_size`, `placebo_controlled`, `safety_notes`. All clinical fields SHALL be null when not determinable from the abstract.

#### Scenario: Successful synthesis run
- **WHEN** the operator runs the synthesis agent with a topic (e.g., "NAC endometriosis")
- **THEN** the agent returns one or more structured findings, each containing a claim, a quoted excerpt, a valid-format PMID, and best-effort values for all clinical/methodological fields

#### Scenario: No relevant studies found
- **WHEN** the agent finds no relevant abstracts for the given topic
- **THEN** the agent returns an empty result set with a clear message, not an error

#### Scenario: Clinical fields not present in abstract
- **WHEN** the abstract does not report dosage, duration, or other clinical details
- **THEN** the synthesis agent stores null for those fields; it SHALL NOT fabricate values

## ADDED Requirements

### Requirement: Pipeline attempts PMC full-text fallback for missing dosage
After synthesis, if a finding has a null `dosage`, the pipeline SHALL attempt to retrieve the open-access PMC full text for that PMID via Entrez. If found, it SHALL ask Claude to extract the dosage from the Methods section. If PMC full text is unavailable or dosage is still not determinable, `dosage` remains null.

#### Scenario: PMC full text available and dosage found
- **WHEN** a finding has null dosage and an open-access PMC version exists for its PMID
- **THEN** the pipeline fetches the full text, extracts the dosage, and updates the finding's `dosage` field before database load

#### Scenario: PMC full text unavailable
- **WHEN** a finding has null dosage and no PMC version exists for its PMID
- **THEN** the pipeline leaves `dosage` null and proceeds without error

#### Scenario: PMC full text available but dosage not in Methods
- **WHEN** the PMC full text is retrieved but the Methods section does not state a specific dosage
- **THEN** `dosage` remains null; the pipeline SHALL NOT guess or infer a value
