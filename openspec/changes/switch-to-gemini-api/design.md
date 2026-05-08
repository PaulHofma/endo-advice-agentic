## Context

The pipeline uses two modules (`synthesis.py` and `verification.py`) that call an LLM to extract and verify research findings. Both currently use the `anthropic` Python SDK with `ANTHROPIC_API_KEY` and the `claude-opus-4-5` model. The goal is to replace this with Google's `google-generativeai` SDK backed by `GEMINI_API_KEY`.

The pipeline is the only LLM consumer; no backend or frontend changes are needed.

## Goals / Non-Goals

**Goals:**
- Replace `anthropic` SDK with `google-generativeai` in `synthesis.py` and `verification.py`
- Replace `ANTHROPIC_API_KEY` env var check in `pipeline.py` with `GEMINI_API_KEY`
- Keep the same prompt content and JSON output contract — only the transport layer changes
- Update `requirements.txt` and README

**Non-Goals:**
- Changing prompt wording or LLM behavior
- Supporting multiple LLM providers simultaneously
- Modifying the backend or frontend

## Decisions

### Use `google-generativeai` (v0.8+) with `gemini-2.0-flash` as the default model

**Rationale**: `gemini-2.0-flash` is Google's recommended general-purpose model, broadly available, and cost-effective. The `google-generativeai` SDK is the official Python client.

**Alternatives considered**:
- `gemini-1.5-pro`: Higher capability but slower and more expensive; not necessary for structured JSON extraction.
- Using the REST API directly: More portable but adds maintenance burden vs. the SDK.

### Adapt to Gemini's `generate_content` API

The Anthropic SDK uses `client.messages.create(model=..., messages=[...])` and returns `message.content[0].text`. The Gemini SDK uses `model.generate_content(prompt)` and returns `response.text`. The call sites in `synthesis.py` and `verification.py` will be updated accordingly, keeping the same prompt strings.

**No changes to response parsing**: Both APIs return plain text; existing JSON-extraction and markdown-fence stripping logic remains unchanged.

## Risks / Trade-offs

- [Model parity] Gemini may produce slightly different JSON formatting than Claude → Mitigation: existing markdown-fence stripping and `json.loads` error handling already guards against this.
- [API quota / rate limits] Gemini free-tier limits differ from Anthropic → Mitigation: no pipeline throttling logic exists today; this is unchanged.
- [Key rotation] Developers need to obtain a Gemini API key → Mitigation: update README with clear instructions.
