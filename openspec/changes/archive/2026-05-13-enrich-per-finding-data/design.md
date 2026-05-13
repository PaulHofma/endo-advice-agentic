## Context

The pipeline currently extracts a single plain-language claim and abstract excerpt per finding. The synthesis agent (Claude Haiku) reads PubMed abstracts and produces `RawFinding` objects; these are verified and then loaded into the `findings` table. The verification agent independently re-fetches each abstract to check the claim.

BioPython's Entrez is already used for PubMed access. The `findings` table has no clinical or methodological metadata. The backend exposes findings via a Spring Boot REST API; the frontend is early-stage React.

## Goals / Non-Goals

**Goals:**
- Extract dosage, duration, study type, sample size, placebo flag, and safety notes from abstracts during synthesis
- Fall back to PMC full text for dosage when the abstract doesn't report it
- Store null honestly when data is not recoverable
- Expose new fields through the backend API and render them in the frontend

**Non-Goals:**
- Full-text extraction for anything other than dosage (scope creep risk)
- Structured dosage parsing (e.g. normalising "2g EPA" vs "2000mg EPA") — store as free text
- Paywalled full-text access — PMC open-access only
- Backfilling existing findings — new fields apply to future pipeline runs only

## Decisions

### 1. Extend `RawFinding` rather than a separate extraction pass

**Decision**: Add the new fields directly to `RawFinding` and extract them in the same synthesis prompt call.

**Rationale**: A separate extraction pass would double LLM calls per finding. The synthesis prompt already reads the full abstract; extracting additional structured fields in the same pass is cheap and keeps the pipeline linear.

**Alternative considered**: A dedicated enrichment agent that runs after verification. Rejected — adds pipeline stages without meaningful benefit since all data comes from the same source text.

---

### 2. PMC fallback scoped to dosage only

**Decision**: Full-text retrieval via PMC is attempted only when `dosage` is null after synthesis. Other fields remain abstract-only.

**Rationale**: Dosage is the highest-value field missing from abstracts. Full-text retrieval adds latency and rate-limit risk; broadening scope to all fields multiplies that cost without proportionate user benefit. Other fields (study type, sample size) are almost always reported in abstracts.

**Alternative considered**: Fetch full text for all findings unconditionally. Rejected — many papers are not on PMC, adds ~1s/paper latency, and marginal gain outside dosage is low.

---

### 3. PMC fallback as a standalone module (`pmcfetch.py`)

**Decision**: PMC logic lives in a new `pipeline/pmcfetch.py` module, called from `synthesis.py` after the main extraction.

**Rationale**: Keeps synthesis.py focused on the synthesis task. The fallback is independently testable and can be extended later (e.g. to other fields) without touching synthesis logic.

---

### 4. `study_type` as a constrained string, not an enum in the DB

**Decision**: Store `study_type` as `VARCHAR(20)` with application-level values: `rct`, `observational`, `meta_analysis`, `case_report`, `review`, null.

**Rationale**: Flyway enums are painful to alter. A constrained string is simpler to extend if we add a new study type later. The pipeline is the only writer; there's no risk of arbitrary values entering the DB.

---

### 5. No backfill of existing findings

**Decision**: Existing findings retain null for all new fields. The pipeline is re-run to enrich them.

**Rationale**: We have no reliable way to recover the original articles for already-loaded findings without re-running synthesis. The operator can re-run the pipeline for any supplement to refresh findings.

## Risks / Trade-offs

- **PMC rate limits** → Mitigation: Entrez already respects NCBI rate limits via BioPython; add a small sleep between PMC fetches (same pattern as verification.py).
- **PMC coverage gap** → Accepted: ~40-60% of papers have PMC full text. The `null` case is explicitly surfaced to readers as "not reported."
- **LLM hallucination on dosage** → Mitigation: Verification agent already checks claims; dosage from PMC full text is extracted with a targeted prompt ("what dosage was administered?") rather than open-ended synthesis, reducing hallucination surface.
- **Larger synthesis prompt** → Accepted: Adding ~6 fields to the JSON schema slightly increases token usage per call. At Haiku pricing this is negligible.

## Migration Plan

1. Add Flyway migration (`V6__enrich_findings.sql`) with six nullable columns — additive, no downtime
2. Deploy backend with updated entity and DTO — old findings return null for new fields (safe)
3. Update pipeline — next run populates new fields for new findings
4. Update frontend to render new fields with null-safe fallbacks

Rollback: drop the six columns (data loss only for new fields, no existing data affected).

## Open Questions

- Should the verification agent also verify dosage claims extracted from PMC full text, or treat them as trusted (lower hallucination risk from targeted extraction)? Current inclination: skip verification for PMC-sourced dosage to avoid re-fetching full text a second time.
