import argparse
from unittest.mock import patch

import pytest

from pipeline import _load_topics_file, _resolve_topics, _run_topic, main


def _args(topic=None, topics=None, topics_file=None) -> argparse.Namespace:
    return argparse.Namespace(topic=topic, topics=topics, topics_file=topics_file)


# ---------------------------------------------------------------------------
# _resolve_topics
# ---------------------------------------------------------------------------

def test_resolve_topics_single_flag():
    result = _resolve_topics(_args(topic="NAC endometriosis"))
    assert result == ["NAC endometriosis"]


def test_resolve_topics_multiple_flags():
    result = _resolve_topics(_args(topics=[["NAC endometriosis"], ["Omega-3 endometriosis"]]))
    assert result == ["NAC endometriosis", "Omega-3 endometriosis"]


def test_resolve_topics_deduplicates():
    result = _resolve_topics(_args(topic="NAC endometriosis", topics=[["NAC endometriosis"]]))
    assert result == ["NAC endometriosis"]


def test_resolve_topics_no_input_raises_value_error():
    with pytest.raises(ValueError, match="At least one topic"):
        _resolve_topics(_args())


# ---------------------------------------------------------------------------
# _load_topics_file
# ---------------------------------------------------------------------------

def test_load_topics_file_reads_non_blank_non_comment_lines(tmp_path):
    content = "NAC endometriosis\n# this is a comment\n\nOmega-3 endometriosis\n"
    f = tmp_path / "topics.txt"
    f.write_text(content)

    result = _load_topics_file(str(f))

    assert result == ["NAC endometriosis", "Omega-3 endometriosis"]


# ---------------------------------------------------------------------------
# main — missing API key
# ---------------------------------------------------------------------------

def test_main_exits_when_api_key_missing(monkeypatch, tmp_path):
    monkeypatch.delenv("ENDO_API_KEY", raising=False)
    monkeypatch.setattr("sys.argv", ["pipeline.py", "--topic", "NAC endometriosis"])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# _run_topic — exception isolation
# ---------------------------------------------------------------------------

def test_run_topic_exception_returns_error_tuple():
    with patch("synthesis.run_synthesis", side_effect=Exception("API timeout")):
        topic, findings, error = _run_topic("NAC endometriosis", 15)

    assert topic == "NAC endometriosis"
    assert findings is None
    assert "API timeout" in error
