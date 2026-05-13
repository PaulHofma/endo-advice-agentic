## 1. Backend Linting (ktlint)

- [ ] 1.1 Add `jlleitschuh/ktlint-gradle` plugin to `backend/build.gradle.kts`
- [ ] 1.2 Run `./gradlew ktlintFormat` to auto-fix existing formatting violations
- [ ] 1.3 Manually resolve any remaining violations that ktlintFormat cannot fix
- [ ] 1.4 Verify `./gradlew ktlintCheck` exits zero with no violations

## 2. Pipeline Linting (ruff)

- [ ] 2.1 Add `ruff` (pinned version) to `pipeline/requirements.txt`
- [ ] 2.2 Create `pipeline/pyproject.toml` with `[tool.ruff]` config (enable E, W, F rule sets; set `line-length = 88`)
- [ ] 2.3 Run `ruff check --fix .` from inside `pipeline/` to auto-fix existing violations
- [ ] 2.4 Manually resolve any remaining violations that ruff cannot auto-fix
- [ ] 2.5 Verify `ruff check .` exits zero with no violations

## 3. Workflow Gate Update

- [ ] 3.1 Add a **Linting** section to `CLAUDE.md` listing all three lint commands and stating they must pass before archiving
- [ ] 3.2 Update the `verification-before-completion` skill to include the linting gate step with all three commands

## 4. Final Verification

- [ ] 4.1 Run `./gradlew ktlintCheck` — confirm clean
- [ ] 4.2 Run `npm run lint` from `frontend/` — confirm clean
- [ ] 4.3 Run `ruff check .` from `pipeline/` — confirm clean
- [ ] 4.4 Run `./gradlew test` from `backend/` — confirm tests still pass
