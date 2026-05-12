# Endo Advice

A freely accessible, research-backed information tool for people with endometriosis and adenomyosis. It aggregates evidence on supplements for symptom management, explains findings in plain language, and anchors every claim to a verifiable PubMed source.

> **Note:** This tool provides research summaries only. It does not replace medical advice or specialist care.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Operator (you)                                                 │
│                                                                 │
│  pipeline/pipeline.py ──► review_*.md ──► pipeline/load.py     │
│       │  PubMed + Claude API (offline)          │              │
└───────┼──────────────────────────────────────────┼─────────────┘
        │                                          │
        ▼                                          ▼
   PubMed / NCBI                           PostgreSQL (Docker)
                                                   │
                                      ┌────────────┘
                                      ▼
                              backend/ (Spring Boot)
                              GET /api/supplements
                              GET /api/symptoms/…
                                      │
                                      ▼
                              frontend/ (React + Vite)
                              localhost:5173
```

| Component | Tech | Purpose |
|---|---|---|
| `pipeline/` | Python 3, Google Gemini API (`google-genai`), Biopython | Operator-run tool: queries PubMed, synthesises findings with Gemini, verifies claims, produces a review file for human approval |
| `backend/` | Kotlin, Spring Boot 3, Flyway, JPA | Read-only REST API over a Postgres database of supplements, findings, and citations |
| `frontend/` | React 19, Vite, TypeScript, React Router | Browse supplements and navigate by symptom; zero AI at runtime |

**Data flow:** Operator runs the pipeline → reviews and approves findings → loads them into Postgres → users browse via the React frontend backed by the Spring Boot API.

---

## Prerequisites

| Tool | Version | Install |
|---|---|---|
| Java | 21 | [SDKMAN](#java--sdkman) (recommended) |
| Node.js | 20+ | [nodejs.org](https://nodejs.org) |
| Python | 3.11+ | [python.org](https://python.org) |
| Docker | any recent | [docker.com](https://www.docker.com) |

### Java / SDKMAN

The repo includes `.sdkmanrc` which pins the correct Java version. If you use [SDKMAN](https://sdkman.io):

```bash
sdk env install   # installs pinned version if missing
sdk env           # switches to pinned version
```

To enable automatic switching when you `cd` into the project:

```bash
# in ~/.sdkman/etc/config
sdkman_auto_env=true
```

---

## Local Setup

### 1. Clone and start Postgres

```bash
git clone <repo-url>
cd endo-advice-agentic

docker compose up -d        # starts Postgres on localhost:6543
```

Postgres credentials (see `docker-compose.yml`):

| Setting | Value |
|---|---|
| Host | `localhost:6543` |
| Database | `endo_advice` |
| Username | `endo` |
| Password | `endo_secret` |

### 2. Start the backend

```bash
cd backend
./gradlew bootRun
```

The API will be available at `http://localhost:8080`. Flyway runs migrations automatically on startup.

### 3. Start the frontend

```bash
cd frontend
npm install       # first time only
npm run dev
```

The app will be available at `http://localhost:5173`.

---

## Running the Pipeline

The pipeline is an operator-side CLI tool. You need an Anthropic API key.

### Install dependencies

```bash
cd pipeline
pip3 install -r requirements.txt
```

### Set your API key

```bash
export ANTHROPIC_API_KEY=your-key-here
```

### Run synthesis + verification

```bash
python3 pipeline.py --topic "NAC endometriosis"
```

This will:
1. Search PubMed for relevant abstracts
2. Use Claude to synthesise structured findings (claims + PMIDs)
3. Use a separate Claude call to independently verify each claim against its source abstract
4. Write a review file: `review_NAC_endometriosis_<timestamp>.md`

Options:
```
--topic          Search topic, e.g. "Vitamin D adenomyosis"  (required)
--max-articles   Max PubMed results to fetch (default: 15)
--output         Output review file path (default: auto-generated)
```

### Review the output

Open the generated `review_*.md` file. Each finding is a JSON block with an `approved` field:

- `"approved": true` — verified findings are pre-approved; spot-check these
- `"approved": false` — flagged/rejected findings; edit to `true` to include, or leave as `false` to skip

You may also edit the `claim` field to correct wording before loading.

### Load approved findings into Postgres

```bash
python3 load_findings.py --review review_NAC_endometriosis_<timestamp>.md
```

Repeat for each supplement topic. The loader upserts supplements and symptoms, so running it multiple times is safe.

---

## Project Structure

```
endo-advice-agentic/
├── backend/                  Kotlin + Spring Boot API
│   ├── src/main/kotlin/com/endoadvice/
│   │   ├── model/            JPA entities (Supplement, Finding, Citation, Symptom)
│   │   ├── repository/       Spring Data repositories + custom JPQL queries
│   │   ├── api/              REST controllers + DTOs
│   │   └── config/           CORS configuration
│   └── src/main/resources/
│       └── db/migration/     Flyway SQL migrations (V1–V5)
├── frontend/                 React + Vite app
│   └── src/
│       ├── api/              Typed fetch client
│       ├── components/       Layout, SupplementCard
│       └── pages/            SupplementList, SupplementDetail, SymptomList, SymptomDetail
├── pipeline/                 Python operator tool
│   ├── pipeline.py           Main CLI entry point
│   ├── pubmed.py             PubMed Entrez API wrapper
│   ├── synthesis.py          Synthesis agent (Claude)
│   ├── verification.py       Verification agent (Claude)
│   ├── review_writer.py      Review file writer
│   ├── load_findings.py      Database loader
│   └── requirements.txt
├── docker-compose.yml        Local Postgres
└── .sdkmanrc                 Java version pin (SDKMAN)
```

---

## API Reference (brief)

| Endpoint | Description |
|---|---|
| `GET /api/supplements` | List all supplements with at least one finding |
| `GET /api/supplements/{id}` | Supplement detail with findings and citations |
| `GET /api/symptoms` | List all symptoms that have findings |
| `GET /api/symptoms/{slug}/supplements` | Supplements for a given symptom |

All endpoints are read-only. CORS is enabled for `localhost:5173` and `localhost:3000`.
