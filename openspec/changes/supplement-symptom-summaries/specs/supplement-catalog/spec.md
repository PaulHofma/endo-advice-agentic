## MODIFIED Requirements

### Requirement: Each supplement has a detail page with findings
The system SHALL provide a detail page for each supplement. The detail page SHALL display, in order: the supplement overview summary, then symptom sections each beginning with the supplement×symptom summary, followed by individual findings with quoted excerpts and PubMed links.

#### Scenario: User views supplement detail
- **WHEN** a user navigates to a supplement's detail page
- **THEN** they see the supplement overview summary first, followed by symptom sections each led by a supplement×symptom summary, followed by individual study findings within each section

#### Scenario: Finding links to PubMed
- **WHEN** a user clicks a citation on the detail page
- **THEN** they are taken to the corresponding PubMed abstract page (opens in new tab)
