#!/usr/bin/env python3
"""Database loader — reads approved findings from a review file, inserts into Postgres.

Usage:
    python3 load_findings.py --review review_NAC_endometriosis_20250101_120000.md
    python3 load_findings.py --review review.md --db-url postgresql://endo:endo_secret@localhost:6543/endo_advice
"""

import argparse
import json
import re

import psycopg2
import psycopg2.extras

DEFAULT_DB_URL = "postgresql://endo:endo_secret@localhost:6543/endo_advice"


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
        dosage = entry.get("dosage") or None
        duration = entry.get("duration") or None
        study_type = entry.get("study_type") or None
        sample_size = int(entry["sample_size"]) if entry.get("sample_size") is not None else None
        placebo_controlled = entry.get("placebo_controlled")
        safety_notes = entry.get("safety_notes") or None

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

        # Upsert finding — ON CONFLICT updates all pipeline-derived columns so re-runs refresh stale data
        cur.execute(
            """
            INSERT INTO findings (
                supplement_id, pmid, plain_language_summary, evidence_snapshot,
                dosage, duration, study_type, sample_size, placebo_controlled, safety_notes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (supplement_id, pmid) DO UPDATE SET
                plain_language_summary = EXCLUDED.plain_language_summary,
                evidence_snapshot = EXCLUDED.evidence_snapshot,
                dosage = EXCLUDED.dosage,
                duration = EXCLUDED.duration,
                study_type = EXCLUDED.study_type,
                sample_size = EXCLUDED.sample_size,
                placebo_controlled = EXCLUDED.placebo_controlled,
                safety_notes = EXCLUDED.safety_notes
            RETURNING id
            """,
            (supplement_id, pmid, claim, f"Source: {title} ({year})",
             dosage, duration, study_type, sample_size, placebo_controlled, safety_notes),
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
        print(f"  ✓ Upserted finding for {supplement_name} / PMID {pmid}")

    conn.commit()
    cur.close()
    conn.close()
    print(f"\nLoaded {inserted_findings} findings. Skipped {skipped}.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Load approved pipeline findings into Postgres")
    parser.add_argument("--review", required=True, help="Path to review markdown file")
    parser.add_argument("--db-url", default=DEFAULT_DB_URL, help="Postgres connection URL")
    parser.add_argument("--skip-summarise", action="store_true", help="Skip the summarisation stage after loading")
    args = parser.parse_args()

    print(f"Parsing review file: {args.review}")
    entries = parse_review_file(args.review)
    print(f"Found {len(entries)} approved entries\n")

    load_findings(entries, args.db_url)

    if not args.skip_summarise:
        print("\n=== Running summarisation stage ===")
        from summarise import run as run_summarise
        run_summarise(db_url=args.db_url)
        print("\nSummarisation complete.")
        _append_summaries_to_review(args.review, args.db_url)


def _append_summaries_to_review(review_path: str, db_url: str) -> None:
    """Append generated summaries to the review file for operator inspection."""
    import psycopg2
    import psycopg2.extras

    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute("""
            SELECT s.name AS supplement, sy.name AS symptom,
                   sss.content, sss.evidence_strength
            FROM supplement_symptom_summaries sss
            JOIN supplements s ON s.id = sss.supplement_id
            JOIN symptoms sy ON sy.id = sss.symptom_id
            ORDER BY s.name, sy.name
        """)
        pairs = cur.fetchall()

        cur.execute("""
            SELECT s.name, ss.content
            FROM supplement_summaries ss
            JOIN supplements s ON s.id = ss.supplement_id
            ORDER BY s.name
        """)
        sup_summaries = cur.fetchall()

        cur.execute("""
            SELECT sy.name, ys.content
            FROM symptom_summaries ys
            JOIN symptoms sy ON sy.id = ys.symptom_id
            ORDER BY sy.name
        """)
        sym_summaries = cur.fetchall()
        cur.close()
        conn.close()

        lines = [
            "\n\n---\n",
            "## Generated Summaries\n\n",
            "### Supplement × Symptom Pair Summaries\n\n",
        ]
        for p in pairs:
            lines.append(f"**{p['supplement']} × {p['symptom']}** `{p['evidence_strength']}`\n")
            lines.append(f"{p['content']}\n\n")

        lines.append("### Supplement Overview Summaries\n\n")
        for s in sup_summaries:
            lines.append(f"**{s['name']}**\n{s['content']}\n\n")

        lines.append("### Symptom Overview Summaries\n\n")
        for s in sym_summaries:
            lines.append(f"**{s['name']}**\n{s['content']}\n\n")

        with open(review_path, "a", encoding="utf-8") as f:
            f.writelines(lines)

        print(f"Summaries appended to {review_path}")
    except Exception as e:
        print(f"Warning: could not append summaries to review file: {e}")


if __name__ == "__main__":
    main()
