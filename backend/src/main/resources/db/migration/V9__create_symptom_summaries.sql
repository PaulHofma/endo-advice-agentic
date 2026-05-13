CREATE TABLE symptom_summaries (
    symptom_id   BIGINT      NOT NULL PRIMARY KEY REFERENCES symptoms(id),
    content      TEXT        NOT NULL,
    generated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
