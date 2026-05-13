"""Summarisation stage — generates three tiers of AI summaries from loaded findings.

Reads from the database, generates summaries with Claude, and upserts results.
Full-replace semantics: all existing summaries are deleted on each run.

Can be run standalone:
    python3 summarise.py
    python3 summarise.py --db-url postgresql://endo:endo_secret@localhost:6543/endo_advice
"""

import argparse
import json
import os
import time

import anthropic
import psycopg2
import psycopg2.extras

DEFAULT_DB_URL = "postgresql://endo:endo_secret@localhost:6543/endo_advice"
CLAUDE_MODEL = "claude-haiku-4-5"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run(db_url: str = DEFAULT_DB_URL) -> None:
    """Orchestrate all three summary generation stages (full-replace)."""
    print("[summarise] Connecting to database...")
    conn = psycopg2.connect(db_url)
    conn.autocommit = False

    client = anthropic.Anthropic(api_key=os.environ["ENDO_API_KEY"])

    try:
        _delete_all_summaries(conn)
        pair_summaries = _generate_supplement_symptom_summaries(conn, client)
        _generate_supplement_summaries(conn, pair_summaries, client)
        _generate_symptom_summaries(conn, pair_summaries, client)
        conn.commit()
        print("[summarise] All summaries committed.")
    except Exception as e:
        conn.rollback()
        print(f"[summarise] ERROR — rolled back: {e}")
        raise
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Stage 0: full-replace delete
# ---------------------------------------------------------------------------

def _delete_all_summaries(conn) -> None:
    cur = conn.cursor()
    cur.execute("DELETE FROM symptom_summaries")
    cur.execute("DELETE FROM supplement_summaries")
    cur.execute("DELETE FROM supplement_symptom_summaries")
    cur.close()
    print("[summarise] Cleared existing summaries.")


# ---------------------------------------------------------------------------
# Stage 1: supplement × symptom pair summaries
# ---------------------------------------------------------------------------

def _generate_supplement_symptom_summaries(conn, client) -> list[dict]:
    """Generate one summary per supplement×symptom pair that has findings."""
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("""
        SELECT DISTINCT
            s.id   AS supplement_id,
            s.name AS supplement_name,
            sy.id  AS symptom_id,
            sy.name AS symptom_name
        FROM supplements s
        JOIN findings f ON f.supplement_id = s.id
        JOIN finding_symptoms fs ON fs.finding_id = f.id
        JOIN symptoms sy ON sy.id = fs.symptom_id
        ORDER BY s.name, sy.name
    """)
    pairs = cur.fetchall()
    print(f"[summarise] Generating pair summaries for {len(pairs)} supplement×symptom pairs...")

    results = []

    for pair in pairs:
        sup_id = pair["supplement_id"]
        sym_id = pair["symptom_id"]
        sup_name = pair["supplement_name"]
        sym_name = pair["symptom_name"]

        cur.execute("""
            SELECT
                f.plain_language_summary,
                f.dosage, f.duration, f.study_type, f.sample_size,
                f.placebo_controlled, f.safety_notes
            FROM findings f
            JOIN finding_symptoms fs ON fs.finding_id = f.id
            WHERE f.supplement_id = %s AND fs.symptom_id = %s
        """, (sup_id, sym_id))
        findings = cur.fetchall()

        findings_text = "\n\n".join(
            _format_finding(i + 1, f) for i, f in enumerate(findings)
        )

        prompt = f"""You are a medical evidence synthesizer for endometriosis research.

Supplement: {sup_name}
Symptom: {sym_name}

Research findings ({len(findings)} total):
{findings_text}

Write a 2-4 sentence plain-language synthesis of all findings above. Then output an evidence_strength rating.

Rules:
- Summarise what the research collectively shows, noting dosage range and study quality where available
- Be honest about limitations (e.g. "one small study", "preliminary evidence only")
- Do NOT overstate; match language to evidence strength
- Return JSON only with two keys: "content" (the synthesis text) and "evidence_strength" (one of: strong, moderate, preliminary, conflicting)

Example:
{{"content": "Two small RCTs suggest NAC may reduce endometrioma size when taken for 3 months at 600mg three times daily, though sample sizes were limited.", "evidence_strength": "preliminary"}}"""

        time.sleep(0.4)
        try:
            response = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}],
            )
            data = _parse_json_response(response.content[0].text.strip())
            content = data["content"]
            evidence_strength = data["evidence_strength"]
        except Exception as e:
            print(f"[summarise] Warning: failed to generate pair summary for {sup_name}×{sym_name}: {e}")
            content = f"Research findings are available for {sup_name} in relation to {sym_name}."
            evidence_strength = "preliminary"

        cur.execute("""
            INSERT INTO supplement_symptom_summaries
                (supplement_id, symptom_id, content, evidence_strength)
            VALUES (%s, %s, %s, %s)
        """, (sup_id, sym_id, content, evidence_strength))

        results.append({
            "supplement_id": sup_id,
            "supplement_name": sup_name,
            "symptom_id": sym_id,
            "symptom_name": sym_name,
            "content": content,
            "evidence_strength": evidence_strength,
        })
        print(f"[summarise]   ✓ {sup_name} × {sym_name} ({evidence_strength})")

    cur.close()
    return results


# ---------------------------------------------------------------------------
# Stage 2: supplement overview summaries
# ---------------------------------------------------------------------------

def _generate_supplement_summaries(conn, pair_summaries: list[dict], client) -> None:
    """Generate one overview summary per supplement."""
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT id, name FROM supplements ORDER BY name")
    supplements = cur.fetchall()
    print(f"[summarise] Generating supplement summaries for {len(supplements)} supplements...")

    for sup in supplements:
        sup_id = sup["id"]
        sup_name = sup["name"]

        pairs_for_sup = [p for p in pair_summaries if p["supplement_id"] == sup_id]

        if not pairs_for_sup:
            prompt = f"""You are a medical evidence synthesizer for endometriosis research.

Supplement: {sup_name}

No verified research findings were found for {sup_name} in the current database.

Write 1-2 sentences clearly stating that no evidence is currently available, without being dismissive.
Return JSON with one key: "content" (the summary text)."""
        else:
            pairs_text = "\n\n".join(
                f"Symptom: {p['symptom_name']}\nSummary: {p['content']}\nEvidence strength: {p['evidence_strength']}"
                for p in pairs_for_sup
            )
            prompt = f"""You are a medical evidence synthesizer for endometriosis research.

Supplement: {sup_name}

Per-symptom evidence summaries:
{pairs_text}

Write 3-5 sentences giving an overall picture of the evidence for {sup_name} in endometriosis/adenomyosis research.
Highlight which symptoms have the strongest evidence and where findings are most limited.
Return JSON with one key: "content" (the summary text)."""

        time.sleep(0.4)
        try:
            response = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}],
            )
            content = _parse_json_response(response.content[0].text.strip())["content"]
        except Exception as e:
            print(f"[summarise] Warning: failed to generate supplement summary for {sup_name}: {e}")
            content = f"Research summary for {sup_name} could not be generated at this time."

        cur.execute("""
            INSERT INTO supplement_summaries (supplement_id, content)
            VALUES (%s, %s)
        """, (sup_id, content))
        print(f"[summarise]   ✓ Supplement summary: {sup_name}")

    cur.close()


# ---------------------------------------------------------------------------
# Stage 3: symptom overview summaries
# ---------------------------------------------------------------------------

def _generate_symptom_summaries(conn, pair_summaries: list[dict], client) -> None:
    """Generate one overview summary per symptom that has at least one pair summary."""
    if not pair_summaries:
        return

    symptom_ids = list({p["symptom_id"] for p in pair_summaries})

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT id, name FROM symptoms WHERE id = ANY(%s) ORDER BY name", (symptom_ids,))
    symptoms = cur.fetchall()
    print(f"[summarise] Generating symptom summaries for {len(symptoms)} symptoms...")

    for sym in symptoms:
        sym_id = sym["id"]
        sym_name = sym["name"]

        pairs_for_sym = [p for p in pair_summaries if p["symptom_id"] == sym_id]
        pairs_text = "\n\n".join(
            f"Supplement: {p['supplement_name']}\nSummary: {p['content']}\nEvidence strength: {p['evidence_strength']}"
            for p in pairs_for_sym
        )

        prompt = f"""You are a medical evidence synthesizer for endometriosis research.

Symptom: {sym_name}

Per-supplement evidence summaries:
{pairs_text}

Write 3-5 sentences summarising the supplement evidence landscape for {sym_name}.
Help readers understand which supplements have the most evidence and which are more exploratory.
Return JSON with one key: "content" (the summary text)."""

        time.sleep(0.4)
        try:
            response = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}],
            )
            content = _parse_json_response(response.content[0].text.strip())["content"]
        except Exception as e:
            print(f"[summarise] Warning: failed to generate symptom summary for {sym_name}: {e}")
            content = f"Research summary for {sym_name} could not be generated at this time."

        cur.execute("""
            INSERT INTO symptom_summaries (symptom_id, content)
            VALUES (%s, %s)
        """, (sym_id, content))
        print(f"[summarise]   ✓ Symptom summary: {sym_name}")

    cur.close()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_json_response(raw: str) -> dict:
    """Strip optional markdown fences and parse JSON from a Claude response."""
    if raw.startswith("```"):
        raw = raw[3:]  # strip opening ```
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.rsplit("```", 1)[0]
    return json.loads(raw.strip())


def _format_finding(n: int, f) -> str:
    parts = [f"Finding {n}: {f['plain_language_summary']}"]
    if f["study_type"]:
        parts.append(f"Study type: {f['study_type']}")
    if f["sample_size"]:
        parts.append(f"Sample size: n={f['sample_size']}")
    if f["dosage"]:
        parts.append(f"Dosage: {f['dosage']}")
    if f["duration"]:
        parts.append(f"Duration: {f['duration']}")
    if f["placebo_controlled"] is not None:
        parts.append(f"Placebo-controlled: {f['placebo_controlled']}")
    if f["safety_notes"]:
        parts.append(f"Safety notes: {f['safety_notes']}")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the summarisation stage standalone")
    parser.add_argument("--db-url", default=DEFAULT_DB_URL)
    args = parser.parse_args()

    if not os.environ.get("ENDO_API_KEY"):
        import sys
        print("Error: ENDO_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    run(db_url=args.db_url)
