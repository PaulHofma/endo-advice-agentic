## MODIFIED Requirements

### Requirement: Users can browse supplements by symptom
The system SHALL expose a list of symptoms that have at least one associated finding. Selecting a symptom SHALL show a symptom overview summary followed by all supplements with findings related to that symptom, each supplement section led by its supplement×symptom summary.

#### Scenario: User browses by symptom
- **WHEN** a user selects a symptom (e.g., "dysmenorrhea")
- **THEN** they see the symptom overview summary first, then a list of supplements with findings for that symptom, each with its supplement×symptom summary and individual findings below

#### Scenario: Symptom with no findings
- **WHEN** a symptom exists in the database but has no approved findings linked to it
- **THEN** it SHALL NOT appear in the symptom navigation list
