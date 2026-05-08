## MODIFIED Requirements

### Requirement: README documents the operator pipeline workflow
The README SHALL describe how to run the Python pipeline, review the output, and load approved findings into the database. Setup instructions SHALL reference `GEMINI_API_KEY` (not `ANTHROPIC_API_KEY`) as the required environment variable.

#### Scenario: Operator runs the pipeline
- **WHEN** the operator reads the pipeline section of the README
- **THEN** they can find the exact commands to run synthesis, review the output file, and load approved findings, and they see `GEMINI_API_KEY` as the required API key env var
