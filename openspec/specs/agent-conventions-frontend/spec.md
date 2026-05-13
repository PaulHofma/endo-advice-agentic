## ADDED Requirements

### Requirement: CLAUDE.md documents frontend skill conventions
`CLAUDE.md` SHALL contain a **Frontend conventions** section that specifies which Copilot CLI skill or sub-agent to invoke for each category of frontend work. It SHALL also document that all CSS color values MUST use CSS custom properties from `index.css` — hardcoded hex colors are not permitted in component CSS files.

#### Scenario: Agent starts UI design or polish work
- **WHEN** an agent is about to create, redesign, audit, or polish any frontend UI
- **THEN** it SHALL invoke the `impeccable` skill before writing or modifying component code

#### Scenario: Agent performs an accessibility or best-practice review
- **WHEN** an agent is asked to review UI code for accessibility, design quality, or web best practices
- **THEN** it SHALL invoke the `web-design-guidelines` skill

#### Scenario: Agent explores early-stage UI ideas
- **WHEN** an agent is generating UI inspiration or exploring layout options before committing to an implementation
- **THEN** it SHALL invoke the `ui-design` skill

#### Scenario: Agent implements a React feature
- **WHEN** an agent is implementing frontend features, components, hooks, or TypeScript logic
- **THEN** it SHALL use the `frontend-web-dev:expert-react-frontend-engineer` sub-agent

#### Scenario: Developer reads the conventions section
- **WHEN** a developer opens `CLAUDE.md` and reads the Frontend conventions section
- **THEN** they can identify the correct tool for any frontend task without ambiguity

#### Scenario: Agent writes new component CSS
- **WHEN** an agent writes CSS for a new or existing component
- **THEN** it SHALL use CSS custom properties from `index.css` for all color values and SHALL NOT introduce hardcoded hex colors

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
