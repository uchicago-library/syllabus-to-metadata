# syllabus-to-metadata

Python library that extracts bibliographic citation metadata from course syllabi (PDF or Word format) using Claude as the LLM backend.

## Project structure

```
syllabus_metadata/
├── __init__.py     # public API: extract_citations(), citations_to_tsv()
├── models.py       # Citation dataclass
├── ingestion.py    # file -> plain text (pdfplumber for PDF, python-docx for docx)
├── llm.py          # Claude API call + JSON response -> list[Citation]
└── output.py       # list[Citation] -> TSV string
tests/
requirements.txt
PLAN.md             # full design record and background
```

## Key design decisions

- **LLM-powered extraction**: Claude (`claude-sonnet-4-6`) does citation identification and field extraction. This handles messy, non-standard citation formats that rule-based parsers can't.
- **LLM returns JSON**: The prompt asks Claude for a JSON array of citation objects. We parse that internally and convert to TSV — do not ask the LLM to produce TSV directly.
- **Abstraction-ready**: LLM logic is isolated in `llm.py` so the backend can be swapped later. Do not scatter Anthropic SDK calls across multiple files.
- **Library, not app**: No CLI entrypoint yet. Keep all code importable.

## Citation fields

All fields are `str | None`. The `item_format` field must be one of: `article`, `bookchapter`, `book`, `audio`, `video`, `streaming video`.

Fields in canonical order (used for TSV output):
`item_format`, `book_journal_title`, `chapter_article_title`, `volume`, `issue`, `journal_year`, `author`, `publisher`, `edition`, `publication_date`, `isxn`, `page_numbers`, `doi`, `url`

## TSV output format

- Two columns: field name (tab) value
- All 14 fields always emitted, value blank if absent
- Citations separated by a blank line

## Dependencies

```
anthropic
pdfplumber
python-docx
```

## General design principles

- **Short functions**: break complex logic into functions of 5-10 lines; factor reusable parts into helpers
- **Prefer pure functions**: avoid side effects where possible; favor referentially transparent functions that map input data to output data, operating on immutable data structures
- **Imperative style**: when required (e.g. for runtime complexity), keep definitions short and modular, and include one-line comments explaining the control flow
- **Handrolled over third-party**: prefer handrolled solutions unless a library is needed because a handrolled solution would be too complex, too slow, or insecure
- **Third-party libraries**: rely on them for document parsing (pdfplumber, python-docx), the LLM API (anthropic), and similarly irreplaceable integrations — not for logic that is straightforward to implement directly
- **Avoid OOP in application code**: prefer ordinary operations on dicts, tuples, lists, and other built-in data structures; prefer higher-order functions over classes and inheritance for abstraction
- **OOP only when required**: adopt object-oriented style only when demanded by a third-party library or framework

## Code style

- **Formatter**: black (line length 88, default settings)
- **Type annotations**: annotate all public API and complex internals; skip obvious cases (e.g. simple one-liners where the type is self-evident)
- **Docstrings**: Google style for public functions and classes; skip docstrings on trivial private helpers
- **Imports**: standard library first, then third-party, then local — separated by blank lines

## Environment

Requires `ANTHROPIC_API_KEY` to be set.
