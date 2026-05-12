## Why

The pipeline was migrated to Gemini to experiment with alternatives, but we're returning to Anthropic as the LLM provider. Claude Haiku 4.5 is chosen for cost-efficiency — it's the most affordable Claude model while still being capable enough for the synthesis and verification tasks this pipeline performs.

## What Changes

- Remove `google-genai` dependency from `requirements.txt`, add `anthropic`
- Replace `GEMINI_API_KEY` environment variable requirement with `ANTHROPIC_API_KEY`
- Replace Gemini client calls in `synthesis.py` with Anthropic SDK (`claude-haiku-4-5`)
- Replace Gemini client calls in `verification.py` with Anthropic SDK (`claude-haiku-4-5`)
- Update startup guard in `pipeline.py` to check `ANTHROPIC_API_KEY`
- Update `README.md` to reference `ANTHROPIC_API_KEY`

## Capabilities

### New Capabilities

_(none — this is a provider swap, not a new capability)_

### Modified Capabilities

- `project-readme`: README setup instructions reference `ANTHROPIC_API_KEY` instead of `GEMINI_API_KEY`

## Impact

- `pipeline/requirements.txt`: swap `google-genai` for `anthropic`
- `pipeline/synthesis.py`: full provider swap
- `pipeline/verification.py`: full provider swap
- `pipeline/pipeline.py`: env var guard update
- `README.md`: setup instructions update
