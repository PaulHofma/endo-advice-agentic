## MODIFIED Requirements

### Requirement: README covers local setup end-to-end
The README SHALL include step-by-step instructions to run all three components locally (Postgres via Docker, Spring Boot backend, React frontend). The frontend section SHALL note that frontend development follows the agent conventions documented in `CLAUDE.md`.

#### Scenario: Developer follows setup instructions
- **WHEN** a developer follows the README setup steps from a fresh clone
- **THEN** they can start all components and reach the frontend in a browser, and they are directed to `CLAUDE.md` for frontend development conventions
