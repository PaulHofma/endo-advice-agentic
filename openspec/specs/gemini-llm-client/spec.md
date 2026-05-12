# gemini-llm-client Specification

## Purpose
TBD - created by archiving change switch-to-gemini-api. Update Purpose after archive.
## Requirements
### Requirement: Pipeline uses Gemini for LLM inference
The pipeline SHALL use the `google-generativeai` SDK (configured with `GEMINI_API_KEY`) for all LLM calls, replacing the Anthropic SDK.

#### Scenario: Synthesis module calls Gemini
- **WHEN** `run_synthesis` is invoked
- **THEN** it initialises a Gemini client using `os.environ["GEMINI_API_KEY"]` and calls `generate_content` with the synthesis prompt

#### Scenario: Verification module calls Gemini
- **WHEN** the verification step is invoked
- **THEN** it initialises a Gemini client using `os.environ["GEMINI_API_KEY"]` and calls `generate_content` with the verification prompt

#### Scenario: Missing API key
- **WHEN** `GEMINI_API_KEY` is not set in the environment
- **THEN** the pipeline exits early with a clear error message before making any API calls

### Requirement: Gemini model is configurable via a named constant
The pipeline SHALL define the Gemini model name as a module-level constant (e.g. `GEMINI_MODEL = "gemini-2.0-flash"`) so it can be changed in one place.

#### Scenario: Model constant used in API calls
- **WHEN** a Gemini API call is made in synthesis or verification
- **THEN** the model name is read from the `GEMINI_MODEL` constant, not hardcoded inline

