import json
from unittest.mock import MagicMock, patch

import pytest

from summarise import _format_finding, _parse_json_response


# ---------------------------------------------------------------------------
# _parse_json_response
# ---------------------------------------------------------------------------

def test_parse_json_response_plain_json():
    raw = '{"content": "test summary", "evidence_strength": "moderate"}'
    assert _parse_json_response(raw) == {"content": "test summary", "evidence_strength": "moderate"}


def test_parse_json_response_fenced_with_json_label():
    raw = "```json\n{\"content\": \"test\", \"evidence_strength\": \"strong\"}\n```"
    assert _parse_json_response(raw) == {"content": "test", "evidence_strength": "strong"}


def test_parse_json_response_fenced_without_label():
    raw = "```\n{\"content\": \"test\", \"evidence_strength\": \"preliminary\"}\n```"
    assert _parse_json_response(raw) == {"content": "test", "evidence_strength": "preliminary"}


def test_parse_json_response_raises_on_invalid_json():
    with pytest.raises(json.JSONDecodeError):
        _parse_json_response("This is not JSON at all.")


# ---------------------------------------------------------------------------
# _format_finding
# ---------------------------------------------------------------------------

def _make_finding(**overrides):
    base = {
        "plain_language_summary": "NAC may reduce endometrioma size.",
        "study_type": "rct",
        "sample_size": 92,
        "dosage": "600 mg three times daily",
        "duration": "3 months",
        "placebo_controlled": True,
        "safety_notes": None,
    }
    base.update(overrides)
    return base


def test_format_finding_includes_all_non_null_fields():
    result = _format_finding(1, _make_finding())
    assert "NAC may reduce endometrioma size." in result
    assert "rct" in result
    assert "92" in result
    assert "600 mg three times daily" in result
    assert "3 months" in result
    assert "True" in result


def test_format_finding_omits_none_fields():
    f = _make_finding(study_type=None, sample_size=None, dosage=None, duration=None, placebo_controlled=None)
    result = _format_finding(1, f)
    assert "Study type" not in result
    assert "Sample size" not in result
    assert "Dosage" not in result
    assert "Duration" not in result
    assert "Placebo" not in result


def test_format_finding_includes_safety_notes_when_present():
    result = _format_finding(1, _make_finding(safety_notes="No adverse effects reported."))
    assert "No adverse effects reported." in result


def test_format_finding_omits_safety_notes_when_none():
    result = _format_finding(1, _make_finding(safety_notes=None))
    assert "Safety" not in result


# ---------------------------------------------------------------------------
# _generate_symptom_summaries — early return when no pairs
# ---------------------------------------------------------------------------

def test_generate_symptom_summaries_returns_early_when_no_pairs():
    import summarise
    conn = MagicMock()
    client = MagicMock()
    summarise._generate_symptom_summaries(conn, [], client)
    conn.cursor.assert_not_called()
    client.messages.create.assert_not_called()


# ---------------------------------------------------------------------------
# _generate_supplement_symptom_summaries — happy path + API failure fallback
# ---------------------------------------------------------------------------

def _mock_client_returning(text):
    response = MagicMock()
    response.content = [MagicMock(text=text)]
    client = MagicMock()
    client.messages.create.return_value = response
    return client


def _pair_row(sup_id=1, sup_name="NAC", sym_id=10, sym_name="pelvic pain"):
    return {"supplement_id": sup_id, "supplement_name": sup_name,
            "symptom_id": sym_id, "symptom_name": sym_name}


def _finding_row():
    return {
        "plain_language_summary": "NAC may reduce pain.",
        "dosage": "600 mg", "duration": "3 months",
        "study_type": "rct", "sample_size": 40,
        "placebo_controlled": True, "safety_notes": None,
    }


def test_generate_supplement_symptom_summaries_inserts_result():
    import summarise
    cur = MagicMock()
    cur.fetchall.side_effect = [[_pair_row()], [_finding_row()]]
    conn = MagicMock()
    conn.cursor.return_value = cur

    payload = json.dumps({"content": "NAC shows promise.", "evidence_strength": "moderate"})
    client = _mock_client_returning(payload)

    with patch("summarise.time.sleep"):
        results = summarise._generate_supplement_symptom_summaries(conn, client)

    assert len(results) == 1
    assert results[0]["content"] == "NAC shows promise."
    assert results[0]["evidence_strength"] == "moderate"
    cur.execute.assert_called()


def test_generate_supplement_symptom_summaries_falls_back_on_api_error():
    import summarise
    cur = MagicMock()
    cur.fetchall.side_effect = [[_pair_row()], [_finding_row()]]
    conn = MagicMock()
    conn.cursor.return_value = cur

    client = MagicMock()
    client.messages.create.side_effect = Exception("API error")

    with patch("summarise.time.sleep"):
        results = summarise._generate_supplement_symptom_summaries(conn, client)

    assert len(results) == 1
    assert "NAC" in results[0]["content"]
    assert results[0]["evidence_strength"] == "preliminary"


# ---------------------------------------------------------------------------
# run() creates exactly one anthropic client
# ---------------------------------------------------------------------------

def test_run_creates_single_anthropic_client(monkeypatch):
    monkeypatch.setenv("ENDO_API_KEY", "test-key")

    import summarise

    with (
        patch("summarise.psycopg2.connect"),
        patch("summarise._delete_all_summaries"),
        patch("summarise._generate_supplement_symptom_summaries", return_value=[]) as mock_pairs,
        patch("summarise._generate_supplement_summaries") as mock_sup,
        patch("summarise._generate_symptom_summaries") as mock_sym,
        patch("summarise.anthropic.Anthropic") as mock_anthropic,
    ):
        summarise.run()

    mock_anthropic.assert_called_once()
    client = mock_anthropic.return_value
    # All three stages receive the same client instance
    assert mock_pairs.call_args[0][1] is client
    assert mock_sup.call_args[0][2] is client
    assert mock_sym.call_args[0][2] is client
