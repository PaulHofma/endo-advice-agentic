CREATE TABLE citations (
    id               BIGSERIAL PRIMARY KEY,
    finding_id       BIGINT       NOT NULL REFERENCES findings(id) ON DELETE CASCADE,
    pmid             VARCHAR(20)  NOT NULL,
    title            TEXT         NOT NULL,
    authors          TEXT         NOT NULL,
    year             INT          NOT NULL,
    abstract_excerpt TEXT         NOT NULL,
    CONSTRAINT uq_citations_finding_pmid UNIQUE (finding_id, pmid)
);

CREATE INDEX idx_citations_finding_id ON citations(finding_id);
