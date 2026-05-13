## ADDED Requirements

### Requirement: Articles are split into bounded chunks before synthesis
`run_synthesis()` SHALL split the fetched article list into chunks of at most `chunk_size` articles (default: 4) before making any Claude API calls. Each chunk is synthesized independently.

#### Scenario: Articles divide evenly into chunks
- **WHEN** 12 articles are fetched and chunk_size is 4
- **THEN** exactly 3 Claude synthesis calls are made, each with 4 articles

#### Scenario: Articles do not divide evenly
- **WHEN** 14 articles are fetched and chunk_size is 4
- **THEN** 4 Claude calls are made: three with 4 articles and one with 2 articles

#### Scenario: Fewer articles than chunk size
- **WHEN** 3 articles are fetched and chunk_size is 4
- **THEN** exactly 1 Claude call is made with all 3 articles

### Requirement: Results from all successful chunks are merged
`run_synthesis()` SHALL collect `RawFinding` results from every chunk that parses successfully and return them as a single flat list, in chunk order.

#### Scenario: All chunks succeed
- **WHEN** 3 chunks each produce 2 findings
- **THEN** `run_synthesis()` returns a list of 6 findings

#### Scenario: One chunk fails, others succeed
- **WHEN** chunk 2 of 3 fails all retries and chunks 1 and 3 each produce 2 findings
- **THEN** `run_synthesis()` returns a list of 4 findings (chunks 1 and 3 only)

### Requirement: Failed chunks are retried before being skipped
When a chunk produces a `JSONDecodeError`, the synthesis SHALL be retried up to `max_retries` times (default: 2) with the same prompt before the chunk is skipped.

#### Scenario: Chunk succeeds on retry
- **WHEN** a chunk fails to parse on the first attempt but succeeds on the second
- **THEN** its findings are included in the merged results

#### Scenario: Chunk exhausts all retries
- **WHEN** a chunk fails to parse on every attempt including all retries
- **THEN** the chunk is skipped, a warning is logged, and the pipeline continues with findings from other chunks

### Requirement: Failure log distinguishes chunk failure from zero findings
The pipeline SHALL emit distinct log messages for two different zero-result conditions.

#### Scenario: Chunk parse failure
- **WHEN** a chunk fails all retries
- **THEN** a log line containing "failed after retries" and the chunk index is emitted

#### Scenario: Successful parse with no findings
- **WHEN** Claude returns a valid empty JSON array `[]` for a chunk
- **THEN** no failure warning is logged; the chunk contributes 0 findings silently

### Requirement: `run_synthesis()` public interface is unchanged
Callers of `run_synthesis(topic, max_articles)` SHALL require no modification. The function SHALL continue to return `list[RawFinding]`.

#### Scenario: Existing call site works without changes
- **WHEN** `pipeline.py` calls `run_synthesis(topic, max_articles=15)`
- **THEN** it receives a `list[RawFinding]` with no awareness of internal chunking
