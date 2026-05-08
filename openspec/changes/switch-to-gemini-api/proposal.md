## Why

The pipeline currently depends on the Anthropic SDK and `ANTHROPIC_API_KEY` for all LLM calls. Switching to Google Gemini allows use of a Gemini API key instead, replacing the Anthropic dependency with the `google-generativeai` SDK.

## What Changes

- Remove the `anthropic` Python package dependency; add `google-generativeai`
- Replace `anthropic.Anthropic` client instantiation in `synthesis.py` and `verification.py` with the Gemini client
- Replace the `claude-opus-4-5` model constant with an equivalent Gemini model (e.g. `gemini-2.0-flash`)
- Replace `ANTHROPIC_API_KEY` environment variable with `GEMINI_API_KEY` in all pipeline files
- Update README / documentation references to reflect the new key name

## Capabilities

### New Capabilities
- `gemini-llm-client`: Pipeline uses the Google Gemini API (`google-generativeai`) for all LLM inference, configured via `GEMINI_API_KEY`

### Modified Capabilities
- `project-readme`: README references to `ANTHROPIC_API_KEY` and Anthropic SDK are replaced with `GEMINI_API_KEY` and `google-generativeai`

## Impact

- `pipeline/requirements.txt`: `anthropic>=0.30.0` → `google-generativeai>=0.8.0` (or latest stable)
- `pipeline/pipeline.py`: env var check `ANTHROPIC_API_KEY` → `GEMINI_API_KEY`
- `pipeline/synthesis.py`: import, client init, model constant, and message call updated
- `pipeline/verification.py`: same updates as `synthesis.py`
- `README.md`: setup instructions updated for new env var
- No backend or frontend changes required
