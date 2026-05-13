## Context

`synthesis.py` makes a single Claude call per topic with all abstracts concatenated into one prompt. With `max_tokens=2048` and up to 15 abstracts, output is regularly truncated, producing a broken JSON array. The `JSONDecodeError` is caught but swallowed — the topic is recorded as having zero findings, with no distinction from a topic that genuinely returned nothing.

All callers (`pipeline.py`) treat the return value of `run_synthesis()` as a plain list; the fix must be transparent to them.

## Goals / Non-Goals

**Goals:**
- Bound each Claude synthesis call to a small number of abstracts so output fits within token limits
- Retry failed chunks independently, preserving results from successful chunks
- Make chunk failures visible in logs, distinguishable from zero-findings outcomes
- Keep `run_synthesis()` signature and return type unchanged

**Non-Goals:**
- Dynamic chunk sizing based on token estimation
- Persistent retry queues or async execution
- Changing the Claude model or switching to tool/structured-output mode
- Surfacing chunk failure counts in the review file output (pipeline.py concern)

## Decisions

### Chunking inside `run_synthesis()`

Articles are split into fixed-size chunks before any Claude calls are made. Each chunk goes through its own `_synthesize_chunk()` call (a new private function wrapping the existing prompt + parse logic). Results are concatenated after all chunks complete.

**Alternative considered**: chunking at the `pipeline.py` level by calling `run_synthesis()` multiple times with fewer `max_articles`. Rejected because it multiplies PubMed searches and complicates caller logic; chunking post-fetch keeps the search unified.

### Retry per chunk, not per topic

On `JSONDecodeError`, the failed chunk is retried up to `max_retries` times (default: 2) with the same prompt. If all retries fail, the chunk is skipped and a warning is logged; the topic continues with findings from other chunks.

**Alternative considered**: retrying with a smaller sub-chunk on failure. Adds complexity for marginal gain given chunking already bounds the output size. Can be added later if needed.

### Chunk size as a parameter with a default of 4

`run_synthesis()` accepts an optional `chunk_size: int = 4` argument. Four abstracts per chunk produces well-bounded output (~600–900 tokens) and keeps call count reasonable (15 articles → 4 calls).

**Alternative considered**: hardcoding chunk size. Rejected — testability and future tuning require it to be configurable without code changes.

### Log line distinguishing failure modes

Two distinct log prefixes:
- `[synthesis] Chunk N/M failed after retries — skipping` (parse failure)
- `[synthesis] Produced 0 findings` (successful parse, nothing extracted)

This makes silent data loss visible in pipeline logs.

## Risks / Trade-offs

- **More API calls per topic** → Slightly higher latency and cost per run. Acceptable given Haiku pricing and current run frequency.
- **Retry on same prompt may not help if failure is structural** → If Claude consistently adds commentary for a given topic, retries will all fail. Mitigation: log clearly so the operator can investigate; add tool-use mode later if needed.
- **Chunk boundaries may split related abstracts** → Articles are chunked sequentially (no semantic grouping). Risk is low since each finding maps to a single PMID.

## Open Questions

- Should `chunk_size` be exposed as a CLI flag in `pipeline.py`? Deferred — internal default is sufficient for now.
- Should failed-chunk PMIDs be recorded anywhere (review file, separate log)? Deferred — log output is enough for current usage.
