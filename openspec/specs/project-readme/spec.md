### Requirement: README exists at the repository root
The repository SHALL contain a `README.md` at the root that is the primary entry point for understanding the project.

#### Scenario: Developer opens the repository
- **WHEN** a developer navigates to the repository root
- **THEN** they find a `README.md` that explains the project purpose and intended audience

### Requirement: README covers local setup end-to-end
The README SHALL include step-by-step instructions to run all three components locally (Postgres via Docker, Spring Boot backend, React frontend).

#### Scenario: Developer follows setup instructions
- **WHEN** a developer follows the README setup steps from a fresh clone
- **THEN** they can start all components and reach the frontend in a browser

### Requirement: README documents the operator pipeline workflow
The README SHALL describe how to run the Python pipeline, review the output, and load approved findings into the database.

#### Scenario: Operator runs the pipeline
- **WHEN** the operator reads the pipeline section of the README
- **THEN** they can find the exact commands to run synthesis, review the output file, and load approved findings

### Requirement: README describes the architecture
The README SHALL include a brief architecture overview describing the three components and how they relate to each other.

#### Scenario: Developer reads architecture section
- **WHEN** a developer reads the architecture section
- **THEN** they understand the role of each component (pipeline, backend, frontend) and the data flow between them
