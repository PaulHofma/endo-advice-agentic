import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from load_findings import load_findings, parse_review_file, slug_from_name


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _valid_entry(approved: bool = True) -> dict:
    return {
        "approved": approved,
        "supplement": "NAC",
        "claim": "NAC may reduce endometrioma size.",
        "pmid": "12345678",
        "title": "A Study on NAC and Endometriosis",
        "authors": "Smith J et al.",
        "year": 2023,
        "abstract_excerpt": "Endometrioma size decreased significantly.",
        "suggested_symptom": "endometrioma",
        "dosage": "600 mg daily",
        "duration": "3 months",
        "study_type": "rct",
        "sample_size": 92,
        "placebo_controlled": True,
        "safety_notes": None,
    }


def _write_review(entries: list[dict], path: Path) -> str:
    lines = []
    for entry in entries:
        lines.append("```json")
        lines.append(json.dumps(entry))
        lines.append("```")
    path.write_text("\n".join(lines))
    return str(path)


def _mock_db(
    supplement_id: int = 1,
    finding_id: int = 2,
    citation_count: int = 1,
    symptom_id: int = 3,
) -> tuple[MagicMock, MagicMock]:
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value = mock_cur
    # fetchone call sequence for a full new entry with symptom:
    # 1. supplement INSERT RETURNING id
    # 2. finding INSERT RETURNING id
    # 3. SELECT COUNT(*) citations
    # 4. symptom INSERT RETURNING id
    mock_cur.fetchone.side_effect = [
        (supplement_id,),
        (finding_id,),
        (citation_count,),
        (symptom_id,),
    ]
    return mock_conn, mock_cur


# ---------------------------------------------------------------------------
# parse_review_file
# ---------------------------------------------------------------------------

def test_parse_review_file_returns_only_approved(tmp_path):
    entries = [_valid_entry(approved=True), _valid_entry(approved=False), _valid_entry(approved=False)]
    path = _write_review(entries, tmp_path / "review.md")

    result = parse_review_file(path)

    assert len(result) == 1
    assert result[0]["approved"] is True


def test_parse_review_file_skips_malformed_json_blocks(tmp_path):
    content = "```json\n{not valid json}\n```\n```json\n" + json.dumps(_valid_entry()) + "\n```"
    path = tmp_path / "review.md"
    path.write_text(content)

    result = parse_review_file(str(path))

    assert len(result) == 1
    assert result[0]["approved"] is True


def test_parse_review_file_returns_empty_when_none_approved(tmp_path):
    entries = [_valid_entry(approved=False), _valid_entry(approved=False)]
    path = _write_review(entries, tmp_path / "review.md")

    result = parse_review_file(path)

    assert result == []


# ---------------------------------------------------------------------------
# load_findings
# ---------------------------------------------------------------------------

def test_load_findings_inserts_new_entry():
    entry = _valid_entry()
    mock_conn, mock_cur = _mock_db()

    with patch("load_findings.psycopg2.connect", return_value=mock_conn):
        load_findings([entry], "postgresql://test")

    # supplement, finding, citation, citation-count check, symptom, finding_symptoms
    assert mock_cur.execute.call_count >= 5
    mock_conn.commit.assert_called_once()


def test_load_findings_skips_entry_with_empty_pmid():
    entry = {**_valid_entry(), "pmid": ""}
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value = mock_cur

    with patch("load_findings.psycopg2.connect", return_value=mock_conn):
        load_findings([entry], "postgresql://test")

    mock_cur.execute.assert_not_called()
    mock_conn.commit.assert_called_once()


def test_load_findings_citation_integrity_error_rolls_back():
    entry = _valid_entry()
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value = mock_cur
    # citation count returns 0 — integrity check fails
    mock_cur.fetchone.side_effect = [(1,), (2,), (0,)]

    with patch("load_findings.psycopg2.connect", return_value=mock_conn):
        with pytest.raises(RuntimeError, match="no citations"):
            load_findings([entry], "postgresql://test")

    mock_conn.rollback.assert_called_once()


def test_load_findings_no_symptom_skips_symptom_upsert():
    entry = {**_valid_entry(), "suggested_symptom": ""}
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value = mock_cur
    # only 3 fetchone calls without symptom branch
    mock_cur.fetchone.side_effect = [(1,), (2,), (1,)]

    with patch("load_findings.psycopg2.connect", return_value=mock_conn):
        load_findings([entry], "postgresql://test")

    assert mock_cur.fetchone.call_count == 3
    mock_conn.commit.assert_called_once()


def test_load_findings_empty_list_does_not_open_db():
    with patch("load_findings.psycopg2.connect") as mock_connect:
        load_findings([], "postgresql://test")

    mock_connect.assert_not_called()


# ---------------------------------------------------------------------------
# slug_from_name
# ---------------------------------------------------------------------------

def test_slug_from_name_converts_spaces():
    assert slug_from_name("Pelvic Pain") == "pelvic-pain"


def test_slug_from_name_strips_special_characters():
    assert slug_from_name("Omega-3 (Fish Oil)") == "omega-3-fish-oil"
