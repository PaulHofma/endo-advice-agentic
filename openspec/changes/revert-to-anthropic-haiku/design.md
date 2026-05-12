## Context

The pipeline currently uses the `google-genai` SDK with `gemini-2.0-flash`. Each of the two agentic modules (`synthesis.py`, `verification.py`) instantiates a `genai.Client` and calls `client.models.generate_content(...)`. The switch back to Anthropic replaces this with the `anthropic` SDK's `client.messages.create(...)` pattern.

The model chosen is `claude-haiku-4-5` — the most cost-effective Claude model, priced at $1/$5 per million input/output tokens. For this pipeline's use case (structured JSON extraction from short medical abstracts), Haiku is sufficient.

## Goals / Non-Goals

**Goals:**
- Restore Anthropic SDK as the LLM provider
- Use `claude-haiku-4-5` for cost efficiency
- Keep the pipeline interface identical (same inputs, same output schema)

**Non-Goals:**
- Changing prompts or the structured output format
- Adding streaming (the responses are short; non-streaming is fine)
- Adding prompt caching (nice-to-have but out of scope here)

## Decisions

**Model: `claude-haiku-4-5`**
The synthesis and verification tasks are JSON extraction tasks against short abstracts. They don't require deep reasoning — Haiku handles them well. Opus or Sonnet would cost 3–25× more per run with no meaningful quality benefit for this workload.

**Non-streaming messages API**
Responses are small (a JSON array or object). Using `client.messages.create()` with `max_tokens=2048` is simpler than streaming and won't hit timeout limits at this size.

**Response parsing unchanged**
Both modules already strip markdown fences and parse JSON from the response text. The same logic applies to Claude's output.

## Risks / Trade-offs

- [Model response format] Claude may format JSON differently than Gemini → the existing fence-stripping + `json.loads()` approach handles this; no change needed
- [Cost] Haiku is cheap but not free; each full pipeline run (synthesis + verification for one supplement) will use roughly 50–100 API calls → acceptable cost for a personal project

## Migration Plan

1. Swap dependency in `requirements.txt`
2. Update env var guard in `pipeline.py`
3. Update `synthesis.py` (client init + API call)
4. Update `verification.py` (client init + API call)
5. Update `README.md`
6. Re-install dependencies: `pip install -r requirements.txt`

No database changes. No rollback needed — reverting means reinstating the Gemini code from git history.
