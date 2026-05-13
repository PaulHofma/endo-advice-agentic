## Why

When synthesizing large sets of abstracts, Claude's output can exceed `max_tokens=2048`, truncating the JSON array mid-stream. The resulting `JSONDecodeError` silently returns an empty findings list — indistinguishable from a topic that genuinely produced no results, causing data loss with no operator visibility.

## What Changes

- `run_synthesis()` splits articles into chunks (default size: 4) before calling Claude
- Each chunk is synthesized in a separate Claude call, bounding output size per call
- Failed chunks are retried up to 2 times before being skipped with a warning
- Partial results from successful chunks are merged and returned
- Log messages distinguish "0 findings extracted" from "synthesis failed for N chunks"

## Capabilities

### New Capabilities

- `chunked-synthesis`: Article lists are split into bounded chunks; each chunk is independently synthesized and retried on failure, then results are merged

### Modified Capabilities

_(none — no spec-level behavior changes to existing capabilities)_

## Impact

- `pipeline/synthesis.py`: all changes contained here; `run_synthesis()` signature unchanged
- No changes to `pipeline.py`, `verification.py`, or any callers
- Slightly increased Claude API call count per topic (e.g., 15 articles → ~4 calls instead of 1)
