CREATE TABLE supplement_symptom_summaries (
    supplement_id    BIGINT       NOT NULL REFERENCES supplements(id),
    symptom_id       BIGINT       NOT NULL REFERENCES symptoms(id),
    content          TEXT         NOT NULL,
    evidence_strength VARCHAR(20) NOT NULL,
    generated_at     TIMESTAMPTZ  NOT NULL DEFAULT now(),
    PRIMARY KEY (supplement_id, symptom_id)
);
