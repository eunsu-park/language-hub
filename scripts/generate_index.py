#!/usr/bin/env python3
"""Generate _index.yaml for vocabulary directories.

Usage:
    python generate_index.py                     # All courses
    python generate_index.py --course Spanish    # One course
"""
import argparse
from pathlib import Path

import yaml

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"


def count_words(data: dict) -> int:
    """Count total words across all categories."""
    total = 0
    for cat in data.get("categories", []):
        total += len(cat.get("words", []))
    return total


def generate_index(course: str) -> None:
    """Generate _index.yaml for a course's vocabulary directory."""
    vocab_dir = CONTENT_DIR / course / "vocabulary"
    if not vocab_dir.exists():
        print(f"  {course}: vocabulary directory not found, skipping")
        return

    word_key = course.lower()
    files_data = []
    total_words = 0

    for yaml_path in sorted(vocab_dir.glob("*.yaml")):
        if yaml_path.name.startswith("_"):
            continue
        with open(yaml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        wc = count_words(data)
        total_words += wc

        entry = {
            "file": yaml_path.name,
            "lesson": data.get("lesson", ""),
            "word_count": wc,
            "categories": [c.get("id", "") for c in data.get("categories", [])],
        }

        # Add supplementary-specific fields
        if data.get("type") == "supplementary":
            entry["type"] = "supplementary"
            entry["topic"] = data.get("topic", "")
            prof = data.get("cefr", data.get("jlpt", ""))
            if prof:
                entry["cefr"] = prof

        files_data.append(entry)

    index = {
        "course": course,
        "total_words": total_words,
        "files": files_data,
    }

    index_path = vocab_dir / "_index.yaml"
    with open(index_path, "w", encoding="utf-8") as f:
        yaml.dump(index, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"  {course}: {len(files_data)} files, {total_words} words → {index_path.name}")


def main():
    parser = argparse.ArgumentParser(description="Generate vocabulary _index.yaml")
    parser.add_argument("--course", help="Generate for a specific course only")
    args = parser.parse_args()

    courses = [args.course] if args.course else [
        d.name for d in sorted(CONTENT_DIR.iterdir())
        if d.is_dir() and not d.name.startswith("_")
        and (d / "vocabulary").exists()
    ]

    for course in courses:
        print(f"Generating index for {course}...")
        generate_index(course)

    print("Done.")


if __name__ == "__main__":
    main()
