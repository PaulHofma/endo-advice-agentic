## Context

The pipeline currently produces findings at the paper level. After `load_findings.py` inserts them, the pipeline terminates. There is no cross-paper synthesis — readers see individual findings with no aggregated picture of the evidence. The backend serves findings flat; the frontend has no summary layer.

The product needs two navigation axes: supplement-first (current) and symptom-first (planned). Both axes benefit from pre-generated summaries rather than on-demand LLM calls at read time.

## Goals / Non-Goals

**Goals:**
- Generate three summary types in a new pipeline stage after findings load
- Use `supplement_symptom_summaries` as the shared input for both higher-level summary types
- Full-replace all summaries on every pipeline run (no incremental logic)
- Expose all three via the backend API
- Render them in the frontend on supplement and symptom pages

**Non-Goals:**
- On-demand summary generation at API request time
- Incremental summary updates (only new findings trigger regeneration)
- User-facing editing or correction of summaries
- Summaries for supplement×symptom pairs with zero findings (no row is written)

## Decisions

### 1. Three-tier summary hierarchy generated bottom-up

**Decision**: Generate `supplement_symptom_summaries` first, then derive `supplement_summaries` and `symptom_summaries` from them (not from raw findings).

**Rationale**: Each higher-level summary reads already-synthesised text, keeping Claude's context window small and focused. Generating supplement/symptom summaries directly from all raw findings would create large, unwieldy prompts and repeat synthesis work already done at the pair level.

**Alternative considered**: Single pass generating all three simultaneously. Rejected — no natural way to feed pair summaries into higher-level prompts without a sequential dependency.

---

### 2. Full-replace on every run

**Decision**: Each pipeline run DELETEs all existing summaries and regenerates them from scratch.

**Rationale**: Summaries aggregate across all findings; any new finding for a supplement changes the correct summary. Incremental logic (detect what changed, update only affected summaries) adds significant complexity with minimal benefit given the small data volume and offline/operator-run nature of the pipeline.

**Alternative considered**: Upsert only changed supplement×symptom pairs. Rejected — requires change detection, and the pipeline is not performance-sensitive.

---

### 3. `evidence_strength` on `supplement_symptom_summaries` only

**Decision**: Only the pair-level summary carries a structured `evidence_strength` field. Higher-level summaries use free-text to describe evidence quality.

**Rationale**: Evidence strength is most meaningful at the specific supplement×symptom level. At the supplement or symptom level, strength varies across pairs — a structured single value would be misleading. Free-text prose handles the nuance better.

---

### 4. Summarise module reads from DB, not in-memory pipeline state

**Decision**: `summarise.py` reads findings and pair summaries from the database, not from in-memory objects passed through the pipeline.

**Rationale**: Keeps `summarise.py` independently runnable (operator can re-run summarisation without re-running the full pipeline). Also simplifies the pipeline orchestration — `pipeline.py` just calls `summarise.run()` after load, with no data passing needed.

---

### 5. supplement_symptom_summaries serves double duty on both pages

**Decision**: The same `supplement_symptom_summary` row is rendered on both the supplement page (under its symptom group) and the symptom page (under its supplement group). There is no separate "supplement view" vs "symptom view" variant.

**Rationale**: The content is the same question answered from the same data — "what does evidence say about this supplement for this symptom?" The rendering context differs (grouped by symptom vs grouped by supplement) but the content does not.

## Risks / Trade-offs

- **LLM cost per run** → All summaries regenerated every run. With ~10 supplements × ~5 symptoms = ~50 pair summaries + ~10 supplement summaries + ~5 symptom summaries = ~65 Claude calls per full pipeline run. At Haiku pricing this is negligible, but will grow with data volume. Mitigation: acceptable for now; can add change-detection later if cost becomes an issue.
- **Summary quality regression** → A new finding could lower the overall evidence quality description. Mitigation: operator reviews pipeline output; summaries are in the review file alongside findings.
- **Zero-findings supplement** → If a supplement has no verified findings, `supplement_summaries` must still say something useful ("no evidence found"). Mitigation: the summarisation prompt explicitly handles this case; the supplement summary is generated even if there are no pair summaries, using the absence of data as its input.

## Migration Plan

1. Add three Flyway migrations (V7, V8, V9) — additive, no downtime
2. Deploy backend with new entities and endpoints — new endpoints return empty until pipeline runs
3. Run pipeline — summaries populate
4. Deploy frontend with summary rendering

Rollback: drop the three new tables; remove new backend/frontend code.

## Open Questions

- Should the review file (currently showing findings by verdict) also show generated summaries for operator review, or are summaries implicitly trusted as post-processing? Current inclination: include summaries in the review file so the operator can spot obviously wrong synthesis before it goes live.
