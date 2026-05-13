## Why

The frontend is in early development and there are no documented conventions for when to apply design skills or follow web design principles. Without this, AI-assisted frontend work risks skipping quality checks — producing functional but visually mediocre or inaccessible UI. Adding these conventions to `CLAUDE.md` ensures they're applied consistently from the start.

## What Changes

- Add a **Frontend conventions** section to `CLAUDE.md` documenting which skills to invoke for frontend work:
  - `impeccable` skill: for any UI design, redesign, polish, audit, or visual improvement work
  - `web-design-guidelines` skill: for accessibility audits and compliance checks against web best practices
  - `ui-design` skill: for early-stage UI exploration and generating design inspiration
  - `frontend-web-dev:expert-react-frontend-engineer` sub-agent: for React 19 feature implementation
- Document the *when* for each skill so it's unambiguous which tool to reach for

## Capabilities

### New Capabilities
- `agent-conventions-frontend`: Documents the required skills and sub-agents to invoke for frontend design and implementation work, codified in `CLAUDE.md`

### Modified Capabilities
- `project-readme`: The README's Frontend section SHALL note that frontend work follows agent conventions in `CLAUDE.md`

## Impact

- `CLAUDE.md`: New "Frontend conventions" section added
- `README.md`: Minor note added to frontend section pointing to `CLAUDE.md`
- No code, schema, or dependency changes
