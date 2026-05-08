CREATE TABLE findings (
    id                     BIGSERIAL PRIMARY KEY,
    supplement_id          BIGINT       NOT NULL REFERENCES supplements(id) ON DELETE CASCADE,
    plain_language_summary TEXT         NOT NULL,
    evidence_snapshot      TEXT         NOT NULL,
    created_at             TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE INDEX idx_findings_supplement_id ON findings(supplement_id);
