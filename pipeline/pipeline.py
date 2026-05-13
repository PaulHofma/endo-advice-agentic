#!/usr/bin/env python3
"""Main pipeline CLI — run synthesis, verification, and produce a review file.

Usage:
    python3 pipeline.py --topic "NAC endometriosis"
    python3 pipeline.py --topics "NAC endometriosis" --topics "Vitamin D endometriosis"
    python3 pipeline.py --topics-file supplements.txt
    python3 pipeline.py --topic "Vitamin D adenomyosis" --max-articles 20 --output review.md
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


def _load_topics_file(path: str) -> list[str]:
    topics = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            topics.append(line)
    return topics


def _resolve_topics(args: argparse.Namespace) -> list[str]:
    topics: list[str] = []
    if args.topic:
        topics.append(args.topic.strip())
    if args.topics:
        for t in args.topics:
            if isinstance(t, list):
                topics.extend(t)
            else:
                topics.append(t.strip())
    if args.topics_file:
        topics.extend(_load_topics_file(args.topics_file))
    seen: set[str] = set()
    deduped = []
    for t in topics:
        if t not in seen:
            seen.add(t)
            deduped.append(t)
    if not deduped:
        raise ValueError("At least one topic must be provided via --topic, --topics, or --topics-file")
    return deduped


def _run_topic(topic: str, max_articles: int) -> tuple[str, Optional[list], Optional[str]]:
    try:
        from synthesis import run_synthesis
        raw_findings = run_synthesis(topic, max_articles=max_articles)
        if not raw_findings:
            print(f"\n[{topic}] No findings produced by synthesis.")
            return (topic, [], None)
        print(f"\n[{topic}] Synthesis complete: {len(raw_findings)} raw findings")

        from verification import run_verification
        verified_findings = run_verification(raw_findings)
        print(f"[{topic}] Verification complete: {len(verified_findings)} findings assessed")
        return (topic, verified_findings, None)
    except Exception as exc:
        msg = str(exc)
        print(f"\n[{topic}] ERROR: {msg}", file=sys.stderr)
        return (topic, None, msg)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Endo Advice research pipeline: PubMed → synthesis → verification → review file"
    )
    parser.add_argument(
        "--topic", default=None, help='Single search topic (backward-compatible), e.g. "NAC endometriosis"'
    )
    parser.add_argument("--topics", action="append", nargs="+", metavar="TOPIC", help="One or more topics (repeatable)")
    parser.add_argument("--topics-file", default=None, metavar="PATH", help="Path to newline-separated topics file")
    parser.add_argument(
        "--max-articles", type=int, default=15, help="Max PubMed results to fetch per topic (default: 15)"
    )
    parser.add_argument("--output", default=None, help="Output review file path (default: auto-generated)")
    args = parser.parse_args()

    if not os.environ.get("ENDO_API_KEY"):
        print("Error: ENDO_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    try:
        topics = _resolve_topics(args)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    reviews_dir = Path(__file__).parent / "reviews"
    reviews_dir.mkdir(exist_ok=True)

    is_batch = len(topics) > 1

    if is_batch:
        output_path = args.output or str(reviews_dir / f"review_batch_{timestamp}.md")
        print(f"=== Endo Advice Pipeline (batch: {len(topics)} topics) ===")
        print(f"Topics: {', '.join(topics)}")
    else:
        safe_topic = topics[0].replace(" ", "_").replace("/", "_")
        output_path = args.output or str(reviews_dir / f"review_{safe_topic}_{timestamp}.md")
        print("=== Endo Advice Pipeline ===")
        print(f"Topic: {topics[0]}")

    print(f"Max articles: {args.max_articles}")
    print(f"Output: {output_path}")
    print()

    findings_by_supplement: dict[str, list] = {}
    failures: list[str] = []

    for topic in topics:
        _, findings, error = _run_topic(topic, args.max_articles)
        if error is not None:
            failures.append(f"{topic}: {error}")
        else:
            findings_by_supplement[topic] = findings or []

    if is_batch:
        from review_writer import write_consolidated_review_file
        write_consolidated_review_file(findings_by_supplement, failures, output_path)
        total_findings = sum(len(v) for v in findings_by_supplement.values())
        print(f"\n{len(topics)} topics processed, {total_findings} findings total")
        if failures:
            print(f"{len(failures)} topic(s) failed — see review file for details.")
    else:
        from review_writer import write_review_file
        all_findings = findings_by_supplement.get(topics[0], [])
        write_review_file(all_findings, output_path)

    print(f"\nDone. Review {output_path}, then run:")
    print(f"  python3 load_findings.py --review {output_path}")
    print("\nThe load command will automatically run the summarisation stage and append")
    print("generated summaries to the review file for inspection.")


if __name__ == "__main__":
    main()
