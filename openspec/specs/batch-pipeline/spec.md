### Requirement: Pipeline accepts multiple topics in a single invocation
The pipeline CLI SHALL accept multiple research topics via `--topics` (repeatable) or `--topics-file` (path to a newline-separated file). When multiple topics are provided, synthesis and verification SHALL run for each topic in sequence, and all findings SHALL be collected before the review file is written.

#### Scenario: Multiple topics via --topics flag
- **WHEN** the operator runs `python3 pipeline.py --topics "NAC endometriosis" --topics "Vitamin D endometriosis"`
- **THEN** the pipeline runs synthesis and verification for both topics and produces a single consolidated review file containing findings from both

#### Scenario: Topics provided via file
- **WHEN** the operator runs `python3 pipeline.py --topics-file supplements.txt` where `supplements.txt` contains one topic per line
- **THEN** the pipeline processes all non-blank, non-comment lines as topics and produces a single consolidated review file

#### Scenario: Single --topic still works
- **WHEN** the operator runs `python3 pipeline.py --topic "NAC endometriosis"` (singular flag)
- **THEN** the pipeline behaves identically to the previous single-topic behaviour

### Requirement: Consolidated review file groups findings by supplement
When multiple topics are processed, the review file SHALL group findings by supplement, with each supplement's findings presented under a named heading and grouped by verdict within that supplement.

#### Scenario: Two supplements in review file
- **WHEN** the pipeline processes two topics producing findings for NAC and Vitamin D
- **THEN** the review file contains a section for NAC and a section for Vitamin D, each with verified/flagged/rejected sub-sections

#### Scenario: Topic produces no findings
- **WHEN** a topic returns no usable abstracts or all findings are rejected
- **THEN** the review file includes a note for that supplement indicating no findings were produced, rather than silently omitting it

### Requirement: Per-topic failure is isolated
If synthesis or verification fails for one topic in a batch run, the pipeline SHALL log the error, skip that topic, and continue processing remaining topics. The review file SHALL include a failure note for the skipped topic.

#### Scenario: One topic fails, others succeed
- **WHEN** synthesis raises an exception for one topic in a batch of three
- **THEN** the pipeline logs the error, continues with the remaining two topics, and notes the failure in the review file
