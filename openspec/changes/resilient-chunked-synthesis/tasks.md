## 1. Extract chunk synthesis into a private function

- [ ] 1.1 Extract the Claude API call + JSON parse logic from `run_synthesis()` into a new private function `_synthesize_chunk(topic, articles, client) -> list[RawFinding]`
- [ ] 1.2 Verify `run_synthesis()` still works end-to-end by calling `_synthesize_chunk()` once with all articles (no chunking yet)

## 2. Add retry logic to `_synthesize_chunk()`

- [ ] 2.1 Wrap the Claude call + parse in a retry loop with `max_retries=2`
- [ ] 2.2 On `JSONDecodeError`, log the attempt number and retry; on final failure raise or return an empty list with a failure flag
- [ ] 2.3 Return a tuple or use an exception to signal chunk-level failure to the caller

## 3. Add chunking to `run_synthesis()`

- [ ] 3.1 Add `chunk_size: int = 4` parameter to `run_synthesis()`
- [ ] 3.2 Split the article list into chunks of `chunk_size` using a helper (e.g. `itertools.batched` or a simple slice loop)
- [ ] 3.3 Loop over chunks, call `_synthesize_chunk()` for each, accumulate results
- [ ] 3.4 On chunk failure (all retries exhausted), log `"Chunk N/M failed after retries — skipping"` and continue

## 4. Fix logging to distinguish failure modes

- [ ] 4.1 Ensure a failed chunk emits a log line with the chunk index and "failed after retries"
- [ ] 4.2 Ensure a successful parse returning zero findings does NOT emit a failure warning
- [ ] 4.3 Update the final summary log to show `"Produced X findings from Y chunks (Z failed)"` when any chunks failed

## 5. Verify PMC dosage fallback still works

- [ ] 5.1 Confirm the PMC dosage fallback loop at the end of `run_synthesis()` runs over the merged results from all chunks unchanged
