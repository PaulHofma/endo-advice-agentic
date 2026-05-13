import pytest

from pubmed import PubMedArticle
from synthesis import RawFinding
from verification import VerifiedFinding, Verdict


@pytest.fixture
def make_pubmed_article():
    def _make(
        pmid="12345678",
        title="A Study on Supplement Effects",
        authors="Smith J et al.",
        year=2023,
        abstract="Participants showed significant reduction in pain scores after treatment.",
    ):
        return PubMedArticle(pmid=pmid, title=title, authors=authors, year=year, abstract=abstract)

    return _make


@pytest.fixture
def make_raw_finding(make_pubmed_article):
    def _make(
        claim="Test supplement may reduce pelvic pain.",
        abstract_excerpt="Participants showed significant reduction in pain scores.",
        pmid="12345678",
        suggested_symptom="pelvic pain",
        supplement_name="TestSupp",
        article=None,
        dosage=None,
        duration=None,
        study_type=None,
        sample_size=None,
        placebo_controlled=None,
        safety_notes=None,
    ):
        return RawFinding(
            claim=claim,
            abstract_excerpt=abstract_excerpt,
            pmid=pmid,
            suggested_symptom=suggested_symptom,
            supplement_name=supplement_name,
            article=article or make_pubmed_article(pmid=pmid),
            dosage=dosage,
            duration=duration,
            study_type=study_type,
            sample_size=sample_size,
            placebo_controlled=placebo_controlled,
            safety_notes=safety_notes,
        )

    return _make


@pytest.fixture
def make_verified_finding(make_raw_finding):
    def _make(
        verdict=Verdict.VERIFIED,
        reason="Claim is well supported by the abstract.",
        verified_excerpt="Participants showed significant reduction in pain scores.",
        raw=None,
    ):
        return VerifiedFinding(
            raw=raw or make_raw_finding(),
            verdict=verdict,
            reason=reason,
            verified_excerpt=verified_excerpt,
        )

    return _make
