### Requirement: Users can browse supplements by symptom
The system SHALL expose a list of symptoms that have at least one associated finding. Selecting a symptom SHALL show a symptom overview summary followed by all supplements with findings related to that symptom, each supplement section led by its supplement×symptom summary.

#### Scenario: User browses by symptom
- **WHEN** a user selects a symptom (e.g., "dysmenorrhea")
- **THEN** they see the symptom overview summary first, then a list of supplements with findings for that symptom, each with its supplement×symptom summary and individual findings below

#### Scenario: Symptom with no findings
- **WHEN** a symptom exists in the database but has no approved findings linked to it
- **THEN** it SHALL NOT appear in the symptom navigation list

### Requirement: Each finding is tagged with the symptom it addresses
Every finding in the database SHALL be associated with at least one symptom. The association SHALL be set during the pipeline review stage and stored as a many-to-many relationship.

#### Scenario: Finding with multiple symptoms
- **WHEN** a finding addresses more than one symptom (e.g., both pain and fatigue)
- **THEN** it SHALL appear under each relevant symptom in the navigation

#### Scenario: Finding appears in both supplement and symptom views
- **WHEN** a finding exists for supplement "Vitamin D" and symptom "fatigue"
- **THEN** it is visible both on the Vitamin D supplement page and on the fatigue symptom page
