from unittest.mock import MagicMock, patch

import pytest

from pmcfetch import _get_pmcid, fetch_pmc_dosage


def _entrez_record_with_pmcid(pmcid: str) -> list:
    return [{"LinkSetDb": [{"Link": [{"Id": pmcid}]}]}]


def _mock_claude(text: str) -> MagicMock:
    response = MagicMock()
    response.content = [MagicMock(text=text)]
    client = MagicMock()
    client.messages.create.return_value = response
    return client


def _pmc_xml_with_methods(dosage_text: str) -> bytes:
    return (
        f"<article><sec><title>Methods</title>"
        f"<p>{dosage_text}</p></sec></article>"
    ).encode()


@pytest.fixture(autouse=True)
def api_key(monkeypatch):
    monkeypatch.setenv("ENDO_API_KEY", "test-key")


def test_dosage_found_end_to_end():
    handle_mock = MagicMock()
    handle_mock.read.return_value = _pmc_xml_with_methods("Participants received 400 mg twice daily for 12 weeks.")
    with (
        patch("pmcfetch.Entrez.elink", return_value=MagicMock()),
        patch("pmcfetch.Entrez.read", return_value=_entrez_record_with_pmcid("654321")),
        patch("pmcfetch.Entrez.efetch", return_value=handle_mock),
        patch("pmcfetch.anthropic.Anthropic", return_value=_mock_claude("400 mg twice daily")),
        patch("pmcfetch.time.sleep"),
    ):
        result = fetch_pmc_dosage("12345678")

    assert result == "400 mg twice daily"


def test_no_pmc_entry_returns_none():
    with (
        patch("pmcfetch.Entrez.elink", return_value=MagicMock()),
        patch("pmcfetch.Entrez.read", return_value=[{"LinkSetDb": []}]),
        patch("pmcfetch.time.sleep"),
    ):
        result = fetch_pmc_dosage("12345678")

    assert result is None


def test_claude_returns_null_string_gives_none():
    handle_mock = MagicMock()
    handle_mock.read.return_value = _pmc_xml_with_methods("No dosage information provided.")
    with (
        patch("pmcfetch.Entrez.elink", return_value=MagicMock()),
        patch("pmcfetch.Entrez.read", return_value=_entrez_record_with_pmcid("654321")),
        patch("pmcfetch.Entrez.efetch", return_value=handle_mock),
        patch("pmcfetch.anthropic.Anthropic", return_value=_mock_claude("null")),
        patch("pmcfetch.time.sleep"),
    ):
        result = fetch_pmc_dosage("12345678")

    assert result is None


def test_entrez_exception_returns_none_without_propagating():
    with (
        patch("pmcfetch.Entrez.elink", side_effect=Exception("network error")),
        patch("pmcfetch.time.sleep"),
    ):
        result = _get_pmcid("12345678")

    assert result is None
