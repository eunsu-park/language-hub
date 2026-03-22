#!/usr/bin/env python3
"""Extract vocabulary from Spanish lesson Markdown files into structured YAML.

Reads bilingual (EN/KO) lesson Markdown tables and produces per-lesson YAML
files in content/Spanish/vocabulary/, plus an _index.yaml manifest.

Usage:
    cd language_hub
    python scripts/extract_vocabulary.py
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content" / "Spanish"
EN_DIR = CONTENT_DIR / "en"
KO_DIR = CONTENT_DIR / "ko"
VOCAB_DIR = CONTENT_DIR / "vocabulary"
METADATA_FILE = CONTENT_DIR / "course_metadata.yaml"


# ---------------------------------------------------------------------------
# CEFR mapping from course_metadata.yaml
# ---------------------------------------------------------------------------

def load_cefr_map(path: Path) -> dict[str, str]:
    """Return {lesson_number: cefr_level} from course_metadata.yaml."""
    with open(path, encoding="utf-8") as f:
        meta = yaml.safe_load(f)
    mapping: dict[str, str] = {}
    for stage in meta.get("stages", []):
        cefr = stage["cefr"]
        for lesson_num in stage["lessons"]:
            mapping[lesson_num] = cefr
    return mapping


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def strip_bold(text: str) -> str:
    """Remove **bold** markers, keeping inner text."""
    return _BOLD_RE.sub(r"\1", text)


def clean_cell(text: str) -> str:
    """Strip whitespace and bold markers from a table cell."""
    return strip_bold(text.strip())


def slugify(text: str) -> str:
    """Convert a heading into a slug suitable for a YAML id."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s_]", "", text)
    text = re.sub(r"\s+", "_", text.strip())
    return text or "unknown"


# ---------------------------------------------------------------------------
# Markdown table parsing
# ---------------------------------------------------------------------------

@dataclass
class MdTable:
    """A parsed Markdown table."""
    headers: list[str]
    rows: list[list[str]]
    section_heading: str = ""
    subsection_heading: str = ""


def _parse_table_rows(lines: list[str], start: int) -> tuple[list[str], list[list[str]], int]:
    """Parse a Markdown table starting at *start* (header row).

    Returns (headers, rows, next_line_index).
    """
    header_line = lines[start].strip()
    cells = [clean_cell(c) for c in header_line.split("|")]
    # First and last are empty due to leading/trailing |
    headers = [c for c in cells if c != "" or cells.index(c) not in (0, len(cells) - 1)]
    # Re-parse more carefully
    headers = [clean_cell(c) for c in header_line.split("|")[1:-1]]

    # Skip separator row
    idx = start + 1
    if idx < len(lines) and re.match(r"^\|[\s\-:]+\|", lines[idx].strip()):
        idx += 1
    else:
        return headers, [], idx

    rows: list[list[str]] = []
    while idx < len(lines):
        line = lines[idx].strip()
        if not line.startswith("|"):
            break
        # Another separator? (some tables have mid-separators)
        if re.match(r"^\|[\s\-:]+\|$", line):
            idx += 1
            continue
        row_cells = [clean_cell(c) for c in line.split("|")[1:-1]]
        if row_cells:
            rows.append(row_cells)
        idx += 1

    return headers, rows, idx


def extract_tables(filepath: Path) -> list[MdTable]:
    """Extract all Markdown tables from a file with section context."""
    with open(filepath, encoding="utf-8") as f:
        lines = f.readlines()

    tables: list[MdTable] = []
    section = ""
    subsection = ""
    in_code_block = False
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Track code blocks to avoid parsing ASCII-art tables
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            i += 1
            continue

        if in_code_block:
            i += 1
            continue

        # Track section headings
        if stripped.startswith("## ") and not stripped.startswith("### "):
            section = stripped.lstrip("# ").strip()
            subsection = ""
            i += 1
            continue
        if stripped.startswith("### "):
            subsection = stripped.lstrip("# ").strip()
            i += 1
            continue

        # Detect table header row: must be followed by a separator row
        if stripped.startswith("|") and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if next_line.startswith("|") and re.search(r"---", next_line):
                headers, rows, new_i = _parse_table_rows(lines, i)
                if rows:
                    tables.append(MdTable(
                        headers=headers,
                        rows=rows,
                        section_heading=section,
                        subsection_heading=subsection,
                    ))
                i = new_i
                continue

        i += 1

    return tables


# ---------------------------------------------------------------------------
# Table classification
# ---------------------------------------------------------------------------

class TableType:
    VOCABULARY = "vocabulary"
    VOCABULARY_GENDER = "vocabulary_gender"
    VOCABULARY_PAIRED = "vocabulary_paired"
    CONJUGATION = "conjugation"
    PRONOUN = "pronoun"
    PREPOSITION = "preposition"
    COMPARISON = "comparison"
    UNKNOWN = "unknown"


# English header signatures (lowered, stripped)
_EN_HEADER_SIGS: dict[tuple[str, ...], str] = {}

# We classify dynamically based on column content patterns.


def _norm_headers(headers: list[str]) -> list[str]:
    return [h.lower().strip() for h in headers]


def classify_table(table: MdTable, lang: str = "en") -> str:
    """Classify a table by its header pattern."""
    h = _norm_headers(table.headers)
    n = len(h)

    if lang == "en":
        # Pattern C: 4-column paired vocabulary
        if n == 4 and h[0] == "spanish" and h[2] == "spanish":
            return TableType.VOCABULARY_PAIRED

        # Pattern D: Conjugation
        if n >= 3 and h[0] == "subject" and "conjugation" in h[1]:
            return TableType.CONJUGATION

        # Pattern B: Vocabulary with gender
        if n == 3 and h[0] == "spanish" and h[2] == "gender":
            return TableType.VOCABULARY_GENDER

        # Pattern A: Basic vocabulary (Spanish | English | optional)
        if n >= 2 and h[0] == "spanish" and h[1] in ("english", "meaning"):
            if n == 3 and h[2] == "gender":
                return TableType.VOCABULARY_GENDER
            return TableType.VOCABULARY

        # Pattern E: Prepositions
        if n >= 2 and h[0] in ("preposition", "prepositions"):
            return TableType.PREPOSITION

        # Pattern F: Pronouns (Person | Singular | Plural)
        if n >= 3 and h[0] == "person" and "singular" in h[1] and "plural" in h[2]:
            return TableType.PRONOUN

        # Conjugation variant: Subject-based tables
        if n >= 2 and h[0] == "subject" and ("conjugation" in " ".join(h) or "form" in " ".join(h)):
            return TableType.CONJUGATION

        # Expression tables (Expression | Region | Meaning) or similar
        if n >= 2 and h[0] == "expression" and any(
            x in h for x in ("meaning", "region")
        ):
            return TableType.VOCABULARY

        # Politeness Level | Spanish | English
        if n >= 3 and "spanish" in h and ("english" in h or "meaning" in h):
            return TableType.VOCABULARY

        # Time | Greeting | Usage
        if n >= 3 and h[0] == "time" and h[1] in ("greeting",):
            return TableType.VOCABULARY

        # Adjective comparison: Adjective | with SER | with ESTAR
        if n >= 3 and h[0] == "adjective" and any("ser" in x or "estar" in x for x in h):
            return TableType.COMPARISON

        # Articles or grammar structure tables (skip)
        if h[0] in ("", "singular", "plural") and any(
            x in h for x in ("masculine", "feminine")
        ):
            return TableType.UNKNOWN

        # Shortened forms, meaning changes etc.
        if n >= 3 and h[0] in ("full form", "adjective") and any(
            x in h for x in ("shortened", "before noun", "after noun")
        ):
            return TableType.UNKNOWN

        # Verb table with specific verbs as headers
        if n >= 3 and h[0] in ("subject", "person") and all(
            x not in h for x in ("english", "meaning")
        ):
            return TableType.CONJUGATION

        # Compound prepositions
        if n >= 2 and h[0] in ("preposition",) and h[1] in ("meaning",):
            return TableType.PREPOSITION

        # Category | Examples (skip)
        if h[0] in ("category", "structure"):
            return TableType.UNKNOWN

        # Vowel | IPA ... table from lesson 01
        if h[0] in ("letter", "vowel", "digraph"):
            return TableType.UNKNOWN

        # Distance | Masculine ... (demonstratives)
        if h[0] in ("distance",):
            return TableType.UNKNOWN

        # Irregular comparatives
        if n >= 3 and h[0] == "adjective" and any("comparative" in x for x in h):
            return TableType.UNKNOWN

        # Use | Example (para/por usage)
        if n == 2 and h[0] == "use":
            return TableType.UNKNOWN

        # Fallback: tables with Spanish-looking first column data
        # Check first row
        if table.rows and n >= 2:
            first_cell = table.rows[0][0] if table.rows[0] else ""
            # If first cell contains Spanish characters or looks Spanish
            if any(c in first_cell for c in "áéíóúñ¿¡"):
                return TableType.VOCABULARY

    elif lang == "ko":
        # Korean header patterns
        if n == 4 and h[0] == "스페인어" and h[2] == "스페인어":
            return TableType.VOCABULARY_PAIRED
        if n >= 3 and h[0] == "스페인어" and h[2] == "성":
            return TableType.VOCABULARY_GENDER
        if n >= 2 and h[0] == "스페인어" and h[1] == "한국어":
            return TableType.VOCABULARY
        if n >= 3 and h[0] == "주어" and h[1] == "활용형":
            return TableType.CONJUGATION
        if n >= 3 and h[0] == "인칭" and ("단수" in h[1] or "singular" in h[1].lower()):
            return TableType.PRONOUN
        if n >= 2 and h[0] == "전치사":
            return TableType.PREPOSITION
        if n >= 2 and h[0] == "인칭" and "활용형" in h[1]:
            return TableType.CONJUGATION
        if n >= 2 and h[0] == "인칭" and "대명사" in h[1]:
            return TableType.PRONOUN

    return TableType.UNKNOWN


# ---------------------------------------------------------------------------
# Entry extraction
# ---------------------------------------------------------------------------

@dataclass
class VocabEntry:
    spanish: str
    translation_en: str = ""
    translation_ko: str = ""
    gender: Optional[str] = None
    notes_en: str = ""
    notes_ko: str = ""


@dataclass
class ConjugationEntry:
    subject: str
    form: str
    example_es: str = ""
    example_en: str = ""


@dataclass
class PronounEntry:
    person: str
    singular: str
    plural: str


@dataclass
class PrepositionEntry:
    preposition: str
    meaning_en: str = ""
    meaning_ko: str = ""
    example: str = ""


@dataclass
class Category:
    id: str
    label_en: str
    label_ko: str
    type: str  # vocabulary | conjugation | pronoun | preposition
    entries: list = field(default_factory=list)
    # Conjugation-specific
    verb: str = ""
    tense: str = ""


def _detect_gender(text: str) -> Optional[str]:
    """Detect gender from a cell value like 'f', 'm', 'm / f', etc."""
    text = text.strip().lower()
    if text in ("f", "feminine", "femenino"):
        return "f"
    if text in ("m", "masculine", "masculino"):
        return "m"
    if "/" in text:
        # e.g. "m / f" for paired entries -- handled at row level
        return text.replace(" ", "")
    return None


def _split_gender_pairs(spanish: str, english: str, gender_str: str) -> list[tuple[str, str, Optional[str]]]:
    """Split entries like 'el padre / la madre' into separate entries with individual genders.

    Returns list of (spanish, english, gender) tuples.
    """
    # Check for slash-separated pairs in Spanish
    if " / " in spanish and " / " in english:
        es_parts = [p.strip() for p in spanish.split(" / ")]
        en_parts = [p.strip() for p in english.split(" / ")]
        gender_parts = [g.strip() for g in gender_str.split("/")] if "/" in gender_str else [gender_str] * len(es_parts)

        result = []
        for i in range(min(len(es_parts), len(en_parts))):
            g = gender_parts[i].strip().lower() if i < len(gender_parts) else None
            if g in ("m", "f"):
                result.append((es_parts[i], en_parts[i], g))
            else:
                result.append((es_parts[i], en_parts[i], None))
        return result

    gender = _detect_gender(gender_str) if gender_str else None
    # Normalise combined genders like "m/f" to None (ambiguous at entry level)
    if gender and "/" in gender:
        gender = None
    return [(spanish, english, gender)]


def extract_vocab_from_table(
    en_table: MdTable,
    ko_table: Optional[MdTable],
    table_type: str,
) -> Optional[Category]:
    """Convert an EN table (optionally merged with KO) into a Category."""

    section = en_table.subsection_heading or en_table.section_heading
    cat_id = slugify(section)
    label_en = section
    label_ko = ""
    if ko_table:
        ko_section = ko_table.subsection_heading or ko_table.section_heading
        label_ko = ko_section

    if table_type == TableType.VOCABULARY:
        entries = _extract_basic_vocab(en_table, ko_table)
        if not entries:
            return None
        return Category(
            id=cat_id, label_en=label_en, label_ko=label_ko,
            type="vocabulary", entries=entries,
        )

    if table_type == TableType.VOCABULARY_GENDER:
        entries = _extract_gender_vocab(en_table, ko_table)
        if not entries:
            return None
        return Category(
            id=cat_id, label_en=label_en, label_ko=label_ko,
            type="vocabulary", entries=entries,
        )

    if table_type == TableType.VOCABULARY_PAIRED:
        entries = _extract_paired_vocab(en_table, ko_table)
        if not entries:
            return None
        return Category(
            id=cat_id, label_en=label_en, label_ko=label_ko,
            type="vocabulary", entries=entries,
        )

    if table_type == TableType.CONJUGATION:
        entries, verb, tense = _extract_conjugation(en_table, ko_table)
        if not entries:
            return None
        return Category(
            id=cat_id, label_en=label_en, label_ko=label_ko,
            type="conjugation", entries=entries,
            verb=verb, tense=tense,
        )

    if table_type == TableType.PRONOUN:
        entries = _extract_pronouns(en_table, ko_table)
        if not entries:
            return None
        return Category(
            id=cat_id, label_en=label_en, label_ko=label_ko,
            type="pronoun", entries=entries,
        )

    if table_type == TableType.PREPOSITION:
        entries = _extract_prepositions(en_table, ko_table)
        if not entries:
            return None
        return Category(
            id=cat_id, label_en=label_en, label_ko=label_ko,
            type="preposition", entries=entries,
        )

    return None


# --- Extraction helpers ---

def _extract_basic_vocab(en_t: MdTable, ko_t: Optional[MdTable]) -> list[VocabEntry]:
    """Pattern A: Spanish | English | Notes (3-col) or Spanish | English (2-col)."""
    entries: list[VocabEntry] = []
    h = _norm_headers(en_t.headers)

    # Find column indices dynamically
    es_col = _find_col(h, ("spanish", "expression", "greeting"))
    en_col = _find_col(h, ("english", "meaning"))
    notes_col = _find_col(h, ("notes", "usage", "formality", "region"))

    # Fallback: for tables like "Politeness Level | Spanish | English"
    if es_col is None:
        es_col = _find_col(h, ("spanish",))
    if en_col is None:
        en_col = _find_col(h, ("english",))

    # For tables where first col is the Spanish word
    if es_col is None and en_col is None and len(h) >= 2:
        es_col = 0
        en_col = 1
        if len(h) >= 3:
            notes_col = 2

    if es_col is None or en_col is None:
        return entries

    # Build KO lookup: match by Spanish word
    ko_map: dict[str, str] = {}
    ko_notes_map: dict[str, str] = {}
    if ko_t:
        ko_h = _norm_headers(ko_t.headers)
        ko_es_col = _find_col(ko_h, ("스페인어", "표현"))
        ko_trans_col = _find_col(ko_h, ("한국어", "의미"))
        ko_notes_col = _find_col(ko_h, ("비고", "용법", "격식 수준", "지역"))
        if ko_es_col is None and ko_trans_col is None and len(ko_h) >= 2:
            ko_es_col = 0
            ko_trans_col = 1
            if len(ko_h) >= 3:
                ko_notes_col = 2
        if ko_es_col is not None and ko_trans_col is not None:
            for row in ko_t.rows:
                if ko_es_col < len(row) and ko_trans_col < len(row):
                    key = row[ko_es_col]
                    ko_map[key] = row[ko_trans_col]
                    if ko_notes_col is not None and ko_notes_col < len(row):
                        ko_notes_map[key] = row[ko_notes_col]

    for row in en_t.rows:
        if es_col >= len(row) or en_col >= len(row):
            continue
        spanish = row[es_col]
        english = row[en_col]
        notes_en = row[notes_col] if notes_col is not None and notes_col < len(row) else ""
        if not spanish:
            continue
        entries.append(VocabEntry(
            spanish=spanish,
            translation_en=english,
            translation_ko=ko_map.get(spanish, ""),
            gender=None,
            notes_en=notes_en,
            notes_ko=ko_notes_map.get(spanish, ""),
        ))

    return entries


def _extract_gender_vocab(en_t: MdTable, ko_t: Optional[MdTable]) -> list[VocabEntry]:
    """Pattern B: Spanish | English | Gender."""
    entries: list[VocabEntry] = []
    h = _norm_headers(en_t.headers)

    es_col = _find_col(h, ("spanish",))
    en_col = _find_col(h, ("english",))
    gen_col = _find_col(h, ("gender",))

    if es_col is None or en_col is None:
        return entries

    # KO lookup
    ko_map: dict[str, str] = {}
    if ko_t:
        ko_h = _norm_headers(ko_t.headers)
        ko_es_col = _find_col(ko_h, ("스페인어",))
        ko_trans_col = _find_col(ko_h, ("한국어",))
        if ko_es_col is None and len(ko_h) >= 2:
            ko_es_col = 0
            ko_trans_col = 1
        if ko_es_col is not None and ko_trans_col is not None:
            for row in ko_t.rows:
                if ko_es_col < len(row) and ko_trans_col < len(row):
                    ko_map[row[ko_es_col]] = row[ko_trans_col]

    for row in en_t.rows:
        if es_col >= len(row) or en_col >= len(row):
            continue
        spanish = row[es_col]
        english = row[en_col]
        gender_str = row[gen_col] if gen_col is not None and gen_col < len(row) else ""
        if not spanish:
            continue

        # Handle slash-separated pairs (e.g. "el padre / la madre")
        for sp, en, g in _split_gender_pairs(spanish, english, gender_str):
            entries.append(VocabEntry(
                spanish=sp,
                translation_en=en,
                translation_ko=ko_map.get(spanish, ""),
                gender=g,
            ))

    return entries


def _extract_paired_vocab(en_t: MdTable, ko_t: Optional[MdTable]) -> list[VocabEntry]:
    """Pattern C: Spanish | English | Spanish | English (4-col)."""
    entries: list[VocabEntry] = []

    # KO lookup
    ko_map: dict[str, str] = {}
    if ko_t:
        for row in ko_t.rows:
            if len(row) >= 2:
                ko_map[row[0]] = row[1]
            if len(row) >= 4:
                ko_map[row[2]] = row[3]

    for row in en_t.rows:
        if len(row) >= 2 and row[0]:
            entries.append(VocabEntry(
                spanish=row[0],
                translation_en=row[1],
                translation_ko=ko_map.get(row[0], ""),
            ))
        if len(row) >= 4 and row[2]:
            entries.append(VocabEntry(
                spanish=row[2],
                translation_en=row[3],
                translation_ko=ko_map.get(row[2], ""),
            ))

    return entries


def _extract_conjugation(
    en_t: MdTable, ko_t: Optional[MdTable],
) -> tuple[list[ConjugationEntry], str, str]:
    """Pattern D: Subject | Conjugation | Example."""
    entries: list[ConjugationEntry] = []
    h = _norm_headers(en_t.headers)

    subj_col = _find_col(h, ("subject", "person"))
    conj_col = _find_col(h, ("conjugation", "form"))
    ex_col = _find_col(h, ("example",))

    if subj_col is None:
        subj_col = 0
    if conj_col is None:
        conj_col = 1 if len(h) > 1 else None
    if conj_col is None:
        return entries, "", ""

    # Infer verb and tense from section heading
    verb, tense = _infer_verb_tense(en_t.section_heading, en_t.subsection_heading)

    for row in en_t.rows:
        if subj_col >= len(row) or conj_col >= len(row):
            continue
        subject = row[subj_col]
        form = row[conj_col]
        example_es = ""
        example_en = ""
        if ex_col is not None and ex_col < len(row):
            example_raw = row[ex_col]
            # Examples often have format: "Spanish sentence. (English sentence.)"
            m = re.match(r"^(.+?)\s*\((.+?)\)\s*$", example_raw)
            if m:
                example_es = m.group(1).strip()
                example_en = m.group(2).strip()
            else:
                example_es = example_raw

        entries.append(ConjugationEntry(
            subject=subject,
            form=form,
            example_es=example_es,
            example_en=example_en,
        ))

    return entries, verb, tense


def _infer_verb_tense(section: str, subsection: str) -> tuple[str, str]:
    """Try to infer verb name and tense from section headings."""
    combined = f"{section} {subsection}".lower()

    # Common verbs
    verbs = ["ser", "estar", "tener", "haber", "ir", "hablar", "comer", "vivir"]
    verb = ""
    for v in verbs:
        if v in combined:
            verb = v
            break

    tense = "present"
    tense_map = {
        "present": "present",
        "preterite": "preterite",
        "imperfect": "imperfect",
        "future": "future",
        "conditional": "conditional",
        "subjunctive": "subjunctive",
        "imperative": "imperative",
    }
    for key, val in tense_map.items():
        if key in combined:
            tense = val
            break

    return verb, tense


def _extract_pronouns(en_t: MdTable, ko_t: Optional[MdTable]) -> list[PronounEntry]:
    """Pattern F: Person | Singular | Plural."""
    entries: list[PronounEntry] = []

    for row in en_t.rows:
        if len(row) >= 3:
            entries.append(PronounEntry(
                person=row[0],
                singular=row[1],
                plural=row[2],
            ))

    return entries


def _extract_prepositions(en_t: MdTable, ko_t: Optional[MdTable]) -> list[PrepositionEntry]:
    """Pattern E: Preposition | Meaning | Example."""
    entries: list[PrepositionEntry] = []
    h = _norm_headers(en_t.headers)

    prep_col = 0
    meaning_col = _find_col(h, ("meaning",))
    example_col = _find_col(h, ("example",))

    if meaning_col is None and len(h) >= 2:
        meaning_col = 1
    if example_col is None and len(h) >= 3:
        example_col = 2

    # KO lookup
    ko_map: dict[str, str] = {}
    if ko_t:
        for row in ko_t.rows:
            if len(row) >= 2:
                ko_map[row[0]] = row[1]

    for row in en_t.rows:
        if prep_col >= len(row):
            continue
        prep = row[prep_col]
        meaning_en = row[meaning_col] if meaning_col is not None and meaning_col < len(row) else ""
        example = row[example_col] if example_col is not None and example_col < len(row) else ""
        if not prep:
            continue
        entries.append(PrepositionEntry(
            preposition=prep,
            meaning_en=meaning_en,
            meaning_ko=ko_map.get(prep, ""),
            example=example,
        ))

    return entries


def _find_col(headers: list[str], candidates: tuple[str, ...]) -> Optional[int]:
    """Find the first column index whose header matches any candidate."""
    for i, h in enumerate(headers):
        for c in candidates:
            if c == h or c in h:
                return i
    return None


# ---------------------------------------------------------------------------
# Table pairing between EN and KO
# ---------------------------------------------------------------------------

def _section_key(table: MdTable) -> str:
    """Create a key for matching tables between EN and KO by section."""
    # We use the section number prefix if available (e.g. "6. Essential Nouns: Family")
    # But the text differs between EN and KO, so we extract the number prefix
    sec = table.section_heading
    sub = table.subsection_heading

    # Extract leading number from section heading like "6. Essential Nouns: Family"
    sec_num = ""
    m = re.match(r"^(\d+[\.\d]*)", sec)
    if m:
        sec_num = m.group(1)

    sub_num = ""
    m = re.match(r"^(\d+[\.\d]*)", sub)
    if m:
        sub_num = m.group(1)

    return f"{sec_num}|{sub_num}"


def pair_tables(
    en_tables: list[MdTable], ko_tables: list[MdTable],
) -> list[tuple[MdTable, Optional[MdTable]]]:
    """Pair EN tables with their KO counterparts by section numbering."""

    # Group KO tables by section key, preserving order within each key
    ko_by_section: dict[str, list[MdTable]] = {}
    for t in ko_tables:
        key = _section_key(t)
        ko_by_section.setdefault(key, []).append(t)

    # Track consumption index per section key
    ko_consumed: dict[str, int] = {}

    pairs: list[tuple[MdTable, Optional[MdTable]]] = []
    for en_t in en_tables:
        key = _section_key(en_t)
        ko_list = ko_by_section.get(key, [])
        idx = ko_consumed.get(key, 0)
        if idx < len(ko_list):
            pairs.append((en_t, ko_list[idx]))
            ko_consumed[key] = idx + 1
        else:
            pairs.append((en_t, None))

    return pairs


# ---------------------------------------------------------------------------
# YAML output
# ---------------------------------------------------------------------------

def _vocab_entry_to_dict(e: VocabEntry) -> dict:
    d: dict = {"spanish": e.spanish}
    translation: dict = {}
    if e.translation_en:
        translation["en"] = e.translation_en
    if e.translation_ko:
        translation["ko"] = e.translation_ko
    if translation:
        d["translation"] = translation
    d["gender"] = e.gender
    notes: dict = {}
    if e.notes_en:
        notes["en"] = e.notes_en
    if e.notes_ko:
        notes["ko"] = e.notes_ko
    if notes:
        d["notes"] = notes
    return d


def _conjugation_entry_to_dict(e: ConjugationEntry) -> dict:
    d: dict = {"subject": e.subject, "form": e.form}
    example: dict = {}
    if e.example_es:
        example["es"] = e.example_es
    if e.example_en:
        example["en"] = e.example_en
    if example:
        d["example"] = example
    return d


def _pronoun_entry_to_dict(e: PronounEntry) -> dict:
    return {"person": e.person, "singular": e.singular, "plural": e.plural}


def _preposition_entry_to_dict(e: PrepositionEntry) -> dict:
    d: dict = {"preposition": e.preposition}
    meaning: dict = {}
    if e.meaning_en:
        meaning["en"] = e.meaning_en
    if e.meaning_ko:
        meaning["ko"] = e.meaning_ko
    if meaning:
        d["meaning"] = meaning
    if e.example:
        d["example"] = e.example
    return d


def category_to_dict(cat: Category) -> dict:
    d: dict = {
        "id": cat.id,
        "label": {"en": cat.label_en},
        "type": cat.type,
    }
    if cat.label_ko:
        d["label"]["ko"] = cat.label_ko

    if cat.type == "conjugation":
        if cat.verb:
            d["verb"] = cat.verb
        if cat.tense:
            d["tense"] = cat.tense
        d["entries"] = [_conjugation_entry_to_dict(e) for e in cat.entries]
    elif cat.type == "pronoun":
        d["entries"] = [_pronoun_entry_to_dict(e) for e in cat.entries]
    elif cat.type == "preposition":
        d["entries"] = [_preposition_entry_to_dict(e) for e in cat.entries]
    else:
        # vocabulary
        d["words"] = [_vocab_entry_to_dict(e) for e in cat.entries]

    return d


# ---------------------------------------------------------------------------
# Lesson processing
# ---------------------------------------------------------------------------

def _lesson_name_from_filename(filename: str) -> str:
    """Convert '02_Greetings_and_Basic_Conversation.md' to '02_Greetings_and_Basic_Conversation'."""
    return filename.rsplit(".", 1)[0]


def _lesson_number(filename: str) -> int:
    """Extract lesson number from filename like '02_Greetings...'."""
    m = re.match(r"^(\d+)_", filename)
    return int(m.group(1)) if m else 0


def process_lesson(
    en_file: Path,
    ko_file: Path,
    cefr: str,
) -> Optional[dict]:
    """Process a single lesson and return the YAML-ready dict."""
    filename = en_file.name
    lesson_name = _lesson_name_from_filename(filename)
    lesson_num = _lesson_number(filename)

    en_tables = extract_tables(en_file)
    ko_tables = extract_tables(ko_file) if ko_file.exists() else []

    pairs = pair_tables(en_tables, ko_tables)

    categories: list[Category] = []
    for en_t, ko_t in pairs:
        ttype = classify_table(en_t, "en")
        if ttype == TableType.UNKNOWN:
            continue
        cat = extract_vocab_from_table(en_t, ko_t, ttype)
        if cat and cat.entries:
            categories.append(cat)

    if not categories:
        return None

    # Deduplicate category IDs
    seen_ids: dict[str, int] = {}
    for cat in categories:
        if cat.id in seen_ids:
            seen_ids[cat.id] += 1
            cat.id = f"{cat.id}_{seen_ids[cat.id]}"
        else:
            seen_ids[cat.id] = 0

    return {
        "lesson": lesson_name,
        "lesson_number": lesson_num,
        "cefr": cefr,
        "categories": [category_to_dict(c) for c in categories],
    }


def _count_words(lesson_data: dict) -> int:
    """Count total word/entry items across all categories."""
    total = 0
    for cat in lesson_data.get("categories", []):
        total += len(cat.get("words", cat.get("entries", [])))
    return total


def _category_ids(lesson_data: dict) -> list[str]:
    return [c["id"] for c in lesson_data.get("categories", [])]


# ---------------------------------------------------------------------------
# Custom YAML representer for clean output
# ---------------------------------------------------------------------------

def _str_representer(dumper: yaml.Dumper, data: str) -> yaml.ScalarNode:
    """Use literal block style for multiline strings, otherwise default."""
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


def _none_representer(dumper: yaml.Dumper, data: None) -> yaml.ScalarNode:
    return dumper.represent_scalar("tag:yaml.org,2002:null", "null")


yaml.add_representer(str, _str_representer)
yaml.add_representer(type(None), _none_representer)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not CONTENT_DIR.exists():
        print(f"Error: Content directory not found: {CONTENT_DIR}", file=sys.stderr)
        sys.exit(1)

    if not METADATA_FILE.exists():
        print(f"Error: Metadata file not found: {METADATA_FILE}", file=sys.stderr)
        sys.exit(1)

    cefr_map = load_cefr_map(METADATA_FILE)
    VOCAB_DIR.mkdir(parents=True, exist_ok=True)

    en_files = sorted(EN_DIR.glob("*.md"))
    index_entries: list[dict] = []

    for en_file in en_files:
        filename = en_file.name
        # Skip overview
        if filename == "00_Overview.md":
            continue

        lesson_num_str = re.match(r"^(\d+)_", filename)
        if not lesson_num_str:
            continue
        lesson_num_str = lesson_num_str.group(1)

        ko_file = KO_DIR / filename
        cefr = cefr_map.get(lesson_num_str, "")

        lesson_data = process_lesson(en_file, ko_file, cefr)
        if lesson_data is None:
            print(f"  Skipping {filename} (no extractable tables)")
            continue

        # Write per-lesson YAML
        yaml_filename = f"{_lesson_name_from_filename(filename).lower()}.yaml"
        yaml_path = VOCAB_DIR / yaml_filename

        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(
                lesson_data,
                f,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False,
                width=120,
            )

        word_count = _count_words(lesson_data)
        cat_ids = _category_ids(lesson_data)
        print(f"  {yaml_filename}: {word_count} entries, {len(cat_ids)} categories")

        index_entries.append({
            "file": yaml_filename,
            "lesson": lesson_data["lesson"],
            "word_count": word_count,
            "categories": cat_ids,
        })

    # Write _index.yaml
    index_data = {
        "course": "Spanish",
        "files": index_entries,
    }
    index_path = VOCAB_DIR / "_index.yaml"
    with open(index_path, "w", encoding="utf-8") as f:
        yaml.dump(
            index_data,
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            width=120,
        )

    total_words = sum(e["word_count"] for e in index_entries)
    print(f"\nDone. {len(index_entries)} lessons, {total_words} total entries.")
    print(f"Output: {VOCAB_DIR}")


if __name__ == "__main__":
    main()
