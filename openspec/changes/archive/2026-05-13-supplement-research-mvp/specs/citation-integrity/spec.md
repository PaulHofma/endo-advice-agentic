## ADDED Requirements

### Requirement: Every finding MUST have at least one verified PubMed citation
The system SHALL reject any attempt to load a finding into the database that does not have at least one associated citation with a valid PMID. This constraint SHALL be enforced at the database level.

#### Scenario: Finding loaded with valid citation
- **WHEN** a finding is loaded with a citation containing a non-null PMID
- **THEN** the finding is persisted successfully

#### Scenario: Finding loaded without citation
- **WHEN** an attempt is made to load a finding with no citations
- **THEN** the load operation fails with a clear error message

### Requirement: Citations store a quoted excerpt from the source abstract
Each citation SHALL include a short quoted excerpt from the actual PubMed abstract that supports the associated finding. The excerpt SHALL be set by the synthesis agent and validated by the verification agent.

#### Scenario: Citation has excerpt
- **WHEN** a citation is displayed to a user
- **THEN** the quoted excerpt is shown alongside the PMID link

### Requirement: PubMed links are constructed from PMID and are directly accessible
All PubMed links displayed to users SHALL use the canonical PMID URL format (`https://pubmed.ncbi.nlm.nih.gov/<PMID>/`). Links SHALL open in a new browser tab.

#### Scenario: User follows a citation link
- **WHEN** a user clicks a citation link
- **THEN** the browser opens the PubMed abstract page in a new tab at the correct URL
