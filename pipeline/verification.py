"""Verification agent — re-fetches abstracts and verifies each synthesized claim with Gemini."""

import json
import os
import time
from dataclasses import dataclass
from enum import Enum

from google import genai

from pubmed import fetch_abstract
from synthesis import RawFinding

GEMINI_MODEL = "gemini-2.0-flash"


class Verdict(str, Enum):
    VERIFIED = "verified"
    FLAGGED = "flagged"
    REJECTED = "rejected"


@dataclass
class VerifiedFinding:
    raw: RawFinding
    verdict: Verdict
    reason: str
    verified_excerpt: str = ""


def _build_verification_prompt(finding: RawFinding, fresh_abstract: str) -> str:
    return f"""You are an independent medical research verifier for endometriosis research.

A synthesis agent produced this finding:
- Claim: "{finding.claim}"
- Quoted excerpt: "{finding.abstract_excerpt}"
- PMID: {finding.pmid}

The current PubMed abstract for PMID {finding.pmid} is:
{fresh_abstract}

Your job: determine whether the claim is supported by the abstract.

Respond with valid JSON only:
{{
  "verdict": "verified" | "flagged" | "rejected",
  "reason": "one sentence explanation",
  "verified_excerpt": "1-2 sentence excerpt from the ACTUAL abstract that supports (or refutes) the claim"
}}

Verdicts:
- "verified": The claim is a reasonable, non-overstated summary of the abstract content
- "flagged": The claim is directionally correct but overstates the evidence (e.g., says "cures" when paper says "may reduce")
- "rejected": The claim is not supported by this abstract, or the excerpt was fabricated
"""


def run_verification(findings: list[RawFinding]) -> list[VerifiedFinding]:
    """Verify each finding independently. Returns VerifiedFinding for each."""
    if not findings:
        return []

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    results: list[VerifiedFinding] = []

    for i, finding in enumerate(findings, 1):
        print(f"[verification] Verifying finding {i}/{len(findings)}: PMID {finding.pmid}")

        # Re-fetch the abstract independently
        time.sleep(0.4)
        article = fetch_abstract(finding.pmid)

        if article is None or not article.abstract:
            results.append(
                VerifiedFinding(
                    raw=finding,
                    verdict=Verdict.REJECTED,
                    reason="PMID not found or abstract unavailable",
                )
            )
            continue

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=_build_verification_prompt(finding, article.abstract),
        )

        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]

        try:
            data = json.loads(raw_text)
            verdict = Verdict(data.get("verdict", "flagged").lower())
        except (json.JSONDecodeError, ValueError):
            verdict = Verdict.FLAGGED
            data = {"reason": "Could not parse verification response", "verified_excerpt": ""}

        results.append(
            VerifiedFinding(
                raw=finding,
                verdict=verdict,
                reason=data.get("reason", ""),
                verified_excerpt=data.get("verified_excerpt", ""),
            )
        )
        print(f"[verification]   → {verdict.value}: {data.get('reason', '')[:80]}")

    return results
