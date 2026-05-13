## Context

The frontend currently defines a small set of CSS custom properties in `index.css` for light and dark mode (text, bg, border, accent, etc.), but every component CSS file ignores them entirely and hardcodes Tailwind-like gray/purple hex values. In dark mode the page background switches to `#16171d` while cards, borders, and text remain light-mode colors — producing jarring white cards on a dark background.

## Goals / Non-Goals

**Goals:**
- A complete, semantically-named CSS token palette in `index.css` covering all color roles used across the app
- All component CSS files use only CSS custom properties — zero hardcoded hex colors (exception: the purple nav header, which is intentionally brand-fixed)
- Dark-mode values for all tokens that produce a soft, legible, low-strain dark theme
- No visual regression in light mode

**Non-Goals:**
- Introducing a CSS framework, design system library, or build-time tooling
- Adding a user-controlled theme toggle (system preference only)
- Changing layout, spacing, typography, or component structure
- Migrating to CSS-in-JS or Tailwind

## Decisions

### Decision 1: Expand tokens in `index.css`, keep single source of truth

All color tokens live in the `:root` block of `index.css`, with overrides in the existing `@media (prefers-color-scheme: dark)` block. Components never define their own color variables.

*Alternatives considered:*
- Per-component CSS variables: adds indirection with no benefit since there's no theming beyond light/dark
- Tailwind CSS: too large a migration for a CSS-only fix; adds build complexity

### Decision 2: Semantic token names, not scale names

Tokens are named by role (`--surface`, `--surface-raised`, `--text-muted`) rather than by color value (`--gray-200`, `--purple-500`). This makes the dark-mode swap straightforward without needing to rename tokens.

*Alternatives considered:*
- Scale-based naming (Tailwind style): would require cognitive mapping at every use site

### Decision 3: Token palette to add

New tokens (light → dark):

| Token | Light | Dark | Role |
|---|---|---|---|
| `--surface` | `#ffffff` | `#1f2028` | Card / panel background |
| `--surface-raised` | `#f9fafb` | `#252631` | Slightly elevated surface (pair-summary, citation bg) |
| `--surface-accent` | `#f5f3ff` | `#1e1730` | Light purple tint (overview sections, summary blocks) |
| `--surface-tag` | `#ede9fe` | `#2e1a4a` | Pill/tag background |
| `--text-muted` | `#6b7280` | `#9ca3af` | Secondary body text |
| `--text-secondary` | `#374151` | `#d1d5db` | Body text slightly below heading |
| `--text-tag` | `#6d28d9` | `#c084fc` | Tag label color (maps to `--accent` effectively) |
| `--badge-strong-bg` | `#dcfce7` | `#14532d` | Evidence badge: strong |
| `--badge-strong-text` | `#15803d` | `#86efac` | Evidence badge: strong text |
| `--badge-moderate-bg` | `#dbeafe` | `#1e3a5f` | Evidence badge: moderate |
| `--badge-moderate-text` | `#1d4ed8` | `#93c5fd` | Evidence badge: moderate text |
| `--badge-preliminary-bg` | `#fef9c3` | `#3d2e00` | Evidence badge: preliminary |
| `--badge-preliminary-text` | `#854d0e` | `#fde68a` | Evidence badge: preliminary text |
| `--badge-conflicting-bg` | `#fee2e2` | `#450a0a` | Evidence badge: conflicting |
| `--badge-conflicting-text` | `#b91c1c` | `#fca5a5` | Evidence badge: conflicting text |
| `--safety-bg` | `#fff7ed` | `#2d1e0f` | Safety callout background |
| `--safety-border` | `#f97316` | `#f97316` | Safety callout left border |
| `--safety-label` | `#c2410c` | `#fb923c` | Safety label text |
| `--input-border` | `#d1d5db` | `#3f4150` | Input border |

Existing tokens already cover: `--bg`, `--text`, `--text-h`, `--border`, `--accent`, `--accent-bg`, `--accent-border`, `--shadow`.

### Decision 4: Dark-mode surface hierarchy

Dark surfaces use a layered approach so the depth cue is preserved:
- Page background: `#16171d` (existing `--bg`)
- Cards/panels (`--surface`): `#1f2028` — slightly lighter than page
- Elevated (`--surface-raised`): `#252631` — one step above surface
- Accent tint (`--surface-accent`): `#1e1730` — warm purple-dark for branded sections

## Risks / Trade-offs

- **Duplication of badge tokens** → These are defined inline in two page CSS files today. Consolidating them into `index.css` tokens reduces duplication and makes them consistent. Risk: slight scope creep, but the alternative is two separate `@media` blocks in two files.
- **Purple nav header stays hardcoded** → The `#7c3aed` header is intentional brand color. It looks fine on both modes. Tokenising it risks accidental darkening.
- **No visual QA tool** → Changes must be manually checked in both light and dark modes. Mitigation: test in browser with `prefers-color-scheme: dark` devtools override before closing the task.

## Migration Plan

1. Add new tokens to `index.css` `:root` and dark-mode `@media` blocks
2. Update `Layout.css`
3. Update `SupplementCard.css`
4. Update `SupplementList.css`
5. Update `SymptomList.css`
6. Update `SupplementDetail.css`
7. Update `SymptomDetail.css`
8. Visual check in browser (both modes)

No backend changes. No data migration. Rollback = revert CSS files.

## Open Questions

None — approach is fully resolved.
