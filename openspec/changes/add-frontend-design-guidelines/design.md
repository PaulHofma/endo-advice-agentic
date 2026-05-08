## Context

`CLAUDE.md` is the authoritative source of project conventions for AI agents working on this codebase. It currently covers backend, pipeline, and general agent behaviour, but has no frontend section. The Copilot CLI exposes several skills and sub-agents specifically for frontend work; without documenting when to use them, they will be overlooked.

This change adds one focused section to `CLAUDE.md` — no code, schema, or tooling changes are needed.

## Goals / Non-Goals

**Goals:**
- Add a **Frontend conventions** section to `CLAUDE.md` that specifies exactly which skill or sub-agent to invoke for each frontend activity
- Make the conventions unambiguous: one activity → one tool

**Non-Goals:**
- Changing any frontend source code
- Adding new skills or sub-agents (we document existing ones only)
- Covering backend, pipeline, or infrastructure conventions (already documented)

## Decisions

### Put conventions in `CLAUDE.md`, not a separate file

`CLAUDE.md` is the single file AI agents read for project context. A separate `FRONTEND.md` would be ignored unless explicitly referenced. Keeping everything in one place guarantees discovery.

**Alternatives considered:**
- `frontend/CLAUDE.md` (subdirectory override): Works for directory-scoped agents but not for agents starting at the repo root — fragile.
- `docs/frontend-guidelines.md` + link from README: Requires the agent to follow a link; easier to miss.

### Document four distinct activity categories

Each maps to a different skill with different purposes:
| Activity | Tool |
|---|---|
| Visual design / polish / audit | `impeccable` skill |
| Accessibility & best-practice review | `web-design-guidelines` skill |
| Early-stage UI exploration / inspiration | `ui-design` skill |
| React feature implementation | `frontend-web-dev:expert-react-frontend-engineer` sub-agent |

This avoids overlap ambiguity — each tool has one clear trigger condition.

## Risks / Trade-offs

- [Skill availability] Skills listed in `CLAUDE.md` must be installed; if they're not, the convention is aspirational → Mitigation: skills are already present in `.github/skills/` or are built-in to the Copilot CLI.
- [Over-prescription] Forcing skill invocation for every small frontend edit adds friction → Mitigation: conventions specify *categories* of work (design, audit, implementation), not every file edit.
