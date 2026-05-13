## Why

All component CSS files use hardcoded light-mode hex colors, so dark mode renders harsh white-background cards and light surfaces on a dark page background — the `@media (prefers-color-scheme: dark)` tokens defined in `index.css` are simply never used by any component. The result is an uncomfortable contrast mismatch throughout the app.

## What Changes

- Expand the CSS custom property palette in `index.css` to cover all color roles used across components (surfaces, muted text, accent tints, semantic badges, safety callouts, citation blocks)
- Replace every hardcoded hex color in all component CSS files (`Layout.css`, `SupplementCard.css`, `SupplementList.css`, `SymptomList.css`, `SupplementDetail.css`, `SymptomDetail.css`) with the appropriate custom property
- Provide well-tuned dark-mode values for all new tokens in the existing `@media (prefers-color-scheme: dark)` block

## Capabilities

### New Capabilities
- `dark-mode-token-system`: A complete, semantically-named CSS custom property system that drives both light and dark themes across all UI components from a single source of truth in `index.css`

### Modified Capabilities
- `agent-conventions-frontend`: Frontend color system is now token-based; all new components must use CSS custom properties, not hardcoded hex values

## Impact

- `frontend/src/index.css` — new/updated custom property definitions
- `frontend/src/components/Layout.css` — hardcoded colors replaced with tokens
- `frontend/src/components/SupplementCard.css` — hardcoded colors replaced with tokens
- `frontend/src/pages/SupplementList.css` — hardcoded colors replaced with tokens
- `frontend/src/pages/SymptomList.css` — hardcoded colors replaced with tokens
- `frontend/src/pages/SupplementDetail.css` — hardcoded colors replaced with tokens
- `frontend/src/pages/SymptomDetail.css` — hardcoded colors replaced with tokens
- No API or backend changes; purely visual/CSS
