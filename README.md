# Language Hub

언어 학습 콘텐츠 저장소입니다. 구조화된 어휘, 문법 참조, 레슨 자료를 관리합니다.

A language learning content repository. Manages structured vocabulary, grammar references, and lesson materials.

---

## Project Structure / 프로젝트 구조

```
language-hub/
├── README.md
├── LICENSE
│
├── content/
│   ├── _shared/                       # Cross-language metadata
│   │   ├── cefr_levels.yaml           # CEFR A1-C2 level definitions
│   │   └── proficiency_frameworks.yaml  # CEFR/JLPT/TOPIK/HSK mapping
│   │
│   ├── Spanish/                       # Spanish course (A1→C1 CEFR)
│   │   ├── course_metadata.yaml       # Language config, CEFR stage definitions
│   │   ├── en/                        # Lessons in English (26 files)
│   │   ├── ko/                        # Lessons in Korean (26 files)
│   │   ├── vocabulary/                # Structured vocabulary YAML (25 files, 1,031 words)
│   │   └── grammar/                   # Structured grammar YAML
│   │       ├── conjugations.yaml      # 22 verbs × 7 tenses
│   │       ├── grammar_rules.yaml     # 7 rule types
│   │       ├── tense_rules.yaml       # Tense formation patterns
│   │       └── _index.yaml            # Grammar index metadata
│   │
│   ├── German/                        # German course (A1→C1 CEFR)
│   │   ├── course_metadata.yaml       # Language config, CEFR stage definitions
│   │   ├── en/                        # Lessons in English (26 files)
│   │   ├── ko/                        # Lessons in Korean (26 files)
│   │   ├── vocabulary/                # Structured vocabulary YAML (25 files, 997 words)
│   │   └── grammar/                   # Structured grammar YAML
│   │       ├── conjugations.yaml      # 20 verbs × 6 tenses
│   │       ├── grammar_rules.yaml     # 7 rule types
│   │       ├── tense_rules.yaml       # 10 tense rules
│   │       └── _index.yaml            # Grammar index metadata
│   │
│   └── Japanese/                      # Japanese course (N5→N1 JLPT)
│       ├── course_metadata.yaml       # Language config, JLPT stage definitions
│       ├── en/                        # Lessons in English (26 files)
│       ├── ko/                        # Lessons in Korean (26 files)
│       ├── vocabulary/                # Structured vocabulary YAML (25 files, 891 words)
│       └── grammar/                   # Structured grammar YAML
│           ├── conjugations.yaml      # 17 verbs × 10 forms
│           ├── grammar_rules.yaml     # 7 rule types
│           ├── tense_rules.yaml       # 15 tense rules
│           └── _index.yaml            # Grammar index metadata
│
└── scripts/                           # Content management utilities
```

## Courses / 코스

### Spanish (스페인어)

25-lesson progressive course from A1 to C1 (CEFR).

| Stage | CEFR | Lessons | Focus |
|-------|------|---------|-------|
| Foundations / 기초 | A1 | 01-05 | Pronunciation, greetings, nouns, verbs, present tense |
| Elementary / 초급 | A2 | 06-10 | Adjectives, pronouns, numbers, daily vocabulary |
| Intermediate / 중급 | B1 | 11-15 | Past tenses, future, subjunctive, conjugation system |
| Advanced / 고급 | B2 | 16-20 | Complex sentences, regional variations, idioms |
| Practical / 실전 | B2-C1 | 21-25 | Reading, writing, culture, business, exam prep |

**Content stats:**
- 26 lesson files per language (en + ko)
- 25 vocabulary YAML files (1,031 words total)
- 22 verbs × 7 tenses (conjugation tables)
- 7 grammar rule types

### German (독일어)

25-lesson progressive course from A1 to C1 (CEFR).

| Stage | CEFR | Lessons | Focus |
|-------|------|---------|-------|
| Foundations / 기초 | A1 | 01-05 | Pronunciation, greetings, nouns & gender, essential verbs, present tense |
| Elementary / 초급 | A2 | 06-10 | Cases (Nom/Acc), adjectives, numbers & time, modal verbs, daily vocabulary |
| Intermediate / 중급 | B1 | 11-15 | Cases (Dat/Gen), past tenses, separable verbs, pronouns, verb system |
| Advanced / 고급 | B2 | 16-20 | Konjunktiv II, adjective declension, passive voice, idioms, thematic vocab |
| Practical / 실전 | B2-C1 | 21-25 | Reading, writing, culture, business, exam prep |

**Content stats:**
- 26 lesson files per language (en + ko)
- 25 vocabulary YAML files (997 words total)
- 20 verbs × 6 tenses (conjugation tables)
- 7 grammar rule types, 10 tense rules

### Japanese (일본어)

25-lesson progressive course from N5 to N1 (JLPT).

| Stage | JLPT | Lessons | Focus |
|-------|------|---------|-------|
| Foundations / 기초 | N5 | 01-05 | Writing systems, greetings, sentence structure, numbers, verbs |
| Elementary / 초급 | N4 | 06-10 | Adjectives, particles, て-form, daily vocabulary, giving/receiving |
| Intermediate / 중급 | N3 | 11-15 | Verb forms, conditionals, opinions, honorifics, complex sentences |
| Advanced / 고급 | N2 | 16-20 | Advanced grammar, reading, kanji strategies, idioms, thematic vocab |
| Practical / 실전 | N1 | 21-25 | Business, writing, culture, media, JLPT prep |

**Content stats:**
- 26 lesson files per language (en + ko)
- 25 vocabulary YAML files (891 words total)
- 17 verbs × 10 forms (conjugation tables)
- 7 grammar rule types, 15 tense rules

## Companion Viewer / 뷰어

This content is rendered by the [language-hub-viewer](https://github.com/eunsu-park/language-hub-viewer) — a Flask-based web viewer with flashcards, quizzes, TTS pronunciation, and proficiency progress tracking.

이 콘텐츠는 [language-hub-viewer](https://github.com/eunsu-park/language-hub-viewer)로 렌더링됩니다 — Flask 기반 웹 뷰어로 플래시카드, 퀴즈, TTS 발음, 숙련도 진도 추적을 지원합니다.

## Bilingual Policy / 다국어 정책

All lessons are available in both English (`en/`) and Korean (`ko/`).

모든 레슨은 영어(`en/`)와 한국어(`ko/`) 두 언어로 제공됩니다.

## License / 라이센스

| Target / 대상 | License / 라이센스 |
|---|---|
| Study materials (`content/`) / 학습 자료 | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) |

## Author

**Eunsu Park**
- [ORCID: 0000-0003-0969-286X](https://orcid.org/0000-0003-0969-286X)
