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

### Requirement: Verification agent checks each claim against its source
The verification agent SHALL accept the synthesis output and, for each finding, independently fetch the abstract by PMID from PubMed and assess whether the claim is supported by the abstract text. It SHALL output a verdict for each finding: `verified`, `flagged`, or `rejected`, with a reason.

#### Scenario: Claim is well-supported
- **WHEN** the synthesis claim is a reasonable summary of the abstract content
- **THEN** the verification agent marks it `verified`

#### Scenario: Claim overstates the evidence
- **WHEN** the synthesis claim goes beyond what the abstract states (e.g., claims efficacy when paper only reports a trend)
- **THEN** the verification agent marks it `flagged` with an explanation

#### Scenario: PMID does not resolve
- **WHEN** the PMID provided by synthesis does not return a result from PubMed
- **THEN** the verification agent marks it `rejected` with reason "PMID not found"

### Requirement: Operator reviews pipeline output before database load
The pipeline SHALL produce a human-readable review file containing all findings grouped by verdict (`verified`, `flagged`, `rejected`). The operator SHALL approve, edit, or discard each finding before it is loaded into the database.

#### Scenario: Operator approves a verified finding
- **WHEN** the operator marks a finding as approved in the review file
- **THEN** the finding is included in the database load

#### Scenario: Operator discards a flagged finding
- **WHEN** the operator marks a finding as discarded
- **THEN** the finding is excluded from the database load and not persisted

### Requirement: Pipeline is runnable as a local CLI command
The pipeline SHALL be invokable from the command line with one or more topic arguments. It SHALL accept `--topic` (singular, backward-compatible), `--topics` (repeatable), or `--topics-file` (path to newline-separated file). It SHALL run synthesis, then verification for all topics, then produce a single review output — all in a single command.

#### Scenario: End-to-end single-topic run
- **WHEN** the operator runs `python pipeline.py --topic "NAC endometriosis"`
- **THEN** the pipeline completes synthesis, verification, and produces a review file without manual intervention between steps

#### Scenario: End-to-end multi-topic run
- **WHEN** the operator runs `python pipeline.py --topics "NAC endometriosis" --topics "Omega-3 endometriosis"`
- **THEN** the pipeline completes synthesis and verification for both topics and produces a single consolidated review file

### Requirement: Pipeline generates all summary types after findings are loaded
After loading verified findings into the database, the pipeline SHALL run a summarisation stage that generates `supplement_symptom_summaries`, `supplement_summaries`, and `symptom_summaries` in that order. All existing summary rows SHALL be deleted and replaced on every run.

#### Scenario: Summarisation runs after load
- **WHEN** the findings load stage completes
- **THEN** the summarisation stage runs automatically, regenerating all three summary types

#### Scenario: Summarisation is idempotent
- **WHEN** the pipeline is run twice with the same findings
- **THEN** the summary content is equivalent on both runs (deterministic given the same input)
