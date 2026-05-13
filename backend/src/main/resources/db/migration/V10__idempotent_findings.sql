-- Step 1: add pmid column (nullable initially to allow backfill)
ALTER TABLE findings ADD COLUMN pmid VARCHAR(20);

-- Step 2: backfill pmid from citations (one citation per finding in current data)
UPDATE findings f
SET pmid = (SELECT pmid FROM citations WHERE finding_id = f.id LIMIT 1);

-- Step 3: remove findings with no citations (citation-integrity violation — orphans from earlier bugs)
DELETE FROM findings WHERE pmid IS NULL;

-- Step 4: remove duplicate (supplement_id, pmid) rows, keeping the highest id (most recent load)
DELETE FROM findings
WHERE id NOT IN (
    SELECT MAX(id)
    FROM findings
    GROUP BY supplement_id, pmid
);

-- Step 5: enforce NOT NULL now that backfill is complete
ALTER TABLE findings ALTER COLUMN pmid SET NOT NULL;

-- Step 6: add unique constraint
ALTER TABLE findings ADD CONSTRAINT uq_findings_supplement_pmid UNIQUE (supplement_id, pmid);
