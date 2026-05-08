#!/usr/bin/env python3
"""Database loader — reads approved findings from a review file, inserts into Postgres.

Usage:
    python3 load_findings.py --review review_NAC_endometriosis_20250101_120000.md
    python3 load_findings.py --review review.md --db-url postgresql://endo:endo_secret@localhost:5432/endo_advice
"""

import argparse
import json
import re
import sys

import psycopg2
import psycopg2.extras

DEFAULT_DB_URL = "postgresql://endo:endo_secret@localhost:5432/endo_advice"


def parse_review_file(path: str) -> list[dict]:
    """Extract all approved JSON entries from the review markdown file."""
    content = open(path, encoding="utf-8").read()
    blocks = re.findall(r"```json\s*(.*?)\s*```", content, re.DOTALL)
    approved = []
    for block in blocks:
        try:
            entry = json.loads(block)
            if entry.get("approved") is True:
                approved.append(entry)
        except json.JSONDecodeError:
            continue
    return approved


def slug_from_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def load_findings(entries: list[dict], db_url: str) -> None:
    """Insert approved findings into Postgres. Enforces citation requirement."""
    if not entries:
        print("No approved findings to load.")
        return

    conn = psycopg2.connect(db_url)
    conn.autocommit = False
    cur = conn.cursor()

    inserted_findings = 0
    skipped = 0

    for entry in entries:
        supplement_name = entry["supplement"].strip().title()
        symptom_name = entry.get("suggested_symptom", "").strip().lower()
        claim = entry["claim"].strip()
        pmid = str(entry["pmid"]).strip()
        title = entry["title"].strip()
        authors = entry["authors"].strip()
        year = int(entry["year"])
        abstract_excerpt = entry["abstract_excerpt"].strip()

        if not pmid or not claim or not abstract_excerpt:
            print(f"  Skipping malformed entry: supplement={supplement_name}, pmid={pmid}")
            skipped += 1
            continue

        # Upsert supplement
        cur.execute(
            """
            INSERT INTO supplements (name, summary)
            VALUES (%s, %s)
            ON CONFLICT (name) DO NOTHING
            RETURNING id
            """,
            (supplement_name, f"Research findings for {supplement_name} in endometriosis/adenomyosis."),
        )
        row = cur.fetchone()
        if row:
            supplement_id = row[0]
        else:
            cur.execute("SELECT id FROM supplements WHERE name = %s", (supplement_name,))
            supplement_id = cur.fetchone()[0]

        # Insert finding
        cur.execute(
            """
            INSERT INTO findings (supplement_id, plain_language_summary, evidence_snapshot)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (supplement_id, claim, f"Source: {title} ({year})"),
        )
        finding_id = cur.fetchone()[0]

        # Insert citation (REQUIRED — enforces 2.6 constraint)
        cur.execute(
            """
            INSERT INTO citations (finding_id, pmid, title, authors, year, abstract_excerpt)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (finding_id, pmid) DO NOTHING
            """,
            (finding_id, pmid, title, authors, year, abstract_excerpt),
        )

        # Validate citation was inserted (application-layer enforcement of 2.6)
        cur.execute("SELECT COUNT(*) FROM citations WHERE finding_id = %s", (finding_id,))
        citation_count = cur.fetchone()[0]
        if citation_count == 0:
            conn.rollback()
            raise RuntimeError(
                f"Integrity error: finding {finding_id} has no citations — rolling back. "
                "Every finding must have at least one citation (spec: citation-integrity)."
            )

        # Upsert symptom and link to finding
        if symptom_name:
            slug = slug_from_name(symptom_name)
            cur.execute(
                """
                INSERT INTO symptoms (name, slug)
                VALUES (%s, %s)
                ON CONFLICT (slug) DO NOTHING
                RETURNING id
                """,
                (symptom_name.title(), slug),
            )
            row = cur.fetchone()
            if row:
                symptom_id = row[0]
            else:
                cur.execute("SELECT id FROM symptoms WHERE slug = %s", (slug,))
                symptom_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO finding_symptoms (finding_id, symptom_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                """,
                (finding_id, symptom_id),
            )

        inserted_findings += 1
        print(f"  ✓ Inserted finding for {supplement_name} / PMID {pmid}")

    conn.commit()
    cur.close()
    conn.close()
    print(f"\nLoaded {inserted_findings} findings. Skipped {skipped}.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Load approved pipeline findings into Postgres")
    parser.add_argument("--review", required=True, help="Path to review markdown file")
    parser.add_argument("--db-url", default=DEFAULT_DB_URL, help="Postgres connection URL")
    args = parser.parse_args()

    print(f"Parsing review file: {args.review}")
    entries = parse_review_file(args.review)
    print(f"Found {len(entries)} approved entries\n")

    load_findings(entries, args.db_url)


if __name__ == "__main__":
    main()
