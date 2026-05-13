## MODIFIED Requirements

### Requirement: Pipeline is runnable as a local CLI command
The pipeline SHALL be invokable from the command line with one or more topic arguments. It SHALL accept `--topic` (singular, backward-compatible), `--topics` (repeatable), or `--topics-file` (path to newline-separated file). It SHALL run synthesis, then verification for all topics, then produce a single review output — all in a single command.

#### Scenario: End-to-end single-topic run
- **WHEN** the operator runs `python pipeline.py --topic "NAC endometriosis"`
- **THEN** the pipeline completes synthesis, verification, and produces a review file without manual intervention between steps

#### Scenario: End-to-end multi-topic run
- **WHEN** the operator runs `python pipeline.py --topics "NAC endometriosis" --topics "Omega-3 endometriosis"`
- **THEN** the pipeline completes synthesis and verification for both topics and produces a single consolidated review file
