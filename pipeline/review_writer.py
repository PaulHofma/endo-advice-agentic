"""Review file writer — produces a human-readable review file grouped by verdict."""

import json
from pathlib import Path

from verification import VerifiedFinding, Verdict


def _finding_entry(f: VerifiedFinding) -> dict:
    return {
        "approved": f.verdict == Verdict.VERIFIED,
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


def _write_verdict_sections(lines: list[str], findings: list[VerifiedFinding]) -> None:
    verified = [f for f in findings if f.verdict == Verdict.VERIFIED]
    flagged = [f for f in findings if f.verdict == Verdict.FLAGGED]
    rejected = [f for f in findings if f.verdict == Verdict.REJECTED]
    for section_label, section_findings in [
        ("✅ VERIFIED", verified),
        ("⚠️  FLAGGED", flagged),
        ("❌ REJECTED", rejected),
    ]:
        lines.append(f"### {section_label} ({len(section_findings)})")
        lines.append("")
        if not section_findings:
            lines.append("*(none)*")
            lines.append("")
            continue
        for f in section_findings:
            lines.append("```json")
            lines.append(json.dumps(_finding_entry(f), indent=2, ensure_ascii=False))
            lines.append("```")
            lines.append("")


def write_consolidated_review_file(
    findings_by_supplement: dict[str, list[VerifiedFinding]],
    failures: list[str],
    output_path: str,
) -> None:
    """Write a consolidated review file covering multiple supplements."""
    total = sum(len(v) for v in findings_by_supplement.values())
    supplements = list(findings_by_supplement.keys())

    lines = [
        "# Pipeline Review File (Batch)",
        "",
        f"Supplements: {len(supplements)} | Total findings: {total} | Failed topics: {len(failures)}",
        "",
        "## Instructions",
        "- Mark `approved: true` on findings you want to load into the database.",
        "- You may edit the `claim` field to correct wording.",
        "- Rejected findings are excluded by default — change `approved` to true to override.",
        "- Save this file, then run: `python3 load_findings.py --review <path>`",
        "",
    ]

    for supplement, findings in findings_by_supplement.items():
        lines.append(f"## Supplement: {supplement}")
        lines.append("")
        if not findings:
            lines.append("*(no findings produced)*")
            lines.append("")
        else:
            _write_verdict_sections(lines, findings)

    for failure in failures:
        topic, _, error = failure.partition(": ")
        lines.append(f"## Supplement: {topic} — FAILED")
        lines.append("")
        lines.append(f"**Error:** {error}")
        lines.append("")

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"[writer] Consolidated review file written to: {output_path}")
    print(f"[writer] {len(supplements)} supplement(s), {total} total findings, {len(failures)} failure(s)")


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
