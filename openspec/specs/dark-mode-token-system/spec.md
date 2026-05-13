## ADDED Requirements

### Requirement: CSS custom property palette covers all color roles
`index.css` SHALL define a complete set of semantically-named CSS custom properties covering every color role used by any component, including surfaces, text hierarchy, semantic badges, safety callouts, citation blocks, input fields, and tag elements. Both light and dark values SHALL be defined.

#### Scenario: Dark mode applies without component changes
- **WHEN** the user's OS is set to dark mode
- **THEN** all component colors SHALL update automatically via CSS custom properties, with no white or near-white surfaces visible on the dark page background

#### Scenario: Light mode is visually unchanged
- **WHEN** the user's OS is set to light mode
- **THEN** the visual appearance SHALL be identical to the pre-change state

### Requirement: Component CSS uses only CSS custom properties for color
All component and page CSS files SHALL reference CSS custom properties from `index.css` for every color value. Hardcoded hex color literals are NOT permitted, except for the nav header background (`#7c3aed`) which is a fixed brand color.

#### Scenario: A developer adds a new component
- **WHEN** a developer writes a new CSS file for a component
- **THEN** they SHALL use an existing token from `index.css` for every color, or add a new token to `index.css` rather than hardcoding a hex value

#### Scenario: Code review of CSS file
- **WHEN** a CSS file is reviewed
- **THEN** the reviewer SHALL reject any PR that introduces a hardcoded hex color outside of `index.css`

### Requirement: Surface hierarchy conveys depth in dark mode
The dark-mode surface tokens SHALL form a clear visual depth hierarchy: page background < card surface < elevated surface < accent-tinted surface, each step being perceptibly distinct.

#### Scenario: Card on dark background
- **WHEN** a supplement card or finding card is rendered in dark mode
- **THEN** the card background SHALL be visibly lighter than the page background, creating a clear panel boundary without a harsh border

### Requirement: Evidence badges remain legible in dark mode
The four evidence badge variants (strong, moderate, preliminary, conflicting) SHALL each have dedicated background and text color tokens with adequate contrast in dark mode.

#### Scenario: Strong evidence badge in dark mode
- **WHEN** a finding with strong evidence is displayed in dark mode
- **THEN** the badge background SHALL be a dark green tint and the badge text SHALL be a light green, maintaining the semantic color association

#### Scenario: Moderate evidence badge in dark mode
- **WHEN** a finding with moderate evidence is displayed in dark mode
- **THEN** the badge background SHALL be a dark blue tint and the badge text SHALL be a light blue

#### Scenario: Preliminary evidence badge in dark mode
- **WHEN** a finding with preliminary evidence is displayed in dark mode
- **THEN** the badge background SHALL be a dark amber tint and the badge text SHALL be a light amber

#### Scenario: Conflicting evidence badge in dark mode
- **WHEN** a finding with conflicting evidence is displayed in dark mode
- **THEN** the badge background SHALL be a dark red tint and the badge text SHALL be a light red

### Requirement: Safety callouts remain visually prominent in dark mode
Safety callout blocks SHALL retain their orange left-border accent and readable text in dark mode, using darkened background and adjusted label color.

#### Scenario: Safety callout in dark mode
- **WHEN** a finding with a safety note is displayed in dark mode
- **THEN** the callout SHALL have a dark warm background, an orange left border, and legible orange-toned label text
