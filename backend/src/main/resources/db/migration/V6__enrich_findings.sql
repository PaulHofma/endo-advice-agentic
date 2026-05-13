ALTER TABLE findings
    ADD COLUMN dosage            TEXT,
    ADD COLUMN duration          TEXT,
    ADD COLUMN study_type        VARCHAR(20),
    ADD COLUMN sample_size       INT,
    ADD COLUMN placebo_controlled BOOLEAN,
    ADD COLUMN safety_notes      TEXT;
