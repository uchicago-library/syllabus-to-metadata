# syllabus-to-metadata

`syllabus-to-metadata` is a Python library that extracts bibliographic
citation metadata from course syllabi in PDF or Word format. It uses
an LLM to identify and parse citations in messy, real-world documents,
outputting structured metadata as TSV for use in downstream workflows
such as course reserve requests.

## Quickstart

### Install

```bash
pip install syllabus-metadata
```

### Run as a command-line tool

```bash
$ syllabus-metadata <prompt_file> <syllabus_file> [--backend ollama|bedrock|openai]
```

Example:

```bash
$ syllabus-metadata prompts/citations.txt syllabus.pdf --backend bedrock
```

A sample prompt file is provided in `prompts/citations.txt`.

### Use as a library

```python
from syllabus_metadata import extract_citations
from syllabus_metadata.ingestion import extract_text

doc_text = extract_text("syllabus.pdf")  # also accepts .docx
prompt = open("prompts/citations.txt").read()
tsv = extract_citations(prompt, doc_text, backend="bedrock")
print(tsv)
```

## Background and System Requirements

### Python Build Requirements

- **Python** >= 3.10
- **python-docx** — Word document ingestion
- **pdfplumber** — PDF ingestion
- **boto3** — required for the `bedrock` backend
- **openai** — required for the `openai` backend

### System Requirements

| Backend | Requirement |
|---------|-------------|
| `ollama` (default) | [Ollama](https://ollama.com) running locally with `llama3.1:latest` pulled |
| `bedrock` | AWS credentials in the environment (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) and Bedrock access enabled in your AWS account |
| `openai` | `OPENAI_API_KEY` set in the environment |
