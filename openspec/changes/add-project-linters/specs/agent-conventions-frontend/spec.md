## ADDED Requirements

### Requirement: CLAUDE.md documents the linting gate as a change-completion prerequisite
`CLAUDE.md` SHALL contain a **Linting** section that lists the three lint commands (BE, FE, pipeline) and states that all must pass clean before a change may be archived.

#### Scenario: Agent is about to archive a change
- **WHEN** an agent is preparing to archive a change (run `/opsx:archive` or equivalent)
- **THEN** it SHALL first run all three lint commands and confirm each exits zero before proceeding

#### Scenario: Developer reads the linting section
- **WHEN** a developer opens `CLAUDE.md` and reads the Linting section
- **THEN** they can identify the exact command to run for each layer (BE, FE, pipeline) without ambiguity

### Requirement: verification-before-completion skill enforces the linting gate
The `verification-before-completion` skill SHALL include linting as an explicit required step, specifying all three commands, before any change is declared complete.

#### Scenario: Agent invokes the verification skill before completing work
- **WHEN** an agent invokes the `verification-before-completion` skill
- **THEN** the skill requires the agent to run `./gradlew ktlintCheck` (backend), `npm run lint` (frontend), and `ruff check .` (pipeline) and confirm all three pass before the change is marked done
