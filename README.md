# Language Hub

언어 학습 콘텐츠 저장소입니다. 품질 검사를 통과한 구조화된 어휘, 문법 참조, 레슨 자료를 공개합니다.

A language learning content repository. Publishes structured vocabulary, grammar references, and lesson materials that have passed quality review.

> This repository contains curated content selected from a private working repository after passing quality checks.
> It starts empty and grows as content passes quality review.

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
│   └── <Language>/                    # Per-language course directory
│       ├── course_metadata.yaml       # Language config, proficiency definitions
│       ├── en/                        # Lessons in English
│       ├── ko/                        # Lessons in Korean
│       ├── vocabulary/                # Structured vocabulary YAML
│       └── grammar/                   # Structured grammar YAML
│
└── scripts/                           # Content management utilities
```

## Courses / 코스

| Language / 언어 | Framework | Lessons | Words | Status |
|---|---|---|---|---|
| [Spanish / 스페인어](./content/Spanish/en/00_Overview.md) | CEFR A1→C1 | 25 | 9,917 | Published |
| [German / 독일어](./content/German/en/00_Overview.md) | CEFR A1→C1 | 25 | 9,232 | Published |
| [English / 영어](./content/English/en/00_Overview.md) | CEFR A1→C1 | 25 | 9,280 | Published |
| [Italian / 이탈리아어](./content/Italian/en/00_Overview.md) | CEFR A1→C1 | 25 | 7,870 | Published |
| [Japanese / 일본어](./content/Japanese/en/00_Overview.md) | JLPT N5→N1 | 25 | 8,856 | Published |
| [Latin / 라틴어](./content/Latin/en/00_Overview.md) | CEFR A1→C1 | 25 | 4,329 | Published |
| [Korean / 한국어](./content/Korean/en/00_Overview.md) | TOPIK I-1→II-5 | 25 | 5,294 | Published |
| [Classical Chinese / 한문](./content/Classical_Chinese/en/00_Overview.md) | 한자능력등급 L5→L1 | 25 | 1,783 | Published |

---

## Bilingual Policy / 다국어 정책

All lessons are available in both English (`en/`) and Korean (`ko/`).

모든 레슨은 영어(`en/`)와 한국어(`ko/`) 두 언어로 제공됩니다.

---

## Companion Viewer / 뷰어

This content is rendered by the [language-hub-viewer](https://github.com/eunsu-park/language-hub-viewer) — a Flask-based web viewer with flashcards, quizzes, TTS pronunciation, and proficiency progress tracking.

이 콘텐츠는 [language-hub-viewer](https://github.com/eunsu-park/language-hub-viewer)로 렌더링됩니다 — Flask 기반 웹 뷰어로 플래시카드, 퀴즈, TTS 발음, 숙련도 진도 추적을 지원합니다.

---

## License / 라이센스

| Target / 대상 | License / 라이센스 |
|---|---|
| Study materials (`content/`) / 학습 자료 | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) |

## Author

**Eunsu Park**
- [ORCID: 0000-0003-0969-286X](https://orcid.org/0000-0003-0969-286X)
