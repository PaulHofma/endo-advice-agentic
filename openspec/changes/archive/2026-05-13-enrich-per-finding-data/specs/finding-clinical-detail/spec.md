## ADDED Requirements

### Requirement: Finding carries structured dosage information
Each finding SHALL store a `dosage` field containing the dose used in the studied intervention (e.g., "2g EPA + 1g DHA daily"). The field SHALL be null when dosage is not recoverable from the abstract or PMC full text.

#### Scenario: Dosage present in abstract
- **WHEN** the synthesis agent processes an abstract that states the intervention dose
- **THEN** the finding is stored with a non-null `dosage` value reflecting the stated dose

#### Scenario: Dosage absent from abstract but present in PMC full text
- **WHEN** the abstract does not mention dosage but an open-access PMC version exists
- **THEN** the pipeline fetches the PMC full text, extracts dosage from the Methods section, and stores it as the finding's `dosage`

#### Scenario: Dosage not recoverable
- **WHEN** the abstract does not mention dosage and no PMC full text is available
- **THEN** the finding is stored with `dosage` null; the frontend SHALL render this as "not reported"

### Requirement: Finding carries intervention duration
Each finding SHALL store a `duration` field describing the length of the studied intervention (e.g., "3 months"). The field SHALL be null when duration is not reported in the abstract.

#### Scenario: Duration present in abstract
- **WHEN** the abstract states the duration of the intervention
- **THEN** the finding is stored with a non-null `duration` value

#### Scenario: Duration not reported
- **WHEN** the abstract does not state intervention duration
- **THEN** the finding is stored with `duration` null

### Requirement: Finding carries study type classification
Each finding SHALL store a `study_type` field with one of the values: `rct`, `observational`, `meta_analysis`, `case_report`, `review`, or null. The field SHALL be null when the study design is ambiguous or not determinable from the abstract.

#### Scenario: RCT clearly identified
- **WHEN** the abstract uses language indicating a randomised controlled trial (e.g., "randomized", "double-blind", "placebo-controlled")
- **THEN** the finding is stored with `study_type = 'rct'`

#### Scenario: Study design ambiguous
- **WHEN** the abstract does not clearly indicate the study design
- **THEN** the finding is stored with `study_type` null; the pipeline SHALL NOT guess

### Requirement: Finding carries sample size
Each finding SHALL store a `sample_size` integer representing the number of participants in the study. The field SHALL be null when sample size is not reported in the abstract.

#### Scenario: Sample size reported
- **WHEN** the abstract reports the number of participants (e.g., "n=75", "75 women")
- **THEN** the finding is stored with the corresponding integer value

#### Scenario: Sample size not reported
- **WHEN** the abstract does not report participant count
- **THEN** the finding is stored with `sample_size` null

### Requirement: Finding carries placebo-controlled flag
Each finding SHALL store a nullable boolean `placebo_controlled` indicating whether the study used a placebo control. The field SHALL be null when this cannot be determined from the abstract.

#### Scenario: Placebo control confirmed
- **WHEN** the abstract explicitly states that a placebo was used
- **THEN** the finding is stored with `placebo_controlled = true`

#### Scenario: No placebo or ambiguous
- **WHEN** no placebo is mentioned or it cannot be determined
- **THEN** the finding is stored with `placebo_controlled` null or false as appropriate

### Requirement: Finding carries safety notes
Each finding SHALL store a nullable `safety_notes` text field containing any adverse effects, contraindications, or safety signals mentioned in the abstract. The field SHALL be null when the abstract mentions no safety-relevant information.

#### Scenario: Safety signal present
- **WHEN** the abstract mentions adverse effects, contraindications, or drug interactions
- **THEN** the finding stores a concise plain-language summary of those signals in `safety_notes`

#### Scenario: No safety information
- **WHEN** the abstract does not mention safety-relevant information
- **THEN** the finding is stored with `safety_notes` null; the frontend SHALL NOT render a safety section
