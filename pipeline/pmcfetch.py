"""PMC full-text fallback — looks up dosage from open-access PMC articles when absent from abstracts."""

import os
import time

import anthropic
from Bio import Entrez

CLAUDE_MODEL = "claude-haiku-4-5"
Entrez.email = os.environ.get("ENTREZ_EMAIL", "endo-pipeline@example.com")


def fetch_pmc_dosage(pmid: str) -> str | None:
    """Return the dosage string extracted from a PMC full-text Methods section, or None."""
    pmcid = _get_pmcid(pmid)
    if not pmcid:
        return None

    time.sleep(0.4)
    full_text = _fetch_pmc_text(pmcid)
    if not full_text:
        return None

    return _extract_dosage_with_claude(full_text)


def _get_pmcid(pmid: str) -> str | None:
    """Look up the PMCID for a given PMID via Entrez elink."""
    try:
        time.sleep(0.4)
        handle = Entrez.elink(dbfrom="pubmed", db="pmc", id=pmid, linkname="pubmed_pmc")
        record = Entrez.read(handle)
        handle.close()
        link_sets = record[0].get("LinkSetDb", [])
        if not link_sets:
            return None
        links = link_sets[0].get("Link", [])
        if not links:
            return None
        return links[0]["Id"]
    except Exception:
        return None


def _fetch_pmc_text(pmcid: str) -> str | None:
    """Fetch PMC full-text XML and return a plain-text excerpt focused on the Methods section."""
    try:
        handle = Entrez.efetch(db="pmc", id=pmcid, rettype="xml", retmode="xml")
        xml_bytes = handle.read()
        handle.close()

        xml_text = xml_bytes.decode("utf-8", errors="replace") if isinstance(xml_bytes, bytes) else xml_bytes

        # Extract a rough Methods section — look for <sec> tags containing "method"
        import re
        methods_match = re.search(
            r"<sec[^>]*>.*?<title[^>]*>[^<]*[Mm]ethod[^<]*</title>(.*?)</sec>",
            xml_text,
            re.DOTALL,
        )
        if methods_match:
            raw = methods_match.group(1)
        else:
            # Fall back to a broad slice of the XML to avoid sending the whole document
            raw = xml_text[:8000]

        # Strip XML tags
        plain = re.sub(r"<[^>]+>", " ", raw)
        plain = re.sub(r"\s+", " ", plain).strip()
        return plain[:4000] if plain else None
    except Exception:
        return None


def _extract_dosage_with_claude(methods_text: str) -> str | None:
    """Ask Claude to extract the administered dosage from the Methods text."""
    client = anthropic.Anthropic(api_key=os.environ["ENDO_API_KEY"])
    prompt = f"""You are extracting a specific fact from a clinical study Methods section.

Methods section text:
{methods_text}

Question: What dosage of the intervention was administered to participants?

Rules:
- If a specific dosage is stated, return it exactly as described (e.g. "2g EPA + 1g DHA daily", "400 mg twice daily").
- If no specific dosage is mentioned in this text, return the single word: null
- Return ONLY the dosage string or the word null. No explanation, no extra text."""

    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=64,
            messages=[{"role": "user", "content": prompt}],
        )
        result = response.content[0].text.strip()
        return None if result.lower() == "null" else result
    except Exception:
        return None
