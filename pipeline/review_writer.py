"""Review file writer — produces a human-readable review file grouped by verdict."""

import json
from pathlib import Path

from verification import VerifiedFinding, Verdict


def write_review_file(findings: list[VerifiedFinding], output_path: str) -> None:
    """Write a human-readable review file. Operator edits this before loading to DB."""
    verified = [f for f in findings if f.verdict == Verdict.VERIFIED]
    flagged = [f for f in findings if f.verdict == Verdict.FLAGGED]
    rejected = [f for f in findings if f.verdict == Verdict.REJECTED]

    lines = [
        "# Pipeline Review File",
        "",
        f"Total findings: {len(findings)} | Verified: {len(verified)} | Flagged: {len(flagged)} | Rejected: {len(rejected)}",
        "",
        "## Instructions",
        "- Mark `approved: true` on findings you want to load into the database.",
        "- You may edit the `claim` field to correct wording.",
        "- Rejected findings are excluded by default — change `approved` to true to override.",
        "- Save this file, then run: `python3 load_findings.py --review <path>`",
        "",
    ]

    for section_label, section_findings in [
        ("✅ VERIFIED", verified),
        ("⚠️  FLAGGED", flagged),
        ("❌ REJECTED", rejected),
    ]:
        lines.append(f"## {section_label} ({len(section_findings)})")
        lines.append("")
        if not section_findings:
            lines.append("*(none)*")
            lines.append("")
            continue

        for f in section_findings:
            default_approved = f.verdict == Verdict.VERIFIED
            entry = {
                "approved": default_approved,
                "supplement": f.raw.supplement_name,
                "claim": f.raw.claim,
                "pmid": f.raw.pmid,
                "title": f.raw.article.title,
                "authors": f.raw.article.authors,
                "year": f.raw.article.year,
                "abstract_excerpt": f.verified_excerpt or f.raw.abstract_excerpt,
                "suggested_symptom": f.raw.suggested_symptom,
                "verdict": f.verdict.value,
                "reason": f.reason,
            }
            lines.append("```json")
            lines.append(json.dumps(entry, indent=2, ensure_ascii=False))
            lines.append("```")
            lines.append("")

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"[writer] Review file written to: {output_path}")
    print(f"[writer] {len(verified)} verified (auto-approved), {len(flagged)} flagged, {len(rejected)} rejected")
