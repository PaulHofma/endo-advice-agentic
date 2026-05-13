import json
import re
from pathlib import Path

from review_writer import write_consolidated_review_file, write_review_file
from verification import Verdict


def _parse_json_blocks(content: str) -> list[dict]:
    blocks = re.findall(r"```json\s*(.*?)\s*```", content, re.DOTALL)
    entries = []
    for block in blocks:
        try:
            entries.append(json.loads(block))
        except json.JSONDecodeError:
            pass
    return entries


def test_write_review_file_sets_correct_approval_flags(make_verified_finding, tmp_path):
    verified = make_verified_finding(verdict=Verdict.VERIFIED)
    flagged = make_verified_finding(verdict=Verdict.FLAGGED, reason="Overstated.")
    rejected = make_verified_finding(verdict=Verdict.REJECTED, reason="Not supported.")

    out = str(tmp_path / "review.md")
    write_review_file([verified, flagged, rejected], out)

    entries = _parse_json_blocks(Path(out).read_text())
    assert len(entries) == 3
    by_verdict = {e["verdict"]: e["approved"] for e in entries}
    assert by_verdict["verified"] is True
    assert by_verdict["flagged"] is False
    assert by_verdict["rejected"] is False


def test_write_review_file_empty_findings_writes_none_placeholder(tmp_path):
    out = str(tmp_path / "review.md")
    write_review_file([], out)

    content = Path(out).read_text()
    assert Path(out).exists()
    assert "*(none)*" in content


def test_write_consolidated_two_supplements_produce_two_headings(make_verified_finding, tmp_path):
    findings = {
        "NAC endometriosis": [make_verified_finding(verdict=Verdict.VERIFIED)],
        "Vitamin D endometriosis": [make_verified_finding(verdict=Verdict.VERIFIED)],
    }
    out = str(tmp_path / "batch.md")
    write_consolidated_review_file(findings, [], out)

    content = Path(out).read_text()
    assert "## Supplement: NAC endometriosis" in content
    assert "## Supplement: Vitamin D endometriosis" in content


def test_write_consolidated_empty_supplement_shows_placeholder(tmp_path):
    out = str(tmp_path / "batch.md")
    write_consolidated_review_file({"Magnesium endometriosis": []}, [], out)

    content = Path(out).read_text()
    assert "*(no findings produced)*" in content


def test_write_consolidated_failed_topic_shows_failed_section(tmp_path):
    out = str(tmp_path / "batch.md")
    write_consolidated_review_file({}, ["Bad Topic: connection timeout"], out)

    content = Path(out).read_text()
    assert "Bad Topic" in content
    assert "FAILED" in content
    assert "connection timeout" in content
