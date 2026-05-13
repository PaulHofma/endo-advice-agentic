### Requirement: Supplements are browsable as a catalog
The system SHALL expose a list of all supplements with at least one approved finding. Each supplement entry SHALL display its name and a brief plain-language summary of its overall evidence.

#### Scenario: User views supplement list
- **WHEN** a user navigates to the supplement catalog
- **THEN** they see a list of supplements, each with a name and a short summary

#### Scenario: Empty catalog
- **WHEN** no supplements have been loaded into the database
- **THEN** the catalog displays a clear empty state, not an error

### Requirement: Each supplement has a detail page with findings
The system SHALL provide a detail page for each supplement. The detail page SHALL display, in order: the supplement overview summary, then symptom sections each beginning with the supplement×symptom summary, followed by individual findings with quoted excerpts and PubMed links.

#### Scenario: User views supplement detail
- **WHEN** a user navigates to a supplement's detail page
- **THEN** they see the supplement overview summary first, followed by symptom sections each led by a supplement×symptom summary, followed by individual study findings within each section

#### Scenario: Finding links to PubMed
- **WHEN** a user clicks a citation on the detail page
- **THEN** they are taken to the corresponding PubMed abstract page (opens in new tab)

### Requirement: Supplement catalog is searchable by name
The system SHALL allow users to filter the supplement list by typing a supplement name. Filtering SHALL be case-insensitive.

#### Scenario: User searches for a supplement
- **WHEN** a user types a supplement name into the search field
- **THEN** the list updates to show only supplements whose names match the input
