## Context

Greenfield project. No existing codebase to migrate. The operator (Paul) will run a local Python pipeline periodically to gather and verify research, then push approved content to a deployed Postgres database. End users interact only with the React frontend, which reads from the Spring Boot API — no AI in the user request path.

Tech stack: Python (agent pipeline), Kotlin + Spring Boot (backend), Postgres (data), React (frontend), Claude API (Anthropic, operator-side only), PubMed Entrez API (free, no auth required for basic use).

## Goals / Non-Goals

**Goals:**
- Establish a repeatable, trustworthy content pipeline from PubMed research to browsable UI
- Every user-visible claim is backed by a real, fetchable PubMed citation
- Users can navigate by supplement or by symptom
- Operator controls all content — no user-generated content
- Zero AI cost at runtime

**Non-Goals:**
- User accounts or personalization
- Real-time or live AI queries for users
- Specialty center directory
- Languages other than English
- Replacing medical care

## Decisions

### 1. Two-stage agent pipeline (synthesis → verification)

Synthesis and verification are separated into two distinct agents rather than one.

**Rationale:** A single agent tasked with "find and verify" has incentive to rationalize its own output. A separate verification agent re-fetches the source independently, treating the synthesis output as a claim to be challenged. This catches both hallucinated citations (PMID doesn't exist) and overstated conclusions (PMID exists but paper doesn't say what was claimed).

**Alternatives considered:** Human-only review — too slow and requires deep reading of every abstract. Single agent with self-critique — weaker separation of concerns, same model verifying its own output.

### 2. Operator review of flagged items only

The verification agent outputs a structured report: verified / flagged / rejected. Operator reviews flagged and rejected items; verified items are spot-checked.

**Rationale:** Reduces operator cognitive load while preserving human judgment at decision boundaries. Full review of every item is not scalable as the corpus grows.

### 3. Python for agent pipeline

The agent pipeline is Python, not Kotlin, despite the backend being Kotlin.

**Rationale:** Python has a mature ecosystem for LLM tooling (Anthropic SDK, LangChain, etc.) and PubMed API access. The pipeline is a developer tool, not a deployed service — language consistency with the backend is not required.

### 4. Data model: findings as the join entity

The core model is `Supplement ←→ Finding ←→ Symptom` where `Finding` is the rich join entity containing the synthesized claim, evidence level, and citations.

**Rationale:** A direct M2M between supplement and symptom loses the claim content. `Finding` makes the evidence explicit and queryable. A single supplement may have multiple findings per symptom (e.g., different mechanisms or conflicting evidence).

### 5. Read-only REST API

The Spring Boot API exposes read-only endpoints. Content is loaded via a separate admin CLI or migration script, not through the API.

**Rationale:** Simplest secure design for the current phase. No write surface exposed to the internet. Operator loads content directly to the database.

### 6. PubMed Entrez API for citation verification

The verification agent uses the NCBI Entrez API to fetch abstracts by PMID.

**Rationale:** Free, no authentication required for low-volume use, authoritative source. Rate limit is 3 requests/second unauthenticated (10/second with API key) — sufficient for a batch pipeline.

## Risks / Trade-offs

- **Hallucinated but plausible PMIDs** → Verification agent must confirm the PMID resolves and the abstract is relevant, not just that the PMID returns a result. Mitigated by having the agent quote a supporting excerpt from the actual abstract.
- **Research corpus going stale** → Pipeline must be re-run periodically. No auto-refresh mechanism in MVP. Mitigated by operator discipline and clear "last updated" metadata on findings.
- **Overstated conclusions** → Verification agent can check claim vs. abstract but cannot assess the quality of the study itself (sample size, methodology). Mitigated by surfacing study metadata (n=, study type) in the UI so users can judge.
- **Claude API cost for pipeline** → Pipeline runs on operator's machine at operator's discretion. Cost is bounded and predictable. Not a runtime cost.

## Open Questions

- Should the content loading step be a CLI tool (e.g., `./load-findings.py`) or a Spring Boot admin endpoint protected by a secret? CLI is simpler for MVP.
- What is the initial seed set of supplements? A handful (5-10) to prove the pipeline end-to-end before scaling.
- Should findings include a structured "evidence level" field (e.g., RCT / observational / case study) or free-text? Structured is more queryable; decision deferred to spec.
