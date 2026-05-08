## 1. Project Scaffolding

- [x] 1.1 Initialize Kotlin + Spring Boot project with Gradle (Spring Web, Spring Data JPA, Postgres driver)
- [x] 1.2 Initialize React project with Vite
- [x] 1.3 Create Python project directory for agent pipeline with requirements.txt (anthropic, requests, biopython or entrez-direct)
- [x] 1.4 Add docker-compose.yml for local Postgres instance
- [x] 1.5 Configure Spring Boot datasource for local Postgres

## 2. Database Schema & Migrations

- [x] 2.1 Create Flyway (or Liquibase) migration: `supplements` table (id, name, summary, created_at)
- [x] 2.2 Create migration: `symptoms` table (id, name, slug, created_at)
- [x] 2.3 Create migration: `findings` table (id, supplement_id, plain_language_summary, evidence_snapshot, created_at)
- [x] 2.4 Create migration: `finding_symptoms` join table (finding_id, symptom_id)
- [x] 2.5 Create migration: `citations` table (id, finding_id, pmid, title, authors, year, abstract_excerpt) with NOT NULL constraint on pmid and finding_id
- [x] 2.6 Add DB constraint: finding must have at least one citation (enforced via application layer + check at load time)

## 3. Backend: Data Model & Repository Layer

- [x] 3.1 Create Kotlin entity classes: `Supplement`, `Symptom`, `Finding`, `Citation`, `FindingSymptom`
- [x] 3.2 Create JPA repositories for each entity
- [x] 3.3 Write repository query: find all supplements with at least one finding
- [x] 3.4 Write repository query: find all symptoms with at least one finding
- [x] 3.5 Write repository query: find findings by symptom slug

## 4. Backend: REST API

- [x] 4.1 `GET /api/supplements` — list all supplements (id, name, summary)
- [x] 4.2 `GET /api/supplements/{id}` — supplement detail with findings and citations
- [x] 4.3 `GET /api/symptoms` — list all symptoms that have findings
- [x] 4.4 `GET /api/symptoms/{slug}/supplements` — supplements with findings for a given symptom
- [x] 4.5 Enable CORS for local React dev server
- [x] 4.6 Add basic integration tests for each endpoint

## 5. Python Agent Pipeline

- [x] 5.1 Implement PubMed Entrez API wrapper (search by query, fetch abstract by PMID)
- [x] 5.2 Implement synthesis agent: given a topic, query PubMed, produce structured findings with claims and PMIDs using Claude API
- [x] 5.3 Implement verification agent: for each finding, re-fetch abstract by PMID and verify claim is supported using Claude API
- [x] 5.4 Implement review file writer: output grouped findings (verified / flagged / rejected) to a human-readable file
- [x] 5.5 Wire into single CLI: `python pipeline.py --topic "<supplement> endometriosis"`
- [x] 5.6 Implement database loader: reads approved findings from review file, inserts into Postgres

## 6. Frontend: Core Layout & Routing

- [x] 6.1 Set up React Router with routes: `/`, `/supplements`, `/supplements/:id`, `/symptoms`, `/symptoms/:slug`
- [x] 6.2 Create top-level layout with navigation (Supplements | By Symptom)
- [x] 6.3 Add API client utility (fetch wrapper pointing to Spring Boot)

## 7. Frontend: Supplement Catalog

- [x] 7.1 Build `SupplementList` page: fetches `/api/supplements`, renders cards with name + summary
- [x] 7.2 Add name search filter (client-side, case-insensitive)
- [x] 7.3 Build `SupplementDetail` page: plain-language summary → evidence snapshot → findings list
- [x] 7.4 Each finding shows quoted excerpt + PubMed link (opens new tab, canonical PMID URL)

## 8. Frontend: Symptom Navigation

- [x] 8.1 Build `SymptomList` page: fetches `/api/symptoms`, renders symptom tags/cards
- [x] 8.2 Build `SymptomDetail` page: fetches supplements for symptom, reuses supplement card component

## 9. End-to-End Seed & Verification

- [ ] 9.1 Run pipeline for 3-5 seed supplements (e.g., NAC, Vitamin D, Omega-3, Magnesium, Resveratrol)
- [ ] 9.2 Review and approve pipeline output
- [ ] 9.3 Load approved findings into local Postgres
- [ ] 9.4 Verify full flow: browse supplement → view finding → follow PubMed link
- [ ] 9.5 Verify symptom navigation: select symptom → see relevant supplements
