## ADDED Requirements

### Requirement: CLAUDE.md documents frontend skill conventions
`CLAUDE.md` SHALL contain a **Frontend conventions** section that specifies which Copilot CLI skill or sub-agent to invoke for each category of frontend work.

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
