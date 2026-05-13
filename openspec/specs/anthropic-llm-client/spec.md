# anthropic-llm-client Specification

## Purpose
Documents the LLM provider configuration for the research pipeline. The pipeline uses the Anthropic SDK with Claude Haiku for all synthesis and verification inference.

## Requirements

### Requirement: Pipeline uses the Anthropic SDK for LLM inference
The pipeline SHALL use the `anthropic` SDK (configured with `ANTHROPIC_API_KEY`) for all LLM calls.

#### Scenario: Synthesis module calls Claude
- **WHEN** `run_synthesis` is invoked
- **THEN** it initialises an Anthropic client and calls the Claude API with the synthesis prompt

#### Scenario: Verification module calls Claude
- **WHEN** the verification step is invoked
- **THEN** it initialises an Anthropic client and calls the Claude API with the verification prompt

#### Scenario: Missing API key
- **WHEN** `ANTHROPIC_API_KEY` is not set in the environment
- **THEN** the pipeline exits early with a clear error message before making any API calls

### Requirement: Claude model is configurable via a named constant
The pipeline SHALL define the Claude model name as a module-level constant (e.g. `CLAUDE_MODEL = "claude-haiku-4-5"`) so it can be changed in one place.

#### Scenario: Model constant used in API calls
- **WHEN** a Claude API call is made in synthesis or verification
- **THEN** the model name is read from the `CLAUDE_MODEL` constant, not hardcoded inline
