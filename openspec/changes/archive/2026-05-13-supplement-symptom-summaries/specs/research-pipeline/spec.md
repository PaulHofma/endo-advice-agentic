## MODIFIED Requirements

### Requirement: Pipeline is runnable as a local CLI command
The pipeline SHALL be invokable from the command line with a topic argument. It SHALL run synthesis, then verification, then produce the review output, then load approved findings, then generate all summary types — all in a single command.

#### Scenario: End-to-end pipeline run
- **WHEN** the operator runs `python pipeline.py --topic "NAC endometriosis"`
- **THEN** the pipeline completes synthesis, verification, review output, findings load, and summary generation without manual intervention between steps

## ADDED Requirements

### Requirement: Pipeline generates all summary types after findings are loaded
After loading verified findings into the database, the pipeline SHALL run a summarisation stage that generates `supplement_symptom_summaries`, `supplement_summaries`, and `symptom_summaries` in that order. All existing summary rows SHALL be deleted and replaced on every run.

#### Scenario: Summarisation runs after load
- **WHEN** the findings load stage completes
- **THEN** the summarisation stage runs automatically, regenerating all three summary types

#### Scenario: Summarisation is idempotent
- **WHEN** the pipeline is run twice with the same findings
- **THEN** the summary content is equivalent on both runs (deterministic given the same input)
