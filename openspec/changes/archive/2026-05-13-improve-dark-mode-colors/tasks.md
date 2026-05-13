## 1. Expand CSS token palette in index.css

- [x] 1.1 Add `--surface`, `--surface-raised`, `--surface-accent`, `--surface-tag` tokens with light values to `:root` in `index.css`
- [x] 1.2 Add `--text-muted`, `--text-secondary`, `--text-tag` tokens with light values to `:root` in `index.css`
- [x] 1.3 Add evidence badge tokens (`--badge-strong-bg/text`, `--badge-moderate-bg/text`, `--badge-preliminary-bg/text`, `--badge-conflicting-bg/text`) to `:root`
- [x] 1.4 Add `--safety-bg`, `--safety-border`, `--safety-label` tokens to `:root`
- [x] 1.5 Add `--input-border` token to `:root`
- [x] 1.6 Add dark-mode overrides for all new tokens in the `@media (prefers-color-scheme: dark)` block

## 2. Update component and layout CSS

- [x] 2.1 Replace hardcoded colors in `Layout.css` with CSS custom properties
- [x] 2.2 Replace hardcoded colors in `SupplementCard.css` with CSS custom properties
- [x] 2.3 Replace hardcoded colors in `SupplementList.css` with CSS custom properties
- [x] 2.4 Replace hardcoded colors in `SymptomList.css` with CSS custom properties
- [x] 2.5 Replace hardcoded colors in `SupplementDetail.css` with CSS custom properties (includes evidence badges, safety callout, citation block, symptom tags)
- [x] 2.6 Replace hardcoded colors in `SymptomDetail.css` with CSS custom properties (includes evidence badges, safety callout, citation block)

## 3. Update CLAUDE.md

- [x] 3.1 Add CSS token convention to the Frontend conventions section in `CLAUDE.md`: all component CSS MUST use custom properties from `index.css`, no hardcoded hex colors

## 4. Visual verification

- [x] 4.1 Start dev server and verify light mode appearance is unchanged across all pages (Supplement list, Supplement detail, Symptom list, Symptom detail)
- [x] 4.2 Toggle browser to dark mode (DevTools → Rendering → prefers-color-scheme: dark) and verify all pages render with soft dark surfaces, legible text, and correct badge/callout colors
- [x] 4.3 Confirm no white or near-white card backgrounds appear on the dark page background
