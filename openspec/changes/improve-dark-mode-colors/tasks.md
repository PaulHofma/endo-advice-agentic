## 1. Expand CSS token palette in index.css

- [ ] 1.1 Add `--surface`, `--surface-raised`, `--surface-accent`, `--surface-tag` tokens with light values to `:root` in `index.css`
- [ ] 1.2 Add `--text-muted`, `--text-secondary`, `--text-tag` tokens with light values to `:root` in `index.css`
- [ ] 1.3 Add evidence badge tokens (`--badge-strong-bg/text`, `--badge-moderate-bg/text`, `--badge-preliminary-bg/text`, `--badge-conflicting-bg/text`) to `:root`
- [ ] 1.4 Add `--safety-bg`, `--safety-border`, `--safety-label` tokens to `:root`
- [ ] 1.5 Add `--input-border` token to `:root`
- [ ] 1.6 Add dark-mode overrides for all new tokens in the `@media (prefers-color-scheme: dark)` block

## 2. Update component and layout CSS

- [ ] 2.1 Replace hardcoded colors in `Layout.css` with CSS custom properties
- [ ] 2.2 Replace hardcoded colors in `SupplementCard.css` with CSS custom properties
- [ ] 2.3 Replace hardcoded colors in `SupplementList.css` with CSS custom properties
- [ ] 2.4 Replace hardcoded colors in `SymptomList.css` with CSS custom properties
- [ ] 2.5 Replace hardcoded colors in `SupplementDetail.css` with CSS custom properties (includes evidence badges, safety callout, citation block, symptom tags)
- [ ] 2.6 Replace hardcoded colors in `SymptomDetail.css` with CSS custom properties (includes evidence badges, safety callout, citation block)

## 3. Update CLAUDE.md

- [ ] 3.1 Add CSS token convention to the Frontend conventions section in `CLAUDE.md`: all component CSS MUST use custom properties from `index.css`, no hardcoded hex colors

## 4. Visual verification

- [ ] 4.1 Start dev server and verify light mode appearance is unchanged across all pages (Supplement list, Supplement detail, Symptom list, Symptom detail)
- [ ] 4.2 Toggle browser to dark mode (DevTools → Rendering → prefers-color-scheme: dark) and verify all pages render with soft dark surfaces, legible text, and correct badge/callout colors
- [ ] 4.3 Confirm no white or near-white card backgrounds appear on the dark page background
