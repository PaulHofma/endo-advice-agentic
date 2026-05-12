"""Synthesis agent — queries PubMed and uses Claude to produce structured findings."""

import json
import os
from dataclasses import dataclass, field

import anthropic

from pubmed import PubMedArticle, fetch_abstracts, search_pubmed

CLAUDE_MODEL = "claude-haiku-4-5"


@dataclass
class RawFinding:
    claim: str
    abstract_excerpt: str
    pmid: str
    suggested_symptom: str
    supplement_name: str
    article: PubMedArticle


def _build_synthesis_prompt(topic: str, articles: list[PubMedArticle]) -> str:
    articles_text = "\n\n".join(
        f"PMID: {a.pmid}\nTitle: {a.title}\nAuthors: {a.authors} ({a.year})\nAbstract: {a.abstract}"
        for a in articles
    )
    return f"""You are a medical research synthesizer for endometriosis and adenomyosis. 
Your task is to extract structured research findings from PubMed abstracts.

Topic: {topic}

Abstracts:
{articles_text}

For each relevant finding, produce a JSON array. Each entry must have:
- "claim": A clear, single-sentence plain-language claim about the supplement's effect
- "abstract_excerpt": A SHORT quoted excerpt (1-2 sentences max) from the abstract that directly supports the claim
- "pmid": The PMID of the source article
- "suggested_symptom": The primary symptom addressed (e.g., "dysmenorrhea", "pelvic pain", "inflammation", "fatigue")

Rules:
- Only include findings supported by the abstract text
- Do not overstate; match the strength of the claim to the evidence (e.g., "may reduce" not "cures")
- Skip articles with no relevant content
- Return valid JSON only, no commentary

Example output:
[
  {{
    "claim": "NAC may reduce endometrioma size when taken for 3 months.",
    "abstract_excerpt": "After 3 months of treatment, endometrioma diameter significantly decreased in the NAC group compared to controls.",
    "pmid": "12345678",
    "suggested_symptom": "endometrioma"
  }}
]
"""


def run_synthesis(topic: str, max_articles: int = 15) -> list[RawFinding]:
    """Search PubMed for topic, synthesize findings with Claude."""
    supplement_name = topic.split()[0]

    print(f"[synthesis] Searching PubMed for: {topic}")
    pmids = search_pubmed(f"{topic}", max_results=max_articles)

    if not pmids:
        print(f"[synthesis] No results found for topic: {topic}")
        return []

    print(f"[synthesis] Found {len(pmids)} PMIDs, fetching abstracts...")
    articles = fetch_abstracts(pmids)

    if not articles:
        print("[synthesis] No usable abstracts retrieved")
        return []

    print(f"[synthesis] Synthesizing {len(articles)} abstracts with Claude...")
    client = anthropic.Anthropic(api_key=os.environ["ENDO_API_KEY"])
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2048,
        messages=[{"role": "user", "content": _build_synthesis_prompt(topic, articles)}],
    )

    raw_text = response.content[0].text.strip()
    # Strip markdown code fences if present
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]

    try:
        findings_data: list[dict] = json.loads(raw_text)
    except json.JSONDecodeError as e:
        print(f"[synthesis] Failed to parse Claude output as JSON: {e}")
        return []

    article_by_pmid = {a.pmid: a for a in articles}
    results: list[RawFinding] = []
    for entry in findings_data:
        pmid = str(entry.get("pmid", "")).strip()
        article = article_by_pmid.get(pmid)
        if not article:
            print(f"[synthesis] Warning: PMID {pmid} not in fetched articles — skipping")
            continue
        results.append(
            RawFinding(
                claim=entry["claim"],
                abstract_excerpt=entry["abstract_excerpt"],
                pmid=pmid,
                suggested_symptom=entry.get("suggested_symptom", ""),
                supplement_name=supplement_name,
                article=article,
            )
        )

    print(f"[synthesis] Produced {len(results)} findings")
    return results
