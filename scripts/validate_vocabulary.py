#!/usr/bin/env python3
"""Validate vocabulary YAML files for schema compliance and duplicates.

Usage:
    python validate_vocabulary.py                     # Validate all courses
    python validate_vocabulary.py --course Spanish    # Validate one course
    python validate_vocabulary.py --check-dupes       # Also check cross-file duplicates
"""
import argparse
import sys
from pathlib import Path

import yaml

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"

REQUIRED_ROOT = {"lesson", "lesson_number", "categories"}
REQUIRED_WORD_COMMON = {"translation"}
BILINGUAL_KEYS = {"translation", "notes"}

# lesson_number ranges
LESSON_RANGE = range(1, 100)
SUPPLEMENTARY_RANGE = range(100, 200)


def load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def validate_file(path: Path, course: str, errors: list[str]) -> list[dict]:
    """Validate a single vocabulary YAML file. Returns list of words found."""
    data = load_yaml(path)
    fname = path.name
    words_found: list[dict] = []

    # Root fields
    for key in REQUIRED_ROOT:
        if key not in data:
            errors.append(f"{fname}: missing required field '{key}'")

    lesson_num = data.get("lesson_number", -1)
    if not isinstance(lesson_num, int):
        errors.append(f"{fname}: lesson_number must be int, got {type(lesson_num).__name__}")
    elif lesson_num not in LESSON_RANGE and lesson_num not in SUPPLEMENTARY_RANGE:
        errors.append(f"{fname}: lesson_number {lesson_num} outside valid ranges (1-99, 100-199)")

    # Must have cefr or jlpt
    if "cefr" not in data and "jlpt" not in data:
        errors.append(f"{fname}: must have 'cefr' or 'jlpt' field")

    # Supplementary-specific fields
    if lesson_num in SUPPLEMENTARY_RANGE:
        if data.get("type") != "supplementary":
            errors.append(f"{fname}: supplementary file (lesson_number={lesson_num}) must have type: supplementary")
        if not data.get("topic"):
            errors.append(f"{fname}: supplementary file must have 'topic' field")

    # Word key for this course
    word_key = course.lower()

    categories = data.get("categories", [])
    if not isinstance(categories, list):
        errors.append(f"{fname}: categories must be a list")
        return words_found

    cat_ids: set[str] = set()
    for ci, cat in enumerate(categories):
        cat_id = cat.get("id", "")
        if not cat_id:
            errors.append(f"{fname}: category[{ci}] missing 'id'")
        elif cat_id in cat_ids:
            errors.append(f"{fname}: duplicate category id '{cat_id}'")
        cat_ids.add(cat_id)

        # Check bilingual label
        label = cat.get("label", {})
        if isinstance(label, dict):
            if "en" not in label:
                errors.append(f"{fname}: category '{cat_id}' label missing 'en'")
            if "ko" not in label:
                errors.append(f"{fname}: category '{cat_id}' label missing 'ko'")

        words = cat.get("words", [])
        if not isinstance(words, list):
            errors.append(f"{fname}: category '{cat_id}' words must be a list")
            continue

        for wi, word in enumerate(words):
            target = word.get(word_key, word.get("target", ""))
            if not target:
                errors.append(f"{fname}: category '{cat_id}' word[{wi}] missing '{word_key}' or 'target'")

            # Translation must be bilingual
            trans = word.get("translation", {})
            if isinstance(trans, dict):
                if "en" not in trans:
                    errors.append(f"{fname}: word '{target}' translation missing 'en'")
                if "ko" not in trans:
                    errors.append(f"{fname}: word '{target}' translation missing 'ko'")
            elif not trans:
                errors.append(f"{fname}: word '{target}' missing translation")

            words_found.append({
                "file": fname,
                "target": target,
                "lesson_number": lesson_num,
                "category": cat_id,
            })

    return words_found


def check_duplicates(all_words: list[dict], errors: list[str]):
    """Check for duplicate target words across files."""
    seen: dict[str, str] = {}  # target_lower -> first_file
    for w in all_words:
        key = w["target"].lower().strip()
        if not key:
            continue
        if key in seen:
            errors.append(
                f"DUPLICATE: '{w['target']}' in {w['file']} "
                f"(first seen in {seen[key]})"
            )
        else:
            seen[key] = w["file"]


def validate_course(course: str, check_dupes: bool = False) -> list[str]:
    """Validate all vocabulary files for a course."""
    vocab_dir = CONTENT_DIR / course / "vocabulary"
    if not vocab_dir.exists():
        return [f"Course '{course}' vocabulary directory not found"]

    errors: list[str] = []
    all_words: list[dict] = []
    file_count = 0

    for yaml_path in sorted(vocab_dir.glob("*.yaml")):
        if yaml_path.name.startswith("_"):
            continue
        file_count += 1
        words = validate_file(yaml_path, course, errors)
        all_words.extend(words)

    if check_dupes:
        check_duplicates(all_words, errors)

    print(f"  {course}: {file_count} files, {len(all_words)} words, {len(errors)} errors")
    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate vocabulary YAML files")
    parser.add_argument("--course", help="Validate a specific course only")
    parser.add_argument("--check-dupes", action="store_true",
                        help="Check for duplicate words across files")
    args = parser.parse_args()

    courses = [args.course] if args.course else [
        d.name for d in sorted(CONTENT_DIR.iterdir())
        if d.is_dir() and not d.name.startswith("_")
        and (d / "vocabulary").exists()
    ]

    all_errors: list[str] = []
    for course in courses:
        print(f"Validating {course}...")
        errors = validate_course(course, args.check_dupes)
        for e in errors:
            all_errors.append(f"[{course}] {e}")

    if all_errors:
        print(f"\n{len(all_errors)} error(s) found:")
        for e in all_errors:
            print(f"  ERROR: {e}")
        sys.exit(1)
    else:
        print("\nAll validations passed.")


if __name__ == "__main__":
    main()
