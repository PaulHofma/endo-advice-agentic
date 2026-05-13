## ADDED Requirements

### Requirement: ktlint is configured as a Gradle task
The backend Gradle build SHALL include the `jlleitschuh/ktlint-gradle` plugin, exposing `ktlintCheck` and `ktlintFormat` tasks for all Kotlin source sets.

#### Scenario: Developer checks for lint violations
- **WHEN** a developer runs `./gradlew ktlintCheck` from the `backend/` directory
- **THEN** the task exits zero if all Kotlin sources conform to the standard ktlint ruleset, or exits non-zero and prints each violation with file and line number

#### Scenario: Developer auto-fixes formatting
- **WHEN** a developer runs `./gradlew ktlintFormat` from the `backend/` directory
- **THEN** ktlint rewrites all fixable formatting issues in-place and reports any remaining violations that require manual attention

### Requirement: Existing backend code is lint-clean at the time of rollout
All Kotlin source files in `backend/src/` SHALL conform to the ktlint ruleset before this change is archived.

#### Scenario: Agent verifies lint cleanliness before archiving
- **WHEN** an agent runs `./gradlew ktlintCheck` as part of the pre-archive gate
- **THEN** the command exits zero with no violations reported
