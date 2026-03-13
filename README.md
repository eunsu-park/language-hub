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
│   │   ├── jlpt_levels.yaml           # JLPT N5-N1 level definitions
│   │   ├── topik_levels.yaml          # TOPIK I-1→II-6 level definitions
│   │   └── proficiency_frameworks.yaml  # CEFR/JLPT/TOPIK/HSK mapping
│   │
│   ├── Spanish/                       # Spanish course (A1→C1 CEFR)
│   │   ├── course_metadata.yaml       # Language config, CEFR stage definitions
│   │   ├── en/                        # Lessons in English (26 files)
│   │   ├── ko/                        # Lessons in Korean (26 files)
│   │   ├── vocabulary/                # Structured vocabulary YAML (66 files, 9,917 words)
│   │   │   ├── 01_*.yaml ... 25_*.yaml  # Lesson vocabulary (25 files)
│   │   │   └── sup_*.yaml               # Supplementary packs by level (41 files)
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
│   │   ├── vocabulary/                # Structured vocabulary YAML (67 files, 9,232 words)
│   │   │   ├── 01_*.yaml ... 25_*.yaml  # Lesson vocabulary (25 files)
│   │   │   └── sup_*.yaml               # Supplementary packs by level (42 files)
│   │   └── grammar/                   # Structured grammar YAML
│   │       ├── conjugations.yaml      # 20 verbs × 6 tenses
│   │       ├── grammar_rules.yaml     # 7 rule types
│   │       ├── tense_rules.yaml       # 10 tense rules
│   │       └── _index.yaml            # Grammar index metadata
│   │
│   ├── Japanese/                      # Japanese course (N5→N1 JLPT)
│   │   ├── course_metadata.yaml       # Language config, JLPT stage definitions
│   │   ├── en/                        # Lessons in English (26 files)
│   │   ├── ko/                        # Lessons in Korean (26 files)
│   │   ├── vocabulary/                # Structured vocabulary YAML (68 files, 8,856 words)
│   │   │   ├── 01_*.yaml ... 25_*.yaml  # Lesson vocabulary (25 files)
│   │   │   └── sup_*.yaml               # Supplementary packs by level (43 files)
│   │   └── grammar/                   # Structured grammar YAML
│   │       ├── conjugations.yaml      # 17 verbs × 10 forms
│   │       ├── grammar_rules.yaml     # 7 rule types
│   │       ├── tense_rules.yaml       # 15 tense rules
│   │       └── _index.yaml            # Grammar index metadata
│   │
│   ├── English/                       # English course (A1→C1 CEFR)
│   │   ├── course_metadata.yaml       # Language config, CEFR stage definitions
│   │   ├── en/                        # Lessons in English (26 files)
│   │   ├── ko/                        # Lessons in Korean (26 files)
│   │   ├── vocabulary/                # Structured vocabulary YAML (67 files, 9,280 words)
│   │   │   ├── 01_*.yaml ... 25_*.yaml  # Lesson vocabulary (25 files)
│   │   │   └── sup_*.yaml               # Supplementary packs by level (42 files)
│   │   └── grammar/                   # Structured grammar YAML
│   │       ├── conjugations.yaml      # 20 verbs × 12 tenses
│   │       ├── grammar_rules.yaml     # 7 rule types
│   │       ├── tense_rules.yaml       # 14 tense rules
│   │       └── _index.yaml            # Grammar index metadata
│   │
│   ├── Italian/                       # Italian course (A1→C1 CEFR)
│   │   ├── course_metadata.yaml       # Language config, CEFR stage definitions
│   │   ├── en/                        # Lessons in English (26 files)
│   │   ├── ko/                        # Lessons in Korean (26 files)
│   │   ├── vocabulary/                # Structured vocabulary YAML (66 files, 7,870 words)
│   │   │   ├── 01_*.yaml ... 25_*.yaml  # Lesson vocabulary (25 files)
│   │   │   └── sup_*.yaml               # Supplementary packs by level (41 files)
│   │   └── grammar/                   # Structured grammar YAML
│   │       ├── conjugations.yaml      # 20 verbs × 7 tenses
│   │       ├── grammar_rules.yaml     # 7 rule types
│   │       ├── tense_rules.yaml       # 14 tense rules
│   │       └── _index.yaml            # Grammar index metadata
│   │
│   ├── Latin/                         # Latin course (A1→C1 CEFR)
│   │   ├── course_metadata.yaml       # Language config, CEFR stage definitions
│   │   ├── en/                        # Lessons in English (26 files)
│   │   ├── ko/                        # Lessons in Korean (26 files)
│   │   ├── vocabulary/                # Structured vocabulary YAML (66 files, ~4,100 words)
│   │   │   ├── 01_*.yaml ... 25_*.yaml  # Lesson vocabulary (25 files)
│   │   │   └── sup_*.yaml               # Supplementary packs by level (40 files)
│   │   └── grammar/                   # Structured grammar YAML
│   │       ├── conjugations.yaml      # 20 verbs × 9 tenses
│   │       ├── grammar_rules.yaml     # 7 rule types
│   │       ├── tense_rules.yaml       # 16 tense rules
│   │       ├── declensions.yaml       # 7 declension paradigms
│   │       └── _index.yaml            # Grammar index metadata
│   │
│   └── Korean/                        # Korean course (TOPIK I-1→II-5)
│       ├── course_metadata.yaml       # Language config, TOPIK stage definitions
│       ├── en/                        # Lessons in English (26 files)
│       ├── ko/                        # Lessons in Korean (26 files)
│       ├── vocabulary/                # Structured vocabulary YAML (69 files, 5,294 words)
│       │   ├── 01_*.yaml ... 25_*.yaml  # Lesson vocabulary (25 files)
│       │   └── sup_*.yaml               # Supplementary packs by level (43 files)
│       └── grammar/                   # Structured grammar YAML
│           ├── conjugations.yaml      # 20 verbs × 7 forms
│           ├── grammar_rules.yaml     # 7 rule types
│           ├── tense_rules.yaml       # 14 tense rules
│           └── _index.yaml            # Grammar index metadata
│
└── scripts/                           # Content management utilities
    ├── validate_vocabulary.py         # Schema + duplicate validation
    ├── generate_index.py              # Regenerate _index.yaml files
    └── supplementary_template.yaml    # YAML schema reference for new packs
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
- 66 vocabulary YAML files (9,917 words)
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
- 67 vocabulary YAML files (9,232 words)
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
- 68 vocabulary YAML files (8,856 words)
- 17 verbs × 10 forms (conjugation tables)
- 7 grammar rule types, 15 tense rules

### English (영어)

25-lesson progressive course from A1 to C1 (CEFR), designed for Korean speakers.

| Stage | CEFR | Lessons | Focus |
|-------|------|---------|-------|
| Foundations / 기초 | A1 | 01-05 | Pronunciation, greetings, articles & nouns, essential verbs, word order |
| Elementary / 초급 | A2 | 06-10 | Past tense, prepositions, adjectives & adverbs, numbers, daily vocabulary |
| Intermediate / 중급 | B1 | 11-15 | Continuous/perfect tenses, modals, passive voice, complete tense system |
| Advanced / 고급 | B2 | 16-20 | Relative clauses, conditionals, phrasal verbs, discourse, vocabulary |
| Practical / 실전 | B2-C1 | 21-25 | Reading, writing, culture, business English, exam prep (TOEIC/IELTS) |

**Content stats:**
- 26 lesson files per language (en + ko)
- 67 vocabulary YAML files (9,280 words)
- 20 verbs × 12 tenses (conjugation tables)
- 7 grammar rule types, 14 tense rules

### Italian (이탈리아어)

25-lesson progressive course from A1 to C1 (CEFR), designed for Korean speakers.

| Stage | CEFR | Lessons | Focus |
|-------|------|---------|-------|
| Foundations / 기초 | A1 | 01-05 | Pronunciation, greetings, articles & gender, essential verbs, present tense |
| Elementary / 초급 | A2 | 06-10 | Adjectives, pronouns & prepositions, numbers, conversation, daily vocabulary |
| Intermediate / 중급 | B1 | 11-15 | Past tenses, future/conditional, subjunctive, complete conjugation system |
| Advanced / 고급 | B2 | 16-20 | Complex sentences, discourse, regional dialects, idioms, vocabulary expansion |
| Practical / 실전 | B2-C1 | 21-25 | Reading, writing, culture, business Italian, exam prep (CILS/CELI) |

**Content stats:**
- 26 lesson files per language (en + ko)
- 66 vocabulary YAML files (7,870 words)
- 20 verbs × 7 tenses (conjugation tables)
- 7 grammar rule types, 14 tense rules

### Latin (라틴어)

25-lesson progressive course from A1 to C1 (CEFR). A classical language course focused on reading ancient texts rather than modern conversation.

| Stage | CEFR | Lessons | Focus |
|-------|------|---------|-------|
| Foundations / 기초 | A1 | 01-05 | Pronunciation, basic phrases, 1st-2nd declension, essential verbs, present tense |
| Elementary / 초급 | A2 | 06-10 | All five declensions, pronouns, prepositions, imperfect/future, numbers |
| Intermediate / 중급 | B1 | 11-15 | Perfect system, passive voice, participles, subjunctive, deponent verbs |
| Advanced / 고급 | B2 | 16-20 | Subordinate clauses, indirect discourse, conditions, ablative absolute |
| Mastery / 고전 완성 | C1 | 21-25 | Classical prose/poetry, Roman civilization, philosophical/legal Latin |

**Content stats:**
- 26 lesson files per language (en + ko)
- 66 vocabulary YAML files (~4,100 words)
- 20 verbs × 9 tenses (conjugation tables)
- 7 grammar rule types, 16 tense rules, 7 declension paradigms

### Korean (한국어)

25-lesson progressive course from TOPIK I-1 to TOPIK II-5 (TOPIK), designed for Korean learners.

| Stage | TOPIK | Lessons | Focus |
|-------|-------|---------|-------|
| Foundations / 기초 | TOPIK I-1 | 01-05 | Hangul, greetings, sentence structure, numbers, present/past tense |
| Elementary / 초급 | TOPIK I-2 | 06-10 | Adjectives, particles, verb endings, daily vocabulary, relationships |
| Intermediate / 중급 | TOPIK II-3 | 11-15 | Irregular conjugation, connective endings, indirect speech, honorifics |
| Advanced / 고급 | TOPIK II-4 | 16-20 | Advanced grammar, reading, Hanja, idioms, thematic vocabulary |
| Practical / 실전 | TOPIK II-5 | 21-25 | Business, writing, culture, media, TOPIK prep |

**Content stats:**
- 26 lesson files per language (en + ko)
- 69 vocabulary YAML files (5,294 words)
- 20 verbs × 7 forms (conjugation tables)
- 7 grammar rule types, 14 tense rules

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
