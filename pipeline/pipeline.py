#!/usr/bin/env python3
"""Main pipeline CLI — run synthesis, verification, and produce a review file.

Usage:
    python3 pipeline.py --topic "NAC endometriosis"
    python3 pipeline.py --topic "Vitamin D adenomyosis" --max-articles 20 --output review.md
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Endo Advice research pipeline: PubMed → synthesis → verification → review file"
    )
    parser.add_argument("--topic", required=True, help='Search topic, e.g. "NAC endometriosis"')
    parser.add_argument("--max-articles", type=int, default=15, help="Max PubMed results to fetch (default: 15)")
    parser.add_argument("--output", default=None, help="Output review file path (default: review_<topic>_<timestamp>.md)")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    topic = args.topic.strip()
    safe_topic = topic.replace(" ", "_").replace("/", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = args.output or f"review_{safe_topic}_{timestamp}.md"

    print(f"=== Endo Advice Pipeline ===")
    print(f"Topic: {topic}")
    print(f"Max articles: {args.max_articles}")
    print(f"Output: {output_path}")
    print()

    # Stage 1: Synthesis
    from synthesis import run_synthesis
    raw_findings = run_synthesis(topic, max_articles=args.max_articles)

    if not raw_findings:
        print("\nNo findings produced by synthesis. Check the topic and try again.")
        sys.exit(0)

    print(f"\nSynthesis complete: {len(raw_findings)} raw findings\n")

    # Stage 2: Verification
    from verification import run_verification
    verified_findings = run_verification(raw_findings)

    print(f"\nVerification complete: {len(verified_findings)} findings assessed\n")

    # Stage 3: Write review file
    from review_writer import write_review_file
    write_review_file(verified_findings, output_path)

    print(f"\nDone. Review {output_path}, then run:")
    print(f"  python3 load_findings.py --review {output_path}")


if __name__ == "__main__":
    main()
