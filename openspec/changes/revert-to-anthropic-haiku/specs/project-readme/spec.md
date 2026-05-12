## MODIFIED Requirements

### Requirement: README documents the operator pipeline workflow
The README SHALL describe how to run the Python pipeline, review the output, and load approved findings into the database. Setup instructions SHALL reference `ANTHROPIC_API_KEY` (not `GEMINI_API_KEY`).

#### Scenario: Operator runs the pipeline
- **WHEN** the operator reads the pipeline section of the README
- **THEN** they can find the exact commands to run synthesis, review the output file, and load approved findings

#### Scenario: Operator sets up API credentials
- **WHEN** the operator follows setup instructions
- **THEN** the README instructs them to set `ANTHROPIC_API_KEY`, not `GEMINI_API_KEY`
