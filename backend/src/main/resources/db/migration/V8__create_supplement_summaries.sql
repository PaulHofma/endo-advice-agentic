CREATE TABLE supplement_summaries (
    supplement_id BIGINT      NOT NULL PRIMARY KEY REFERENCES supplements(id),
    content       TEXT        NOT NULL,
    generated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
