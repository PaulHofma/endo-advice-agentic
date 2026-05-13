## ADDED Requirements

### Requirement: Synthesis agent queries PubMed for relevant studies
The synthesis agent SHALL accept a search topic (e.g., supplement name + condition) and query the PubMed Entrez API to retrieve relevant abstracts. It SHALL produce structured output containing: claim text, supporting excerpt from the abstract, PMID, and a suggested symptom tag.

#### Scenario: Successful synthesis run
- **WHEN** the operator runs the synthesis agent with a topic (e.g., "NAC endometriosis")
- **THEN** the agent returns one or more structured findings, each containing a claim, a quoted excerpt, and a valid-format PMID

#### Scenario: No relevant studies found
- **WHEN** the agent finds no relevant abstracts for the given topic
- **THEN** the agent returns an empty result set with a clear message, not an error

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
The pipeline SHALL be invokable from the command line with a topic argument. It SHALL run synthesis, then verification, then produce the review output — all in a single command.

#### Scenario: End-to-end pipeline run
- **WHEN** the operator runs `python pipeline.py --topic "NAC endometriosis"`
- **THEN** the pipeline completes synthesis, verification, and produces a review file without manual intervention between steps
