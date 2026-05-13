import json
from unittest.mock import MagicMock, patch

import pytest

from verification import Verdict, run_verification


def _mock_claude(text: str) -> MagicMock:
    response = MagicMock()
    response.content = [MagicMock(text=text)]
    client = MagicMock()
    client.messages.create.return_value = response
    return client


@pytest.fixture(autouse=True)
def api_key(monkeypatch):
    monkeypatch.setenv("ENDO_API_KEY", "test-key")


def test_verified_verdict(make_raw_finding, make_pubmed_article):
    finding = make_raw_finding(pmid="12345678")
    article = make_pubmed_article(pmid="12345678")
    payload = {
        "verdict": "verified",
        "reason": "Claim accurately summarizes the abstract.",
        "verified_excerpt": "Pain scores significantly decreased.",
    }
    with (
        patch("verification.fetch_abstract", return_value=article),
        patch("verification.anthropic.Anthropic", return_value=_mock_claude(json.dumps(payload))),
        patch("verification.time.sleep"),
    ):
        results = run_verification([finding])

    assert len(results) == 1
    assert results[0].verdict == Verdict.VERIFIED
    assert results[0].reason == "Claim accurately summarizes the abstract."
    assert results[0].verified_excerpt == "Pain scores significantly decreased."


def test_flagged_verdict(make_raw_finding, make_pubmed_article):
    finding = make_raw_finding(pmid="12345678")
    article = make_pubmed_article(pmid="12345678")
    payload = {
        "verdict": "flagged",
        "reason": "Claim overstates the evidence.",
        "verified_excerpt": "A trend was observed but did not reach significance.",
    }
    with (
        patch("verification.fetch_abstract", return_value=article),
        patch("verification.anthropic.Anthropic", return_value=_mock_claude(json.dumps(payload))),
        patch("verification.time.sleep"),
    ):
        results = run_verification([finding])

    assert results[0].verdict == Verdict.FLAGGED


def test_pmid_not_resolved_gives_rejected(make_raw_finding):
    finding = make_raw_finding(pmid="00000000")
    with (
        patch("verification.fetch_abstract", return_value=None),
        patch("verification.anthropic.Anthropic", return_value=MagicMock()),
        patch("verification.time.sleep"),
    ):
        results = run_verification([finding])

    assert results[0].verdict == Verdict.REJECTED
    assert "PMID not found" in results[0].reason


def test_unparseable_json_gives_flagged(make_raw_finding, make_pubmed_article):
    finding = make_raw_finding(pmid="12345678")
    article = make_pubmed_article(pmid="12345678")
    with (
        patch("verification.fetch_abstract", return_value=article),
        patch("verification.anthropic.Anthropic", return_value=_mock_claude("not json at all")),
        patch("verification.time.sleep"),
    ):
        results = run_verification([finding])

    assert results[0].verdict == Verdict.FLAGGED
    assert "parse" in results[0].reason.lower()


def test_empty_input_returns_empty_without_calling_claude():
    with patch("verification.anthropic.Anthropic") as mock_anthropic:
        results = run_verification([])

    assert results == []
    mock_anthropic.assert_not_called()
