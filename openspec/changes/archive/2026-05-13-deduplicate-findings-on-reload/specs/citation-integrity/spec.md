## MODIFIED Requirements

### Requirement: Every finding MUST have at least one verified PubMed citation
The system SHALL reject any attempt to load a finding into the database that does not have at least one associated citation with a valid PMID. This constraint SHALL be enforced at the database level. On upsert (when a finding with the same `supplement_id` and `pmid` already exists), the system SHALL verify that at least one citation remains associated after the operation.

#### Scenario: Finding loaded with valid citation
- **WHEN** a finding is loaded with a citation containing a non-null PMID
- **THEN** the finding is persisted successfully

#### Scenario: Finding loaded without citation
- **WHEN** an attempt is made to load a finding with no citations
- **THEN** the load operation fails with a clear error message

#### Scenario: Re-loaded finding retains citation
- **WHEN** a finding that already has a citation is re-loaded (upsert path)
- **THEN** the existing citation is preserved and the integrity check passes
