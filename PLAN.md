# syllabus-to-metadata: Project Plan

## Background

This document records the design decisions made during initial planning for the syllabus-to-metadata library. It serves as both a record of the discussion and a reference for future development sessions.

## Problem Statement

Course syllabi (typically in PDF or Word format) contain bibliographic citations in a variety of formats (APA, Chicago, MLA, or ad hoc). We want a utility that:
1. Ingests a syllabus file
2. Identifies all bibliographic citations, even in messy or non-standard formats
3. Extracts structured metadata for each citation
4. Outputs the metadata in a parseable format

The intended downstream use is improving the user flow for course reserve requests, though the output is designed to be general-purpose.

## Design Decisions

### Extraction approach: LLM-powered
Given that input is intentionally messy and format-agnostic, we use an LLM (Claude) for citation identification and field extraction. This provides "best effort" handling of non-standard citation formats. Rule-based parsers were considered but rejected due to their fragility on messy input.

### LLM backend: Claude (abstraction-ready)
For the first pass, we use the Anthropic Python SDK with `claude-sonnet-4-6`. The LLM logic is isolated in `llm.py` behind a clean interface so that a future `llm_backend` parameter can swap in other providers.

### Document ingestion
- PDF: `pdfplumber`
- Word (.docx): `python-docx`

### Output format: TSV
Two-column TSV: field name in column 1, value in column 2. All fields are always emitted (value is blank if absent). Multiple citations are separated by a blank line.

### Delivery: Python library
The code is structured as a Python library (`syllabus_metadata` package) so it can be imported by CLI tools, GUI applications, or web applications.

## Citation Fields

All fields are optional:

| Field | Notes |
|-------|-------|
| `item_format` | One of: article, bookchapter, book, audio, video, streaming video |
| `book_journal_title` | |
| `chapter_article_title` | |
| `volume` | |
| `issue` | |
| `journal_year` | |
| `author` | |
| `publisher` | |
| `edition` | |
| `publication_date` | |
| `isxn` | ISBN or ISSN |
| `page_numbers` | |
| `doi` | |
| `url` | |

## Project Structure

```
syllabus-to-metadata/
├── syllabus_metadata/
│   ├── __init__.py         # public API: extract_citations, citations_to_tsv
│   ├── models.py           # Citation dataclass
│   ├── ingestion.py        # PDF and docx -> plain text
│   ├── llm.py              # LLM backend (Claude); abstraction-ready
│   └── output.py           # Citation list -> TSV string
├── tests/
│   ├── test_ingestion.py
│   ├── test_output.py
│   └── test_extractor.py
├── requirements.txt
├── PLAN.md                 # this file
└── README.md
```

## Public API

```python
from syllabus_metadata import extract_citations, citations_to_tsv

citations = extract_citations("path/to/syllabus.pdf")
tsv_output = citations_to_tsv(citations)
print(tsv_output)
```

## TSV Output Format

Each citation is a block of 14 rows (one per field), separated from the next citation by a blank line:

```
item_format	article
book_journal_title	Journal of Higher Education
chapter_article_title	Active Learning Strategies
volume	42
issue	3
journal_year	2021
author	Smith, Jane
publisher
edition
publication_date
isxn
page_numbers	100-115
doi	10.1234/jhe.2021.42.3.100
url

item_format	book
book_journal_title	The Craft of Research
chapter_article_title
volume
issue
journal_year
author	Booth, Wayne C.; Colomb, Gregory G.
publisher	University of Chicago Press
edition	4th
publication_date	2016
isxn	9780226239736
page_numbers
doi
url
```

## Dependencies

```
anthropic
pdfplumber
python-docx
```

## Setup & Verification

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
python -m pytest tests/
```

## Development Stages

The project is built incrementally. Each stage is tested manually, then committed before moving on.

### Stage 1: Minimal Claude integration
A single Python function that reads a prompt from a text file on disk, submits it to Claude, and returns Claude's response as a string. Goal: verify the Claude API integration works end-to-end.

### Stage 2: Citation extraction from a Word document
Extend stage 1 with a function that reads a prompt and a `.docx` file from disk, extracts the document text, sends both to Claude, and returns a TSV-formatted string of all citations found. This is the core feature of the library.

### Stage 3: Add PDF support
Extend stage 2 with the ability to also accept a `.pdf` file. The function detects the file type and extracts text accordingly, then proceeds identically to stage 2.

### Stage 4: Pluggable LLM backend
Refactor the LLM call behind an abstraction so the backend is configurable. Add support for a second backend (e.g. Llama 3 via Ollama) alongside Claude. The prompt and document are still read from disk; the caller selects which backend to use.
