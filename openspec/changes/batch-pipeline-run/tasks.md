## 1. CLI Argument Parsing

- [ ] 1.1 Add `--topics` (repeatable, `nargs='+'` or `action='append'`) argument to `pipeline.py` argument parser
- [ ] 1.2 Add `--topics-file` argument to `pipeline.py` argument parser (path to newline-separated file)
- [ ] 1.3 Implement `_resolve_topics(args)` helper that merges `--topic`, `--topics`, and `--topics-file` into a single `list[str]`, deduplicated, raising an error if none are provided
- [ ] 1.4 Add `_load_topics_file(path)` helper that reads the file, strips blank lines and `#`-comment lines

## 2. Pipeline Loop

- [ ] 2.1 Refactor the main pipeline body into a per-topic function `_run_topic(topic, max_articles)` returning `(topic, list[VerifiedFinding] | None, error_message | None)`
- [ ] 2.2 In `main()`, loop over resolved topics, calling `_run_topic` for each; collect results; catch exceptions per topic and record failure without aborting the batch
- [ ] 2.3 After the loop, pass all collected findings (grouped by topic/supplement) to the review writer

## 3. Consolidated Review Writer

- [ ] 3.1 Add `write_consolidated_review_file(findings_by_supplement: dict[str, list[VerifiedFinding]], failures: list[str], output_path: str)` to `review_writer.py`
- [ ] 3.2 The consolidated writer groups output by supplement name, with a `## Supplement: <name>` heading per supplement, then verdict sub-sections within each
- [ ] 3.3 For failed topics, include a `## Supplement: <topic> — FAILED` section with the error message
- [ ] 3.4 Keep the existing `write_review_file` function unchanged (used by single-topic path)

## 4. Wiring & Output Message

- [ ] 4.1 In `pipeline.py`, use `write_consolidated_review_file` when there are multiple topics, `write_review_file` when there is exactly one topic (preserves existing single-topic UX)
- [ ] 4.2 Update the final print message to reflect batch totals (e.g., "X topics processed, Y findings total") when running in batch mode

## 5. Smoke Test

- [ ] 5.1 Verify `python3 pipeline.py --topic "NAC endometriosis"` still works (backward compat)
- [ ] 5.2 Verify `python3 pipeline.py --topics "NAC endometriosis" --topics "Vitamin D endometriosis"` produces a single review file with two supplement sections
