## Why

Women with endometriosis and adenomyosis are underserved by the medical system — GPs and even specialists frequently lack up-to-date knowledge, and specialist centers are not equally accessible. This MVP establishes the foundation of a freely accessible, research-backed information tool that aggregates the latest evidence on supplements for endo/adeno symptom management, explained in plain language and anchored to verifiable PubMed sources.

## What Changes

- New Python agent pipeline (offline, operator-run) that queries PubMed, synthesizes research findings into structured content, and verifies each claim against the source abstract
- New Kotlin/Spring Boot backend exposing a read-only REST API over a Postgres database of supplements, symptoms, findings, and citations
- New React frontend allowing users to browse by supplement or by symptom, with a plain-language summary layer over individual study detail
- Postgres schema for the core data model: supplements, symptoms, findings (many-to-many), citations (PubMed-linked)

## Capabilities

### New Capabilities

- `research-pipeline`: Offline two-stage Python agent that ingests PubMed research, synthesizes claims, verifies them, and produces operator-reviewable output ready to load into the database
- `supplement-catalog`: Backend + frontend capability to browse and search supplements, each with evidence-backed findings and PubMed citations
- `symptom-navigation`: Cross-cutting navigation allowing users to discover supplements by the symptom they address
- `citation-integrity`: System-wide requirement that every finding is linked to a real, fetchable PubMed citation

### Modified Capabilities

*(none — greenfield project)*

## Impact

- New dependencies: PubMed/NCBI Entrez API (free), Claude API (Anthropic, operator-side only), Spring Boot, React, Postgres
- No AI at runtime — zero per-user AI cost
- Operator (Paul) controls content pipeline; no user accounts or user-generated content in this phase
