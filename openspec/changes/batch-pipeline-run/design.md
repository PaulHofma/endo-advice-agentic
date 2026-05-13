## Context

The pipeline currently accepts a single `--topic` argument (e.g., `"NAC endometriosis"`). Running it for multiple supplements requires invoking `pipeline.py` once per supplement, reviewing separate files for each, and calling `load_findings.py` (and therefore `summarise.run()`) once per supplement — triggering redundant summarisation on partial data. This workflow is friction-heavy for the operator and produces lower-quality summaries until all supplements have been loaded.

The pipeline modules (`synthesis.py`, `verification.py`, `review_writer.py`) are all stateless and topic-driven; extending to multiple topics is straightforward. The main changes are in `pipeline.py` (the orchestrator) and `review_writer.py` (the output format).

## Goals / Non-Goals

**Goals:**
- Accept multiple topics in a single `pipeline.py` invocation (`--topics` repeated arg or `--topics-file` pointing to a newline-separated file)
- Run synthesis then verification for each topic independently, collecting all findings
- Write a single consolidated review file with findings grouped by supplement
- Preserve `--topic` (singular) for backward compatibility
- No change to `load_findings.py` or `summarise.py` — summarisation already runs once after load

**Non-Goals:**
- Parallel execution of synthesis/verification across topics (sequential is fine; NCBI rate limits apply)
- Persisting intermediate state between topics (if the run fails halfway, re-run from scratch)
- A topics "catalog" concept — just a flat list of strings per invocation

## Decisions

### 1. Extend `pipeline.py` rather than a wrapper script

**Decision**: Add `--topics` / `--topics-file` args to the existing `pipeline.py`.

**Rationale**: A wrapper script would duplicate argument parsing and the environment check. Keeping everything in `pipeline.py` makes the entry point obvious and the `--topic` / `--topics` distinction clear.

**Alternative considered**: A separate `pipeline_batch.py`. Rejected — two entry points for essentially the same operation creates confusion.

---

### 2. Single consolidated review file

**Decision**: All findings from all topics go into one review file, grouped by supplement with a header per supplement.

**Rationale**: The operator reviews once and loads once. Separate files per topic would require running `load_findings.py` multiple times and trigger summarisation multiple times — defeating the purpose of batching.

**Alternative considered**: One file per topic, operator loads each. Rejected — same fragmentation problem as the current flow.

---

### 3. `review_writer.py` gains a multi-supplement mode

**Decision**: Add a `write_consolidated_review_file(findings_by_supplement, output_path)` function alongside the existing `write_review_file`. The existing function is unchanged for single-topic use.

**Rationale**: Keeping the existing function means the `--topic` (singular) path is unchanged. The consolidated writer groups findings by supplement then by verdict within each supplement.

---

### 4. Topics file format: one topic per line

**Decision**: `--topics-file` reads a newline-separated plain text file (blank lines and `#` comments ignored).

**Rationale**: Simplest possible format for a list of strings. No YAML/JSON overhead.

## Risks / Trade-offs

- **Long run time** → A batch of 10 topics × ~15 articles each = up to 150 synthesis calls + 150 verification calls. At Haiku latency (~1s/call with rate-limit sleeps), a full batch takes ~10 minutes. Mitigation: operator can start small; progress is printed per topic.
- **Partial failure** → If synthesis fails for one topic mid-batch, findings from earlier topics are not yet in the review file. Mitigation: per-topic failures are caught and logged; the run continues; partial results are included in the review file with a failure note.
- **Review file size** → A large batch produces a large file. Mitigation: accepted — the file is human-readable markdown, operators can search within it.

## Migration Plan

1. Update `pipeline.py` with new args (backward-compatible — `--topic` still works)
2. Update `review_writer.py` with the consolidated writer
3. No DB migration, no backend changes, no frontend changes
4. No rollback needed — operator workflow is unchanged for `--topic` users
