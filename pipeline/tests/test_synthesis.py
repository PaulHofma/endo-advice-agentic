import json
from unittest.mock import MagicMock, patch

import pytest

from synthesis import RawFinding, run_synthesis

VALID_FINDING = {
    "claim": "NAC may reduce endometrioma size.",
    "abstract_excerpt": "After 3 months, endometrioma diameter significantly decreased.",
    "pmid": "12345678",
    "suggested_symptom": "endometrioma",
    "dosage": "600 mg three times daily",
    "duration": "3 months",
    "study_type": "rct",
    "sample_size": 92,
    "placebo_controlled": True,
    "safety_notes": None,
}


def _mock_claude(text: str) -> MagicMock:
    response = MagicMock()
    response.content = [MagicMock(text=text)]
    client = MagicMock()
    client.messages.create.return_value = response
    return client


@pytest.fixture(autouse=True)
def api_key(monkeypatch):
    monkeypatch.setenv("ENDO_API_KEY", "test-key")


def test_happy_path_returns_populated_findings(make_pubmed_article):
    article = make_pubmed_article(pmid="12345678")
    with (
        patch("synthesis.search_pubmed", return_value=["12345678"]),
        patch("synthesis.fetch_abstracts", return_value=[article]),
        patch("synthesis.anthropic.Anthropic", return_value=_mock_claude(json.dumps([VALID_FINDING]))),
        patch("synthesis.fetch_pmc_dosage", return_value=None),
    ):
        results = run_synthesis("NAC endometriosis")

    assert len(results) == 1
    f = results[0]
    assert isinstance(f, RawFinding)
    assert f.claim == VALID_FINDING["claim"]
    assert f.pmid == "12345678"
    assert f.dosage == "600 mg three times daily"
    assert f.duration == "3 months"
    assert f.study_type == "rct"
    assert f.sample_size == 92
    assert f.placebo_controlled is True
    assert f.safety_notes is None


def test_no_pubmed_results_returns_empty_without_calling_claude():
    with (
        patch("synthesis.search_pubmed", return_value=[]),
        patch("synthesis.anthropic.Anthropic") as mock_anthropic,
    ):
        results = run_synthesis("NAC endometriosis")

    assert results == []
    mock_anthropic.assert_not_called()


def test_no_usable_abstracts_returns_empty_without_calling_claude():
    with (
        patch("synthesis.search_pubmed", return_value=["12345678"]),
        patch("synthesis.fetch_abstracts", return_value=[]),
        patch("synthesis.anthropic.Anthropic") as mock_anthropic,
    ):
        results = run_synthesis("NAC endometriosis")

    assert results == []
    mock_anthropic.assert_not_called()


def test_invalid_json_returns_empty(make_pubmed_article):
    article = make_pubmed_article(pmid="12345678")
    with (
        patch("synthesis.search_pubmed", return_value=["12345678"]),
        patch("synthesis.fetch_abstracts", return_value=[article]),
        patch("synthesis.anthropic.Anthropic", return_value=_mock_claude("This is not JSON at all.")),
        patch("synthesis.fetch_pmc_dosage", return_value=None),
    ):
        results = run_synthesis("NAC endometriosis")

    assert results == []


def test_unknown_pmid_in_claude_response_is_skipped(make_pubmed_article):
    article = make_pubmed_article(pmid="12345678")
    unknown = {**VALID_FINDING, "pmid": "99999999"}
    valid = {**VALID_FINDING, "pmid": "12345678"}
    with (
        patch("synthesis.search_pubmed", return_value=["12345678"]),
        patch("synthesis.fetch_abstracts", return_value=[article]),
        patch("synthesis.anthropic.Anthropic", return_value=_mock_claude(json.dumps([unknown, valid]))),
        patch("synthesis.fetch_pmc_dosage", return_value=None),
    ):
        results = run_synthesis("NAC endometriosis")

    assert len(results) == 1
    assert results[0].pmid == "12345678"


def test_all_clinical_fields_null(make_pubmed_article):
    article = make_pubmed_article(pmid="12345678")
    null_finding = {
        "claim": "NAC may help.",
        "abstract_excerpt": "Some effect was noted.",
        "pmid": "12345678",
        "suggested_symptom": "pain",
        "dosage": None,
        "duration": None,
        "study_type": None,
        "sample_size": None,
        "placebo_controlled": None,
        "safety_notes": None,
    }
    with (
        patch("synthesis.search_pubmed", return_value=["12345678"]),
        patch("synthesis.fetch_abstracts", return_value=[article]),
        patch("synthesis.anthropic.Anthropic", return_value=_mock_claude(json.dumps([null_finding]))),
        patch("synthesis.fetch_pmc_dosage", return_value=None),
    ):
        results = run_synthesis("NAC endometriosis")

    assert len(results) == 1
    f = results[0]
    assert f.dosage is None
    assert f.duration is None
    assert f.study_type is None
    assert f.sample_size is None
    assert f.placebo_controlled is None
    assert f.safety_notes is None


def test_pmc_fallback_updates_dosage_when_null(make_pubmed_article):
    article = make_pubmed_article(pmid="12345678")
    null_dosage = {**VALID_FINDING, "dosage": None}
    with (
        patch("synthesis.search_pubmed", return_value=["12345678"]),
        patch("synthesis.fetch_abstracts", return_value=[article]),
        patch("synthesis.anthropic.Anthropic", return_value=_mock_claude(json.dumps([null_dosage]))),
        patch("synthesis.fetch_pmc_dosage", return_value="400 mg daily") as mock_pmc,
    ):
        results = run_synthesis("NAC endometriosis")

    assert len(results) == 1
    assert results[0].dosage == "400 mg daily"
    mock_pmc.assert_called_once_with("12345678")


def test_pmc_fallback_leaves_dosage_none_when_not_found(make_pubmed_article):
    article = make_pubmed_article(pmid="12345678")
    null_dosage = {**VALID_FINDING, "dosage": None}
    with (
        patch("synthesis.search_pubmed", return_value=["12345678"]),
        patch("synthesis.fetch_abstracts", return_value=[article]),
        patch("synthesis.anthropic.Anthropic", return_value=_mock_claude(json.dumps([null_dosage]))),
        patch("synthesis.fetch_pmc_dosage", return_value=None),
    ):
        results = run_synthesis("NAC endometriosis")

    assert len(results) == 1
    assert results[0].dosage is None
