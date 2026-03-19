import argparse

from syllabus_metadata import extract_citations, query_llm
from syllabus_metadata.ingestion import extract_text


def read_prompt(path: str) -> str:
    with open(path) as f:
        return f.read()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Syllabus citation extractor")
    parser.add_argument("prompt_file", help="Path to the prompt text file")
    parser.add_argument("doc_file", nargs="?", help="Path to a .docx or .pdf syllabus file")
    parser.add_argument(
        "--backend",
        choices=["ollama", "bedrock", "openai"],
        default="ollama",
        help="LLM backend to use (default: ollama)",
    )
    args = parser.parse_args()

    prompt = read_prompt(args.prompt_file)

    if args.doc_file:
        # Citation extraction mode
        doc_text = extract_text(args.doc_file)
        print(extract_citations(prompt, doc_text, backend=args.backend))
    else:
        # Simple query mode
        print(query_llm(prompt, backend=args.backend))
