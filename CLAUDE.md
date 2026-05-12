# endo-advice-agentic

A personal project that uses an agentic research pipeline to surface evidence-based supplement information for people with endometriosis. Claude (via the Anthropic SDK) drives the research pipeline, pulling studies from PubMed (via BioPython/Entrez), extracting structured findings, and persisting them to PostgreSQL. A Spring Boot API serves those findings; a React frontend (in progress) will present them.

## Architecture

```
pipeline/   Python agentic pipeline — researches supplements, writes to DB
backend/    Kotlin/Spring Boot REST API — serves findings from DB
frontend/   React 19 + TypeScript (Vite) — UI (early stage)
```

Shared database: **PostgreSQL** (Docker Compose).

## Domain model

| Entity | Description |
|---|---|
| `Supplement` | A supplement being researched (e.g. "Omega-3", "Magnesium") |
| `Symptom` | An endometriosis symptom (name + URL slug) |
| `Finding` | A research result: links a supplement to symptoms, with a plain-language summary and evidence snapshot |
| `Citation` | A PubMed paper (PMID, title, authors, year, abstract excerpt) backing a Finding |
| `finding_symptoms` | Many-to-many join between Finding and Symptom |

## Tech stack

| Layer | Tech |
|---|---|
| Database | PostgreSQL 16 (Docker) |
| Pipeline | Python 3, Anthropic SDK, BioPython (Entrez/PubMed), psycopg2 |
| Backend | Kotlin 1.9, Spring Boot 3.3, Spring Data JPA, Flyway, Java 21 |
| Frontend | React 19, TypeScript, Vite |

## Development setup

**Start the database:**
```bash
docker-compose up -d
```

**Backend** (connects to `localhost:5432`):
```bash
cd backend
./gradlew bootRun        # run
./gradlew test           # test (uses Testcontainers — no running DB needed)
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev              # dev server
npm run build            # production build
npm run lint             # ESLint
```

**Pipeline:**
```bash
cd pipeline
pip install -r requirements.txt
python3 <script>.py
```

> **pyenv**: This project uses pyenv to manage the Python version. Always use the pyenv-resolved `python3` / `pip3` — never bypass it with an absolute path or a system Python. The active version is set by `.python-version` (if present) or the global pyenv config.

## Database migrations

Flyway manages the schema. Migration files live in `backend/src/main/resources/db/migration/` and follow the `V{n}__{description}.sql` naming convention. Add new migrations there — never modify existing ones.

## Agent behavior

- **Never commit automatically.** Stage changes with `git add` in logical, coherent batches (one batch per concern), but always stop short of `git commit`. The human reviews staged changes and commits manually.
- **Batch staging by concern** — e.g. domain model changes in one batch, migration in another, API layer in another. Aim for batches that would make a sensible standalone commit message.
- When a feature is fully implemented, summarize what's staged and why it's grouped that way, then stop.

## Key conventions

- **Backend**: Kotlin idiomatic style. JPA entities are plain classes (no `data class` for JPA roots). Use `FetchType.LAZY` on all associations.
- **Pipeline**: Use `python3`, not `python`. The pipeline is the only writer to the database; the backend is read-only.
- **OpenSpec**: Feature specs live in `openspec/specs/`, changes in `openspec/changes/`. Follow the spec-driven workflow before implementing features.
- **Commits**: Use conventional commits (`feat:`, `fix:`, `chore:`, etc.).
