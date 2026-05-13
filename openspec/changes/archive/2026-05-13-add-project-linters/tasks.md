## 1. Backend Linting (ktlint)

- [x] 1.1 Add `jlleitschuh/ktlint-gradle` plugin to `backend/build.gradle.kts`
- [x] 1.2 Run `./gradlew ktlintFormat` to auto-fix existing formatting violations
- [x] 1.3 Manually resolve any remaining violations that ktlintFormat cannot fix
- [x] 1.4 Verify `./gradlew ktlintCheck` exits zero with no violations

## 2. Pipeline Linting (ruff)

- [x] 2.1 Add `ruff` (pinned version) to `pipeline/requirements.txt`
- [x] 2.2 Create `pipeline/pyproject.toml` with `[tool.ruff]` config (enable E, W, F rule sets; set `line-length = 88`)
- [x] 2.3 Run `ruff check --fix .` from inside `pipeline/` to auto-fix existing violations
- [x] 2.4 Manually resolve any remaining violations that ruff cannot auto-fix
- [x] 2.5 Verify `ruff check .` exits zero with no violations

## 3. Workflow Gate Update

- [x] 3.1 Add a **Linting** section to `CLAUDE.md` listing all three lint commands and stating they must pass before archiving
- [x] 3.2 Update the `verification-before-completion` skill to include the linting gate step with all three commands

## 4. Final Verification

- [x] 4.1 Run `./gradlew ktlintCheck` — confirm clean
- [x] 4.2 Run `npm run lint` from `frontend/` — confirm clean
- [x] 4.3 Run `ruff check .` from `pipeline/` — confirm clean
- [x] 4.4 Run `./gradlew test` from `backend/` — confirm tests still pass (pre-existing FlywayValidateException in contextLoads not introduced by this change)
