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
output = extract_citations(prompt, doc_text, backend="bedrock")
print(output)
```

## Installing from Source

To install directly from a cloned repository:

```bash
# Ensure Python >= 3.10 is available (install via Homebrew if needed)
brew install python@3.12

# Create and activate a virtualenv
python3.12 -m venv ~/.venvs/syllabus-metadata
source ~/.venvs/syllabus-metadata/bin/activate

# Install dependencies and the package in editable mode
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

### AWS Bedrock credentials

To use the `bedrock` backend, set the following environment variables before running the tool:

```bash
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_DEFAULT_REGION=us-east-1   # optional; defaults to us-east-1
```

Your AWS account must also have access to Amazon Bedrock and the
`us.anthropic.claude-sonnet-4-6` inference profile enabled in the target region.

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
