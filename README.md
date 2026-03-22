# Language Hub

언어 학습 콘텐츠 저장소입니다. 품질 검사를 통과한 구조화된 어휘, 문법 참조, 레슨 자료를 공개합니다.

A language learning content repository. Publishes structured vocabulary, grammar references, and lesson materials that have passed quality review.

> This repository contains curated content selected from a private working repository after passing quality checks.
> It starts empty and grows as content passes quality review.

---

## Quality Criteria / 품질 기준

콘텐츠가 이 레포지토리에 게시되려면 다음 검사를 모두 통과해야 합니다:

| Check / 검사 항목 | Description / 설명 |
|---|---|
| EN Content | English content exists and is high quality / 영문 콘텐츠가 존재하고 양질인지 |
| KO Translation | Korean translation is correct / 한글 번역이 올바른지 |
| Vocabulary Count | Vocabulary word count is sufficient / 단어의 수가 충분한지 |
| Grammar Data | Grammar data exists and is non-empty / Grammar 데이터 존재 및 비어있지 않은지 |

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
