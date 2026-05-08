CREATE TABLE finding_symptoms (
    finding_id BIGINT NOT NULL REFERENCES findings(id) ON DELETE CASCADE,
    symptom_id BIGINT NOT NULL REFERENCES symptoms(id) ON DELETE CASCADE,
    PRIMARY KEY (finding_id, symptom_id)
);

CREATE INDEX idx_finding_symptoms_symptom_id ON finding_symptoms(symptom_id);
