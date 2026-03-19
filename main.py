import sys

from syllabus_metadata import extract_citations, query_llm
from syllabus_metadata.ingestion import extract_text


def read_prompt(path: str) -> str:
    with open(path) as f:
        return f.read()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        # Citation extraction mode: prompt file + docx file
        prompt = read_prompt(sys.argv[1])
        doc_text = extract_text(sys.argv[2])
        print(extract_citations(prompt, doc_text))
    else:
        # Simple query mode: prompt file only
        # TODO: at a later time, when we're finessing this code,
        # reconsider defaulting to "prompt.txt"
        prompt_file = sys.argv[1] if len(sys.argv) > 1 else "prompt.txt"
        print(query_llm(read_prompt(prompt_file)))
