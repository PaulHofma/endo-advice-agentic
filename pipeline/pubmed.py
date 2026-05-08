"""PubMed Entrez API wrapper — search and fetch abstracts by PMID."""

import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Optional

import requests

ENTREZ_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
DEFAULT_DELAY = 0.35  # stay under 3 req/s without an API key


@dataclass
class PubMedArticle:
    pmid: str
    title: str
    authors: str
    year: int
    abstract: str


def search_pubmed(query: str, max_results: int = 10) -> list[str]:
    """Return a list of PMIDs matching the query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
    }
    resp = requests.get(f"{ENTREZ_BASE}/esearch.fcgi", params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    pmids: list[str] = data.get("esearchresult", {}).get("idlist", [])
    return pmids


def fetch_abstract(pmid: str) -> Optional[PubMedArticle]:
    """Fetch a single article by PMID. Returns None if PMID not found."""
    time.sleep(DEFAULT_DELAY)
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml",
        "rettype": "abstract",
    }
    resp = requests.get(f"{ENTREZ_BASE}/efetch.fcgi", params=params, timeout=15)
    resp.raise_for_status()

    root = ET.fromstring(resp.text)
    article_node = root.find(".//PubmedArticle")
    if article_node is None:
        return None

    title_node = article_node.find(".//ArticleTitle")
    title = (title_node.text or "").strip() if title_node is not None else ""

    abstract_texts = article_node.findall(".//AbstractText")
    abstract = " ".join((t.text or "") for t in abstract_texts).strip()

    year_node = article_node.find(".//PubDate/Year")
    year = int(year_node.text) if year_node is not None and year_node.text else 0

    author_nodes = article_node.findall(".//Author")
    author_names = []
    for a in author_nodes[:3]:
        last = a.findtext("LastName", "")
        initials = a.findtext("Initials", "")
        if last:
            author_names.append(f"{last} {initials}".strip())
    if len(article_node.findall(".//Author")) > 3:
        author_names.append("et al.")
    authors = ", ".join(author_names)

    return PubMedArticle(
        pmid=pmid,
        title=title,
        authors=authors,
        year=year,
        abstract=abstract,
    )


def fetch_abstracts(pmids: list[str]) -> list[PubMedArticle]:
    """Fetch multiple articles, skipping any that fail."""
    results = []
    for pmid in pmids:
        article = fetch_abstract(pmid)
        if article and article.abstract:
            results.append(article)
    return results
