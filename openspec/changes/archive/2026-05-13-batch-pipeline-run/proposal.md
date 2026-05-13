## Why

Running the pipeline one supplement at a time means the operator must invoke multiple commands per supplement, review multiple separate files, and trigger summarisation redundantly after each load — with summaries being partially stale until all supplements have been loaded. A batch mode lets the operator specify a list of topics once, get a single consolidated review file, load everything in one step, and generate summaries once across the full data set.

## What Changes

- Replace the single-topic `pipeline.py` CLI with a mode that accepts multiple topics (via `--topics` or a topics file)
- Synthesis and verification run for all topics before any review file is produced
- A single consolidated review file is written with all findings grouped by supplement
- `load_findings.py` already triggers summarisation — no change needed there
- The old single-topic `--topic` flag is preserved for backward compatibility

## Capabilities

### New Capabilities
- `batch-pipeline`: Pipeline can accept multiple topics in a single invocation, producing one consolidated review file covering all topics before the operator reviews anything

### Modified Capabilities
- `research-pipeline`: CLI interface gains `--topics` (multiple) and `--topics-file` arguments alongside the existing `--topic`

## Impact

- **Pipeline**: `pipeline.py` refactored to loop over topics; `review_writer.py` updated to support multi-supplement output
- **No backend or frontend changes**
- **No new dependencies**
